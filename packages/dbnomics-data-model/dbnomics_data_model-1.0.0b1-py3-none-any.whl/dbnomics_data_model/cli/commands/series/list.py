from typing import Annotated, Optional

from click import UsageError
from typer import Argument, Context, Option

from dbnomics_data_model.cli import callbacks
from dbnomics_data_model.cli.console import console
from dbnomics_data_model.cli.constants import REVISION
from dbnomics_data_model.cli.renderables.series_metadata_record import SeriesMetadataRecord
from dbnomics_data_model.cli.storage_utils import open_storage
from dbnomics_data_model.model.identifiers.dataset_id import DatasetId

from .app import app

__all__ = ["list_"]


@app.command(name="list")
def list_(
    *,
    ctx: Context,
    dataset_id: Annotated[str, Argument(callback=callbacks.dataset_id, help="List the series of this dataset")],
    code_only: Annotated[bool, Option(help="Only show the provider codes")] = False,
    observations: Annotated[bool, Option(help="Show series observations")] = False,
    revision_id: Annotated[
        Optional[str], Option("--revision", envvar=REVISION, help="List series at this revision")
    ] = None,
    sort: Annotated[bool, Option(help="Sort series by code")] = True,
    stats: Annotated[bool, Option(help="Show series statistics")] = True,
) -> None:
    assert isinstance(dataset_id, DatasetId)

    if code_only and stats:
        msg = "--stats can't be used with --code-only"
        raise UsageError(msg)

    root_ctx_params = ctx.find_root().params
    storage_uri_or_dir: str = root_ctx_params["storage_uri_or_dir"]

    storage = open_storage(storage_uri_or_dir)

    series_items = storage.iter_series(
        dataset_id, revision_id=revision_id, sort_by_code=sort, with_observations=observations or stats
    )

    if code_only:
        assert not stats

        for series in series_items:
            console.print(series.code)

        return

    for series in series_items:
        console.print(SeriesMetadataRecord(series, stats=stats))
        console.print()
