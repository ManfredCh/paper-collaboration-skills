#!/usr/bin/env python3
"""Render a fixed manuscript review, literature, or evidence page."""

import argparse
import json
import re
from html import escape
from pathlib import Path
from string import Template
from urllib.parse import urlsplit

ASSETS = Path(__file__).resolve().parents[1] / "assets"
ITEM_ID = re.compile(r"[a-z][a-z0-9-]*")
TABLE_COLUMNS = {
    "literature": ("paper", "publication", "topic", "finding", "verification", "sources"),
    "evidence": ("claim", "role", "support", "status", "sources"),
}


def field(record, key, required=False):
    value = record.get(key, None if required else "")
    if not isinstance(value, str) or (required and not value.strip()):
        raise ValueError(f"{key} must be {'nonempty ' if required else ''}text")
    return value


def source_links(item):
    sources = item.get("sources", [])
    if not isinstance(sources, list):
        raise ValueError("sources must be a list")
    links = []
    for source in sources:
        if not isinstance(source, dict):
            raise ValueError("each source must be an object")
        label = escape(field(source, "label", required=True))
        href = field(source, "href", required=True)
        url = urlsplit(href)
        if (
            href != href.strip() or re.search(r"[\x00-\x1f\x7f\\]", href)
            or href.startswith("//") or url.username is not None
            or (url.scheme and (url.scheme not in {"http", "https"} or not url.hostname))
        ):
            raise ValueError("use an HTTP(S) or relative source link")
        excerpt = field(source, "excerpt")
        quote = f'<blockquote class="text">{escape(excerpt)}</blockquote>' if excerpt else ""
        links.append(f'<li><a href="{escape(href, quote=True)}">{label}</a>{quote}</li>')
    return f'<ul class="links">{"".join(links)}</ul>' if links else ""


def render_bilingual(items, labels):
    entries = []
    navigation = []
    for anchor, item in items:
        location = escape(field(item, "location", required=True))
        english = escape(field(item, "en", required=True))
        translation = escape(field(item, "translation"))
        paired_class = "pair" if translation else "pair single"
        columns = [
            f'<section><h3>{labels["english"]}</h3><p class="text" lang="en">{english}</p></section>'
        ]
        if translation:
            columns.append(f'<section><h3>{labels["translation"]}</h3><p class="text">{translation}</p></section>')
        sources = source_links(item)
        references = f'<details><summary>{labels["sources"]}</summary>{sources}</details>' if sources else ""
        entries.append(
            f'<article id="{anchor}"><h2>{location}</h2>'
            f'<div class="{paired_class}">{"".join(columns)}</div>{references}</article>'
        )
        navigation.append(f'<li><a href="#{anchor}">{location}</a></li>')
    nav = f'<nav aria-label="{labels["navigation"]}"><ul>{"".join(navigation)}</ul></nav>' if len(entries) > 1 else ""
    return nav + "\n".join(entries)


def render_table(layout, items, labels):
    keys = TABLE_COLUMNS[layout]
    headers = "".join(f'<th scope="col">{labels[key]}</th>' for key in keys)
    rows = []
    for anchor, item in items:
        first = escape(field(item, keys[0], required=True))
        values = [escape(field(item, key, required=key != "publication")) for key in keys[1:-1]]
        cells = "".join(f'<td class="text">{value}</td>' for value in values)
        rows.append(f'<tr id="{anchor}"><th scope="row">{first}</th>{cells}<td>{source_links(item)}</td></tr>')
    return (f'<div class="table-scroll" role="region" aria-labelledby="page-title" tabindex="0">'
            f'<table><thead><tr>{headers}</tr></thead><tbody>{"".join(rows)}</tbody></table></div>')


def render_page(layout, manifest):
    if not isinstance(manifest, dict):
        raise ValueError("the page input must be a JSON object")
    title = field(manifest, "title", required=True)
    note = field(manifest, "note")
    records = manifest.get("items")
    if not isinstance(records, list) or not records:
        raise ValueError("items must be a nonempty list")
    items = []
    seen = set()
    for item in records:
        if not isinstance(item, dict):
            raise ValueError("each item must be an object")
        key = field(item, "id", required=True)
        if not ITEM_ID.fullmatch(key) or key in seen:
            raise ValueError(f"invalid or repeated item ID: {key}")
        items.append((f"item-{key}", item))
        seen.add(key)

    raw_labels = json.loads((ASSETS / "labels.json").read_text(encoding="utf-8"))
    labels = {key: escape(value, quote=True) for key, value in raw_labels.items()}
    content = (render_bilingual(items, labels) if layout == "bilingual"
               else render_table(layout, items, labels))
    return Template((ASSETS / "paper-page.html").read_text(encoding="utf-8")).substitute(
        lang=labels["lang"], title=escape(title), content=content,
        note=f'<p class="note text">{escape(note)}</p>' if note else "",
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("layout", choices=("bilingual", *TABLE_COLUMNS))
    parser.add_argument("input", type=Path, help="UTF-8 JSON")
    parser.add_argument("output", type=Path, help="HTML output path")
    args = parser.parse_args()
    try:
        if args.input.resolve() == args.output.resolve():
            raise ValueError("use different input and output paths")
        manifest = json.loads(args.input.read_text(encoding="utf-8"))
        args.output.write_text(render_page(args.layout, manifest), encoding="utf-8")
    except (OSError, ValueError) as error:
        parser.exit(1, f"{error}\n")


if __name__ == "__main__":
    main()
