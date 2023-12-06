from dbnomics_data_model.errors import DataModelError
from dbnomics_data_model.model import DatasetId
from dbnomics_data_model.validation.errors.validation_error_code_registry import ValidationErrorCodeRegistry
from dbnomics_data_model.validation.errors.validation_error_data import ValidationErrorData

from .validation_error_level import ValidationErrorLevel

DR001 = ValidationErrorCodeRegistry.request("DR001")


class DanglingDatasetReleasesDatasetReference(DataModelError):
    def __init__(self, dataset_id: DatasetId) -> None:
        msg = f"The dataset {str(dataset_id)!r} is referenced by dataset releases but was not found in storage"
        super().__init__(msg=msg)
        self.dataset_id = dataset_id

    @property
    def __validation_error_data__(self) -> ValidationErrorData:
        return ValidationErrorData(
            code=DR001,
            level=ValidationErrorLevel.ERROR,
            path=self.dataset_id.validation_error_path,
        )
