from typing import Annotated, Optional

from typer import Abort, Argument, Context, Option

from dbnomics_data_model.cli import callbacks
from dbnomics_data_model.cli.console import console
from dbnomics_data_model.cli.constants import REVISION
from dbnomics_data_model.cli.error_chain import format_error_chain
from dbnomics_data_model.cli.renderables.observation_table import ObservationTable
from dbnomics_data_model.cli.renderables.series_metadata_record import SeriesMetadataRecord
from dbnomics_data_model.cli.storage_utils import open_storage
from dbnomics_data_model.errors import DataModelError
from dbnomics_data_model.model.identifiers.series_id import SeriesId

from .app import app

__all__ = ["show"]


@app.command(name="show")
def show(
    *,
    ctx: Context,
    revision_id: Annotated[
        Optional[str], Option("--revision", envvar=REVISION, help="Show series at this revision")
    ] = None,
    series_id: Annotated[str, Argument(callback=callbacks.series_id, help="Show this series")],
    metadata: Annotated[bool, Option(help="Show series metadata")] = True,
    observations: Annotated[bool, Option(help="Show series observations")] = True,
    stats: Annotated[bool, Option(help="Show series statistics")] = True,
) -> None:
    assert isinstance(series_id, SeriesId)

    root_ctx_params = ctx.find_root().params
    storage_uri_or_dir: str = root_ctx_params["storage_uri_or_dir"]

    storage = open_storage(storage_uri_or_dir)

    try:
        series = storage.load_series(series_id, revision_id=revision_id, with_observations=observations or stats)
    except DataModelError as exc:
        console.print(format_error_chain(exc))
        raise Abort from exc

    if metadata:
        console.print(SeriesMetadataRecord(series, stats=stats))

    if observations:
        console.print(ObservationTable(series))
