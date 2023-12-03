import asyncio
import re
from unittest.mock import AsyncMock, Mock, PropertyMock, call

import pytest

from upsies.uis.tui.tui import TUI


class Job:
    def __init__(self, name, **kwargs):
        self.name = name
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __repr__(self):
        return f'<{type(self).__name__} {self.name!r}>'


class JobInfo:
    def __init__(self, *, job=None, widget=None, container=None):
        self.job = job
        self.widget = widget
        self.container = container

    def __repr__(self):
        return f'<{type(self).__name__} {self.job.name!r}>'


def test_uncaught_exception(mocker):
    tui = TUI()
    mocker.patch.object(tui, '_exit')

    counter = 0

    def bad_callback(task):
        nonlocal counter
        raise RuntimeError(f'bad, bad, bad: {counter}')

    async def with_running_loop():
        for _ in range(3):
            task = asyncio.create_task(AsyncMock()())
            task.add_done_callback(bad_callback)
            await task

    tui._loop.run_until_complete(with_running_loop())

    assert type(tui._exception) is RuntimeError
    assert str(tui._exception) == 'bad, bad, bad: 0'
    assert tui._exit.call_args_list == [call(), call(), call()]


def test_add_jobs(mocker):
    jobs = {
        'a': Job(name='a'),
        'b': Job(name='b'),
        'c': Job(name='c'),
    }

    ui = TUI()

    mocks = Mock()
    mocks.attach_mock(mocker.patch.object(ui, '_add_job'), '_add_job')
    mocks.attach_mock(mocker.patch.object(ui, '_update_jobs_container'), '_update_jobs_container')
    mocks.attach_mock(mocker.patch.object(ui, '_connect_jobs'), '_connect_jobs')

    ui.add_jobs(*jobs.values())

    assert mocks.mock_calls == [
        call._add_job(jobs['a']),
        call._add_job(jobs['b']),
        call._add_job(jobs['c']),
        call._update_jobs_container(),
        call._connect_jobs((jobs['a'], jobs['b'], jobs['c'])),
    ]


def test__add_job_detects_job_name_duplicate(mocker):
    mocker.patch('upsies.uis.tui.jobwidgets.JobWidget')
    mocker.patch('upsies.uis.tui.tui.to_container')
    ui = TUI()
    ui._add_job(Job(name='a'))
    ui._add_job(Job(name='b'))
    with pytest.raises(RuntimeError, match=r'^Conflicting job name: b$'):
        ui._add_job(Job(name='b'))


def test__add_job_gracefully_ignores_adding_exact_job_duplicate(mocker):
    mocker.patch('upsies.uis.tui.jobwidgets.JobWidget')
    mocker.patch('upsies.uis.tui.tui.to_container')
    ui = TUI()
    jobs = {
        'a': Job(name='a'),
        'b': Job(name='b'),
        'c': Job(name='c'),
        'd': Job(name='d'),
    }

    ui._add_job(jobs['a'])
    ui._add_job(jobs['b'])
    ui._add_job(jobs['c'])
    ui._add_job(jobs['b'])
    ui._add_job(jobs['d'])
    assert list(ui._jobs) == list(jobs)
    assert [jobinfo.job for jobinfo in ui._jobs.values()] == list(jobs.values())


def test__add_job_creates_JobWidget_and_Container(mocker):
    JobWidget_mock = mocker.patch('upsies.uis.tui.jobwidgets.JobWidget')
    to_container_mock = mocker.patch('upsies.uis.tui.tui.to_container')
    ui = TUI()
    job = Job(name='a')
    ui._add_job(job)
    assert tuple(ui._jobs) == (job.name,)
    assert ui._jobs[job.name].widget == JobWidget_mock.return_value
    assert ui._jobs[job.name].container == to_container_mock.return_value
    assert JobWidget_mock.call_args_list == [call(job, ui._app)]
    assert to_container_mock.call_args_list == [call(JobWidget_mock.return_value)]


def test_update_jobs_container_only_adds_first_unfinished_job_and_focuses_it_if_no_job_has_errors(mocker):
    ui = TUI()
    mocker.patch.object(ui, '_update_focus')
    ui._jobs = {
        'an': JobInfo(job=Job('a', is_enabled=False, was_started=False, is_finished=False, errors=()), widget=Mock(is_interactive=False), container=Mock(name='aw')),

        'bi': JobInfo(job=Job('b', is_enabled=False, was_started=False, is_finished=False, errors=()), widget=Mock(is_interactive=True), container=Mock(name='bw')),
        'cn': JobInfo(job=Job('c', is_enabled=False, was_started=True, is_finished=False, errors=()), widget=Mock(is_interactive=False), container=Mock(name='cw')),
        'dn': JobInfo(job=Job('d', is_enabled=True, was_started=False, is_finished=False, errors=()), widget=Mock(is_interactive=False), container=Mock(name='dw')),

        'ei': JobInfo(job=Job('e', is_enabled=False, was_started=True, is_finished=False, errors=()), widget=Mock(is_interactive=True), container=Mock(name='ew')),
        'fi': JobInfo(job=Job('f', is_enabled=True, was_started=False, is_finished=False, errors=()), widget=Mock(is_interactive=True), container=Mock(name='fw')),
        'gn': JobInfo(job=Job('g', is_enabled=True, was_started=True, is_finished=False, errors=()), widget=Mock(is_interactive=False), container=Mock(name='gw')),

        'hi': JobInfo(job=Job('h', is_enabled=True, was_started=True, is_finished=False, errors=()), widget=Mock(is_interactive=True), container=Mock(name='hw')),

        'xi': JobInfo(job=Job('x', is_enabled=True, was_started=True, is_finished=False, errors=()), widget=Mock(is_interactive=True), container=Mock(name='xw')),
        'yn': JobInfo(job=Job('y', is_enabled=True, was_started=True, is_finished=False, errors=()), widget=Mock(is_interactive=False), container=Mock(name='yw')),
        'zi': JobInfo(job=Job('z', is_enabled=True, was_started=True, is_finished=False, errors=()), widget=Mock(is_interactive=True), container=Mock(name='zw')),
    }
    ui._layout = Mock()
    jobs_container_id = id(ui._jobs_container)

    def assert_jobs_container(*keys, focused):
        ui._update_jobs_container()
        assert id(ui._jobs_container) == jobs_container_id
        exp_children = [ui._jobs[k].container for k in keys]
        assert ui._jobs_container.children == exp_children
        if focused:
            assert ui._update_focus.call_args_list == [
                call(ui._jobs[f])
                for f in focused
            ]
        else:
            assert ui._update_focus.call_args_list == []
        ui._update_focus.reset_mock()

    assert_jobs_container('hi', 'gn', 'yn', focused=['hi'])

    ui._jobs['an'].job.is_finished = True
    assert_jobs_container('hi', 'gn', 'yn', focused=['hi'])

    ui._jobs['bi'].job.is_finished = True
    assert_jobs_container('hi', 'gn', 'yn', focused=['hi'])

    ui._jobs['cn'].job.is_finished = True
    assert_jobs_container('hi', 'gn', 'yn', focused=['hi'])

    ui._jobs['dn'].job.is_finished = True
    assert_jobs_container('hi', 'gn', 'yn', focused=['hi'])

    ui._jobs['ei'].job.is_finished = True
    assert_jobs_container('hi', 'gn', 'yn', focused=['hi'])

    ui._jobs['fi'].job.is_finished = True
    assert_jobs_container('hi', 'gn', 'yn', focused=['hi'])

    ui._jobs['gn'].job.is_finished = True
    assert_jobs_container('hi', 'gn', 'yn', focused=['hi'])

    ui._jobs['hi'].job.is_finished = True
    assert_jobs_container('hi', 'xi', 'gn', 'yn', focused=['xi'])

    ui._jobs['xi'].job.errors = ('Error message',)
    assert_jobs_container('hi', 'xi', 'zi', 'gn', 'yn', focused=['xi', 'zi'])


@pytest.mark.parametrize('raised', (None, ValueError('whatever')))
def test__update_focus(raised, mocker):
    ui = TUI()
    mocker.patch.object(ui._layout, 'focus', side_effect=raised)
    jobinfo = Mock()
    ui._update_focus(jobinfo)
    assert ui._layout.focus.call_args_list == [call(jobinfo.container)]


def test__connect_jobs():
    ui = TUI()
    mocks = Mock()
    jobs = [
        mocks.foo,
        mocks.bar,
        mocks.baz,
    ]
    ui._connect_jobs(jobs)
    assert mocks.mock_calls == [
        call.foo.signal.register('finished', ui._handle_job_finished),
        call.foo.signal.register('refresh_job_list', ui._refresh_jobs),
        call.bar.signal.register('finished', ui._handle_job_finished),
        call.bar.signal.register('refresh_job_list', ui._refresh_jobs),
        call.baz.signal.register('finished', ui._handle_job_finished),
        call.baz.signal.register('refresh_job_list', ui._refresh_jobs),
    ]


@pytest.mark.parametrize(
    argnames='finished_job, enabled_jobs, exp_mock_calls',
    argvalues=(
        pytest.param(
            Job(name='x', exit_code=1, is_finished=True),
            [
                Job(name='foo', is_finished=False),
            ],
            [call._refresh_jobs(), call._exit()],
            id='Finished job failed',
        ),
        pytest.param(
            Job(name='x', exit_code=0, is_finished=True),
            [
                Job(name='foo', is_finished=False),
            ],
            [call._refresh_jobs()],
            id='Finished job succeeded, only other job is not finished',
        ),
        pytest.param(
            Job(name='x', exit_code=0, is_finished=True),
            [
                Job(name='foo', is_finished=True),
            ],
            [call._refresh_jobs(), call._exit()],
            id='Finished job succeeded, only other job is finished',
        ),
        pytest.param(
            Job(name='x', exit_code=0, is_finished=True),
            [
                Job(name='foo', is_finished=True),
                Job(name='bar', is_finished=True),
                Job(name='baz', is_finished=True),
            ],
            [call._refresh_jobs(), call._exit()],
            id='Finished job succeeded, all other jobs are finished',
        ),
        pytest.param(
            Job(name='x', exit_code=0, is_finished=True),
            [
                Job(name='foo', is_finished=True),
                Job(name='bar', is_finished=False),
                Job(name='baz', is_finished=True),
            ],
            [call._refresh_jobs()],
            id='Finished job succeeded, one other job is not finished',
        ),
    ),
)
def test__handle_job_finished(finished_job, enabled_jobs, exp_mock_calls, mocker):
    ui = TUI()

    mocks = Mock()
    mocker.patch.object(type(ui), '_enabled_jobs', PropertyMock(return_value=[
        Mock(job=job) for job in enabled_jobs
    ]))
    mocks.attach_mock(mocker.patch.object(ui, '_exit'), '_exit')
    mocks.attach_mock(mocker.patch.object(ui, '_refresh_jobs'), '_refresh_jobs')

    ui._handle_job_finished(finished_job)

    assert mocks.mock_calls == exp_mock_calls


@pytest.mark.parametrize('app_terminated', (True, False))
def test__refresh_jobs(app_terminated, mocker):
    ui = TUI()

    enabled_jobs = [
        Job(name='foo'),
        Job(name='bar'),
        Job(name='baz'),
    ]

    mocks = Mock()
    mocker.patch.object(type(ui), '_enabled_jobs', PropertyMock(return_value=[
        JobInfo(job=job) for job in enabled_jobs
    ]))
    mocker.patch.object(ui, '_app_terminated', app_terminated)
    mocks.attach_mock(mocker.patch.object(ui, '_start_enabled_jobs'), '_start_enabled_jobs')
    mocks.attach_mock(mocker.patch.object(ui, '_update_jobs_container'), '_update_jobs_container')
    mocks.attach_mock(mocker.patch.object(ui._app, 'invalidate'), 'invalidate')

    ui._refresh_jobs()

    if app_terminated:
        assert mocks.mock_calls == []
    else:
        assert mocks.mock_calls == [
            call._start_enabled_jobs(),
            call._update_jobs_container(),
            call.invalidate(),
        ]


def test__start_enabled_jobs(mocker):
    ui = TUI()
    mocks = Mock()
    jobinfos = {
        'a': JobInfo(job=Job(name='a', was_started=False, autostart=False, start=mocks.start_a)),
        'b': JobInfo(job=Job(name='b', was_started=False, autostart=True, start=mocks.start_b)),
        'c': JobInfo(job=Job(name='c', was_started=True, autostart=False, start=mocks.start_c)),
        'd': JobInfo(job=Job(name='d', was_started=True, autostart=True, start=mocks.start_d)),
        'e': JobInfo(job=Job(name='e', was_started=True, autostart=True, start=mocks.start_e)),
        'f': JobInfo(job=Job(name='f', was_started=True, autostart=False, start=mocks.start_f)),
        'g': JobInfo(job=Job(name='g', was_started=False, autostart=True, start=mocks.start_g)),
        'h': JobInfo(job=Job(name='h', was_started=False, autostart=False, start=mocks.start_h)),
    }

    mocker.patch.object(type(ui), '_enabled_jobs', tuple(jobinfos.values()))

    ui._start_enabled_jobs()

    assert mocks.mock_calls == [
        call.start_b(),
        call.start_g(),
    ]


def test__enabled_jobs(mocker):
    ui = TUI()
    jobinfos = {
        'a': JobInfo(job=Job(name='a', is_enabled=False)),
        'b': JobInfo(job=Job(name='b', is_enabled=False)),
        'c': JobInfo(job=Job(name='c', is_enabled=True)),
        'd': JobInfo(job=Job(name='d', is_enabled=True)),
        'e': JobInfo(job=Job(name='e', is_enabled=False)),
        'f': JobInfo(job=Job(name='f', is_enabled=True)),
    }

    mocker.patch.object(ui, '_jobs', jobinfos)

    assert ui._enabled_jobs == (
        jobinfos['c'],
        jobinfos['d'],
        jobinfos['f'],
    )


def test__all_jobs_finished(mocker):
    ui = TUI()
    jobinfos = {
        'a': JobInfo(job=Job(name='a', is_finished=False)),
        'b': JobInfo(job=Job(name='b', is_finished=False)),
        'c': JobInfo(job=Job(name='c', is_finished=True)),
        'd': JobInfo(job=Job(name='d', is_finished=True)),
        'e': JobInfo(job=Job(name='e', is_finished=False)),
        'f': JobInfo(job=Job(name='f', is_finished=True)),
    }
    mocker.patch.object(type(ui), '_enabled_jobs', PropertyMock(return_value=tuple(jobinfos.values())))

    assert ui._all_jobs_finished is False
    jobinfos['a'].job.is_finished = True
    assert ui._all_jobs_finished is False
    jobinfos['b'].job.is_finished = True
    assert ui._all_jobs_finished is False
    jobinfos['c'].job.is_finished = True
    assert ui._all_jobs_finished is False
    jobinfos['e'].job.is_finished = True
    assert ui._all_jobs_finished is True


@pytest.mark.parametrize(
    argnames='exception_from_jobs, exit_codes, exp_result',
    argvalues=(
        (None, [0, 0, 0], 0),
        (None, [0, 3, 4], 3),
        (RuntimeError('very bad'), [0, 0, 0], RuntimeError('very bad')),
    ),
    ids=lambda v: repr(v),
)
def test_run(exception_from_jobs, exit_codes, exp_result, mocker):
    ui = TUI()
    mocks = Mock(
        wait_a=AsyncMock(),
        wait_b=AsyncMock(),
        wait_c=AsyncMock(),
        wait_d=AsyncMock(),
        wait_e=AsyncMock(),
        wait_f=AsyncMock(),
        wait_g=AsyncMock(),
        wait_h=AsyncMock(),
    )
    mocks.attach_mock(mocker.patch.object(ui, 'add_jobs'), 'add_jobs')
    mocks.attach_mock(mocker.patch.object(ui, '_run'), '_run')
    mocks.attach_mock(
        mocker.patch.object(ui, '_get_exception_from_jobs', return_value=exception_from_jobs),
        '_get_exception_from_jobs',
    )
    jobinfos = {
        'a': JobInfo(job=Job(name='a', exit_code=exit_codes[0])),
        'b': JobInfo(job=Job(name='b', exit_code=exit_codes[1])),
        'c': JobInfo(job=Job(name='c', exit_code=exit_codes[2])),
    }
    mocker.patch.object(type(ui), '_enabled_jobs', tuple(jobinfos.values()))
    jobs = tuple(jobinfo.job for jobinfo in jobinfos.values())

    if isinstance(exp_result, Exception):
        with pytest.raises(type(exp_result), match=rf'^{re.escape(str(exp_result))}$'):
            ui.run(jobs)
    else:
        return_value = ui.run(jobs)
        assert return_value == exp_result

    assert mocks.mock_calls == [
        call.add_jobs(*jobs),
        call._run(),
        call._get_exception_from_jobs(),
    ]


@pytest.mark.asyncio
async def test__run(mocker):
    ui = TUI()
    mocks = Mock(
        wait_a=AsyncMock(),
        wait_b=AsyncMock(),
        wait_c=AsyncMock(),
        wait_d=AsyncMock(),
        wait_e=AsyncMock(),
        wait_f=AsyncMock(),
        wait_g=AsyncMock(),
        wait_h=AsyncMock(),
    )
    mocks.attach_mock(mocker.patch.object(ui, '_start_enabled_jobs'), '_start_enabled_jobs')
    mocks.attach_mock(mocker.patch.object(ui._app, 'run_async'), 'run_async')
    jobinfos = {
        'a': JobInfo(job=Job(name='a', was_started=False, is_finished=False, wait=mocks.wait_a)),
        'b': JobInfo(job=Job(name='b', was_started=False, is_finished=True, wait=mocks.wait_b)),
        'c': JobInfo(job=Job(name='c', was_started=True, is_finished=False, wait=mocks.wait_c)),
        'd': JobInfo(job=Job(name='d', was_started=True, is_finished=True, wait=mocks.wait_d)),
        'e': JobInfo(job=Job(name='e', was_started=True, is_finished=True, wait=mocks.wait_e)),
        'f': JobInfo(job=Job(name='f', was_started=True, is_finished=False, wait=mocks.wait_f)),
        'g': JobInfo(job=Job(name='g', was_started=False, is_finished=True, wait=mocks.wait_g)),
        'h': JobInfo(job=Job(name='h', was_started=False, is_finished=False, wait=mocks.wait_h)),
    }
    mocker.patch.object(type(ui), '_enabled_jobs', tuple(jobinfos.values()))

    await ui._run()

    assert mocks.mock_calls == [
        call._start_enabled_jobs(),
        call.run_async(set_exception_handler=False),
        call.wait_c(),
        call.wait_f(),
    ]


def test__exit_does_nothing_if_app_terminated(mocker):
    ui = TUI()
    ui._app_terminated = True
    mocks = Mock()
    mocks.attach_mock(mocker.patch.object(ui._app, 'exit'), 'exit')
    mocks.attach_mock(mocker.patch.object(ui._loop, 'call_later'), 'call_later')
    ui._exit()
    assert mocks.mock_calls == []


def test__exit_exits_app(mocker):
    ui = TUI()
    ui._app_terminated = False
    mocks = Mock()
    mocks.attach_mock(mocker.patch.object(ui._app, 'exit'), 'exit')
    mocks.attach_mock(mocker.patch.object(ui._loop, 'call_later'), 'call_later')
    ui._exit()
    assert mocks.mock_calls == [
        call.exit(),
    ]
    assert ui._app_terminated is True


def test__exit_exits_app_before_app_is_running(mocker):
    mocker.patch('upsies.uis.tui.jobwidgets.JobWidget')
    mocker.patch('upsies.uis.tui.tui.to_container')

    ui = TUI()
    ui._app_terminated = False
    mocks = Mock()
    mocks.attach_mock(
        mocker.patch.object(ui._app, 'exit', side_effect=Exception('app is still not running')),
        'exit',
    )
    mocks.attach_mock(mocker.patch.object(ui._loop, 'call_later'), 'call_later')

    ui._exit()

    assert mocks.mock_calls == [
        call.exit(),
        call.call_later(0, ui._exit),
    ]
    assert ui._app_terminated is False


def test__terminate_jobs(mocker):
    ui = TUI()
    mocks = Mock()
    ui._jobs = {
        'a': JobInfo(job=Job(name='a', is_finished=False, terminate=mocks.terminate_a)),
        'b': JobInfo(job=Job(name='b', is_finished=False, terminate=mocks.terminate_b)),
        'c': JobInfo(job=Job(name='c', is_finished=True, terminate=mocks.terminate_c)),
        'd': JobInfo(job=Job(name='d', is_finished=True, terminate=mocks.terminate_d)),
        'e': JobInfo(job=Job(name='e', is_finished=False, terminate=mocks.terminate_e)),
        'f': JobInfo(job=Job(name='f', is_finished=False, terminate=mocks.terminate_f)),
        'g': JobInfo(job=Job(name='g', is_finished=True, terminate=mocks.terminate_g)),
        'h': JobInfo(job=Job(name='h', is_finished=True, terminate=mocks.terminate_h)),
    }

    ui._terminate_jobs()

    assert mocks.mock_calls == [
        call.terminate_a(),
        call.terminate_b(),
        call.terminate_e(),
        call.terminate_f(),
    ]


@pytest.mark.parametrize(
    argnames='jobs, exp_exception',
    argvalues=(
        (
            {
                'a': JobInfo(job=Job(name='a', raised=None)),
                'b': JobInfo(job=Job(name='b', raised=None)),
                'c': JobInfo(job=Job(name='c', raised=ValueError('wrong value, mate'))),
                'd': JobInfo(job=Job(name='d', raised=None)),
                'e': JobInfo(job=Job(name='e', raised=TypeError('wrong type, dude'))),
                'f': JobInfo(job=Job(name='f', raised=None)),
            },
            ValueError('wrong value, mate'),
        ),
        (
            {
                'a': JobInfo(job=Job(name='a', raised=None)),
                'b': JobInfo(job=Job(name='b', raised=None)),
                'c': JobInfo(job=Job(name='c', raised=None)),
            },
            None,
        ),
    ),
    ids=lambda v: repr(v),
)
def test__get_exception_from_jobs(jobs, exp_exception, mocker):
    ui = TUI()
    ui._jobs = jobs

    exception = ui._get_exception_from_jobs()
    if exp_exception:
        assert type(exception) is type(exp_exception)
        assert str(exception) is str(exp_exception)
    else:
        assert exception is None
