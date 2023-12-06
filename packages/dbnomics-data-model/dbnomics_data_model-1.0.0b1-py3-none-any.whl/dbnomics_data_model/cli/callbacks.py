from collections.abc import Callable
from typing import TypeVar

from typer import BadParameter

from dbnomics_data_model.model.identifiers.dataset_id import DatasetId
from dbnomics_data_model.model.identifiers.errors import DatasetIdParseError, SeriesIdParseError, SimpleCodeParseError
from dbnomics_data_model.model.identifiers.series_code import SeriesCode
from dbnomics_data_model.model.identifiers.series_id import SeriesId
from dbnomics_data_model.model.identifiers.types import ProviderCode

T = TypeVar("T")


def dataset_id(value: str) -> DatasetId:
    try:
        return DatasetId.parse(value)
    except DatasetIdParseError as exc:
        raise BadParameter(str(exc)) from exc


def from_csv(value: str | None) -> list[str]:
    """Split a string with comma-separated values to a list of strings."""
    if value is None:
        return []

    value = value.strip()
    value1 = (s.strip() for s in value.split(","))
    return list(filter(None, value1))


def simple_code_callback(value: str, *, parse: Callable[[str], T]) -> T:
    try:
        return parse(value)
    except SimpleCodeParseError as exc:
        raise BadParameter(str(exc)) from exc


def provider_code(value: str) -> ProviderCode:
    return simple_code_callback(value, parse=ProviderCode.parse)


def series_code(value: str) -> SeriesCode:
    return simple_code_callback(value, parse=SeriesCode.parse)


def series_id(value: str) -> SeriesId:
    try:
        return SeriesId.parse(value)
    except SeriesIdParseError as exc:
        raise BadParameter(str(exc)) from exc


def series_codes(value: str | None) -> list[SeriesCode] | None:
    if value is None:
        return None

    value = value.strip()
    value1 = (s.strip() for s in value.split(","))
    raw_items = list(filter(None, value1))

    return [series_code(raw_item) for raw_item in raw_items]
