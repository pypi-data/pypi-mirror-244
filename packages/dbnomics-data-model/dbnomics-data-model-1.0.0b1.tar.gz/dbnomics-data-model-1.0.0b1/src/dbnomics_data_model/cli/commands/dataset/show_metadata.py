from typing import Annotated, Optional

from typer import Abort, Argument, Context, Option

from dbnomics_data_model.cli import callbacks
from dbnomics_data_model.cli.console import console
from dbnomics_data_model.cli.constants import REVISION
from dbnomics_data_model.cli.error_chain import format_error_chain
from dbnomics_data_model.cli.storage_utils import open_storage
from dbnomics_data_model.errors import DataModelError
from dbnomics_data_model.model.identifiers.dataset_id import DatasetId

from .app import app

__all__ = ["show_metadata"]


@app.command(name="show-metadata")
def show_metadata(
    *,
    ctx: Context,
    dataset_id: Annotated[str, Argument(callback=callbacks.dataset_id, help="Show this dataset")],
    revision_id: Annotated[
        Optional[str], Option("--revision", envvar=REVISION, help="Show dataset at this revision")
    ] = None,
) -> None:
    assert isinstance(dataset_id, DatasetId)

    root_ctx_params = ctx.find_root().params
    storage_uri_or_dir: str = root_ctx_params["storage_uri_or_dir"]

    storage = open_storage(storage_uri_or_dir)

    try:
        dataset_metadata = storage.load_dataset_metadata(dataset_id, revision_id=revision_id)
    except DataModelError as exc:
        console.print(format_error_chain(exc))
        raise Abort from exc

    console.print(dataset_metadata)
