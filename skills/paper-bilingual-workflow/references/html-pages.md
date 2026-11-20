# Fixed HTML Layouts

The renderer produces standalone HTML from UTF-8 JSON using the Python 3 standard library. Run these examples from a checkout or substitute the installed skill path and your input file. Use the project's established renderer for pages that need typeset equations or complex figures.

```sh
python3 skills/paper-bilingual-workflow/scripts/render_page.py bilingual examples/bilingual.json bilingual.html
python3 skills/paper-bilingual-workflow/scripts/render_page.py literature examples/literature.json literature.html
python3 skills/paper-bilingual-workflow/scripts/render_page.py evidence examples/evidence.json evidence.html
```

Each input has a `title` and a nonempty `items` array. Add an optional `note` above the content. Item IDs start with a lowercase letter and may contain lowercase letters, digits, and hyphens. IDs must be unique within the page. Link to an item with `#item-<id>`.

Set the top-level `lang` to the selected language of each new page. The English distribution bundles English interface labels for `en` and its regional variants. For another interface language, supply a top-level `labels` object with translations of the relevant [label keys](../assets/labels.json). Use the same language for the title, notes, and any authored column content. Preserve original quotations.

| Layout | Required fields per item | Optional fields |
| --- | --- | --- |
| `bilingual` | `id`, `location`, `text` or the original `en` field | `translation`, `sources` |
| `literature` | `id`, `paper`, `topic`, `finding`, `verification` | `publication`, `sources` |
| `evidence` | `id`, `claim`, `role`, `support`, `status` | `sources` |

Each source has a `label` and `href`, with an optional `excerpt`. Use an HTTP(S) URL, a relative path, or a page anchor. Text and source excerpts preserve line breaks. Open the result from its intended location to verify relative links.

For a paragraph review, `manuscript_lang` and `translation_lang` can set the language of each column. An item with `text` defaults to the page language, and the original `en` field still defaults to English. Omit `translation` for a single-language review.

Use the [annotation comparison layout](../../paper-annotation-revision/references/review-page.md) for before-and-after passages and author comments.
