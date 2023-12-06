from typing import Annotated, Optional

from typer import Argument, Context, Option

from dbnomics_data_model.cli import callbacks
from dbnomics_data_model.cli.console import console
from dbnomics_data_model.cli.constants import REVISION
from dbnomics_data_model.cli.storage_utils import open_storage
from dbnomics_data_model.model.identifiers.types import ProviderCode

from .app import app

__all__ = ["show_metadata"]


@app.command(name="show-metadata")
def show_metadata(
    *,
    ctx: Context,
    provider_code: Annotated[str, Argument(callback=callbacks.provider_code, help="Show this provider")],
    revision_id: Annotated[
        Optional[str], Option("--revision", envvar=REVISION, help="Show provider at this revision")
    ] = None,
) -> None:
    assert isinstance(provider_code, ProviderCode)

    root_ctx_params = ctx.find_root().params
    storage_uri_or_dir: str = root_ctx_params["storage_uri_or_dir"]

    storage = open_storage(storage_uri_or_dir)

    provider_metadata = storage.load_provider_metadata(provider_code, revision_id=revision_id)
    console.print(provider_metadata)
