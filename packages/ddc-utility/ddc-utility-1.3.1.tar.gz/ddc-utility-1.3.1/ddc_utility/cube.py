
import xarray as xr
import s3fs
from fsspec import AbstractFileSystem
from fsspec.asyn import AsyncFileSystem

from typing import Union
from ddc_utility.store import ZarrCubeStore


def open_cube(path: str, fs: Union[AbstractFileSystem, AsyncFileSystem] = None, group: str = None, mode: str = "r", **kwargs):

    store = ZarrCubeStore(path, mode=mode, fs=fs)

    return store.read_cube(group=group, **kwargs)
