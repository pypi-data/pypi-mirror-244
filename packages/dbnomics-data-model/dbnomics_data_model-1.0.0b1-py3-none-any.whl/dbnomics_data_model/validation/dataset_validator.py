from collections import Counter, defaultdict
from collections.abc import Iterator
from typing import TYPE_CHECKING

import daiquiri
from more_itertools import take

from dbnomics_data_model.errors import DataModelError
from dbnomics_data_model.model import DatasetId, Series
from dbnomics_data_model.storage import Storage
from dbnomics_data_model.storage.errors.dataset_metadata import DatasetMetadataStorageError

from .errors.dataset_validator import DuplicateSeriesCodeError, DuplicateSeriesNameError
from .series_validator import SeriesValidator
from .validation_reports import DatasetValidationReport

if TYPE_CHECKING:
    from collections.abc import Iterable

    from dbnomics_data_model.model import SeriesCode


logger = daiquiri.getLogger(__name__)


# TODO add validation that series.jsonl is sorted


class DatasetValidator:
    def __init__(
        self,
        *,
        dataset_id: DatasetId,
        series_per_dataset_limit: int | None = None,
        storage: Storage,
        validation_report: DatasetValidationReport,
    ) -> None:
        self.dataset_id = dataset_id
        self.series_per_dataset_limit = series_per_dataset_limit
        self.validation_report = validation_report
        self._storage = storage

    def validate(self) -> None:
        self.validate_dataset_metadata()
        self.validate_series()

    def validate_dataset_metadata(self) -> None:
        dataset_id = self.dataset_id

        logger.debug("Validating dataset metadata...", dataset_id=str(dataset_id))

        try:
            self._storage.load_dataset_metadata(dataset_id)
        except DatasetMetadataStorageError as exc:
            self.validation_report.dataset_metadata_errors.append(exc)

    def validate_series(self) -> None:
        """Validate the series of a dataset.

        Besides validating each series independently, validate that they all have a unique code (and name if defined).
        """
        dataset_id = self.dataset_id

        logger.debug("Validating series of dataset...", dataset_id=str(dataset_id))

        seen_series_codes: Counter[SeriesCode] = Counter()
        seen_series_names: defaultdict[str, set[SeriesCode]] = defaultdict(set)

        series_iter = self._iter_series()
        while True:
            try:
                series = next(series_iter)
            except StopIteration:
                break
            except DataModelError as exc:
                self.validation_report.dataset_errors.append(exc)
                return

            series_code = series.code
            series_name = series.name

            seen_series_codes[series_code] += 1

            if series_name is not None:
                seen_series_names[series_name].add(series_code)

            series_validator = SeriesValidator(
                dataset_id=dataset_id,
                series=series,
                validation_report=self.validation_report.series[series_code],
            )
            series_validator.validate()

        # TODO make a single error like DuplicateSeriesObservationPeriods
        for series_code, count in sorted(seen_series_codes.most_common()):
            if count > 1:
                self.validation_report.dataset_errors.append(
                    DuplicateSeriesCodeError(dataset_id=dataset_id, series_code=series_code)
                )

        for series_name, series_codes in sorted(seen_series_names.items()):
            if len(series_codes) > 1:
                self.validation_report.dataset_errors.append(
                    DuplicateSeriesNameError(dataset_id=dataset_id, series_name=series_name, series_codes=series_codes)
                )

    def _iter_series(self) -> Iterator[Series]:
        dataset_id = self.dataset_id

        series_iter: Iterable[Series] = self._storage.iter_series(dataset_id)

        series_limit = self.series_per_dataset_limit
        if series_limit is not None:
            logger.debug(
                "Will validate a maximum of %d series for this dataset",
                self.series_per_dataset_limit,
                dataset_id=str(self.dataset_id),
            )
            series_iter = take(series_limit, series_iter)

        yield from series_iter
