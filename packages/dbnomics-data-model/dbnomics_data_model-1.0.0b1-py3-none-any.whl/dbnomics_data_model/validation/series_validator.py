from collections import Counter

import daiquiri

from dbnomics_data_model.model import DatasetId, Series, SeriesId
from dbnomics_data_model.utils import find_index_of_first_difference
from dbnomics_data_model.validation.errors.series_validator import (
    DuplicateSeriesObservationPeriods,
    InconsistentPeriodTypes,
    UnorderedSeriesObservations,
)

from .validation_reports import SeriesValidationReport

logger = daiquiri.getLogger(__name__)


class SeriesValidator:
    def __init__(self, *, dataset_id: DatasetId, series: Series, validation_report: SeriesValidationReport) -> None:
        self.dataset_id = dataset_id
        self.series = series
        self.validation_report = validation_report

    @property
    def series_id(self) -> SeriesId:
        return SeriesId.from_dataset_id(self.dataset_id, self.series.code)

    def validate(self) -> None:
        self.validate_observations()

    def validate_observations(self) -> None:
        """Validate that the observation periods have a valid and homogeneous format, are unique and ordered."""
        observations = self.series.observations
        if not observations:
            return

        periods = [observation.period for observation in observations]
        duplicate_periods = {k: v for k, v in Counter(periods).items() if v > 1}
        if duplicate_periods:
            self.validation_report.observation_errors.append(
                DuplicateSeriesObservationPeriods(duplicate_periods=duplicate_periods, series_id=self.series_id)
            )

        periods_sorted = sorted(set(periods))
        first_diverging_index = find_index_of_first_difference(periods, periods_sorted)
        if first_diverging_index is not None:
            self.validation_report.observation_errors.append(
                UnorderedSeriesObservations(first_diverging_index=first_diverging_index, series_id=self.series_id)
            )

        period_types = {type(period) for period in periods}
        if len(period_types) > 1:
            self.validation_report.observation_errors.append(
                InconsistentPeriodTypes(period_types=period_types, series_id=self.series_id)
            )

        # TODO warn if series uses dimension codes and dimension value codes that are not defined in dataset metadata
