import asyncio
import traceback
from typing import Any
from collections.abc import Callable
from asyncdb.exceptions import (
    NoDataFound,
    ProviderError
)
# DataIntegration
from flowtask.components import SkipErrors
from flowtask.utils.stats import StepMonitor
from flowtask.models import (
    TaskState,
    setTaskState
)
from flowtask.exceptions import (
    TaskFailed,
    TaskDefinition,
    TaskError,
    TaskParseError,
    TaskNotFound,
    NotSupported,
    ComponentError,
    DataNotFound,
    FileNotFound,
    FileError,
    DataError,
    EmptyFile
)
from flowtask.tasks.pile import TaskPile
from flowtask.utils import cPrint, check_empty, AttrDict
from .abstract import AbstractTask
from ..events import NotifyEvent, LogError
from ..events.events.exec import (
    LogExecution,
    SaveExecution
)
class Task(AbstractTask):
    """
    Task.

        Object contain a Flow Task.
    """
    def __init__(
        self,
        task_id: str = None,
        task: str = None,
        program: str = None,
        loop: asyncio.AbstractEventLoop = None,
        parser: Callable = None,
        worker: Callable = None,
        **kwargs
    ) -> None:
        self._pile = None
        self._steps = None
        self._vars = None
        super(Task, self).__init__(
            task_id=task_id,
            task=task,
            program=program,
            loop=loop,
            parser=parser,
            **kwargs
        )
        self._taskname = task
        self._conditions = {}
        self._attrs = {}
        self.ignore_steps = []
        self.run_only = []
        self._stepattrs = {}
        self._kwargs = {}
        self._masks = {}
        self._resultset: Any = None
        if not self._taskname:
            raise TaskError(
                'Missing Task Name, \
                HINT: add --task (in command line) or parameter "task" \
                with a task name'
            )
        # change root-level attributes on fly
        if parser:
            self._attrs = parser.attributes
        try:
            attrs = kwargs['attributes']
            del kwargs['attributes']
            self._attrs = {**self._attrs, **attrs}
        except KeyError:
            pass
        # disable Events:
        self._no_events: bool = kwargs.pop('no_events', False)
        # for component-based attributes (ex: --DownloadFromIMAP_1:host)
        if parser:
            self._stepattrs = parser.stepattrs
        try:
            steps = kwargs['steps']
            del kwargs['steps']
            if steps:
                self._stepattrs = {**self._stepattrs, **steps}
        except KeyError:
            pass
        try:
            self.is_subtask = kwargs['is_subtask']
            del kwargs['is_subtask']
        except KeyError:
            self.is_subtask: bool = False
        # ignoring components in task execution.
        if parser:
            self.ignore_steps = self._options.ignore
        if not self.ignore_steps:
            try:
                self.ignore_steps = kwargs['ignore_steps']
                del kwargs['ignore_steps']
            except KeyError:
                self.ignore_steps = []
        # list of "run only" components:
        if parser:
            self.run_only = self._options.run_only
        try:
            self.run_only = kwargs['run_only']
            del kwargs['run_only']
        except KeyError:
            pass
        # variables: can be passed between components as reusable values.
        if parser:
            self._variables = self._options.variables
        try:
            variables = kwargs['variables']
            del kwargs['variables']
            if isinstance(variables, dict):
                self._variables = {**self._variables, **variables}
        except KeyError:
            pass
        self.logger.debug(
            f'CURRENTLY NEW Variables: {self._variables}'
        )
        # masks: replacing masks with values or even new functions
        if parser:
            self._masks = self._options.masks
        # conditions: replacing conditions (on components with conditions support)
        if parser:
            self._conditions = self._options.conditions
            self._args = self._options.args
        try:
            conditions = kwargs['conditions']
        except KeyError:
            conditions = {}
        self._conditions = {**self._conditions, **conditions}
        self.logger.debug(
            f'CURRENTLY NEW CONDS: {self._conditions}'
        )
        self.worker = worker
        if kwargs:
            # remain args go to kwargs:
            self._kwargs = {**kwargs}
        ## set the Task State:
        # self.event_defaults(setTaskState)
        ## add also the Log execution for InfluxDB
        self.event_defaults(
            LogExecution(
                disable_notification=self._no_notify
            )
        )
        # Task Started:
        running = getattr(self._events, 'running')
        running.add(setTaskState)
        completed = getattr(self._events, 'completed')
        completed.add(setTaskState)
        # Special Events:
        self._events.exception += NotifyEvent(
            event='exception'
        )
        self._events.data_not_found += NotifyEvent(
            event='warning'
        )
        self._events.data_error += NotifyEvent(
            event='error'
        )
        self._events.file_not_found += NotifyEvent(
            event='error'
        )
        self._events.file_empty += NotifyEvent(
            event='error'
        )
        # Internal On Finished Events:
        self._events.done += NotifyEvent(
            event='done'
        )
        self._events.on_error += NotifyEvent(
            event='error'
        )
        self._events.completed += SaveExecution(
            disable_notification=self._no_notify
        )
        # and Log for Errors:
        logerr = LogError()
        self._events.file_not_found += logerr
        self._events.data_not_found += logerr
        self._events.exception += logerr

    async def close(self):
        """close.

            Closing the remaining connections.
        """
        if self.is_subtask is False:
            await super(Task, self).close()
        self._pile = None
        self._steps = None
        self._args = None

    @property
    def variables(self):
        return self._vars

    @property
    def taskname(self):
        return self._taskname

    def __repr__(self) -> str:
        return f"{self._program}.{self._taskname}"

    async def prepare(self):
        if self._task:
            # calling steps
            try:
                self._pile = TaskPile(
                    self._task,
                    program=self._program
                )
            except (KeyError, TaskDefinition) as err:
                raise TaskDefinition(
                    f"Bad Task Definition: {err!s}"
                ) from err
            except Exception as err:
                raise TaskDefinition(
                    f"Task Exception {self._program}.{self._taskname}: {err!s}"
                ) from err
            ## Processing Event list:
            try:
                self._events.LoadEvents(self._task['events'])
            except KeyError:
                pass
            return True
        else:
            raise TaskDefinition(
                f'DI: Invalid Task: {self._program}.{self._taskname}'
            )

    def get_component(self, step, prev):
        step_name = step.name
        if self.enable_stat is True:
            stat = StepMonitor(name=step_name, parent=self.stat)
            self.stat.add_step(stat)
        else:
            stat = None
        params = step.params()
        params['program'] = self._program
        params['ENV'] = self._env
        # params:
        params['params'] = self._params
        # parameters
        params['parameters'] = self._parameters
        # useful to change variables in set var components
        params['_vars'] = self._kwargs
        # variables dictionary
        try:
            variables = params['variables']
        except KeyError:
            variables = {}
        if prev:
            variables = {**variables, **prev.variables}
        params['variables'] = {**self._variables, **variables}
        params['_masks'] = self._masks  # override mask value
        try:
            arguments = params['arguments']
        except KeyError:
            arguments = []
        if not self._arguments:
            self._arguments = []
        params['arguments'] = arguments + self._arguments
        # argument list for components (or tasks) that need argument lists
        params['_args'] = self._args
        # for components with conditions, we can add more conditions
        try:
            conditions = params['conditions']
        except KeyError:
            conditions = {}
        params['conditions'] = {**conditions, **self._conditions}
        # attributes only usable component-only
        if step_name in self._stepattrs:
            # this can rewrite attributes for steps
            newattrs = self._stepattrs[step_name]
            self._attrs = {**self._attrs, **newattrs}
        # will be a dictionary with ComponentName: parameter
        params['attributes'] = self._attrs
        # the current Pile of components
        params['TaskPile'] = self._pile
        params['debug'] = self._debug
        params['argparser'] = self._argparser
        component = None
        component = step.component
        # get dependency
        depends = step.getDepends(prev)
        if 'TaskPile' in params['parameters']:
            del params['parameters']['TaskPile']
        try:
            comp = component(
                job=depends,
                loop=self._loop,
                stat=stat,  # stats object
                **params
            )
            self.logger.debug(
                f'Task.{self.task_id}: Component {comp}'
            )
            comp.TaskName = step_name
            comp.set_filestore(self._filestore)
            return comp
        except Exception as err:
            raise ComponentError(
                f"DI: Component Error on {self._taskname}, \
                   Component: {step_name} error: {err}"
            ) from err

    def resultset(self):
        return self._resultset

    async def exchange_variables(
        self,
        component,
        result: Any = None
    ):
        # TODO: saving results on Redis, variables on Memory, etc.
        self._variables = component.variables
        self._resultset = result

    def _on_error(self, status: str, exc: BaseException, step_name: str = None):
        if isinstance(exc, str):
            error = exc
        else:
            error = str(exc)
        try:
            self.logger.error(str(exc))
            self._state = TaskState.ERROR
            self._events.on_error(
                message=error,
                component=self._taskname,
                task=self,
                status=status,
                error=exc
            )
        except AttributeError as err:
            self.logger.error(
                f'Error {self._taskname}={self.task_id}, {err}'
            )
            raise TaskError(
                f"Error on Event System: {err}"
            ) from err
        finally:
            # call the OnComplete Event
            if self._no_events is False:
                self._events.completed(
                    message=f":: Task Error: {self._program}.{self._taskname}",
                    task=self,
                    status='error',
                    error=exc
                )
            if step_name:
                raise ComponentError(
                    f"{error!s}"
                )
            else:
                raise exc

    def _on_exception(self, status: str, exc: BaseException, step_name: str = None):
        try:
            self._state = TaskState.EXCEPTION
            trace = traceback.format_exc()
            self._events.exception(
                message=f'{exc!s}',
                component=step_name,
                task=self,
                status=status,
                stacktrace=trace
            )
        except AttributeError as err:
            self.logger.error(
                f'Error {self._taskname}={self.task_id}, {err}'
            )
            raise TaskError(
                f"Error on Event System: {err}"
            ) from err
        finally:
            # call the OnComplete Event
            if self._no_events is False:
                self._events.completed(
                    message=f":: Task Ended: {self._program}.{self._taskname}",
                    task=self,
                    status=status,
                    error=exc
                )
            if step_name:
                raise ComponentError(
                    f"Error Getting Component {step_name}, error: {exc}"
                )
            else:
                raise TaskError(
                    f"Task Error {self._taskname}.{self._program}: {exc!s}"
                )

    async def start(self):
        # starting a Task
        await super(Task, self).start()
        self.logger.info(
            f'Task Started {self._taskname}'
        )
        # Open Task:
        try:
            self._task = await self.taskstore.open_task(
                self._taskname, self._program
            )
            if not self._task:
                raise TaskNotFound(
                    f'Task Missing or empty: {self._taskname}'
                )
        except TaskParseError as e:
            self._on_error(status='parse error', exc=e)
        except TaskNotFound as e:
            self._on_error(status='task not found', exc=e)
        except Exception as exc:
            self._on_exception(status='task error', exc=exc)
        # task is loaded, we need to check syntax.
        try:
            self.check_syntax(self._task)
        except TaskParseError as exc:
            self._on_exception(
                status='parsing error',
                exc=exc
            )
        # can prepare the task before run.
        try:
            self._task = AttrDict(self._task)
            if 'timezone' in self._task:
                # re-set timezone based on Task parameter
                self.set_timezone(self._task.timezone)
            await self.prepare()
            return True
        except (TaskDefinition, NotSupported) as exc:
            self._on_exception(status='not supported', exc=exc)
        except Exception as exc:
            self._on_exception(status='exception', exc=exc)

    def _task_running(self):
        try:
            self._state = TaskState.RUNNING
            self._events.running(
                message=f":: Task.{self.task_id} Running: {self._program}.{self._taskname}",
                task=self,
                status='running',
                disable_notification=self._no_notify
            )
        except AttributeError as exc:
            raise TaskError(
                f"Error on Event System: {exc}"
            ) from exc
        except Exception as err:  # pytest: disable=W0718
            self.logger.error(
                f'Failed to set Running status on task {self._taskname}={self.task_id}, {err}'
            )

    def _on_done(self, result):
        try:
            self._state = TaskState.DONE
            self._events.done(
                message=f":: Task Ended: {self._program}.{self._taskname}",
                result=result,
                task=self,
                status='done',
                disable_notification=self._no_notify
            )
        except AttributeError as err:
            self.logger.error(
                f'Error {self._taskname}={self.task_id}, {err}'
            )
            raise TaskError(
                f"Error at Task Done: {err}"
            ) from err
        finally:
            if self._no_events is False:
                # call the OnComplete Event
                self._events.completed(
                    message=f":: Task Ended: {self._program}.{self._taskname}",
                    status='done',
                    task=self,
                    result=result,
                )

    def _data_error(self, status: str, exc: BaseException, step_name: str = None):
        try:
            self._state = TaskState.DONE_WITH_WARNINGS
            self._events.data_error(
                message=f'Data Error: {exc}',
                component=step_name,
                task=self,
                status=status
            )
        except AttributeError as err:
            self.logger.error(
                f'Error {self._taskname}={self.task_id}, {err}'
            )
            raise TaskError(
                f"Error on Event System: {err}"
            ) from err
        finally:
            # call the OnComplete Event
            if self._no_events is False:
                self._events.completed(
                    message=f":: Data Error: {self._program}.{self._taskname}",
                    status=status,
                    task=self,
                    error=exc
                )
            # and raise the exception:
            if isinstance(exc, BaseException):
                raise exc
            else:
                raise TaskError(str(exc))

    def _not_found(self, status: str, exc: BaseException, step_name: str = None):
        try:
            self._state = TaskState.DONE_WITH_NODATA
            self._events.data_not_found(
                message=f'Not Found: {exc}',
                component=step_name,
                task=self,
                status=status
            )
        except AttributeError as err:
            self.logger.error(
                f'Error {self._taskname}={self.task_id}, {err}'
            )
            raise TaskError(
                f"Error on Event System: {err}"
            ) from err
        finally:
            # call the OnComplete Event
            if self._no_events is False:
                self._events.completed(
                    message=f":: Not Found: {self._program}.{self._taskname}",
                    status=status,
                    task=self,
                    error=exc
                )
            # and raise the exception:
            if isinstance(exc, BaseException):
                raise exc
            else:
                raise TaskError(str(exc))

    def _file_empty(self, status: str, exc: BaseException, step_name: str = None):
        try:
            self._state = TaskState.ERROR
            self._events.file_empty(
                message=f'Empty File: {exc}',
                error=exc,
                component=step_name,
                task=self,
                status=status
            )
        except AttributeError as err:
            self.logger.error(
                f'Error {self._taskname}={self.task_id}, {err}'
            )
            raise TaskError(
                f"Error on Event System: {err}"
            ) from err
        finally:
            # call the OnComplete Event
            if self._no_events is False:
                self._events.completed(
                    message=f":: Empty File: {self._program}.{self._taskname}",
                    status=status,
                    task=self,
                    error=exc
                )
            # and raise the exception:
            if isinstance(exc, BaseException):
                raise exc
            else:
                raise TaskError(str(exc))

    def _file_not_found(self, status: str, exc: BaseException, step_name: str = None):
        try:
            self._state = TaskState.ERROR
            self._events.file_not_found(
                message=f'File Not Found: {exc}',
                error=exc,
                component=step_name,
                task=self,
                status=status
            )
        except AttributeError as err:
            self.logger.error(
                f'Error {self._taskname}={self.task_id}, {err}'
            )
            raise TaskError(
                f"Error on Event System: {err}"
            ) from err
        finally:
            # call the OnComplete Event
            if self._no_events is False:
                self._events.completed(
                    message=f":: Not Found: {self._program}.{self._taskname}",
                    status=status,
                    task=self,
                    error=exc
                )
            # and raise the exception:
            raise exc

    async def run(self):
        # run Task and returning the result.
        result = None
        comp = None
        prev = None
        _exit = False
        failed: list = []
        try:
            task_name = self._task['name']
        except TypeError:
            task_name = self._taskname
        self._task_running()
        for step in self._pile:
            self.logger.debug(
                f"Step: {step.name}, Task: {self.task_id}"
            )
            step_name = step.name
            if step_name in self.ignore_steps:
                # we can ignore this component for execution
                continue
            if len(self.run_only) > 0:
                # we only need to run the existing list of components
                if step_name not in self.run_only:
                    continue
            prev = comp
            try:
                comp = self.get_component(step, prev)
                step.setStep(comp)  # put the Component initialized in the Pile.
            except Exception as err:
                self._on_exception(
                    status='exception',
                    exc=err, step_name=step_name
                )
            if self._debug:
                cPrint(
                    f':: Running {step_name} from {task_name}',
                    level='DEBUG'
                )
            # try START
            try:
                start = getattr(comp, 'start')
                parameters = comp.user_params()
                if callable(start):
                    if asyncio.iscoroutinefunction(start):
                        await comp.start(**parameters)
                    else:
                        comp.start()
                else:
                    self._on_error(
                        status='not_started',
                        exc=f"DI: Error calling Start on Component {step_name}",
                        step_name=step_name
                    )
            except EmptyFile as exc:
                self._file_empty(status='empty_file', exc=exc, step_name=step_name)
            except FileNotFound as exc:
                self._file_not_found(status='file_not_found', exc=exc, step_name=step_name)
            except (NoDataFound, DataNotFound) as exc:
                self._not_found(status='not_found', exc=exc, step_name=step_name)
            except (ProviderError, ComponentError, NotSupported, FileError) as exc:
                self._on_error(
                    status='error',
                    exc=exc,
                    step_name=step_name
                )
            except Exception as err:
                self._on_exception(step_name, err)
            try:
                run = getattr(comp, 'run', None)
                if asyncio.iscoroutinefunction(run):
                    result = await comp.run()
                elif callable(run):
                    result = comp.run()
                else:
                    raise TaskFailed(
                        f"DI: Component {step_name} is not callable"
                    )
                # close operations
                close = getattr(comp, 'close', None)
                if asyncio.iscoroutinefunction(close):
                    await comp.close()
                else:
                    comp.close()
                if check_empty(result):
                    if comp.skipError == SkipErrors.SKIP:
                        print(
                            f'::: SKIPPING Error on {step_name} :::: '
                        )
                        failed.append(comp)
                        _exit = False
                        continue
                    failed.append(comp)
                    _exit = True
                    break
            except EmptyFile as exc:
                # its a data component a no data was found
                if comp.skipError == SkipErrors.SKIP:
                    failed.append(comp)
                    self.logger.warning(
                        f'SKIP Failed Component: {comp!r} with error: {exc}'
                    )
                    # can skip error for this component
                    continue
                self._file_empty(status='empty_file', exc=exc, step_name=step_name)
            except (NoDataFound, DataNotFound) as err:
                # its a data component a no data was found
                if comp.skipError == SkipErrors.SKIP:
                    failed.append(comp)
                    self.logger.warning(
                        f'SKIP Failed Component: {comp!r} with error: {err}'
                    )
                    # can skip error for this component
                    continue
                self._not_found(status='not_found', exc=err, step_name=step_name)
            except (FileNotFound) as err:
                if comp.skipError == SkipErrors.SKIP:
                    failed.append(comp)
                    self.logger.warning(
                        f'SKIP Failed Component: {comp!r} with error: {err}'
                    )
                    # can skip error for this component
                    continue
                self._file_not_found(status='not_found', exc=err, step_name=step_name)
            except (FileError, DataError) as err:
                if comp.skipError == SkipErrors.SKIP:
                    failed.append(comp)
                    self.logger.warning(
                        f'SKIP Failed Component: {comp!r} with error: {err}'
                    )
                    comp = prev
                    # can skip error for this component
                    continue
                self._data_error(status='data_error', exc=err, step_name=step_name)
            except (ProviderError, ComponentError, NotSupported) as err:
                if comp.skipError == SkipErrors.SKIP:
                    # can skip error for this component
                    failed.append(comp)
                    self.logger.warning(
                        f'SKIP Failed Component: {comp!r} with error: {err}'
                    )
                    empty = check_empty(comp.output())
                    if empty:
                        # avoid when failed, lost the chain of results:
                        others = comp.previous
                        if isinstance(others, list):
                            previous = others[0]
                            comp.result = previous.output()
                        else:
                            try:
                                comp.result = others.output()
                            except AttributeError:
                                self.logger.warning(
                                    'There is no Previous Component Output'
                                )
                                comp.result = None
                    _exit = False
                    continue
                else:
                    self._on_error(
                        status='error',
                        exc=err,
                        step_name=step_name
                    )
            except Exception as err:
                self._on_exception(step_name, err)
            # passing variables between components
            await self.exchange_variables(comp, result=result)
        try:
            # stop stats:
            if self.enable_stat is True:
                await self.stat.stop()
        except Exception as err:
            self.logger.error(str(err))
        # ending the pile:
        self._pile = []
        del self._pile
        if _exit is True:
            # TODO: checking the failed list for returning errors.
            self.logger.error(
                f"Task exit if True: {failed!r}"
            )
            self._state = TaskState.DONE_WITH_WARNINGS
            self._not_found(status='done_warning', exc=failed)
            return False
        else:
            if check_empty(result):
                if self.is_subtask is False:
                    self._state = TaskState.DONE_WITH_NODATA
                    # mark data not found, is a warning
                    self._not_found(status='not_found', exc=None)
                else:
                    self._state = TaskState.DONE_WITH_NODATA
            else:
                if self.is_subtask is False:
                    # avoid firing OnDone when is a subtask
                    self._on_done(result)
            if self._ignore_results is True:
                return True
            else:
                return result

    def plot(self) -> None:
        self._pile.plot_task()
