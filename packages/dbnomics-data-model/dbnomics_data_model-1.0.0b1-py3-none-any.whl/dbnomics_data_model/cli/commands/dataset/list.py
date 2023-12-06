from typing import Annotated, Optional

from typer import Abort, Argument, Context, Option

from dbnomics_data_model.cli import callbacks
from dbnomics_data_model.cli.console import console
from dbnomics_data_model.cli.constants import REVISION
from dbnomics_data_model.cli.error_chain import format_error_chain
from dbnomics_data_model.cli.storage_utils import open_storage
from dbnomics_data_model.errors import DataModelError
from dbnomics_data_model.model.identifiers.dataset_id import DatasetId
from dbnomics_data_model.model.identifiers.types import ProviderCode

from .app import app

__all__ = ["list_"]


@app.command(name="list")
def list_(
    *,
    ctx: Context,
    code_only: Annotated[bool, Option(help="Only show the provider codes")] = False,
    provider_code: Annotated[
        str,
        Argument(
            ...,
            callback=callbacks.provider_code,
            help="List the datasets of this provider",
        ),
    ],
    revision_id: Annotated[
        Optional[str], Option("--revision", envvar=REVISION, help="List datasets at this revision")
    ] = None,
    sort: Annotated[bool, Option(help="Sort datasets by code")] = True,
) -> None:
    assert isinstance(provider_code, ProviderCode)

    root_ctx_params = ctx.find_root().params
    storage_uri_or_dir: str = root_ctx_params["storage_uri_or_dir"]

    storage = open_storage(storage_uri_or_dir)

    for dataset_code in storage.iter_dataset_codes(provider_code, revision_id=revision_id, sort=sort):
        if code_only:
            console.print(str(dataset_code))
            continue

        dataset_id = DatasetId(provider_code, dataset_code)

        try:
            dataset_metadata = storage.load_dataset_metadata(dataset_id, revision_id=revision_id)
        except DataModelError as exc:
            console.print(format_error_chain(exc))
            raise Abort from exc

        console.print(dataset_metadata)
