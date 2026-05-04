# Skill Attrition (Phase C2)

The skill library earns its keep through recipe references. A skill no recipe `requires_skills` is a candidate for vaulting on the next pruning pass.

## How to read this

Run [scripts/skill_attrition_audit.py](../scripts/skill_attrition_audit.py) for the live state:

```
python scripts/skill_attrition_audit.py            # full bucketed list
python scripts/skill_attrition_audit.py --summary  # counts per category
python scripts/skill_attrition_audit.py --json     # machine-readable
```

## Snapshot — 2026-05-04

After Phase C1 (146 → 130) and 4 recipes (daily-briefing, ticket-to-feature, pr-review-prep, git-pr):

- **Total skills:** 130
- **Referenced by recipes:** 6 — `backend-architect`, `comprehensive-review-full-review`, `debrief-teacher`, `plan-writing`, `software-architecture`, `wiki-changelog`
- **Unreferenced:** 124 (95%)

The 95% number is misleading on its own. The recipe set is small (4); the library is intentionally broader so future recipes can reach for skills without first re-importing them. Treat unreferenced-ness as a **signal**, not a verdict.

## When to cut

Vault a category when **all of the following** hold:
1. The audit has been run after a pruning-relevant recipe set has landed (rule of thumb: 8-10 stable recipes covering the user's intended domains).
2. The category still shows 0 references.
3. No planned recipe in the next iteration would plausibly reach for it.

## Candidates flagged today

These categories are the strongest cut candidates at the next pass — large unreferenced footprints with no obvious upcoming recipe demand:

| Category | Count | Notes |
|---|---|---|
| `security-offensive` | 11 | No pentest/red-team recipe is planned. Vault unless one is. |
| `ai-ml-agents` | 14 | Likely retains some — agent recipes are coming (Phase E3). Re-audit after 2-3 agent recipes. |
| `devops-iac` | 12 | Vault candidates if no infra-provisioning recipe is planned. |
| `frontend-core` | 8 | Depends on whether the workspace will host frontend recipes at all. |

## Cadence

Re-run the audit after every +3 recipes. The next genuine C2 cutting pass is reasonable once 8-10 stable recipes exist; before then, the unreferenced count is mostly a function of how many recipes have been authored, not which skills are dead.
