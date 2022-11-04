import re

from mdformat.renderer import RenderContext, RenderTreeNode
from mdformat.renderer._context import (
    RE_CHAR_REFERENCE,
    WRAP_POINT,
    _in_block,
    escape_asterisk_emphasis,
    escape_underscore_emphasis,
)


def text(node: RenderTreeNode, context: RenderContext) -> str:
    """Process a text token.

    Text should always be a child of an inline token. An inline token
    should always be enclosed by a heading or a paragraph.

    Modified from ``mdformat.renderer._context.text``.
    """
    text = node.content

    disable_escape = context.options["mdformat"].get("disable_escape") or []

    if 'backslash' not in disable_escape:
        # Escape backslash to prevent it from making unintended escapes.
        # This escape has to be first, else we start multiplying backslashes.
        text = text.replace("\\", "\\\\")

    if 'asterisk' not in disable_escape:
        text = escape_asterisk_emphasis(text)  # Escape emphasis/strong marker.
    if 'underscore' not in disable_escape:
        text = escape_underscore_emphasis(text)  # Escape emphasis/strong marker.
    if 'link-enclosure' not in disable_escape:
        text = text.replace("[", "\\[")  # Escape link label enclosure
        text = text.replace("]", "\\]")  # Escape link label enclosure
    if 'uri-enclosure' not in disable_escape:
        text = text.replace("<", "\\<")  # Escape URI enclosure
    if 'code-span' not in disable_escape:
        text = text.replace("`", "\\`")  # Escape code span marker

    # Escape "&" if it starts a sequence that can be interpreted as
    # a character reference.
    text = RE_CHAR_REFERENCE.sub(r"\\\g<0>", text)

    # The parser can give us consecutive newlines which can break
    # the markdown structure. Replace two or more consecutive newlines
    # with newline character's decimal reference.
    text = text.replace("\n\n", "&#10;&#10;")

    # If the last character is a "!" and the token next up is a link, we
    # have to escape the "!" or else the link will be interpreted as image.
    next_sibling = node.next_sibling
    if text.endswith("!") and next_sibling and next_sibling.type == "link":
        text = text[:-1] + "\\!"

    if context.do_wrap and _in_block("paragraph", node):
        text = re.sub(r"\s+", WRAP_POINT, text)

    return text
