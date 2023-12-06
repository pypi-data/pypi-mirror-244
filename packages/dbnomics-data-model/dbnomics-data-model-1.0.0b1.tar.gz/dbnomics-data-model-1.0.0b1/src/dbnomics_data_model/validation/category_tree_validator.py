import daiquiri

from dbnomics_data_model.model import CategoryTree, DatasetCode, DatasetReference, ProviderCode
from dbnomics_data_model.model.identifiers import DatasetId
from dbnomics_data_model.storage import Storage
from dbnomics_data_model.storage.errors.dataset_metadata import DatasetMetadataLoadError

from .errors.category_tree_validator import DanglingCategoryTreeDatasetReference, DatasetMissingFromCategoryTree
from .validation_reports import ProviderValidationReport

logger = daiquiri.getLogger(__name__)


class CategoryTreeValidator:
    def __init__(
        self,
        *,
        category_tree: CategoryTree,
        provider_code: ProviderCode,
        storage: Storage,
        validation_report: ProviderValidationReport,
    ) -> None:
        self.category_tree = category_tree
        self.provider_code = provider_code
        self.validation_report = validation_report
        self._storage = storage

    def validate(self) -> None:
        """Check that the datasets referenced by the category tree actually exist in storage.

        Check that the datasets of storage are referenced by the category tree, except for discontinued datasets.
        """
        provider_code = self.provider_code

        storage_dataset_codes = set(self._storage.iter_dataset_codes(provider_code))
        category_tree_dataset_references = list(self.category_tree.iter_dataset_references())

        self.validate_dataset_references(storage_dataset_codes, category_tree_dataset_references)
        self.validate_stored_datasets_are_referenced(storage_dataset_codes, category_tree_dataset_references)

    def validate_dataset_references(
        self,
        storage_dataset_codes: set[DatasetCode],
        category_tree_dataset_references: list[DatasetReference],
    ) -> None:
        for dataset_reference in category_tree_dataset_references:
            if dataset_reference.code in storage_dataset_codes:
                continue

            dataset_id = DatasetId(self.provider_code, dataset_reference.code)
            self.validation_report.category_tree_errors.append(
                DanglingCategoryTreeDatasetReference(dataset_id=dataset_id)
            )

    def validate_stored_datasets_are_referenced(
        self,
        storage_dataset_codes: set[DatasetCode],
        category_tree_dataset_references: list[DatasetReference],
    ) -> None:
        category_tree_dataset_codes = {dataset_reference.code for dataset_reference in category_tree_dataset_references}
        for dataset_code in storage_dataset_codes:
            if dataset_code in category_tree_dataset_codes:
                continue

            dataset_id = DatasetId(self.provider_code, dataset_code)

            try:
                dataset_metadata = self._storage.load_dataset_metadata(dataset_id)
            except DatasetMetadataLoadError:
                logger.exception(
                    "Could not load dataset metadata to see if it's discontinued, considering it's not",
                    dataset_code=dataset_code,
                )
            else:
                # Ignore discontinued dataset because they are allowed be absent from category tree.
                if dataset_metadata.discontinued:
                    continue

            self.validation_report.category_tree_errors.append(DatasetMissingFromCategoryTree(dataset_id))
