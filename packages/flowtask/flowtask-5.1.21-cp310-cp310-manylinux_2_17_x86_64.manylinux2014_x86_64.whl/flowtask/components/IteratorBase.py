# -*- coding: utf-8 -*-
from abc import ABC
import asyncio
from collections.abc import Callable
import traceback
import logging
from asyncdb.exceptions import NoDataFound, ProviderError
from flowtask.exceptions import (
    ComponentError,
    NotSupported,
    DataNotFound
)

from .abstract import DtComponent


class IteratorBase(DtComponent, ABC):
    """
    IteratorBase.

        Overview

        This component the Base Abstract for Task Iterators

    .. table:: Properties
       :widths: auto


    +--------------+----------+-----------+-------------------------------------------+
    | Name         | Required | Summary                                               |
    +--------------+----------+-----------+-------------------------------------------+
    |   start      |   Yes    | Start the function and the execution of the task      |
    +--------------+----------+-----------+-------------------------------------------+
    |  get_set     |   Yes    | function allows me to obtain parameters, conditions, variables    |
    |              |          | among many more data                                              |
    +--------------+----------+-----------+-------------------------------------------------------+
    |  get_job     |   Yes    | The function allows me to obtain the data stored in a job         |
    |              |          | variable                                                          |
    +--------------+----------+-----------+-------------------------------------------------------+
    |   print      |   Yes    | The function allows me to print the data in an organized way      |
    +--------------+----------+-----------+---------------------------------------------+
    |  get_attr    |   Yes    | Function that allows me to extract attributes from the  |
    |              |          |  processed data                                         |
    +--------------+----------+-----------+---------------------------------------------+



    Return the list of arbitrary days

    """

    def __init__(
            self,
            loop: asyncio.AbstractEventLoop = None,
            job: Callable = None,
            stat: Callable = None,
            **kwargs
    ):
        self.iterate: bool = False
        self._iterator: bool = True
        self._conditions: dict = {}
        super(IteratorBase, self).__init__(loop=loop, job=job, stat=stat, **kwargs)

    async def start(self, **kwargs):
        """
        start.

            Initialize (if needed) a task
        """
        if self.previous:
            self.data = self.input
        return True

    def get_step(self):
        params = None
        try:
            step, idx = self._TaskPile.nextStep(self.TaskName)
            params = step.params()
            try:
                if params['conditions']:
                    self._conditions[step.name] = params['conditions']
            except KeyError:
                pass
            params['ENV'] = self._environment
            # params
            params['params'] = self._params
            # parameters
            params['parameters'] = self._parameters
            # useful to change variables in set var components
            params['_vars'] = self._vars
            # variables dictionary
            params['variables'] = self._variables
            params['_args'] = self._args
            # argument list for components (or tasks) that need argument lists
            params['arguments'] = self._arguments
            # for components with conditions, we can add more conditions
            conditions = params.get('conditions', {})
            step_conds = self._conditions.get(step.name, {})
            params['conditions'] = {**conditions, **step_conds}
            # attributes only usable component-only
            params['attributes'] = self._attributes
            # the current Pile of components
            params['TaskPile'] = self._TaskPile
            # params['TaskName'] = step_name
            params['debug'] = self._debug
            params['argparser'] = self._argparser
            # the current in-memory connector
            params['memory'] = self._memory
            target = step.component
            # remove this element from tasks, doesn't need to run again
            self._TaskPile.delStep(idx)
            # return target and params
            return [step, target, params]
        finally:
            pass

    def get_job(self, target, **params):
        job = None
        try:
            job = target(
                job=self,
                loop=self._loop,
                stat=self.stat,
                **params
            )
            return job
        except Exception as err:
            raise ComponentError(
                f"Generic Component Error on {target}, error: {err}"
            ) from err

    async def async_job(self, job, step_name):
        start = getattr(job, 'start', None)
        if callable(start):
            try:
                if asyncio.iscoroutinefunction(start):
                    st = await job.start()
                else:
                    st = job.start()
                self._logger.debug(f'STARTED: {st}')
            except (NoDataFound, DataNotFound) as err:
                raise DataNotFound(f"{err!s}") from err
            except (ProviderError, ComponentError, NotSupported) as err:
                raise ComponentError(
                    f"Error running Start Function on {step_name}, error: {err}"
                ) from err

        else:
            raise ComponentError(
                f"Error running Function on {step_name}"
            )
        try:
            run = getattr(job, 'run', None)
            if asyncio.iscoroutinefunction(run):
                result = await job.run()
            else:
                result = job.run()
            self._result = result
            return self._result
        except (NoDataFound, DataNotFound) as err:
            raise DataNotFound(f"{err!s}") from err
        except (ProviderError, ComponentError, NotSupported) as err:
            raise NotSupported(
                f"Error running Component {step_name}, error: {err}"
            ) from err
        except Exception as err:
            self._logger.exception(err, exc_info=True)
            raise ComponentError(
                f"Iterator Error on {step_name}, error: {err}"
            ) from err
        finally:
            try:
                close = getattr(job, 'close', None)
                if asyncio.iscoroutinefunction(close):
                    await job.close()
                else:
                    job.close()
            except Exception:
                pass
