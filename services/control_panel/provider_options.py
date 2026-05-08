"""Provider/model dropdown data for the Run form.

Walks the runtime's provider registry, collects `available()` providers, and
emits flat `provider/model` ids grouped for the <optgroup> tags. Local is
always shown even when no models can be enumerated (the daemon may be
down at form-render time but reachable at run time); the recipe's declared
model is also injected so it's always selectable.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ProviderOption:
    provider: str
    models: list[str]
    available: bool


def list_provider_options(recipe_default: str | None = None) -> list[ProviderOption]:
    """List dropdown options. `recipe_default` ensures the recipe's declared
    model survives even if `list_models()` doesn't enumerate it."""
    from services.recipe_runtime import providers as registry

    opts: list[ProviderOption] = []
    for name in registry.list_providers():
        p = registry.get_provider(name)
        models = list(p.list_models())
        opts.append(ProviderOption(provider=name, models=models, available=p.available()))

    if recipe_default:
        from services.recipe_runtime.providers import parse_model_ref
        try:
            rp, rm = parse_model_ref(recipe_default)
        except ValueError:
            rp, rm = None, None
        if rp and rm:
            for o in opts:
                if o.provider == rp and rm not in o.models:
                    o.models.insert(0, rm)

    return opts


def default_model_ref(opts: list[ProviderOption], recipe_default: str | None) -> str:
    """Pick a sensible pre-selection for the <select>.

    Order: recipe's declared model > first available provider's first model >
    `local/` (with no model — user must override).
    """
    if recipe_default:
        from services.recipe_runtime.providers import parse_model_ref
        try:
            provider, model = parse_model_ref(recipe_default)
        except ValueError:
            pass
        else:
            return f"{provider}/{model}"

    for o in opts:
        if o.available and o.models:
            return f"{o.provider}/{o.models[0]}"
    return "local/"
