"""
Function Executor.
"""
import logging
import traceback
from typing import Any
import builtins
from collections.abc import Callable
from querysource.types.validators import Entity
import querysource.utils.functions as qsfunctions
from .functions import *


def getFunction(fname: str) -> callable:
    """
    Get any function using name.
    """
    try:
        func = getattr(qsfunctions, fname)
    except AttributeError:
        try:
            func = globals()[fname]
        except AttributeError:
            try:
                func = getattr(builtins, fname)
            except AttributeError:
                func = None
    return func


def fnExecutor(value: Any, env: Callable = None, escape: bool = False, quoting: bool = False) -> Any:
    if isinstance(value, list):
        try:
            fname = value[0]
            try:
                kwargs = value[1]
            except IndexError:
                kwargs = None
            try:
                func = getattr(qsfunctions, fname)
            except AttributeError:
                try:
                    func = getattr(builtins, fname)
                except AttributeError:
                    func = globals()[fname]
            if not func:
                logging.warning(
                    f"Function {fname} doesn't exist in Builtins or DI."
                )
                return None
            if kwargs:
                if env is not None:
                    kwargs['env'] = env
                try:
                    try:
                        return func(**kwargs)
                    except Exception:
                        if 'env' in kwargs:
                            del kwargs['env']
                        return func(**kwargs)
                except (TypeError, ValueError) as err:
                    logging.exception(str(err), exc_info=True, stack_info=True)
                    traceback.print_exc()
                    return ''
            else:
                try:
                    return func()
                except (TypeError, ValueError):
                    return ''
        except (NameError, KeyError) as err:
            logging.exception(str(err), exc_info=True, stack_info=True)
            traceback.print_exc()
            return ''
    else:
        if isinstance(value, str):
            if escape is True:
                return f"'{str(value)}'"
            elif quoting is True:
                return Entity.quoteString(value)
            else:
                return f"{str(value)}"
        return value
