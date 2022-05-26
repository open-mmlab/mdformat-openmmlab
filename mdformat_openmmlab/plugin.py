import types
from typing import Mapping

from markdown_it import MarkdownIt
from mdformat.renderer.typing import Postprocess, Render
from mdit_py_plugins.tasklists import tasklists_plugin

from .gfm import (
    _escape_text,
    _link_renderer,
    _list_item_renderer,
    _postprocess_inline,
    _strikethrough_renderer,
)
from .table import _escape_tables, _render_cell, _render_table


def update_mdit(mdit: MarkdownIt) -> None:
    """Update the parser"""
    # Enable table rules
    mdit.enable("table")

    # Enable linkify-it-py (for GFM autolink extension)
    mdit.options["linkify"] = True
    mdit.enable("linkify")

    # Enable strikethrough markdown-it extension
    mdit.enable("strikethrough")

    # Enable tasklist markdown-it extension
    mdit.use(tasklists_plugin)

    # Disable normalize link
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
    "s": _strikethrough_renderer,
    "list_item": _list_item_renderer,
    "link": _link_renderer,
}
POSTPROCESSORS: Mapping[str, Postprocess] = {
    "paragraph": _escape_tables,
    "text": _escape_text,
    "inline": _postprocess_inline,
}
