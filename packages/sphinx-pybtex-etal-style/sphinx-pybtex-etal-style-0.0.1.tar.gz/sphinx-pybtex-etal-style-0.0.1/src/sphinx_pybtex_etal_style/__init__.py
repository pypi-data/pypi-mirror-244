# pyright: reportMissingTypeStubs=false
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pybtex.plugin import register_plugin
from pybtex.richtext import Tag, Text
from pybtex.style.formatting.unsrt import Style as UnsrtStyle
from pybtex.style.template import (
    FieldIsMissing,
    Node,
    _format_list,  # pyright: ignore[reportPrivateUsage]
    field,
    href,
    join,
    node,
    sentence,
    words,
)

if TYPE_CHECKING:
    from pybtex.database import Entry
    from sphinx.application import Sphinx
    from sphinx.environment import BuildEnvironment


def setup(app: Sphinx) -> dict[str, Any]:
    app.connect("config-inited", register_style)
    return {
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }


def register_style(_: Sphinx, __: BuildEnvironment) -> None:
    register_plugin("pybtex.style.formatting", "unsrt_et_al", MyStyle)


# Specify bibliography style
@node
def et_al(children, data, sep="", sep2=None, last_sep=None):  # type: ignore[no-untyped-def]
    if sep2 is None:
        sep2 = sep
    if last_sep is None:
        last_sep = sep
    parts = [part for part in _format_list(children, data) if part]
    if len(parts) <= 1:
        return Text(*parts)
    if len(parts) == 2:  # noqa: PLR2004
        return Text(sep2).join(parts)
    if len(parts) == 3:  # noqa: PLR2004
        return Text(last_sep).join([Text(sep).join(parts[:-1]), parts[-1]])
    return Text(parts[0], Tag("em", " et al"))


@node
def names(children, context, role, **kwargs):  # type: ignore[no-untyped-def]
    """Return formatted names."""
    if children:
        msg = "The names field should not contain any children"
        raise ValueError(msg)
    try:
        persons = context["entry"].persons[role]
    except KeyError as exc:
        raise FieldIsMissing(role, context["entry"]) from exc

    style = context["style"]
    formatted_names = [
        style.format_name(person, style.abbreviate_names) for person in persons
    ]
    return et_al(**kwargs)[  # pyright: ignore[reportUntypedBaseClass]
        formatted_names
    ].format_data(context)


class MyStyle(UnsrtStyle):
    def __init__(self) -> None:
        super().__init__(abbreviate_names=True)

    def format_names(self, role: Entry, as_sentence: bool = True) -> Node:
        formatted_names = names(role, sep=", ", sep2=" and ", last_sep=", and ")
        if as_sentence:
            return sentence[formatted_names]
        return formatted_names

    def format_eprint(self, e: Entry) -> Node:
        if "doi" in e.fields:
            return ""
        return super().format_eprint(e)

    def format_url(self, e: Entry) -> Node:
        if "doi" in e.fields or "eprint" in e.fields:
            return ""
        return words[
            href[
                field("url", raw=True),
                field("url", raw=True, apply_func=remove_http),
            ]
        ]

    def format_isbn(self, e: Entry) -> Node:
        return href[
            join[
                "https://isbnsearch.org/isbn/",
                field("isbn", raw=True, apply_func=remove_dashes_and_spaces),
            ],
            join[
                "ISBN:",
                field("isbn", raw=True),
            ],
        ]


def remove_dashes_and_spaces(isbn: str) -> str:
    to_remove = ["-", " "]
    for remove in to_remove:
        isbn = isbn.replace(remove, "")
    return isbn


def remove_http(url: str) -> str:
    to_remove = ["https://", "http://"]
    for remove in to_remove:
        url = url.replace(remove, "")
    return url
