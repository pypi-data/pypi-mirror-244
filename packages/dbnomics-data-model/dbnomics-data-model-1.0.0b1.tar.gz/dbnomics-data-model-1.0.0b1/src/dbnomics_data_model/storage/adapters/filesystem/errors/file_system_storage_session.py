from pathlib import Path

from dbnomics_data_model.storage.adapters.filesystem.errors import FileSystemAdapterError


class DebugDirectoryNotFound(FileSystemAdapterError):
    def __init__(self, *, debug_dir: Path) -> None:
        msg = f"Could not find the debug directory {str(debug_dir)!r}"
        super().__init__(msg=msg)
        self.debug_dir = debug_dir


class TmpDirectoryNotFound(FileSystemAdapterError):
    def __init__(self, *, tmp_dir: Path) -> None:
        msg = f"Could not find the temporary directory {str(tmp_dir)!r}"
        super().__init__(msg=msg)
        self.tmp_dir = tmp_dir
