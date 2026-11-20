# Paper Collaboration Skills

Four Codex skills for finding papers, tracing claims to sources, reviewing a manuscript paragraph by paragraph, and applying annotated revisions.

| Skill | Use it to | Fixed HTML layout |
| --- | --- | --- |
| [Bilingual Paper Workflow](skills/paper-bilingual-workflow/SKILL.md) | Draft in English, review in a second language, and merge approved edits into the manuscript | [Bilingual review](examples/bilingual.html) |
| [Paper Literature Search](skills/paper-literature-search/SKILL.md) | Find papers and compare findings or settings with links to the primary sources | [Literature search](examples/literature.html) |
| [Paper Source Trace](skills/paper-source-trace/SKILL.md) | Match a claim or figure to a passage, implementation, or run record | [Claim and evidence](examples/evidence.html) |
| [Paper Annotation Revision](skills/paper-annotation-revision/SKILL.md) | Locate author comments and review the original and proposed wording | [Annotation comparison](examples/revision.html) |

## Install in Codex

Install all four skills to use the shared HTML renderer and the cross-skill workflows. The Codex skill installer accepts these paths directly.

```sh
python3 "${CODEX_HOME:-$HOME/.codex}/skills/.system/skill-installer/scripts/install-skill-from-github.py" \
  --repo ManfredCh/paper-collaboration-skills --ref v1.0.0 \
  --path skills/paper-bilingual-workflow skills/paper-literature-search \
         skills/paper-source-trace skills/paper-annotation-revision
```

You can also download the [English skill bundle](https://github.com/ManfredCh/paper-collaboration-skills/releases/tag/v1.0.0) and copy its four skill directories into your Codex user skills directory. If you already have a skill with the same name, use a separate installation location to keep both editions. Start a new Codex session and invoke a skill by name.

> Use `$paper-literature-search` to find recent approaches to this research problem. Group the papers by method and open the primary sources.

> Use `$paper-bilingual-workflow` to review the introduction one paragraph at a time. Keep LaTeX as the manuscript source and put the review translation in HTML.

## Reuse the HTML layouts

Download this repository or open the generated examples from a local checkout. The examples use fictional data to show the layouts. Each page stands alone and renders without an external library or service.

- [Bilingual, literature, and evidence input formats](skills/paper-bilingual-workflow/references/html-pages.md)
- [Annotation input format and highlighting](skills/paper-annotation-revision/references/review-page.md)

The HTML renderers use Python 3 and its standard library. For a manuscript with its own build and review pages, the skills work with the existing files and anchors.
