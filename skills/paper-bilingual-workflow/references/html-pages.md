# Fixed HTML Layouts

The renderer produces standalone HTML from UTF-8 JSON using the Python 3 standard library. Run these examples from a checkout or substitute the installed skill path and your input file. Use the project's established renderer for pages that need typeset equations or complex figures.

```sh
python3 skills/paper-bilingual-workflow/scripts/render_page.py bilingual examples/bilingual.json bilingual.html
python3 skills/paper-bilingual-workflow/scripts/render_page.py literature examples/literature.json literature.html
python3 skills/paper-bilingual-workflow/scripts/render_page.py evidence examples/evidence.json evidence.html
```

Each input has a `title` and a nonempty `items` array. Add an optional `note` above the content. Item IDs start with a lowercase letter and may contain lowercase letters, digits, and hyphens. IDs must be unique within the page. Link to an item with `#item-<id>`.

| Layout | Required fields per item | Optional fields |
| --- | --- | --- |
| `bilingual` | `id`, `location`, `en` | `translation`, `sources` |
| `literature` | `id`, `paper`, `topic`, `finding`, `verification` | `publication`, `sources` |
| `evidence` | `id`, `claim`, `role`, `support`, `status` | `sources` |

Each source has a `label` and `href`, with an optional `excerpt`. Use an HTTP(S) URL, a relative path, or a page anchor. Text and source excerpts preserve line breaks. Open the result from its intended location to verify relative links.

Use the [annotation comparison layout](../../paper-annotation-revision/references/review-page.md) for before-and-after passages and author comments.
