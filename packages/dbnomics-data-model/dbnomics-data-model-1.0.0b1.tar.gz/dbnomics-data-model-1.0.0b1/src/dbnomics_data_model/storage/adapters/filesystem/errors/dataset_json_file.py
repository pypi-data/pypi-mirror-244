from pathlib import Path
from typing import TYPE_CHECKING

from dbnomics_data_model.model import DatasetId
from dbnomics_data_model.model.revisions.types import RevisionId
from dbnomics_data_model.storage.adapters.filesystem.errors import FileSystemAdapterError
from dbnomics_data_model.storage.adapters.filesystem.errors.json_model import JsonModelError
from dbnomics_data_model.validation.errors.validation_error_chain import build_error_chain
from dbnomics_data_model.validation.errors.validation_error_data import ValidationErrorData
from dbnomics_data_model.validation.errors.validation_error_level import ValidationErrorLevel

if TYPE_CHECKING:
    from jsonalias import Json


class DatasetJsonFileError(FileSystemAdapterError):
    def __init__(self, *, dataset_id: DatasetId, dataset_json_path: Path, msg: str) -> None:
        super().__init__(msg=msg)
        self.dataset_id = dataset_id
        self.dataset_json_path = dataset_json_path


class DatasetJsonDeleteError(DatasetJsonFileError):
    def __init__(self, *, dataset_id: DatasetId, dataset_json_path: Path) -> None:
        msg = f"Error deleting {dataset_json_path} of dataset {str(dataset_id)!r}"
        super().__init__(dataset_id=dataset_id, dataset_json_path=dataset_json_path, msg=msg)


class DatasetJsonLoadError(DatasetJsonFileError):
    def __init__(
        self, *, dataset_id: DatasetId, dataset_json_path: Path, revision_id: RevisionId | None = None
    ) -> None:
        msg = f"Error loading {dataset_json_path} of dataset {str(dataset_id)!r} at revision {revision_id!r}"
        super().__init__(dataset_id=dataset_id, dataset_json_path=dataset_json_path, msg=msg)
        self.revision_id = revision_id


class DatasetJsonNotFound(DatasetJsonFileError):
    def __init__(
        self, *, dataset_id: DatasetId, dataset_json_path: Path, revision_id: RevisionId | None = None
    ) -> None:
        msg = f"Could not find {dataset_json_path} of dataset {str(dataset_id)!r} at revision {revision_id!r}"
        super().__init__(dataset_id=dataset_id, dataset_json_path=dataset_json_path, msg=msg)
        self.revision_id = revision_id


class DatasetJsonSaveError(DatasetJsonFileError):
    def __init__(self, *, dataset_id: DatasetId, dataset_json_path: Path) -> None:
        msg = f"Error saving {dataset_json_path} of dataset {str(dataset_id)!r}"
        super().__init__(dataset_id=dataset_id, dataset_json_path=dataset_json_path, msg=msg)


class DatasetJsonValidationError(DatasetJsonFileError):
    def __init__(
        self,
        *,
        dataset_id: DatasetId,
        dataset_json_path: Path,
        revision_id: RevisionId | None = None,
        validation_errors: list[JsonModelError],
    ) -> None:
        msg = (
            f"File {dataset_json_path} of dataset {str(dataset_id)!r} at revision {revision_id!r} has validation errors"
        )
        super().__init__(dataset_id=dataset_id, dataset_json_path=dataset_json_path, msg=msg)
        self.revision_id = revision_id
        self.validation_errors = validation_errors

    @property
    def __validation_error_data__(self) -> ValidationErrorData:
        validation_errors_json: Json = [build_error_chain(error).to_json() for error in self.validation_errors]
        return ValidationErrorData(
            code=None,
            extra={"validation_errors": validation_errors_json},
            level=ValidationErrorLevel.WARNING,
            path=self.dataset_id.validation_error_path,
        )
