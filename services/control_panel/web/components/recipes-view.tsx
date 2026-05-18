"use client";

import { useMemo, useState } from "react";

import { RecipeCard } from "@/components/recipe-card";
import { SearchInput } from "@/components/search-input";
import type { RecipeSummary } from "@/lib/api";

// Client wrapper around the recipes grid that adds a live filter. The page
// stays a server component and just hands us the full list.
export function RecipesView({ recipes }: { recipes: RecipeSummary[] }) {
  const [query, setQuery] = useState("");

  const filtered = useMemo(() => {
    const q = query.trim().toLowerCase();
    if (!q) return recipes;
    return recipes.filter((r) =>
      [r.id, r.name, r.description, r.execution_type, ...(r.tags ?? [])]
        .join(" ")
        .toLowerCase()
        .includes(q),
    );
  }, [recipes, query]);

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
              ? `${filtered.length} of ${recipes.length} recipe${recipes.length === 1 ? "" : "s"} match “${query}”.`
              : `${recipes.length} recipe${recipes.length === 1 ? "" : "s"} declared in the workspace.`}
          </p>
        </div>
        <SearchInput
          value={query}
          onChange={setQuery}
          placeholder="Search recipes by name, tag, type…"
        />
      </div>

      {filtered.length === 0 ? (
        <div className="rounded-md border border-dashed p-8 text-center text-sm text-muted-foreground">
          No recipes match “{query}”.
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
