# Skills

Skills are domain-expertise modules — short instruction sets that teach an AI to handle a specific task well. A recipe loads only the skills it declares, so the AI's context stays small.

## Live state

Run [scripts/skill_attrition_audit.py](../scripts/skill_attrition_audit.py) for current numbers:

```
python scripts/skill_attrition_audit.py --summary
```

As of 2026-05-04, the library holds **130 skills across 29 categories**, with 6 referenced by the current recipe set. See [SKILL_ATTRITION.md](SKILL_ATTRITION.md) for the candidate watchlist and the rules for the next pruning pass.

## Two-layer model

| Layer | Path | Purpose |
|---|---|---|
| Library | [`.archived/skills/`](../.archived/skills/) | Available skills. Recipes can `requires_skills:` any ID listed in [`.archived/skills/registry.json`](../.archived/skills/registry.json). |
| Vault | [`.archived/_vault/skills/`](../.archived/_vault/skills/) | Skills removed from active circulation but kept on disk. Not loadable by recipes. Restore by moving back into `.archived/skills/<category>/` and updating the registry. |

## Folder structure

Each skill lives in its category directory:

```
.archived/skills/
└── <category>/
    └── <skill-name>/
        ├── SKILL.md      # The instruction set
        ├── scripts/      # Optional helper code
        ├── examples/     # Optional usage examples
        └── resources/    # Optional templates, datasets
```

The category-level `registry.json` lists every skill in that category; the top-level [`.archived/skills/registry.json`](../.archived/skills/registry.json) lists the categories.

## How recipes use skills

A recipe declares its skills in frontmatter:

```yaml
requires_skills:
  - wiki-changelog
  - comprehensive-review-full-review
```

`recipe lint` resolves every ID against the registry; an unknown ID fails the lint. When the recipe runs, the dispatcher loads each declared SKILL.md into the model's context (see [RECIPE_SPEC.md](RECIPE_SPEC.md) for runner behavior).

## Adding a skill

1. Drop the skill into the right category at `.archived/skills/<category>/<skill-name>/SKILL.md`.
2. Add an entry to that category's `registry.json`.
3. Reference it from a recipe (otherwise it's an attrition candidate from day one).

## Removing a skill

1. Move the directory to `.archived/_vault/skills/<category>/<skill-name>/`.
2. Remove the entry from the category's `registry.json`.
3. Run [scripts/validate.py](../scripts/validate.py) — recipe lint will fail any recipe still referencing it.
