"""
CreateReport.

Using a Jinja2 Template to crete a Report and, optionally, send via Email.
"""
import asyncio
import datetime
from typing import Dict, List, Callable
from pathlib import Path
from navconfig.logging import logging
from notify import Notify
from notify.models import Actor
from flowtask.components import DtComponent
from flowtask.template import getTemplateHandler
from flowtask.exceptions import (
    ComponentError,
    FileNotFound
)
from flowtask.conf import BASE_DIR, TASK_PATH
from .charts import loadChart


class CreateReport(DtComponent):
    """CreateReport.

    Create Rich Reports and send it through Notify
    """

    def __init__(
            self,
            loop: asyncio.AbstractEventLoop = None,
            job: Callable = None,
            stat: Callable = None,
            **kwargs
    ):
        """Init Method."""
        self._data: Dict = {}
        self._parser: Callable = None
        self._chartparser: Callable = None
        self.template_file: str = None
        self.recipients = []
        self.send: Dict = None
        self.message: str = None
        super(CreateReport, self).__init__(
            loop=loop,
            job=job,
            stat=stat,
            **kwargs
        )

    async def start(self, **kwargs):
        template_dir = Path(
            TASK_PATH, self._program, 'templates'
        )
        echart_dir = Path(
            BASE_DIR, "DataIntegration", "dataintegration", "templates"
        )
        if self.previous:
            self._data = self.input
        try:
            self._parser = getTemplateHandler(newdir=template_dir)
            self._chartparser = getTemplateHandler(newdir=echart_dir)
        except Exception as err:
            logging.exception(err)
            raise ComponentError(
                f'CreateReport: Unable to load Template Parser: {err}'
            ) from err
        template_file = template_dir.joinpath(self.template_file)
        if not template_file.is_file():
            raise FileNotFound(
                f'CreateReport: Missing Template File: {template_file}'
            )
        if hasattr(self, 'masks'):
            for key, value in self.send.items():
                self.send[key] = self.mask_replacement(value)
        # getting the mailing list:
        try:
            lst = self.send['list']
        except AttributeError:
            lst = 'owner'
        sql = f"SELECT * FROM troc.get_mailing_list('{lst!s}')"
        db = self.get_connection()
        async with await db.connection() as conn:
            try:
                result, error = await conn.query(sql)
                if error:
                    raise ComponentError(
                        f'CreateReport: Error on Recipients: {error!s}.')
                for r in result:
                    actor = Actor(**dict(r))
                    self.recipients.append(actor)
            except Exception as err:
                logging.exception(err)
        if not self.recipients:
            raise ComponentError(
                'CreateReport: Invalid Number of Recipients.'
            )

    def status_sent(self, recipient, message, result, *args, **kwargs):
        print(
            f'Notification status {result!s} to {recipient.account!s}'
        )
        # logger:
        logging.info(
            f'Notification status {result!s} to {recipient.account!s}'
        )
        # TODO: register sent on a logger database

    async def send_message(self, recipients: List, data: Dict = None):
        try:
            emailService = Notify(
                self.send['via'],
                loop=self._loop
            )
        except Exception as err:
            raise ComponentError(
                f"Error loading Notify Service: {err!s}"
            ) from err
        # add event for sent function
        emailService.sent = self.status_sent
        self.message = self.send['message']
        # create echart graph based on template
        graph = {}
        if hasattr(self, 'echarts'):
            for dataset, chart in self.echarts['charts'].items():
                ds = self._data[dataset]
                graph_name = chart['name']
                try:
                    graphtype = chart['type']
                    del chart['type']
                except KeyError:
                    graphtype = 'bar'
                try:
                    title = chart['title']
                    del chart['title']
                except KeyError:
                    title = dataset
                chart = loadChart(
                    graphtype,
                    data=ds,
                    title=title,
                    **chart
                )
                img = chart.image()
                graph[graph_name] = img
        # else:
        emailTemplate = self._parser.get_template(self.template_file)
        for user in recipients:
            # TODO: add dot notation to Actor Model
            email = user.account['address']
            args = {
                "user": user,
                "html": emailTemplate,
                "email": email,
                "created_at": datetime.datetime.now(),
                **graph
            }
            self.message['created_at'] = datetime.datetime.now()
            other = {}
            if 'arguments' in self.send:
                other = self.send['arguments']
            args = {**data, **args, **other}
            content = emailTemplate.render(args)
            try:
                logging.debug(f'Sending Email to {user} via {email}')
                # TODO: Send email via Worker or thread (async)
                await emailService.send(
                    recipient=user,
                    template=None,
                    message=content,
                    **self.message
                )
            except Exception as err:
                logging.exception(err)
                raise ComponentError(
                    f'Error Sending Email: {err}'
                ) from err
            finally:
                try:
                    await emailService.close()
                except Exception as err:
                    logging.error(err)

    def close(self):
        pass

    async def run(self):
        try:
            await self.send_message(self.recipients, self._data)
            self._result = self.data
            return self._result
        except Exception as err:
            logging.exception(err)
            raise ComponentError(
                f'CreateReport: Error sending Report: {err!s}'
            ) from err
