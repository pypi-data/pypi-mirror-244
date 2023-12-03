import asyncio

import pytest

from upsies.jobs import JobBase, QueueJobBase


class FooJob(QueueJobBase):
    name = 'foo'
    label = 'Foo'

    def initialize(self, foo=None, bar=None, enqueue=()):
        self.handled_inputs = []

    async def handle_input(self, value):
        self.handled_inputs.append(value)


@pytest.fixture
@pytest.mark.asyncio
async def qjob(tmp_path):
    qjob = FooJob(home_directory=tmp_path, cache_directory=tmp_path)
    return qjob


def test_QueueJobBase_is_JobBase_subclass(qjob):
    assert isinstance(qjob, JobBase)


@pytest.mark.asyncio
async def test_nothing_is_enqueued(qjob):
    qjob.start()
    # Prevent wait() from blocking forever
    asyncio.get_running_loop().call_later(0.1, qjob.close)
    await qjob.wait()

    assert qjob._enqueue_args == ()
    assert qjob.handled_inputs == []


@pytest.mark.asyncio
async def test_enqueue_argument(tmp_path):
    qjob = FooJob(home_directory=tmp_path, cache_directory=tmp_path, enqueue=(1, 2, 3))
    qjob.start()
    await qjob.wait()

    assert qjob._enqueue_args == (1, 2, 3)
    assert qjob.handled_inputs == [1, 2, 3]


@pytest.mark.asyncio
async def test_enqueue_method(qjob, tmp_path):
    class FeedJob(JobBase):
        name = 'feeder'
        label = 'Feeder'
        cache_directory = str(tmp_path)

        async def run(self):
            await asyncio.sleep(0.01)
            self.send('foo')
            await asyncio.sleep(0.03)
            self.send('bar')
            await asyncio.sleep(0.02)
            self.send('baz')

    fjob = FeedJob()
    fjob.signal.register('output', qjob.enqueue)
    fjob.signal.register('finished', lambda fjob: qjob.close())
    qjob.start()
    fjob.start()

    await asyncio.gather(fjob.wait(), qjob.wait())

    assert qjob._enqueue_args == ()
    assert qjob.handled_inputs == ['foo', 'bar', 'baz']


@pytest.mark.asyncio
async def test_handle_input_raises_exception(tmp_path, mocker):
    class FeedJob(JobBase):
        name = 'feeder'
        label = 'Feeder'
        cache_directory = str(tmp_path)

        async def run(self):
            self.send('foo')
            self.send('bar')
            self.send('baz')

    class QueueJob(FooJob):
        def handle_input(self, input):
            if 'b' in input:
                raise ValueError('No b allowed!')
            else:
                return super().handle_input(input)

    fjob = FeedJob()
    qjob = QueueJob()
    fjob.signal.register('output', qjob.enqueue)
    fjob.signal.register('finished', lambda fjob: qjob.close())
    qjob.start()
    fjob.start()

    await fjob.wait()
    with pytest.raises(ValueError, match=r'^No b allowed!$'):
        await qjob.wait()

    assert qjob._enqueue_args == ()
    assert qjob.handled_inputs == ['foo']
