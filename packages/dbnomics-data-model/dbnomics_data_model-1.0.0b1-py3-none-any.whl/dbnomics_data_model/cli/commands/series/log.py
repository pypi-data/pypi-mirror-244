from typing import Annotated, Optional

from rich.padding import Padding
from typer import Argument, Context, Option

from dbnomics_data_model.cli import callbacks
from dbnomics_data_model.cli.console import console
from dbnomics_data_model.cli.constants import REVISION
from dbnomics_data_model.cli.storage_utils import open_storage
from dbnomics_data_model.model.identifiers.series_id import SeriesId

from .app import app

__all__ = ["log"]


@app.command(name="log")
def log(
    *,
    ctx: Context,
    series_id: Annotated[str, Argument(callback=callbacks.series_id, help="Show the log of this series")],
    patch: Annotated[bool, Option("-p", "--patch", help="Show series patch")] = False,
    revision_id: Annotated[
        Optional[str], Option("--revision", envvar=REVISION, help="Make the log start from this revision")
    ] = None,
) -> None:
    assert isinstance(series_id, SeriesId)

    root_ctx_params = ctx.find_root().params
    storage_uri_or_dir: str = root_ctx_params["storage_uri_or_dir"]

    storage = open_storage(storage_uri_or_dir)

    for revision, series_patch in storage.iter_series_changes(series_id, start_revision_id=revision_id):
        console.print(revision)

        if patch:
            console.print("Patch:")
            console.print(Padding.indent(series_patch, 4))
            console.print()
