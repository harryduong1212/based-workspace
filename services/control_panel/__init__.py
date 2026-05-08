"""Control Panel — local web UI for the based-workspace recipe runtime.

Browse recipes/connectors, run prompt-type recipes against any configured
provider (local llama-swap, Gemini, Anthropic), and edit/create recipe
files. FastAPI + Jinja2 + HTMX + CodeMirror, no Node toolchain.

Heavyweight imports (FastAPI, Jinja2, markdown) are lazy so that
`import services.control_panel` works even when those deps aren't
installed yet — the validate.py imports check stays green.
"""

__all__ = ["config"]
