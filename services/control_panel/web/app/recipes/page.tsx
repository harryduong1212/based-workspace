import { RecipeCard } from "@/components/recipe-card";
import { api } from "@/lib/api";

export const dynamic = "force-dynamic";
export const metadata = { title: "Recipes — Control Panel" };

export default async function RecipesPage() {
  const data = await api.dashboard();
  const recipes = [...data.recipes].sort((a, b) => a.id.localeCompare(b.id));

  return (
    <div className="space-y-6">
      <div>
        <div className="text-xs font-semibold uppercase tracking-wider text-primary/70 mb-1.5">
          Recipes
        </div>
        <h1 className="text-2xl font-semibold tracking-tight">All recipes</h1>
        <p className="text-sm text-muted-foreground mt-1">
          {recipes.length} recipe{recipes.length === 1 ? "" : "s"} declared in the workspace.
        </p>
      </div>

      <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
        {recipes.map((r) => (
          <RecipeCard key={r.id} recipe={r} />
        ))}
      </div>
    </div>
  );
}
