from typing import TYPE_CHECKING

from dbnomics_data_model.errors import DataModelError
from dbnomics_data_model.model.dimensions import Dimension
from dbnomics_data_model.model.frequency import FrequencyCode
from dbnomics_data_model.model.identifiers.types import DimensionCode, DimensionValueCode

if TYPE_CHECKING:
    from dbnomics_data_model.model.identifiers.series_code import SeriesCode
    from dbnomics_data_model.model.series import Series


class SeriesDimensionNotSet(DataModelError):
    def __init__(
        self, *, dimension: Dimension, dimensions: dict[DimensionCode, DimensionValueCode], series: "Series | None"
    ) -> None:
        series_code = "<unknown code>" if series is None else series.code
        msg = f"The series {series_code!r} does not define a value for the dimension {dimension.code!r}"
        super().__init__(msg=msg)
        self.dimension = dimension
        self.dimensions = dimensions
        self.series = series


class SeriesError(DataModelError):
    def __init__(self, *, msg: str, series: "Series") -> None:
        super().__init__(msg=msg)
        self.series = series


class SeriesHasNoDimension(SeriesError):
    def __init__(self, *, series: "Series") -> None:
        msg = f"The series {series.code!r} has no dimension"
        super().__init__(msg=msg, series=series)


class SeriesHasNoObservation(SeriesError):
    def __init__(self, *, series: "Series") -> None:
        msg = f"The series {series.code!r} has no observation"
        super().__init__(msg=msg, series=series)


class InvalidFrequencyDimension(DataModelError):
    def __init__(
        self, *, dimension_code: DimensionCode, dimension_value_code: DimensionValueCode, series_code: "SeriesCode"
    ) -> None:
        allowed_values = list(FrequencyCode)
        msg = f"The series {series_code!r} defines an invalid value for the dimension {dimension_code!r}: {dimension_value_code!r}, allowed values: {allowed_values!r}"
        super().__init__(msg=msg)
        self.dimension_code = dimension_code
        self.dimension_value_code = dimension_value_code
        self.series_code = series_code
