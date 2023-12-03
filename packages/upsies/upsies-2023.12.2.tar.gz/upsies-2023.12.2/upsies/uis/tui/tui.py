"""
Interactive text user interface and job manager
"""

import asyncio
import collections
import types

from prompt_toolkit.application import Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout import Layout
from prompt_toolkit.layout.containers import HSplit, Window, to_container
from prompt_toolkit.output import create_output

from . import jobwidgets, style

import logging  # isort:skip
_log = logging.getLogger(__name__)


class TUI:
    def __init__(self):
        # Map JobBase.name to SimpleNamespace with attributes:
        #   job       - JobBase instance
        #   widget    - JobWidgetBase instance
        #   container - prompttoolkit.Container instance
        self._jobs = collections.defaultdict(lambda: types.SimpleNamespace())
        self._app = self._make_app()
        self._app_terminated = False
        self._exception = None
        self._loop = asyncio.new_event_loop()
        self._loop.set_exception_handler(self._handle_exception)

    def _handle_exception(self, loop, context):
        exception = context.get('exception')
        if exception:
            _log.debug('Caught unhandled exception: %r', exception)
            _log.debug('Unhandled exception context: %r', context)
            if not self._exception:
                self._exception = exception
            self._exit()

    def _make_app(self):
        self._jobs_container = HSplit(
            # FIXME: Layout does not accept an empty list of children, so we add
            #        an empty Window that doesn't display anything.
            #        https://github.com/prompt-toolkit/python-prompt-toolkit/issues/1257
            children=[Window()],
            style='class:default',
        )
        self._layout = Layout(self._jobs_container)

        kb = KeyBindings()

        @kb.add('escape')
        @kb.add('c-g')
        @kb.add('c-q')
        @kb.add('c-c')
        def _(event, self=self):
            _log.debug('Terminating all jobs because the user terminated the application')
            self._terminate_jobs()
            self._exit()

        @kb.add('escape', 'I')
        def _(event, self=self):
            _log.debug('=== CURRENT JOBS ===')
            for jobinfo in self._jobs.values():
                job = jobinfo.job
                if job.is_finished:
                    state = 'finished'
                    bullet = '|'
                elif job.was_started:
                    state = 'running'
                    bullet = '*'
                else:
                    state = 'disabled'
                    bullet = '_'

                _log.debug(' %s %s (%s, %d tasks):', bullet, job.name, state, len(job._tasks))
                for task in job._tasks:
                    _log.debug('   %r', task)

        app = Application(
            # Write TUI to stderr if stdout is redirected. This is useful for
            # allowing the user to make decisions in the TUI (e.g. selecting an
            # item from search results) while redirecting the final output
            # (e.g. an IMDb ID).
            output=create_output(always_prefer_tty=True),
            layout=self._layout,
            key_bindings=kb,
            style=style.style,
            full_screen=False,
            erase_when_done=False,
            mouse_support=False,
            on_invalidate=self._update_jobs_container,
        )
        return app

    def add_jobs(self, *jobs):
        """Add :class:`~.jobs.base.JobBase` instances"""
        for job in jobs:
            self._add_job(job)

        # Add job widgets to the main container widget (no side effects)
        self._update_jobs_container()

        # Register signal callbacks (no side effects)
        self._connect_jobs(jobs)

    def _add_job(self, job):
        if job.name in self._jobs:
            if job is not self._jobs[job.name].job:
                raise RuntimeError(f'Conflicting job name: {job.name}')
        else:
            self._jobs[job.name].job = job
            self._jobs[job.name].widget = jobwidgets.JobWidget(job, self._app)
            self._jobs[job.name].container = to_container(self._jobs[job.name].widget)

    # We accept one argument because the on_invalidate callback passes the
    # Application instance
    def _update_jobs_container(self, _=None):
        enabled_jobs = self._enabled_jobs

        # List interactive jobs first
        jobs_container = []
        for jobinfo in enabled_jobs:
            if jobinfo.widget.is_interactive and jobinfo.job.was_started:
                jobs_container.append(jobinfo.container)

                # Focus the first unfinished job
                if not jobinfo.job.is_finished:
                    self._update_focus(jobinfo)

                    # Don't display more than one unfinished interactive job
                    # unless any job has errors, in which case we are
                    # terminating the application and display all jobs.
                    if not any(jobinfo.job.errors for jobinfo in self._jobs.values()):
                        break

        # Add background jobs below interactive jobs so the interactive widgets
        # don't change position when non-interactive widgets change size.
        for jobinfo in enabled_jobs:
            if not jobinfo.widget.is_interactive and jobinfo.job.was_started:
                jobs_container.append(jobinfo.container)

        # Replace containers with new containers.
        self._jobs_container.children[:] = jobs_container

    def _update_focus(self, jobinfo):
        try:
            self._layout.focus(jobinfo.container)
        except ValueError:
            pass
            # _log.debug('Unfocusable job: %r', jobinfo.job.name)

    def _connect_jobs(self, jobs):
        for job in jobs:
            # Every time a job finishes, other jobs can become enabled due to
            # the dependencies on other jobs or other conditions. We also want
            # to display the next interactive job when an interactive job is
            # done.
            job.signal.register('finished', self._handle_job_finished)

            # A job can also signal explicitly that we should update the job
            # widgets, e.g. to start previously disabled jobs.
            job.signal.register('refresh_job_list', self._refresh_jobs)

    def _handle_job_finished(self, finished_job):
        assert finished_job.is_finished, f'{self.name} is actually not finished'

        # Start and/or display the next interactive jobs. This also generates
        # the regular output if all output was read from cache and the TUI exits
        # immediately.
        self._refresh_jobs()

        # Terminate all jobs and exit if job finished with non-zero exit code
        if finished_job.exit_code != 0:
            _log.debug('Terminating all jobs because job failed: %s: exit_code=%r',
                       finished_job.name, finished_job.exit_code)
            self._terminate_jobs()
            self._exit()

        else:
            if self._all_jobs_finished:
                # Exit application if all jobs finished
                _log.debug('All jobs finished')
                self._exit()

    def _refresh_jobs(self):
        # Update jobs unless its pointless because _exit() was called
        if not self._app_terminated:
            self._start_enabled_jobs()
            self._update_jobs_container()
            self._app.invalidate()

    def _start_enabled_jobs(self):
        for jobinfo in self._enabled_jobs:
            job = jobinfo.job
            if not job.was_started and job.autostart:
                job.start()

    @property
    def _enabled_jobs(self):
        return tuple(
            jobinfo
            for jobinfo in self._jobs.values()
            if jobinfo.job.is_enabled
        )

    @property
    def _all_jobs_finished(self):
        enabled_jobs = [jobinfo.job for jobinfo in self._enabled_jobs]
        return all(job.is_finished for job in enabled_jobs)

    def run(self, jobs):
        """
        Block while running `jobs`

        :param jobs: Iterable of :class:`~.jobs.base.JobBase` instances

        :raise: Any exception that occured while running jobs

        :return: :attr:`~.JobBase.exit_code` from the first failed job or 0 for
            success
        """
        self.add_jobs(*jobs)

        # Block until _exit() is called
        self._loop.run_until_complete(self._run())

        # Raise exception or return exit code
        exception = self._get_exception_from_jobs()
        if exception:
            _log.debug('Exception from jobs: %r', exception)
            raise exception
        else:
            # First non-zero exit_code is the application exit_code
            for jobinfo in self._enabled_jobs:
                _log.debug('Exit code of %r: %r', jobinfo.job.name, jobinfo.job.exit_code)
                if jobinfo.job.exit_code != 0:
                    return jobinfo.job.exit_code
            return 0

    async def _run(self):
        # Call each job's run() method or read cache. This must be done
        # asynchronously because we need a running asyncio event loop to make
        # JobBase.add_task() work.
        self._start_enabled_jobs()

        # Run the TUI
        await self._app.run_async(set_exception_handler=False)

        enabled_jobs = [jobinfo.job for jobinfo in self._enabled_jobs]
        for job in enabled_jobs:
            if job.was_started and not job.is_finished:
                await job.wait()

    def _exit(self):
        if not self._app_terminated:
            _log.debug('Exiting application')
            try:
                # Unblock self._app.run_async() in _run()
                self._app.exit()
            except Exception as e:
                # If we aren't running yet, try again. This happens if a single
                # job is getting output from cache, is finished immediately and
                # self._exit() is called via the "finished" signal before
                # self._app.run_async() is called.
                print('exit() raised:', repr(e))
                self._loop.call_later(0, self._exit)
            else:
                self._app_terminated = True
        else:
            _log.debug('Already exited')

    def _terminate_jobs(self):
        for jobinfo in self._jobs.values():
            job = jobinfo.job
            if not job.is_finished:
                _log.debug('Terminating %s', job.name)
                job.terminate()

    def _get_exception_from_jobs(self):
        # Return first exception from any job or None
        for jobinfo in self._jobs.values():
            job = jobinfo.job
            if job.raised:
                _log.debug('Exception from %s: %r', job.name, job.raised)
                return job.raised
