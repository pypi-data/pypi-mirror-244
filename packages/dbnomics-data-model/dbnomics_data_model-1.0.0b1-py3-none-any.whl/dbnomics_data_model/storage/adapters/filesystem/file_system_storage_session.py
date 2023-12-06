import shutil
from dataclasses import replace
from pathlib import Path
from typing import TYPE_CHECKING, Self

from dbnomics_data_model.storage.adapters.filesystem.constants import (
    GITIGNORE_FILE_NAME,
    SESSION_DEBUG_DIR_NAME,
    SESSION_TMP_DIR_NAME,
)
from dbnomics_data_model.storage.adapters.filesystem.errors.file_system_storage import StorageDirectoryNotFound
from dbnomics_data_model.storage.adapters.filesystem.errors.file_system_storage_session import (
    DebugDirectoryNotFound,
    TmpDirectoryNotFound,
)
from dbnomics_data_model.storage.adapters.filesystem.file_system_storage import FileSystemStorage
from dbnomics_data_model.storage.adapters.filesystem.file_utils import (
    iter_child_files_or_directories,
    merge_directories,
    move_children,
)
from dbnomics_data_model.storage.errors.storage_session import StorageSessionNeverEntered
from dbnomics_data_model.storage.storage_session import StorageSession

if TYPE_CHECKING:
    from dbnomics_data_model.storage.adapters.filesystem.file_system_storage_uri import FileSystemStorageUri


__all__ = ["FileSystemStorageSession"]


class FileSystemStorageSession(StorageSession):
    def __init__(self, *, debug_dir: Path, storage: FileSystemStorage, storage_dir: Path, tmp_dir: Path) -> None:
        super().__init__(storage=storage)

        self.debug_dir = debug_dir
        if not debug_dir.is_dir():
            raise DebugDirectoryNotFound(debug_dir=debug_dir)

        self.tmp_dir = tmp_dir
        if not tmp_dir.is_dir():
            raise TmpDirectoryNotFound(tmp_dir=tmp_dir)

        self.storage_dir = storage_dir
        if not storage_dir.is_dir():
            raise StorageDirectoryNotFound(storage_dir=storage_dir)

    @classmethod
    def from_uri(cls, uri: "FileSystemStorageUri") -> Self:  # type: ignore[override]
        storage_dir = uri.path
        debug_dir = cls._create_debug_dir(storage_dir)
        tmp_dir = cls._recreate_tmp_dir(storage_dir)
        uri_with_tmp_dir = replace(uri, path=tmp_dir)
        storage = FileSystemStorage.from_uri(uri_with_tmp_dir)
        return cls(
            debug_dir=debug_dir,
            storage=storage,
            storage_dir=storage_dir,
            tmp_dir=tmp_dir,
        )

    def commit(self) -> None:
        super().commit()

        if not self._has_entered:
            raise StorageSessionNeverEntered(storage_session=self)

        for child in iter_child_files_or_directories(self.tmp_dir, ignore_hidden=True):
            target_dir = self.storage_dir / child.name
            merge_directories(child, target_dir)

        if self._is_directory_empty(self.debug_dir):
            shutil.rmtree(self.debug_dir)

        if self._is_directory_empty(self.tmp_dir):
            shutil.rmtree(self.tmp_dir)

    def rollback(self) -> None:
        if self._is_directory_empty(self.tmp_dir):
            shutil.rmtree(self.tmp_dir)
            return

        move_children(self.tmp_dir, self.debug_dir, overwrite=True)

    @classmethod
    def _create_debug_dir(cls, storage_dir: Path) -> Path:
        debug_dir = storage_dir / SESSION_DEBUG_DIR_NAME
        debug_dir.mkdir(exist_ok=True)
        return debug_dir

    def _is_directory_empty(self, directory: Path) -> bool:
        return not any(iter_child_files_or_directories(directory, ignore_hidden=True))

    @classmethod
    def _recreate_tmp_dir(cls, storage_dir: Path) -> Path:
        tmp_dir = storage_dir / SESSION_TMP_DIR_NAME
        if tmp_dir.is_dir():
            shutil.rmtree(tmp_dir)
        tmp_dir.mkdir()

        # Add a .gitignore file to avoid committing tmp directory accidentally.
        gitignore_file = tmp_dir / GITIGNORE_FILE_NAME
        if not gitignore_file.is_file():
            gitignore_file.write_text("*")

        return tmp_dir
