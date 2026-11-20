# Offline Annotation Comparison

The renderer accepts UTF-8 JSON and writes a standalone HTML review page. It highlights changed words in the original and proposed passages. The author can open sources and navigate to individual annotations using stable anchors.

```sh
python3 skills/paper-annotation-revision/scripts/render_review.py examples/revision.json revision.html
```

The input has a `title`, an optional `baseline`, and a nonempty array of `items`.

- Every item has a unique `id`, a `location`, and a `status`. An ID starts with a lowercase letter and may contain lowercase letters, digits, and hyphens. Its anchor is `#review-<id>`.
- Status values are `Pending`, `Accepted`, `Applied`, `Evidence needed`, and `Declined`.
- Supply `before` and `after` for a comparison. Use an empty `before` for an insertion, an empty `after` for a deletion, or omit `after` to show the original on its own.
- Add `comment`, `translation`, and `reason` as needed. Each entry in the optional `sources` array has a `label`, an `href`, and an optional `excerpt`.

Use [the example input](https://github.com/ManfredCh/paper-collaboration-skills/blob/v1.0.0/examples/revision.json) as a starting point. Run the example command from a checkout or substitute the installed skill path and your own input file. The page renders with local styles.
