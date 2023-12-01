from abc import abstractmethod
import logging
import asyncio
import glob
from pathlib import PurePath
from collections.abc import Callable
from flowtask.exceptions import (
    FileNotFound,
    ComponentError
)
from flowtask.utils.mail import MailMessage
from flowtask.utils import check_empty
from .abstract import DtComponent


class FileBase(DtComponent):
    """
    FileBase.

        Abstract Component for all kind of File-based Components.
    """

    def __init__(
            self,
            loop: asyncio.AbstractEventLoop = None,
            job: Callable = None,
            stat: Callable = None,
            **kwargs
    ):
        """Init Method."""
        # self.directory: str = None
        self._filenames: list[PurePath] = []
        self._path: str = None
        super(FileBase, self).__init__(
            loop=loop,
            job=job,
            stat=stat,
            **kwargs
        )

    async def start(self, **kwargs):
        """Check for File and Directory information."""
        try:
            if hasattr(self, 'directory'):
                self.directory = self._filestore.get_directory(
                    self.directory
                )
            # check for filename:
            if self.previous and not check_empty(self.input):
                if not hasattr(self, 'ignore_previous') or self.ignore_previous is False:
                    if not isinstance(self.previous, FileBase):
                        # avoid chaining components
                        if isinstance(self.input, list):
                            if isinstance(self.input[0], MailMessage):
                                self._filenames = []
                                for file in self.input:
                                    for f in file.attachments:
                                        fname = f['filename']
                                        logging.debug(f'File: Detected attachment: {fname}')
                                        self._filenames.append(fname)
                            elif 'files' in self.input:
                                self._filenames = self.input['files']
                            else:
                                self._filenames = self.input
                            return True
                        elif isinstance(self.input, dict):
                            if 'files' in self.input:
                                # there is a "files" attribute in dictionary:
                                self._filenames = self.input['files']
                        else:
                            self._filenames = [self.input]
                        return True
            if hasattr(self, 'filename'):
                if isinstance(self.filename, list):
                    for file in self.filename:
                        self._filenames.append(self.directory.joinpath(file))
                elif isinstance(self.filename, PurePath):
                    self._filenames.append(self.filename)
                elif isinstance(self.filename, str):
                    if '*' in self.filename:
                        # is a glob list of files
                        path = self.directory.joinpath(self.filename)
                        listing = glob.glob(str(path))  # TODO using glob from pathlib
                        for fname in listing:
                            logging.debug(
                                f"Filename > {fname}"
                            )
                            self._filenames.append(fname)
                    else:
                        self.filename = self.mask_replacement(self.filename)
                        self._path = self.directory.joinpath(self.filename)
                        self._filenames.append(self._path)
                return True
            elif hasattr(self, 'file'):
                filename = self.process_pattern('file')
                if hasattr(self, 'masks'):
                    filename = self.mask_replacement(filename)
                # path for file
                self._path = self.directory.joinpath(filename)
                listing = glob.glob(str(self._path))
                if not listing:
                    raise FileNotFound(
                        f'FileExists: There are no files in {self._path}'
                    )
                for fname in listing:
                    logging.debug(
                        f"Filename > {fname}"
                    )
                    self._filenames.append(fname)
                    logging.debug(f' ::: Checking for Files: {self._filenames}')
                return True
            else:
                raise ComponentError(
                    'File: Invalid parameters'
                )
        except Exception as err:
            raise ComponentError(
                f'File: Invalid Arguments: {err!s}'
            ) from err

    def get_filelist(self) -> list[PurePath]:
        if hasattr(self, 'pattern'):
            value = self.pattern
            if hasattr(self, 'masks'):
                for mask, replace in self._mask.items():
                    value = str(value).replace(mask, replace)
            if self._variables:
                value = value.format(**self._variables)
            files = (f for f in self.directory.glob(value))
        elif hasattr(self, 'file'):
            # using pattern/file version
            value = self.get_filepattern()
            files = (f for f in self.directory.glob(value))
        elif hasattr(self, 'filename'):
            # already discovered by start:
            files = (self._filenames)
        else:
            files = (f for f in self.directory.iterdir() if f.is_file())
        return files

    @abstractmethod
    async def run(self):
        """Run File checking."""

    @abstractmethod
    async def close(self):
        """Method."""
