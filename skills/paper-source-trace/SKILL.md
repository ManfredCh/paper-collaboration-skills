---
name: paper-source-trace
description: Verify a specific manuscript claim, reported value, or writing precedent against a precise passage, implementation, or run record. Use for sentence-level attribution, short quotations in context, and scientific evidence checks.
---

# Paper Source Trace

Write the findings and HTML in the requested review language or the language of the current request. Keep source titles, quotations, and symbols as published.

1. Identify the sentence or result and the evidence scope. Start with supplied sources, author handoffs, code, and run records. If online lookup is allowed and additional papers are needed, use [Paper Literature Search](../paper-literature-search/SKILL.md).
2. Give each source a clear role. A writing example illustrates the argument's structure. A paper supports statements about prior work. Implementation and run records support claims about the current project. Include a direct link to the relevant passage, equation, table, configuration, or receipt.
3. Read the surrounding argument. Track the question the passage answers, the conditions it assumes, and the conclusion it supports. Use original wording in the new manuscript. When the author requests source text, provide a short permitted excerpt with its location and a summary of context.
4. Match the evidence to the actual run. Identify the model version, dataset split, checkpoint, sample count, units, and evaluation protocol when they matter. Keep measured results, pilot runs, estimates, and proposed configurations clearly labeled.
5. Return the attribution at the level requested by the author. For tracked review, put a source beside each supported claim. In the submission manuscript, use the normal citation format.

Use [claim and evidence records](references/claim-evidence.md) for a reusable ledger. The [fixed evidence layout](../paper-bilingual-workflow/references/html-pages.md) renders the ledger to HTML. Apply edits only within the requested manuscript scope.
