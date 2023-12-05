import pathlib
import typing
import zipfile
from io import BytesIO


class ZipWrapper:
    """ A wrapper around a :py:class:`~zipfile.ZipFile`.
    The zip file can be either located in the filesystem or in memory.

    Example usage::

        zip_wrapper = ZipWrapper('test.zip')
        with zip_wrapper as zip_file, zip_file.open() as f:
            # f is now an open zipfile.ZipFile object

    :param path: The path to the zip file, or
    :param content: A :py:class:`bytes` or :py:class:`memoryview` containing the data of the zip file
    """
    path: typing.Optional[pathlib.Path] = None
    content: typing.Union[bytes, memoryview, None] = None
    zip_file: typing.Optional[zipfile.ZipFile] = None
    __nesting: int = 0

    def __init__(self, *, path: pathlib.Path = None, content: typing.Union[bytes, memoryview] = None):
        self.__init(path=path, content=content)

    def __init(self, path: typing.Optional[pathlib.Path], content: typing.Union[bytes, memoryview, None]):
        self.path = path
        self.content = content
        self.zip_file = None
        self.__nesting = 0

    def __enter__(self):
        if self.zip_file is None:
            self.__nesting = 1
            self.zip_file = zipfile.ZipFile(self.path if self.path else BytesIO(self.content), 'r')
        else:
            self.__nesting += 1

        return self.zip_file

    def __exit__(self, *args, **kwargs):
        self.__nesting -= 1
        if self.__nesting == 0:
            self.close()

    def __del__(self):
        self.close()

    def close(self):
        """ Close the wrapped zip file """
        if self.zip_file:
            try:
                self.zip_file.close()
            except OSError:
                pass

            self.__nesting = 0
            self.zip_file = None

    def __getstate__(self):
        if self.path is not None:
            return {'path': self.path}
        elif self.content is not None:
            return {'content': bytes(self.content)}
        else:
            return {}

    def __setstate__(self, state):
        self.close()
        self.__init(state.get('path'), state.get('content'))
