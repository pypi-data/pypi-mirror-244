from collections import defaultdict
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from dbnomics_data_model.errors import DataModelError
from dbnomics_data_model.json_utils import JsonObject
from dbnomics_data_model.model import DatasetCode, ProviderCode, SeriesCode

from .errors.validation_error_chain import build_error_chain

if TYPE_CHECKING:
    from jsonalias import Json


@dataclass(kw_only=True)
class StorageValidationReport:
    providers: dict[ProviderCode, "ProviderValidationReport"] = field(
        default_factory=lambda: defaultdict(ProviderValidationReport)
    )
    storage_errors: list[DataModelError] = field(default_factory=list)

    def to_json(self) -> JsonObject:
        result: JsonObject = {}

        providers: Json = {k: j for k, v in self.providers.items() if (j := v.to_json())}
        if providers:
            result["providers"] = providers

        storage_errors: Json = [build_error_chain(error).to_json() for error in self.storage_errors]
        if storage_errors:
            result["storage_errors"] = storage_errors

        return result


@dataclass(kw_only=True)
class ProviderValidationReport:
    category_tree_errors: list[DataModelError] = field(default_factory=list)
    dataset_releases_errors: list[DataModelError] = field(default_factory=list)
    datasets: dict[DatasetCode, "DatasetValidationReport"] = field(
        default_factory=lambda: defaultdict(DatasetValidationReport)
    )
    provider_metadata_errors: list[DataModelError] = field(default_factory=list)

    def to_json(self) -> JsonObject:
        result: JsonObject = {}

        category_tree_errors: Json = [build_error_chain(error).to_json() for error in self.category_tree_errors]
        if category_tree_errors:
            result["category_tree_errors"] = category_tree_errors

        dataset_releases_errors: Json = [build_error_chain(error).to_json() for error in self.dataset_releases_errors]
        if dataset_releases_errors:
            result["dataset_releases_errors"] = dataset_releases_errors

        datasets: Json = {str(k): j for k, v in self.datasets.items() if (j := v.to_json())}
        if datasets:
            result["datasets"] = datasets

        provider_metadata_errors: Json = [build_error_chain(error).to_json() for error in self.provider_metadata_errors]
        if provider_metadata_errors:
            result["provider_metadata_errors"] = provider_metadata_errors

        return result


@dataclass(kw_only=True)
class DatasetValidationReport:
    dataset_errors: list[DataModelError] = field(default_factory=list)
    dataset_metadata_errors: list[DataModelError] = field(default_factory=list)
    series: dict[SeriesCode, "SeriesValidationReport"] = field(
        default_factory=lambda: defaultdict(SeriesValidationReport)
    )

    def to_json(self) -> JsonObject:
        result: JsonObject = {}

        dataset_errors: Json = [build_error_chain(error).to_json() for error in self.dataset_errors]
        if dataset_errors:
            result["dataset_errors"] = dataset_errors

        dataset_metadata_errors: Json = [build_error_chain(error).to_json() for error in self.dataset_metadata_errors]
        if dataset_metadata_errors:
            result["dataset_metadata_errors"] = dataset_metadata_errors

        series_json: Json = {k: j for k, v in self.series.items() if (j := v.to_json())}
        if series_json:
            result["series"] = series_json

        return result


@dataclass(kw_only=True)
class SeriesValidationReport:
    observation_errors: list[DataModelError] = field(default_factory=list)
    series_metadata_errors: list[DataModelError] = field(default_factory=list)

    def to_json(self) -> JsonObject:
        result: JsonObject = {}

        observation_errors: Json = [build_error_chain(error).to_json() for error in self.observation_errors]
        if observation_errors:
            result["observation_errors"] = observation_errors

        series_metadata_errors: Json = [build_error_chain(error).to_json() for error in self.series_metadata_errors]
        if series_metadata_errors:
            result["series_metadata_errors"] = series_metadata_errors

        return result
