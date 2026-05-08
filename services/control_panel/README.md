# Control Panel

Local web UI for browsing, running, editing, and creating recipes &
connectors. FastAPI + Jinja2 + HTMX + CodeMirror, no Node toolchain.

## Install

```bash
pip install --user -r services/control_panel/requirements.txt
```

## Run

```bash
python -m services.control_panel
# → control panel — listening on http://127.0.0.1:8765
```

Override binding via env:

| Var | Default | Purpose |
|---|---|---|
| `CONTROL_PANEL_HOST` | `127.0.0.1` | Bind address. Set to `0.0.0.0` inside Docker. |
| `CONTROL_PANEL_PORT` | `8765` | Port. |
| `WORKSPACE_ROOT` | auto-detected | Override for non-standard layouts (CI, container mounts). |

LLM provider keys are read from the workspace `.env` (see `.env.example`):
`LLAMA_SWAP_URL`, `GEMINI_API_KEY`, `ANTHROPIC_API_KEY`. The Run page only
shows providers whose required env vars are set.

## Phase status

- [x] B1 — dashboard (browse recipes/connectors, system health footer)
- [x] B2 — recipe detail (Overview tab with rendered body + frontmatter sidebar)
- [x] B3 — run flow (form generated from `inputs:`, provider/model dropdown
  with free-text override, SSE-streamed output)
- [x] B4 — edit flow (CodeMirror 5 with `yaml-frontmatter` mode, atomic
  write, audit subprocess on save)
- [x] B5 — create flow (form → templated skeleton via `yaml.safe_dump`
  → redirect to /edit)
- [x] B6 — connector detail (rendered body, env-var status pills,
  "test connection" button — checks `requires_env` is set; live API
  probes are deferred per `feedback-defer-external-connectors`)

## Tests

```bash
python -m unittest services.control_panel.tests.test_app
```

The test suite skips itself if FastAPI isn't installed, so `validate.py`
stays green on a fresh checkout that hasn't installed the UI deps yet.
