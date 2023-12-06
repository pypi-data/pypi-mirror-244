from typing import cast

from jsonalias import Json

from dbnomics_data_model.errors import DataModelError
from dbnomics_data_model.model import SeriesId
from dbnomics_data_model.model.periods.periods import Period
from dbnomics_data_model.validation.errors.validation_error_code_registry import ValidationErrorCodeRegistry
from dbnomics_data_model.validation.errors.validation_error_data import ValidationErrorData
from dbnomics_data_model.validation.errors.validation_error_level import ValidationErrorLevel

SO001 = ValidationErrorCodeRegistry.request("SO001")
SO002 = ValidationErrorCodeRegistry.request("SO002")
SO003 = ValidationErrorCodeRegistry.request("SO003")


class DuplicateSeriesObservationPeriods(DataModelError):
    def __init__(self, *, duplicate_periods: dict[Period, int], series_id: SeriesId) -> None:
        msg = "Some series observations have the same period"
        super().__init__(msg=msg)
        self.duplicate_periods = duplicate_periods
        self.series_id = series_id

    @property
    def __validation_error_data__(self) -> ValidationErrorData:
        duplicate_periods_json: Json = {str(k): v for k, v in self.duplicate_periods.items()}
        return ValidationErrorData(
            code=SO001,
            extra={"duplicate_periods": duplicate_periods_json},
            level=ValidationErrorLevel.ERROR,
            path=self.series_id.validation_error_path,
        )


class InconsistentPeriodTypes(DataModelError):
    def __init__(self, *, period_types: set[type[Period]], series_id: SeriesId) -> None:
        msg = "Series observation periods have inconsistent types"
        super().__init__(msg=msg)
        self.period_types = period_types
        self.series_id = series_id

    @property
    def __validation_error_data__(self) -> ValidationErrorData:
        period_types_json = cast(Json, sorted(map(str, self.period_types)))
        return ValidationErrorData(
            code=SO002,
            extra={"period_types": period_types_json},
            level=ValidationErrorLevel.ERROR,
            path=self.series_id.validation_error_path,
        )


class UnorderedSeriesObservations(DataModelError):
    def __init__(self, *, first_diverging_index: int, series_id: SeriesId) -> None:
        msg = "Series observations are not sorted by period"
        super().__init__(msg=msg)
        self.first_diverging_index = first_diverging_index
        self.series_id = series_id

    @property
    def __validation_error_data__(self) -> ValidationErrorData:
        return ValidationErrorData(
            code=SO003,
            extra={"first_diverging_index": self.first_diverging_index},
            level=ValidationErrorLevel.ERROR,
            path=self.series_id.validation_error_path,
        )
