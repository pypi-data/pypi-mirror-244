from typing import cast

from jsonalias import Json

from dbnomics_data_model.errors import DataModelError
from dbnomics_data_model.model import DatasetId, SeriesCode
from dbnomics_data_model.validation.errors.validation_error_code_registry import ValidationErrorCodeRegistry
from dbnomics_data_model.validation.errors.validation_error_data import ValidationErrorData

from .validation_error_level import ValidationErrorLevel

D001 = ValidationErrorCodeRegistry.request("D001")
D002 = ValidationErrorCodeRegistry.request("D002")


class DuplicateSeriesCodeError(DataModelError):
    def __init__(self, *, dataset_id: DatasetId, series_code: SeriesCode) -> None:
        msg = f"The dataset {str(dataset_id)!r} has many series with the same code {series_code!r}"
        super().__init__(msg=msg)
        self.dataset_id = dataset_id
        self.series_code = series_code

    @property
    def __validation_error_data__(self) -> ValidationErrorData:
        return ValidationErrorData(
            code=D001,
            extra={"series_code": self.series_code},
            level=ValidationErrorLevel.ERROR,
            path=self.dataset_id.validation_error_path,
        )


class DuplicateSeriesNameError(DataModelError):
    def __init__(self, *, dataset_id: DatasetId, series_name: str, series_codes: set[SeriesCode]) -> None:
        msg = f"The dataset {str(dataset_id)!r} has many series with the same name {series_name!r}"
        super().__init__(msg=msg)
        self.dataset_id = dataset_id
        self.series_codes = series_codes
        self.series_name = series_name

    @property
    def __validation_error_data__(self) -> ValidationErrorData:
        series_codes_json = cast(Json, sorted(self.series_codes))
        return ValidationErrorData(
            code=D002,
            extra={
                "series_codes": series_codes_json,
                "series_name": self.series_name,
            },
            level=ValidationErrorLevel.ERROR,
            path=self.dataset_id.validation_error_path,
        )
