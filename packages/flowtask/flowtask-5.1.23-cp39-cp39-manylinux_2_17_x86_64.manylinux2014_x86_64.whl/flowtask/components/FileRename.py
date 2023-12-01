import os
import asyncio
from pathlib import Path
from flowtask.exceptions import FileNotFound, FileError, ComponentError
from .FileBase import FileBase


class FileRename(FileBase):
    """
    FileRename.

        Rename a File to a new name.
    """

    def start(self, **kwargs) -> bool:
        """Check for File and Directory information."""
        self._source: str = None
        self._destination: str = None
        if not hasattr(self, 'ignore_missing'):
            self.ignore_missing = False
        if not hasattr(self, 'directory'):
            raise ComponentError(
                "Missing Source Directory."
            )
        if isinstance(self.directory, str):
            self.directory = Path(self.directory).resolve()
        if hasattr(self, 'source'):
            # processing source
            filename = self.set_variables(
                self.mask_replacement(self.source)
            )
            self._logger.notice(f'Source File {filename}')
            path = self.directory.joinpath(filename)
            if '*' in filename:
                raise ComponentError(
                    'FileRename: Cannot Support wildcard on filenames.'
                )
            else:
                if path.is_file():
                    self._logger.debug(
                        f'Source Filename: {filename}'
                    )
                    self._source = path
                else:
                    if self.ignore_missing is False:
                        raise FileNotFound(
                            f"File {path} was not found."
                        )
        else:
            raise ComponentError(
                'FileRename: Missing Source information.'
            )
        if hasattr(self, 'destination'):
            # processing destination
            filename = self.set_variables(
                self.mask_replacement(self.destination)
            )
            path = self.directory.joinpath(filename)
            if self._source and path.exists():  # we cannot rename a file overwriting another.
                raise FileError(
                    f"Cannot Rename to {filename}, file Exists"
                )
            self._destination = path
        else:
            raise FileNotFound(
                'FileRename: Missing Destination.'
            )
        return True

    async def run(self):
        """Delete File(s)."""
        self._result = {}
        if self._source is not None and self._source.exists():
            await asyncio.to_thread(os.rename, self._source, self._destination)
            self._result[self._source] = self._destination
            self.add_metric('FILE_RENAMED', self._result)
        if self.ignore_missing is False:
            raise FileNotFound(
                f"Source File {self._source} was not found."
            )
        return self._result

    async def close(self):
        """Method."""
