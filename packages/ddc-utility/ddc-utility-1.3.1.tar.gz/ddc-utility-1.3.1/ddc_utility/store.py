import xarray as xr
from ddc_utility.fs import BaseFSStore
from zarr.storage import FSStore
import os
import fsspec

class NetCDFCubeStore(BaseFSStore):
    def __init__(self, path, mode="w", **kwargs):
        self._protocol = fsspec.core.split_protocol(path)
        super().__init__(path, mode=mode, **kwargs)

    def __repr__(self):
        return f"NetCDFCubeStore(path={self.path}, mode={self.mode})"
    
    def read_cube(self, path: str, **kwargs):
        if not self.exists(path):
            raise FileNotFoundError(f"File not found: {path}")

        store_path = self.dir_path(path)

        if "engine" not in kwargs:
            kwargs["engine"] = "h5netcdf"
        with self.fs.open(store_path) as fileObj:
            ds = xr.open_dataset(fileObj, **kwargs).compute()

        return ds

    def write_cube(self, ds: xr.Dataset, path: str, **kwargs):
        if "engine" not in kwargs:
            kwargs["engine"] = "h5netcdf"
        if format not in kwargs:
            kwargs["format"] = "NETCDF4"
        ds.to_netcdf(path, **kwargs)

    def clear_cache(self):
        self.fs.invalidate_cache()

    def exists(self, path: str = ""):
        path = self.dir_path(path)
        return self.fs.exists(path)
    
    @classmethod
    def guess_can_open(
        cls,
        path: str,
    ) -> bool:
        if isinstance(path, str):
            _, ext = os.path.splitext(path)
            return ext in {".nc"}

        return False

    @property
    def is_read_only(self):
        if self.mode == "r":
            return True
        else:
            return False

    @property
    def is_remote(self):
        return self._protocol not in (None, "file")
    
class ZarrCubeStore(FSStore):
    def __init__(self, path, mode="w", **kwargs):
        self._protocol = fsspec.core.split_protocol(path)
        super().__init__(path, mode=mode, **kwargs)

    def __repr__(self):
        return f"ZarrCubeStore(path={self.path}, mode={self.mode})"

    def read_cube(self, group: str = None, **kwargs):
        if not self.exists(group):
            raise FileNotFoundError(f"Zarr group under path not found: {group}")
 
        return xr.open_zarr(self, group=group, **kwargs)

    def write_cube(self, ds: xr.Dataset, **kwargs):
        ds.to_zarr(self, **kwargs)
    
    def clear_cache(self):
        self.fs.invalidate_cache()

    def exists(self, path: str = ""):
        path = self.dir_path(path)
        return self.fs.exists(path)
    
    @classmethod
    def guess_can_open(
        cls,
        path: str,
    ) -> bool:
        if isinstance(path, str):
            _, ext = os.path.splitext(path)
            return ext in {".zarr"}

        return False

    @property
    def is_read_only(self):
        if self.mode == "r":
            return True
        else:
            return False

    @property
    def is_remote(self):
        return self._protocol not in (None, "file")
