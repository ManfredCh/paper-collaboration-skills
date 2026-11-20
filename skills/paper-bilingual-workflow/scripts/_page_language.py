"""Load labels for a requested HTML language without fetching resources."""

import json
import re
from html import escape


def language_tag(value):
    if not isinstance(value, str) or not re.fullmatch(r"[A-Za-z]{2,8}(?:-[A-Za-z0-9]{1,8})*", value):
        raise ValueError("use a language tag such as en or en-GB")
    return value


def page_labels(assets, manifest, required):
    """Select bundled labels by language, with optional labels from the author."""
    defaults = json.loads((assets / "labels.json").read_text(encoding="utf-8"))
    lang = language_tag(manifest.get("lang", defaults["lang"]))
    family = lang.split("-", 1)[0].lower()
    overrides = manifest.get("labels", {})
    if not isinstance(overrides, dict):
        raise ValueError("labels must be an object")

    if family == defaults["lang"].split("-", 1)[0].lower():
        labels = defaults
    else:
        localized = assets / f"labels.{family}.json"
        labels = json.loads(localized.read_text(encoding="utf-8")) if localized.is_file() else {}
    labels = {**labels, **overrides}

    missing = [key for key in required if not isinstance(labels.get(key), str) or not labels[key].strip()]
    if missing:
        raise ValueError(f"provide these labels for {lang} in the labels object: {', '.join(missing)}")
    return lang, {key: escape(labels[key], quote=True) for key in required}
