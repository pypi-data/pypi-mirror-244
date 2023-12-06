from collections.abc import Sequence
from dataclasses import KW_ONLY, dataclass

from rich.console import Console, ConsoleOptions, RenderResult
from rich.table import Table

from dbnomics_data_model.cli.renderables.render_utils import render_value
from dbnomics_data_model.model.series import Series


@dataclass(frozen=True)
class SeriesMetadataRecord:
    series: Series

    _: KW_ONLY
    stats: bool = False

    @property
    def field_names(self) -> Sequence[str]:
        result = [
            "code",
            "name",
            "description",
            "notes",
            "doc_href",
            "dimensions",
            "attributes",
            "updated_at",
            "next_release_at",
        ]

        if self.stats:
            result.extend(["period_domain", "value_range"])

        return result

    def __rich_console__(self, console: Console, options: ConsoleOptions) -> RenderResult:
        grid = Table.grid(padding=(0, 1))
        for field_name in self.field_names:
            grid.add_row(
                field_name,
                render_value(getattr(self.series, field_name)),
                style="bold" if field_name == "code" else "",
            )
        yield grid
