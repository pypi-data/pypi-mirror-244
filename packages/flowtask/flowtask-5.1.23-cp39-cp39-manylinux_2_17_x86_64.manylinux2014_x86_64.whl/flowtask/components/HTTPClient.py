"""Basic HTTP Connection Request."""
import os
import asyncio
import random
# configuration and settings
from functools import partial
from typing import (
    Dict,
    List,
    Union
)
from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.parse import urlencode
import urllib3
import pandas as pd
import uvloop
import requests
from requests.auth import HTTPBasicAuth
from requests.exceptions import HTTPError
from navconfig import config
from navconfig.logging import logging
from proxylists.proxies import FreeProxy
from bs4 import BeautifulSoup as bs
from lxml import html, etree
from querysource.types import strtobool
from flowtask.utils.json import JSONContent
from flowtask.utils import cPrint, SafeDict
from flowtask.utils.functions import check_empty
from flowtask.exceptions import (
    DataNotFound,
    ComponentError,
    FileNotFound
)
from .DownloadFrom import DownloadFromBase


logging.getLogger("urllib3").setLevel(logging.WARNING)
urllib3.disable_warnings()

# make asyncio use the event loop provided by uvloop
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

ua = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322)",
    "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko; googleweblight) Chrome/38.0.1025.166 Mobile Safari/535.19",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.10240",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
    "Mozilla/5.0 (X11; Windows NT 10.0; rv:19.0) Gecko/20100101 Firefox/19.0 Iceweasel/19.0.2",
    "Mozilla/5.0 (X11; U; Linux i686; sk; rv:1.9.0.4) Gecko/2008111217 Fedora/3.0.4-1.fc10 Firefox/3.0.4"
]

class HTTPClient(DownloadFromBase):
    """
    HTTPClient.

    Overview

           UserComponent: (abstract) ->

    .. table:: Properties
       :widths: auto


    +-----------+----------+-----------+----------------------------------------------+
    | Name      | Required | Summary                                                  |
    +-----------+----------+-----------+----------------------------------------------+
    | start     |   Yes    | It is executed when the component is "initialized",      |
    |           |          | it MUST return TRUE if it does not fail                  |
    +-----------+----------+-----------+----------------------------------------------+
    | run       |   Yes    | Is the code that will execute the component ,must return TRUE or  |
    |           |          | a content if it does not fail, but fails is declared      |
    +-----------+----------+-----------+-----------------------------------------------+
    | close     |   Yes    | It is used for any cleaning operation                     |
    +-----------+----------+-----------+-----------------------------------------------+


    Return the list of arbitrary days

    """
    accept: str = 'application/xhtml+xml'
    port: int = 80

    def __init__(
            self,
            loop: asyncio.AbstractEventLoop = None,
            job: Callable = None,
            stat: Callable = None,
            **kwargs
    ):
        if 'url' in kwargs:
            self.url = kwargs['url']
            del kwargs['url']
        else:
            self.url: str = None
        self.use_proxy: bool = False
        self._proxies: list = []

        self.rotate_ua: bool = kwargs.pop('rotate_ua', False)
        self.timeout: int = 30
        self.headers: dict = {}
        self.auth: dict = {}
        self.auth_type: str = None
        self.token_type: str = 'Bearer'
        self._user: str = None
        self._pwd: str = None
        # beautiful soup and html parser:
        self._bs: Callable = None
        self._parser: Callable = None
        self._environment = config
        # calling parent
        super(HTTPClient, self).__init__(loop=loop, job=job, stat=stat, **kwargs)
        try:
            as_dataframe = kwargs['as_dataframe']
            del kwargs['as_dataframe']
            if isinstance(as_dataframe, bool):
                self.as_dataframe = as_dataframe
            else:
                self.as_dataframe: bool = strtobool(as_dataframe)
        except KeyError:
            self.as_dataframe: bool = True
        # Credentials:
        self.credentials: dict = kwargs.pop('credentials', {})
        self.method: str = kwargs.pop('method', 'get')
        self.parameters = {}
        if self.rotate_ua is True:
            self._ua = random.choice(ua)
        else:
            self._ua: str = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'
        self.headers = {
            "Accept": self.accept,
            "Accept-Encoding": "gzip, deflate",
            "DNT": "1",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": self._ua,
            **self.headers
        }
        self._encoder = JSONContent()
        # other arguments:
        self._arguments = kwargs

    async def get_proxies(self):
        return await FreeProxy().get_list()

    async def refresh_proxies(self):
        if self.use_proxy is True:
            self._proxies = await self.get_proxies()

    def build_url(self, url, queryparams: str = '', args=None):
        url = str(url).format_map(
            SafeDict(**self._variables)
        )
        if args:
            u = url.format(**args)
        else:
            u = url
        if queryparams:
            if '?' in u:
                full_url = u + '&' + queryparams
            else:
                full_url = u + '?' + queryparams
        else:
            full_url = u
        logging.debug(f'Resource URL: {full_url!s}')
        return full_url

    def get_env_value(self, key, default: str = None):
        if val := os.getenv(key):
            return val
        elif val := self._environment.get(key, default):
            return val
        else:
            return key

    async def request(self, url, method: str = 'GET', data: dict = None):
        """
        request
            connect to an http source
        """
        result = []
        error = {}
        auth = None
        executor = ThreadPoolExecutor(2)
        proxies = None
        if self._proxies:
            proxy = random.choice(self._proxies)
            proxies = {
                "http": proxy,
                "https": proxy,
                "ftp": proxy
            }
        if self.credentials:
            if 'apikey' in self.auth:
                self.headers['Authorization'] = f"{self.token_type} {self.auth['apikey']}"
            elif self.auth_type == 'api_key':
                self.headers = {**self.headers, **self.credentials}
            elif self.auth_type == 'key':
                url = self.build_url(
                    url,
                    args=self._arguments,
                    queryparams=urlencode(self.credentials)
                )
            elif self.auth_type == 'basic':
                auth = HTTPBasicAuth(
                    self.credentials['username'],
                    self.credentials['password']
                )
            else:
                auth = HTTPBasicAuth(
                    self.credentials['username'],
                    self.credentials['password']
                )
        elif self._user and self.auth_type == 'basic':
            auth = HTTPBasicAuth(self._user, self._pwd)
        cPrint(f'HTTP: Connecting to {url}', level='DEBUG')
        self.add_metric('URL', url)
        self.add_metric('METHOD', method)
        if auth is not None:
            args = {
                "auth": auth,
                "verify": False
            }
        else:
            args = {}
        if hasattr(self, 'download'):
            self.headers['Accept'] = 'application/octet-stream'
            self.headers['Content-Type'] = 'application/octet-stream'
            if hasattr(self, 'use_streams'):
                self.headers['Transfer-Encoding'] = 'chunked'
                args["stream"] = True
        if self._debug is True:
            self.add_metric('HEADERS', self.headers)
        if proxies is not None:
            self.add_metric('Proxies', proxies)
        if method == 'get':
            my_request = partial(
                requests.get,
                headers=self.headers,
                timeout=self.timeout,
                proxies=proxies,
                **args
            )
        elif method == 'post':
            my_request = partial(
                requests.post,
                headers=self.headers,
                data=data,
                timeout=self.timeout,
                proxies=proxies,
                **args
            )
        elif method == 'put':
            my_request = partial(
                requests.put,
                headers=self.headers,
                data=data,
                timeout=self.timeout,
                proxies=proxies,
                **args
            )
        elif method == 'delete':
            my_request = partial(
                requests.delete,
                headers=self.headers,
                data=data,
                timeout=self.timeout,
                proxies=proxies,
                **args
            )
        elif method == 'patch':
            my_request = partial(
                requests.patch,
                headers=self.headers,
                data=data,
                timeout=self.timeout,
                proxies=proxies,
                *args
            )
        else:
            my_request = partial(
                requests.post,
                headers=self.headers,
                data=data,
                timeout=self.timeout,
                proxies=proxies,
                **args
            )
        # making request
        loop = asyncio.get_event_loop()
        future = [
            loop.run_in_executor(executor, my_request, url)
        ]
        try:
            result, error = await self.process_request(future, url)
            if error:
                if isinstance(error, BaseException):
                    raise error
                else:
                    raise ComponentError(
                        f"{error!s}"
                    )
            return (result, error)
        except requests.exceptions.ReadTimeout as err:
            self._logger.warning(
                f"Timeout Error: {err!r}"
            )
            # TODO: retrying
            raise ComponentError(
                f"Timeout: {err}"
            ) from err
        except Exception as err:
            print('ERROR >>>> ', err)
            self._logger.exception(
                str(err), stack_info=True
            )
            raise ComponentError(
                f"Error: {err}"
            ) from err

    async def process_request(self, future, url: str):
        # getting the result, based on the Accept logic
        error = None
        result = None
        loop = asyncio.get_running_loop()
        asyncio.set_event_loop(loop)
        for response in await asyncio.gather(*future):
            # Check for HTTP errors
            try:
                response.raise_for_status()
            except HTTPError as http_err:
                # Handle HTTP errors here
                error = http_err
                # Log the error or perform other error handling
                self._logger.error(
                    f"HTTP error occurred: {http_err}"
                )
                # You can choose to continue, break, or return based on your logic
                continue
            try:
                if hasattr(self, 'download'):
                    # Filename:
                    filename = os.path.basename(url)
                    # Get the filename from the response headers, if available
                    content_disposition = response.headers.get('content-disposition')
                    if content_disposition:
                        _, params = content_disposition.split(';')
                        try:
                            key, value = params.strip().split('=')
                            if key == 'filename':
                                filename = value.strip('\'"')
                        except ValueError:
                            pass
                    if '{filename}' in str(self.filename):
                        self.filename = str(self.filename).format_map(
                            SafeDict(filename=filename)
                        )
                    if '{' in str(self.filename):
                        self.filename = str(self.filename).format_map(
                            SafeDict(**self._arguments)
                        )
                    if isinstance(self.filename, str):
                        self.filename = Path(self.filename)
                    # Saving File in Directory:
                    total_length = response.headers.get('Content-Length')
                    self._logger.info(
                        f'HTTPClient: Saving File {self.filename}, size: {total_length}'
                    )
                    pathname = self.filename.parent.absolute()
                    if not pathname.exists():
                        # Create a new directory
                        pathname.mkdir(parents=True, exist_ok=True)
                    response.raise_for_status()
                    transfer = response.headers.get("transfer-encoding", None)
                    if transfer is None:
                        chunk_size = int(total_length)
                    else:
                        chunk_size = 8192
                    # async with AIOFile(self.filename, 'wb') as fp:
                    with open(self.filename, 'wb') as fp:
                        try:
                            for chunk in response.iter_content(
                                chunk_size=chunk_size
                            ):
                                fp.write(chunk)
                            fp.flush()
                        except Exception:
                            pass
                    self._logger.debug(
                        f'Filename Saved Successfully: {self.filename}'
                    )
                    result = self.filename
                elif self.accept in ('text/html'):
                    result = response.content  # Get content of the response as bytes
                    try:
                        # html parser for lxml
                        self._parser = html.fromstring(result)
                        # BeautifulSoup parser
                        self._bs = bs(response.text, 'html.parser')
                        result = self._bs
                    except Exception as e:
                        error = e
                elif self.accept in ('application/xhtml+xml', 'application/xml'):
                    result = response.content  # Get content of the response as bytes
                    try:
                        self._parser = etree.fromstring(result)
                    except Exception as e:
                        error = e
                elif self.accept == 'application/json':
                    try:
                        result = response.json()
                    except Exception as e:
                        logging.error(e)
                        # is not an json, try first with beautiful soup:
                        try:
                            self._bs = bs(response.text, 'html.parser')
                            result = self._bs
                        except Exception:
                            error = e
                else:
                    result = response.text
            except (requests.exceptions.ProxyError) as err:
                raise ComponentError(
                    f"Proxy Connection Error: {err!r}"
                ) from err
            except (requests.ReadTimeout) as err:
                return (result, err)
            except (requests.exceptions.HTTPError) as e:
                # Log the error or perform other error handling
                self._logger.error(
                    f"HTTP error occurred: {error}"
                )
                raise ComponentError(
                    f"HTTP Error: {error!r}, ex: {e!s}"
                ) from e
            except Exception as e:
                logging.exception(e)
                return (result, e)
        # returning results
        return (result, error)

    def create_dataframe(self, result: Union[List, Dict]):
        if check_empty(result):
            self._variables['_numRows_'] = 0
            self._variables[f'{self.TaskName}_NUMROWS'] = 0
            raise DataNotFound(
                "HTTPClient: No Data was Found."
            )
        try:
            df = pd.DataFrame(result)
            # Attempt to infer better dtypes for object columns.
            df.infer_objects()
            if hasattr(self, "infer_types"):
                df = df.convert_dtypes()
            if hasattr(self, "drop_empty"):
                df.dropna(axis=1, how='all', inplace=True)
                df.dropna(axis=0, how='all', inplace=True)
            if hasattr(self, 'dropna'):
                df.dropna(subset=self.dropna, how='all', inplace=True)
            if self._debug:
                print('::: Printing Column Information === ')
                columns = list(df.columns)
                for column in columns:
                    t = df[column].dtype
                    print(column, '->', t, '->', df[column].iloc[0])
            numrows = len(df.index)
            self._variables['_numRows_'] = numrows
            self._variables[f'{self.TaskName}_NUMROWS'] = numrows
            self.add_metric('NUM_ROWS', numrows)
            self.add_metric('NUM_COLS', len(columns))
            return df
        except Exception as err:
            logging.error(
                f'Error Creating Dataframe {err!s}'
            )

    def var_replacement(self):
        for key, _ in self._arguments.items():
            if key in self._variables:
                self._arguments[key] = self._variables[key]

    async def start(self, **kwargs):
        if self.use_proxy is True:
            self._proxies = await self.get_proxies()
        self.var_replacement()
        super(HTTPClient, self).start()
        return True

    async def close(self):
        pass

    async def run(self):
        if isinstance(self.url, list):
            ## iterate over a list of URLs:
            results = {}
            for url in self.url:
                uri = self.build_url(
                    url,
                    args=self._arguments,
                    queryparams=urlencode(self.parameters)
                )
                try:
                    result, error = await self.request(
                        uri, self.method
                    )
                    if not result:
                        raise DataNotFound(
                            f"Data was not found on: {uri}"
                        )
                    if error is not None:
                        if isinstance(error, BaseException):
                            raise error
                        else:
                            raise ComponentError(
                                f"HTTPClient Error: {error}"
                            )
                    ## processing results:
                    if hasattr(self, 'download'):
                        ## add result to resultset
                        results[result] = True
                        if self._debug:
                            self._logger.debug(
                                f"File Exists > {result}"
                            )
                    else:
                        results[result] = result
                except Exception as err:
                    self._logger.exception(err, stack_info=True)
                    raise ComponentError(
                        f"HTTPClient Error: {err}"
                    ) from err
            ##
            self.add_metric('FILENAME', results)
            self._result = results
            return self._result
        else:
            self.url = self.build_url(
                self.url,
                args=self._arguments,
                queryparams=urlencode(self.parameters)
            )
            try:
                result, error = await self.request(
                    self.url, self.method
                )
                if not result:
                    raise DataNotFound(
                        f"Data was not found on: {self.url}"
                    )
                elif error is not None:
                    if isinstance(error, BaseException):
                        raise error
                    else:
                        raise ComponentError(
                            f"HTTPClient Error: {error}"
                        )
                # at here, processing Result
                if self.as_dataframe is True:
                    try:
                        result = self.create_dataframe(result)
                    except Exception as err:
                        raise ComponentError(
                            f"RESTClient Error: {err}"
                        ) from err
                elif hasattr(self, 'download'):
                    # File downloaded, return same as FileExists
                    file = result
                    self._logger.debug(
                        f' ::: Checking for File: {file}'
                    )
                    result = {}
                    if file.exists() and file.is_file():
                        result[file] = True
                        self.setTaskVar('DIRECTORY', file.parent)
                        self.setTaskVar('FILENAME', str(file.name))
                        self.setTaskVar('FILEPATH', file)
                        self.add_metric('FILENAME', file)
                    else:
                        raise FileNotFound(
                            f'FileExists: File Doesn\'t exists: {file}'
                        )
                self._result = result
                return self._result
            except Exception as err:
                self._logger.exception(err, stack_info=True)
                raise ComponentError(
                    f"HTTPClient Error: {err}"
                ) from err
