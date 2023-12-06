#! /usr/bin/env python3


import json
import logging
from typing import Annotated, Final, Optional

import daiquiri
from typer import Abort, Argument, Option, Typer, echo

from dbnomics_data_model.cli import callbacks
from dbnomics_data_model.validation.storage_validator import StorageValidator
from dbnomics_data_model.validation.validation_reports import StorageValidationReport

from .storage_utils import open_storage

DEFAULT_LOG_LEVELS: Final = "dbnomics_data_model.cli=INFO"


app = Typer()
logger = daiquiri.getLogger(__name__)


# TODO move to dbnomics CLI command


@app.command(context_settings={"help_option_names": ["-h", "--help"]})
def main(
    *,
    source_dir_or_uri: Annotated[str, Argument(envvar="SOURCE_URI")],
    # TODO reimplement (?)
    # datasets: list[str] = Option([], envvar="DATASETS", help="Validate only those datasets"),
    debug: Annotated[bool, Option("--debug", help="Display debug logging messages")] = False,
    # TODO reimplement (?)
    # fail_fast: Annotated[
    #     bool, Option("--fail-fast", help="Exit on first exception instead of just logging it")
    # ] = False,
    log_levels: Annotated[
        str,
        Option(
            callback=callbacks.from_csv,
            envvar="LOG_LEVELS",
            help="Logging levels: logger_name1=log_level1,logger_name2=log_level2[,...]",
        ),
    ] = DEFAULT_LOG_LEVELS,
    series_limit: Annotated[
        Optional[int],
        Option(
            envvar="SERIES_LIMIT",
            help="Maximum number of series to validate per dataset. If not set, validate all series.",
        ),
    ] = None,
    verbose: Annotated[bool, Option("-v", "--verbose", help="Display info logging messages")] = False,
) -> None:
    """Validate DBnomics data."""
    daiquiri.setup()
    daiquiri.set_default_log_levels(
        [("dbnomics_data_model.cli", logging.DEBUG if debug else logging.INFO if verbose else logging.WARNING)],
    )
    daiquiri.parse_and_set_default_log_levels(log_levels)

    if series_limit is not None and series_limit <= 0:
        echo(f"series limit must be strictly positive, got {series_limit!r}", err=True)
        raise Abort

    storage = open_storage(source_dir_or_uri)
    storage_validation_report = StorageValidationReport()

    validator = StorageValidator(
        series_per_dataset_limit=series_limit, storage=storage, validation_report=storage_validation_report
    )
    validator.validate()

    validation_report_json = storage_validation_report.to_json()
    if validation_report_json:
        echo(json.dumps(validation_report_json, indent=2, sort_keys=True))
        raise Abort


if __name__ == "__main__":
    app()
