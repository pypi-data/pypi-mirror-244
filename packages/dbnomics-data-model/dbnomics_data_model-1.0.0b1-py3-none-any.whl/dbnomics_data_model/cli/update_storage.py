#! /usr/bin/env python3

import logging
from typing import Annotated

import daiquiri
from typer import Abort, Argument, Option, Typer, echo

from dbnomics_data_model.storage.storage_updater import StorageUpdater
from dbnomics_data_model.storage.types import UpdateStrategy

from .storage_utils import open_storage

app = Typer()
logger = daiquiri.getLogger(__name__)


# TODO move to dbnomics CLI command


@app.command(context_settings={"help_option_names": ["-h", "--help"]})
def main(
    *,
    source_dir_or_uri: Annotated[str, Argument(envvar="SOURCE_URI")],
    target_dir_or_uri: Annotated[str, Argument(envvar="TARGET_URI")],
    category_tree_update_strategy: Annotated[
        UpdateStrategy, Option(envvar="CATEGORY_TREE_UPDATE_STRATEGY")
    ] = UpdateStrategy.MERGE,
    dataset_update_strategy: Annotated[
        UpdateStrategy,
        Option(envvar="DATASET_UPDATE_STRATEGY")
        # TODO Invalid value for '--category-tree-update-strategy': <UpdateStrategy.MERGE: 'merge'> is not one of 'merge', 'replace'.                                     │
        # TODO check that Enum work correctly (before, UpdateStrategy.REPLACE.value was passed, a str)
    ] = UpdateStrategy.REPLACE,
    debug: Annotated[bool, Option("--debug", help="display debug logging messages")] = False,
    verbose: Annotated[bool, Option("-v", "--verbose", help="display info logging messages")] = False,
) -> None:
    """Update a DBnomics storage with data from another one."""
    daiquiri.setup()
    daiquiri.set_default_log_levels(
        [("dbnomics_data_model", logging.DEBUG if debug else logging.INFO if verbose else logging.WARNING)],
    )

    if source_dir_or_uri == target_dir_or_uri:
        echo(f"source {source_dir_or_uri!r} must be different than target {target_dir_or_uri!r}", err=True)
        raise Abort

    source_storage = open_storage(source_dir_or_uri)
    target_storage = open_storage(target_dir_or_uri)

    storage_updater = StorageUpdater(source_storage=source_storage, target_storage=target_storage)

    storage_updater.update(
        category_tree_update_strategy=category_tree_update_strategy,
        dataset_update_strategy=dataset_update_strategy,
    )


if __name__ == "__main__":
    app()
