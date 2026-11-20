#!/usr/bin/env python3
"""Render structured annotations as an offline HTML review page."""

import argparse
import json
import re
from difflib import SequenceMatcher
from html import escape
from pathlib import Path
from string import Template
from urllib.parse import urlsplit

from _page_language import language_tag, page_labels

ASSETS = Path(__file__).resolve().parents[1] / "assets"
REVIEW_LABELS = ("original", "proposed", "added", "deleted", "translation", "rationale", "sources", "navigation")
ITEM_ID = re.compile(r"[a-z][a-z0-9-]*")
TOKEN = re.compile(r"\s+|\w+|[^\w\s]")


def text_field(record, field, context, *, required=False):
    value = record.get(field, None if required else "")
    if not isinstance(value, str) or (required and not value.strip()):
        raise ValueError(f"{context} field {field} must be {'nonempty ' if required else ''}text")
    return value


def list_field(record, field, context, *, required=False):
    value = record.get(field, None if required else [])
    if not isinstance(value, list) or (required and not value):
        raise ValueError(f"{context} field {field} must be {'a nonempty list' if required else 'a list'}")
    return value


def mark_changes(before, after):
    original = TOKEN.findall(before)
    proposed = TOKEN.findall(after)
    original_html = []
    proposed_html = []
    for tag, i, j, k, l in SequenceMatcher(None, original, proposed, autojunk=False).get_opcodes():
        old = escape("".join(original[i:j]))
        new = escape("".join(proposed[k:l]))
        original_html.append(f"<mark>{old}</mark>" if old and tag != "equal" else old)
        proposed_html.append(f"<ins>{new}</ins>" if new and tag != "equal" else new)
    return "".join(original_html), "".join(proposed_html)


def comparison(item, before, after, labels, lang, manuscript_lang):
    if "before" in item and "after" in item:
        old_html, new_html = mark_changes(before, after)
        old_html = old_html or labels["added"]
        new_html = new_html or labels["deleted"]
    else:
        old_html, new_html = escape(before), escape(after)

    panels = []
    for heading, content, passage in (
        (labels["original"], old_html, before), (labels["proposed"], new_html, after)
    ):
        if content:
            content_lang = manuscript_lang if passage else lang
            panels.append(
                f'<section><h3>{heading}</h3><p class="text" lang="{content_lang}">{content}</p></section>'
            )
    return f'<div class="compare">{"".join(panels)}</div>' if panels else ""


def source_list(sources, context, heading):
    links = []
    for index, source in enumerate(sources, 1):
        location = f"{context} source {index}"
        if not isinstance(source, dict):
            raise ValueError(f"{location} must be an object")
        label = text_field(source, "label", location, required=True)
        href = text_field(source, "href", location, required=True)
        excerpt = text_field(source, "excerpt", location)
        url = urlsplit(href)
        if href.strip() != href or re.search(r"[\x00-\x1f\x7f\\]", href):
            raise ValueError(f"{location} URL contains an unsupported character")
        if url.scheme:
            if url.scheme not in {"http", "https"} or not url.hostname or url.username is not None:
                raise ValueError(f"{location} must use an HTTP(S) or relative link")
        elif url.netloc or href.startswith("//"):
            raise ValueError(f"{location} must use a complete HTTP(S) URL")
        quote = f'<blockquote class="text">{escape(excerpt)}</blockquote>' if excerpt else ""
        links.append(f'<li><a href="{escape(href, quote=True)}">{escape(label)}</a>{quote}</li>')
    return f'<details><summary>{heading}</summary><ul>{"".join(links)}</ul></details>' if links else ""


def note(heading, content, lang=""):
    if not content:
        return ""
    lang_attr = f' lang="{lang}"' if lang else ""
    return f'<div class="item-note"><h3>{heading}</h3><p class="text"{lang_attr}>{escape(content)}</p></div>'


def render_review(review):
    if not isinstance(review, dict):
        raise ValueError("the review input must be a JSON object")
    title = text_field(review, "title", "Review", required=True)
    baseline = text_field(review, "baseline", "Review")
    items = list_field(review, "items", "Review", required=True)
    lang, labels = page_labels(ASSETS, review, REVIEW_LABELS)
    manuscript_lang = language_tag(text_field(review, "manuscript_lang", "Review") or review.get("lang", "en"))
    translation_lang = language_tag(text_field(review, "translation_lang", "Review") or lang)
    seen = set()
    articles = []
    navigation = []
    for index, item in enumerate(items, 1):
        context = f"Annotation {index}"
        if not isinstance(item, dict):
            raise ValueError(f"{context} must be an object")
        item_id = text_field(item, "id", context, required=True)
        if not ITEM_ID.fullmatch(item_id) or item_id in seen:
            raise ValueError(f"{context} has an invalid or repeated ID")
        seen.add(item_id)
        location = escape(text_field(item, "location", context, required=True))
        status = escape(text_field(item, "status", context, required=True))

        before = text_field(item, "before", context)
        after = text_field(item, "after", context)
        comment = text_field(item, "comment", context)
        translation = text_field(item, "translation" if "translation" in item else "zh", context)
        reason = text_field(item, "reason", context)
        sources = list_field(item, "sources", context)
        anchor = f"review-{item_id}"
        heading_id = f"heading-{item_id}"
        navigation.append(f'<li><a href="#{anchor}">{location}</a></li>')
        articles.append("".join((
            f'<article id="{anchor}" aria-labelledby="{heading_id}">',
            f'<header class="item-header"><h2 id="{heading_id}">{location}</h2>',
            f'<p class="status">{status}</p></header>',
            f'<blockquote class="comment text">{escape(comment)}</blockquote>' if comment else "",
            comparison(item, before, after, labels, lang, manuscript_lang),
            note(labels["translation"], translation, translation_lang),
            note(labels["rationale"], reason),
            source_list(sources, context, labels["sources"]),
            "</article>",
        )))

    return Template((ASSETS / "review.html").read_text(encoding="utf-8")).substitute(
        lang=lang,
        title=escape(title),
        baseline=f'<p class="baseline">{escape(baseline)}</p>' if baseline else "",
        navigation=f'<nav aria-label="{labels["navigation"]}"><ul>{"".join(navigation)}</ul></nav>' if len(articles) > 1 else "",
        items="\n".join(articles),
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="UTF-8 annotation JSON")
    parser.add_argument("output", type=Path, help="HTML output path")
    args = parser.parse_args()
    try:
        if args.input.resolve() == args.output.resolve():
            raise ValueError("use different input and output paths")
        review = json.loads(args.input.read_text(encoding="utf-8"))
        args.output.write_text(render_review(review), encoding="utf-8")
    except (OSError, ValueError) as error:
        parser.exit(1, f"{error}\n")


if __name__ == "__main__":
    main()
