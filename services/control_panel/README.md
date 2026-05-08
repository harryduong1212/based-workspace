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
- [ ] B2 — recipe detail (Overview tab, rendered body)
- [ ] B3 — run flow (form, provider/model dropdown, SSE-streamed output)
- [ ] B4 — edit flow (CodeMirror + audit-on-save)
- [ ] B5 — create flow (form → templated skeleton → edit)
- [ ] B6 — connector detail + test-connection

## Tests

```bash
python -m unittest services.control_panel.tests.test_app
```

The test suite skips itself if FastAPI isn't installed, so `validate.py`
stays green on a fresh checkout that hasn't installed the UI deps yet.
