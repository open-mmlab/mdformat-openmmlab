# Modified from https://github.com/executablebooks/mdformat-tables

from typing import List, Optional, Sequence
import unicodedata

from mdformat.renderer import RenderContext, RenderTreeNode


def text_width(text: str):
    """Return the true width of a text string.

    A table about the `east_asian_width`:

        - 'W': Wide
        - 'F': Full-width
        - 'H': Half-width
        - 'Na': Narrow
        - 'N': Neutral
        - 'A': Ambiguous
    """
    width = 0
    for c in text:
        if unicodedata.east_asian_width(c) in ["W", "F"]:
            width += 2
        else:
            width += 1
    return width


def _refine_widths(
    head: Sequence[str], widths: Sequence[int], max_width: Optional[int] = None
) -> Sequence[int]:
    """Refine the widths of each column, avoid padding too many whitespaces.

    If the total width exceeds the ``max_width`` while the total text length
    of the head cells doesn't, shrink the target width of each column.

    Args:
        head (Sequence[str]): The text of each head cell in the table.
        widths (Sequence[int]): The target width of each column.
        max_width (int, optional): The maximum width of the table.

    Returns:
        Sequence[int]: The refined widths.
    """
    if (
        max_width is None
        or sum(widths) <= max_width
        or sum(len(text) for text in head) > max_width
    ):
        return widths

    padding_widths = [width - len(text) for width, text in zip(widths, head)]
    while sum(widths) > max_width:
        # Shrink every column evenly according to the padding widths.
        shrink_idx = padding_widths.index(max(padding_widths))
        widths[shrink_idx] -= 1
        padding_widths[shrink_idx] -= 1
    return widths


def _to_string(
    rows: Sequence[Sequence[str]], align: Sequence[Sequence[str]], widths: Sequence[int]
) -> List[str]:
    lines = []
    lines.append(
        "| "
        + " | ".join(
            # This is to adjust the difference between wide and narrow characters.
            f"{{:{al or '<'}{widths[i] - text_width(text) + len(text)}}}".format(text)
            for i, (text, al) in enumerate(zip(rows[0], align[0]))
        )
        + " |"
    )
    lines.append(
        "| "
        + " | ".join(
            (":" if al in ("<", "^") else "-")
            + "-" * (widths[i] - 2)
            + (":" if al in (">", "^") else "-")
            for i, al in enumerate(align[0])
        )
        + " |"
    )
    for row, als in zip(rows[1:], align[1:]):
        lines.append(
            "| "
            + " | ".join(
                f"{{:{al or '<'}{widths[i] - text_width(text) + len(text)}}}".format(
                    text
                )
                for i, (text, al) in enumerate(zip(row, als))
            )
            + " |"
        )
    return lines


def _render_table(node: RenderTreeNode, context: RenderContext) -> str:
    """Render a `RenderTreeNode` of type "table"."""
    # gather rendered cell content into row * column array
    rows: List[List[str]] = []
    align: List[List[str]] = []
    for descendant in node.walk(include_self=False):
        if descendant.type == "tr":
            rows.append([])
            align.append([])
        elif descendant.type in ("th", "td"):
            style = descendant.attrs.get("style") or ""
            assert isinstance(style, str)
            if "text-align:right" in style:
                align[-1].append(">")
            elif "text-align:left" in style:
                align[-1].append("<")
            elif "text-align:center" in style:
                align[-1].append("^")
            else:
                align[-1].append("")
            rows[-1].append(descendant.render(context))

    # work out the widths for each column
    widths = [
        max(3, *(text_width(row[col_idx]) for row in rows))
        for col_idx in range(len(rows[0]))
    ]
    max_width = context.options["mdformat"].get("table_width", None)
    widths = _refine_widths(rows[0], widths, max_width)

    # write content
    # note: assuming always one header row
    lines = _to_string(rows, align, widths)

    return "\n".join(lines)


def _render_cell(node: RenderTreeNode, context: RenderContext) -> str:
    inline_node = node.children[0]
    text = inline_node.render(context)
    return text.replace("|", "\\|")


def _escape_tables(text: str, node: RenderTreeNode, context: RenderContext) -> str:
    # Escape the first "-" character of a line if every character on that line
    # is one of {" ", "|", "-"}. Lines like this could otherwise be parsed
    # as a delimiter row of a table.
    return "\n".join(
        line.replace("-", "\\-", 1) if all(c in "|-: " for c in line) else line
        for line in text.split("\n")
    )
