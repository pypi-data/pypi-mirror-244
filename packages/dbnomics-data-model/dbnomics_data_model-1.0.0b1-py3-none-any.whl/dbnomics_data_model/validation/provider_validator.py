import daiquiri

from dbnomics_data_model.model import ProviderCode
from dbnomics_data_model.model.identifiers import DatasetId
from dbnomics_data_model.storage import Storage
from dbnomics_data_model.storage.errors.category_tree import CategoryTreeStorageError
from dbnomics_data_model.storage.errors.dataset_releases import DatasetReleasesStorageError
from dbnomics_data_model.storage.errors.provider_metadata import ProviderMetadataStorageError

from .category_tree_validator import CategoryTreeValidator
from .dataset_releases_validator import DatasetReleasesValidator
from .dataset_validator import DatasetValidator
from .validation_reports import ProviderValidationReport

logger = daiquiri.getLogger(__name__)


class ProviderValidator:
    def __init__(
        self,
        *,
        provider_code: ProviderCode,
        series_per_dataset_limit: int | None = None,
        storage: Storage,
        validation_report: ProviderValidationReport,
    ) -> None:
        self.provider_code = provider_code
        self.series_per_dataset_limit = series_per_dataset_limit
        self.validation_report = validation_report
        self._storage = storage

    def validate(self) -> None:
        provider_code = self.provider_code
        logger.debug("Validating data related to provider...", provider_code=provider_code)

        self.validate_provider_metadata(provider_code)
        self.validate_category_tree(provider_code)
        self.validate_dataset_releases(provider_code)
        self.validate_datasets(provider_code)

    def validate_category_tree(self, provider_code: ProviderCode) -> None:
        logger.debug("Validating category tree of provider...", provider_code=provider_code)

        try:
            category_tree = self._storage.load_category_tree(provider_code)
        except CategoryTreeStorageError as exc:
            self.validation_report.category_tree_errors.append(exc)
            return

        if category_tree is None:
            return

        category_tree_validator = CategoryTreeValidator(
            category_tree=category_tree,
            provider_code=provider_code,
            storage=self._storage,
            validation_report=self.validation_report,
        )
        category_tree_validator.validate()

    def validate_datasets(self, provider_code: ProviderCode) -> None:
        logger.debug("Validating datasets of provider...", provider_code=provider_code)

        dataset_count = self._storage.get_dataset_count(provider_code)

        for dataset_index, dataset_code in enumerate(sorted(self._storage.iter_dataset_codes(provider_code)), start=1):
            dataset_id = DatasetId(provider_code, dataset_code)
            logger.debug("Validating dataset (%d/%d)...", dataset_index, dataset_count, dataset_id=str(dataset_id))
            dataset_validator = DatasetValidator(
                dataset_id=dataset_id,
                storage=self._storage,
                validation_report=self.validation_report.datasets[dataset_code],
            )
            dataset_validator.validate()

    def validate_dataset_releases(self, provider_code: ProviderCode) -> None:
        logger.debug("Validating releases of datasets of provider...", provider_code=provider_code)

        try:
            dataset_releases_list = list(self._storage.iter_dataset_releases(provider_code))
        except DatasetReleasesStorageError as exc:
            self.validation_report.dataset_releases_errors.append(exc)
            return

        for dataset_releases in dataset_releases_list:
            dataset_releases_validator = DatasetReleasesValidator(
                dataset_releases=dataset_releases,
                provider_code=provider_code,
                storage=self._storage,
                validation_report=self.validation_report,
            )
            dataset_releases_validator.validate()

    def validate_provider_metadata(self, provider_code: ProviderCode) -> None:
        logger.debug("Validating metadata of provider...", provider_code=provider_code)

        try:
            self._storage.load_provider_metadata(provider_code)
        except ProviderMetadataStorageError as exc:
            self.validation_report.provider_metadata_errors.append(exc)
