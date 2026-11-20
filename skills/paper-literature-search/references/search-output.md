# Literature Search Page

Use a row per paper or per reported configuration when a paper has multiple relevant variants. Record the paper, publication or version, research topic, relevant finding, verification level, and primary links. Keep a reported value beside its unit and evaluation or training configuration.

For new HTML outputs, follow the [page schema](../../paper-bilingual-workflow/references/html-pages.md). Use the terminal from the repository root or substitute the installed skill path.

```sh
python3 skills/paper-bilingual-workflow/scripts/render_page.py literature examples/literature.json literature.html
```

Link to the paper or an official proceedings page and add the appendix section, table, or released configuration that supports the row. When only metadata or an abstract was available, record that in the verification column.
