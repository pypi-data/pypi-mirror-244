from typing import TYPE_CHECKING

from dbnomics_data_model.errors import DataModelError

if TYPE_CHECKING:
    from dbnomics_data_model.model.dimensions.dataset_dimensions import DatasetDimensions
    from dbnomics_data_model.model.identifiers.types import DimensionCode


class UnknownFrequencyDimension(DataModelError):
    def __init__(self, *, dataset_dimensions: "DatasetDimensions", frequency_dimension_code: "DimensionCode") -> None:
        msg = f"Frequency dimension {frequency_dimension_code!r} is not one of the dimensions of the dataset."
        super().__init__(msg=msg)
        self.dataset_dimensions = dataset_dimensions
        self.frequency_dimension_code = frequency_dimension_code
