from typing import Union, Type
import os

class BaseFSStore:
    def __init__(
        self,
        url,
        mode="w",
        exceptions=(KeyError, PermissionError, IOError),
        fs=None,
        check=False,
        create=False,
        missing_exceptions=None,
        **storage_options,
    ):
        if not self._fsspec_installed():
            raise ImportError("`fsspec` is required to use ddc_utility.fs.BaseFSStore")
        import fsspec

        mapper_options = {"check": check, "create": create}

        if missing_exceptions is not None:
            mapper_options["missing_exceptions"] = missing_exceptions
    
        if fs is None:
            protocol, _ = fsspec.core.split_protocol(url)
            # set auto_mkdir to True for local file system
            if protocol in (None, "file") and not storage_options.get("auto_mkdir"):
                storage_options["auto_mkdir"] = True
            self.map = fsspec.get_mapper(url, **{**mapper_options, **storage_options})
            self.fs = self.map.fs  # for direct operations
            self.path = self.fs._strip_protocol(url)
        else:
            if storage_options:
                raise ValueError("Cannot specify both fs and storage_options")
            self.fs = fs
            self.path = self.fs._strip_protocol(url)
            self.map = self.fs.get_mapper(self.path, **mapper_options)

        self.mode = mode
        self.exceptions = exceptions

    def __repr__(self):
        return f"BaseFSStore(url={self.path}, mode={self.mode})"
    
    def __getitem__(self, key):
        key = normalize_key(key)
        try:
            return self.map[key]
        except self.exceptions as e:
            raise KeyError(key) from e

    def getitems(self, keys):

        keys_transformed = [normalize_key(key) for key in keys]
        results = self.map.getitems(keys_transformed, on_error="omit")
        # The function calling this method may not recognize the transformed keys
        # So we send the values returned by self.map.getitems back into the original key space.
        return {keys[keys_transformed.index(rk)]: rv for rk, rv in results.items()}

    def __setitem__(self, key, value):
        if self.mode == "r":
            raise ReadOnlyError()
        key = normalize_key(key)
        path = self.dir_path(key)
        try:
            if self.fs.isdir(path):
                self.fs.rm(path, recursive=True)
            self.map[key] = value
            self.fs.invalidate_cache(self.fs._parent(path))
        except self.exceptions as e:
            raise KeyError(key) from e

    def setitems(self, values):
        if self.mode == "r":
            raise ReadOnlyError()

        # Normalize keys and make sure the values are bytes
        values = {
            normalize_key(key): val
            for key, val in values.items()
        }
        self.map.setitems(values)
    
    def __delitem__(self, key):
        if self.mode == "r":
            raise ReadOnlyError()
        key = normalize_key(key)
        path = self.dir_path(key)
        if self.fs.isdir(path):
            self.fs.rm(path, recursive=True)
        else:
            del self.map[key]

    def delitems(self, keys):
        if self.mode == "r":
            raise ReadOnlyError()
        # only remove the keys that exist in the store
        nkeys = [normalize_key(key) for key in keys if key in self]
        # rm errors if you pass an empty collection
        if len(nkeys) > 0:
            self.map.delitems(nkeys)

    def __contains__(self, key):
        key = normalize_key(key)
        return key in self.map

    def __eq__(self, other):
        return type(self) is type(other) and self.map == other.map and self.mode == other.mode

    def keys(self):
        return iter(self.map)

    def __iter__(self):
        return self.keys()

    def __len__(self):
        return len(list(self.keys()))

    def dir_path(self, path=None):
        store_path = normalize_storage_path(path)
        return self.map._key_to_str(store_path)

    def listdir(self, path=None):
        store_path = self.dir_path(path)
        return self.fs.listdir(store_path, detail=False)

    def rmdir(self, path=None):
        if self.mode == "r":
            raise ReadOnlyError()
        store_path = self.dir_path(path)
        if self.fs.isdir(store_path):
            self.fs.rm(store_path, recursive=True)

    def getsize(self, path=None):
        store_path = self.dir_path(path)
        return self.fs.du(store_path, True, None)

    def clear(self):
        if self.mode == "r":
            raise ReadOnlyError()
        self.map.clear()

    @classmethod
    def _fsspec_installed(cls):
        """Returns true if fsspec is installed"""
        import importlib.util

        return importlib.util.find_spec("fsspec") is not None

def normalize_storage_path(path: Union[str, bytes, None]) -> str:

    # handle bytes
    if isinstance(path, bytes):
        path = str(path, "ascii")

    # ensure str
    if path is not None and not isinstance(path, str):
        path = str(path)

    if path:

        # convert backslash to forward slash
        path = path.replace("\\", "/")

        # ensure no leading slash
        while len(path) > 0 and path[0] == "/":
            path = path[1:]

        # ensure no trailing slash
        while len(path) > 0 and path[-1] == "/":
            path = path[:-1]

        # collapse any repeated slashes
        previous_char = None
        collapsed = ""
        for char in path:
            if char == "/" and previous_char == "/":
                pass
            else:
                collapsed += char
            previous_char = char
        path = collapsed

        # don't allow path segments with just '.' or '..'
        segments = path.split("/")
        if any(s in {".", ".."} for s in segments):
            raise ValueError("path containing '.' or '..' segment not allowed")

    else:
        path = ""

    return path

def normalize_key(key):
    key = normalize_storage_path(key).lstrip("/")

    return key
    
class ReadOnlyError(Exception):
    def __init__(
        self, message="This object is read-only. Modification is not allowed."
    ):
        self.message = message
        super().__init__(self.message)