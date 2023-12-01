"""Data Integration Executor."""
import logging
import asyncio
from flowtask.runner import TaskRunner
from flowtask.utils import cPrint
from flowtask.utils.uv import install_uvloop


async def task(loop):
    runner = None
    try:
        runner = TaskRunner(loop=loop)
        async with runner as job:
            if await job.start():
                await job.run()
    except Exception as e:  # pylint: disable=W0718
        logging.exception(e, stack_info=False)
    finally:
        return runner


def main():
    install_uvloop()
    loop = asyncio.get_event_loop()
    loop.slow_callback_duration = 0.5  # Set threshold to 0.5 seconds
    try:
        result = loop.run_until_complete(
            task(loop)
        )
        if result:
            cPrint(' === RESULT === ', level="DEBUG")
            print(result.result)
            cPrint('== Task stats === ', level="INFO")
            print(result.stats)
    finally:
        loop.close()

if __name__ == '__main__':
    main()
