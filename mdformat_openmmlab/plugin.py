import types
from typing import Mapping

from markdown_it import MarkdownIt
from mdformat.renderer.typing import Postprocess, Render

from .table import _escape_tables, _render_cell, _render_table


def update_mdit(mdit: MarkdownIt) -> None:
    """Update the parser, enable table rules and disable the link normalization."""
    mdit.enable("table")

    def mock_normalize_link(self, url: str) -> str:
        return url

    mdit.normalizeLink = types.MethodType(mock_normalize_link, mdit)


def add_cli_options(parser):
    parser.add_argument(
        "--table-width",
        type=int,
        help="The maximum width to pad in tables.",
    )


RENDERERS: Mapping[str, Render] = {
    "table": _render_table,
    "td": _render_cell,
    "th": _render_cell,
}
POSTPROCESSORS: Mapping[str, Postprocess] = {"paragraph": _escape_tables}
