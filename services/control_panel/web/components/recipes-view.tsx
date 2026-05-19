"use client";

import { useMemo, useState } from "react";

import { RecipeCard } from "@/components/recipe-card";
import { SearchInput } from "@/components/search-input";
import { useIsomorphicLayoutEffect } from "@/lib/use-isomorphic-layout-effect";
import type { RecipeSummary } from "@/lib/api";

const STORAGE_KEY_SMOKE = "showSmokeRecipes";

// Smoke recipes (tagged `smoke`) are dispatcher fixtures, not user-facing
// tasks — and `smoke-agent` consumes ANTHROPIC_API_KEY on click. Hide by
// default; surface a toggle so the user can opt in.
function isSmoke(r: RecipeSummary): boolean {
  return (r.tags ?? []).includes("smoke");
}

// Client wrapper around the recipes grid that adds a live filter. The page
// stays a server component and just hands us the full list.
export function RecipesView({ recipes }: { recipes: RecipeSummary[] }) {
  const [query, setQuery] = useState("");
  const [showSmoke, setShowSmoke] = useState(false);
  const [hydrated, setHydrated] = useState(false);

  useIsomorphicLayoutEffect(() => {
    try {
      setShowSmoke(localStorage.getItem(STORAGE_KEY_SMOKE) === "1");
    } catch {
      // private-mode iframes throw on access — stay with the default.
    }
    setHydrated(true);
  }, []);

  const updateShowSmoke = (v: boolean) => {
    setShowSmoke(v);
    try {
      localStorage.setItem(STORAGE_KEY_SMOKE, v ? "1" : "0");
    } catch {
      // no-op
    }
  };

  const smokeCount = useMemo(() => recipes.filter(isSmoke).length, [recipes]);

  const filtered = useMemo(() => {
    const visible = hydrated && showSmoke ? recipes : recipes.filter((r) => !isSmoke(r));
    const q = query.trim().toLowerCase();
    if (!q) return visible;
    return visible.filter((r) =>
      [r.id, r.name, r.description, r.execution_type, ...(r.tags ?? [])]
        .join(" ")
        .toLowerCase()
        .includes(q),
    );
  }, [recipes, query, showSmoke, hydrated]);

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-end justify-between gap-4">
        <div>
          <div className="text-xs font-semibold uppercase tracking-wider text-primary/70 mb-1.5">
            Recipes
          </div>
          <h1 className="text-2xl font-semibold tracking-tight">All recipes</h1>
          <p className="text-sm text-muted-foreground mt-1">
            {query
              ? `${filtered.length} match${filtered.length === 1 ? "" : "es"} for “${query}”.`
              : `${filtered.length} recipe${filtered.length === 1 ? "" : "s"} shown.`}
            {smokeCount > 0 && !showSmoke && (
              <>
                {" "}
                <span className="text-muted-foreground/70">
                  ({smokeCount} smoke recipe{smokeCount === 1 ? "" : "s"} hidden)
                </span>
              </>
            )}
          </p>
        </div>
        <div className="flex items-center gap-3">
          {smokeCount > 0 && (
            <label className="flex items-center gap-1.5 text-xs text-muted-foreground select-none cursor-pointer">
              <input
                type="checkbox"
                checked={showSmoke}
                onChange={(e) => updateShowSmoke(e.target.checked)}
                className="h-3.5 w-3.5 accent-primary cursor-pointer"
              />
              Show smoke recipes
            </label>
          )}
          <SearchInput
            value={query}
            onChange={setQuery}
            placeholder="Search recipes by name, tag, type…"
          />
        </div>
      </div>

      {filtered.length === 0 ? (
        <div className="rounded-md border border-dashed p-8 text-center text-sm text-muted-foreground">
          {query ? <>No recipes match “{query}”.</> : <>No recipes to show.</>}
        </div>
      ) : (
        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {filtered.map((r) => (
            <RecipeCard key={r.id} recipe={r} />
          ))}
        </div>
      )}
    </div>
  );
}
