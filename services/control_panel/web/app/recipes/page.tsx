import { RecipesView } from "@/components/recipes-view";
import { api } from "@/lib/api";

export const dynamic = "force-dynamic";
export const metadata = { title: "Recipes — Control Panel" };

export default async function RecipesPage() {
  const data = await api.dashboard();
  const recipes = [...data.recipes].sort((a, b) => a.id.localeCompare(b.id));

  return <RecipesView recipes={recipes} />;
}
