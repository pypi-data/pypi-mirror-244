#! /usr/bin/env python3

import logging
from typing import Annotated, Final

import daiquiri
from typer import Option, Typer

from dbnomics_data_model.cli import callbacks

from .commands.dataset import app as dataset_app
from .commands.provider import app as provider_app
from .commands.series import app as series_app

DEFAULT_LOG_LEVELS: Final = "dbnomics_data_model.cli=INFO"


logger = daiquiri.getLogger(__name__)


app = Typer()
app.add_typer(dataset_app)
app.add_typer(provider_app)
app.add_typer(series_app)


@app.callback(context_settings={"help_option_names": ["-h", "--help"]})
def app_callback(
    *,
    debug: Annotated[bool, Option(help="Display debug messages logged by dbnomics_data_model")] = False,
    fail_fast: Annotated[bool, Option(envvar="FAIL_FAST", help="Stop at the first exception")] = False,  # noqa: ARG001
    log_levels: Annotated[
        str,
        Option(
            callback=callbacks.from_csv,
            envvar="LOG_LEVELS",
            help="Logging levels: logger_name1=log_level1,logger_name2=log_level2[,...]",
        ),
    ] = DEFAULT_LOG_LEVELS,
    storage_uri_or_dir: Annotated[str, Option(..., envvar="STORAGE_URI")],  # noqa: ARG001
    verbose: Annotated[
        bool, Option("-v", "--verbose", help="Display debug messages logged by dbnomics_data_model")
    ] = False,
) -> None:
    """DBnomics CLI tool."""
    daiquiri.setup()
    daiquiri.set_default_log_levels(
        [("dbnomics_data_model", logging.DEBUG if debug else logging.INFO if verbose else logging.WARNING)],
    )
    daiquiri.parse_and_set_default_log_levels(log_levels)


if __name__ == "__main__":
    app()
