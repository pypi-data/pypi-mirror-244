from collections.abc import Iterator, Sequence
from dataclasses import KW_ONLY, dataclass, field, replace

from dbnomics_data_model.model.dimensions.dimension import Dimension
from dbnomics_data_model.model.dimensions.dimension_role import DimensionRole
from dbnomics_data_model.model.errors.dataset_dimensions import UnknownFrequencyDimension
from dbnomics_data_model.model.identifiers.types import DimensionCode
from dbnomics_data_model.model.merge_utils import merge_iterables_of_items


@dataclass
class DatasetDimensions:
    dimensions: list[Dimension] = field(default_factory=list)

    _: KW_ONLY
    roles: dict[DimensionRole, DimensionCode] = field(default_factory=dict)

    def __post_init__(self) -> None:
        frequency_dimension_code = self.frequency_dimension_code
        if frequency_dimension_code is not None and frequency_dimension_code not in self.codes:
            raise UnknownFrequencyDimension(dataset_dimensions=self, frequency_dimension_code=frequency_dimension_code)

    def __iter__(self) -> Iterator[Dimension]:
        return iter(self.dimensions)

    def __len__(self) -> int:
        return len(self.dimensions)

    @property
    def codes(self) -> Sequence[DimensionCode]:
        return [dimension.code for dimension in self.dimensions]

    @property
    def frequency_dimension_code(self) -> DimensionCode | None:
        return self.roles.get(DimensionRole.FREQUENCY)

    def merge(self, other: "DatasetDimensions") -> "DatasetDimensions":
        dimensions = merge_iterables_of_items(
            key=lambda dimension: dimension.code,
            merge=lambda source, target: target.merge(source),
            source=other.dimensions,
            target=self.dimensions,
        )

        return replace(other, dimensions=dimensions)
