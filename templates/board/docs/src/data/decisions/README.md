# Decision records

One file per decision: `DEC-<NNN>-<slug>.md`, rendered at `/decisions/dec-<nnn>/`.
Superseded decisions are marked (`status: superseded` plus `supersedes:` on the new one), never deleted.

```markdown
---
id: DEC-001
title: LM74910H-Q1 input protection
status: accepted          # proposed / accepted / superseded
date: 2026-10-13
revision: A
page: subsystems/power    # docs page that owns the decision
requirements: [REQ-PWR-001]
parts: [LM74910HQRGERQ1]
gates: [GATE-PWR-01]
supersedes: []
rejected:
  - option: LM74900-Q1
    reason: Latches off after SLEEP-mode overcurrent instead of auto-retrying.
---

## Context
## Decision
## Why
## Consequences
```
