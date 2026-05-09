import Link from "next/link";

import { cn } from "@/lib/utils";

export type RecipeTab = "overview" | "run" | "edit";

const TABS: { key: RecipeTab; label: string; suffix: string }[] = [
  { key: "overview", label: "Overview", suffix: "" },
  { key: "run", label: "Run", suffix: "/run" },
  { key: "edit", label: "Edit", suffix: "/edit" },
];

export function RecipeTabs({ recipeId, active }: { recipeId: string; active: RecipeTab }) {
  return (
    <div className="border-b">
      <nav className="-mb-px flex gap-6">
        {TABS.map((t) => (
          <Link
            key={t.key}
            href={`/recipes/${recipeId}${t.suffix}`}
            className={cn(
              "inline-flex items-center px-1 py-2.5 text-sm border-b-2 transition-colors",
              t.key === active
                ? "border-primary text-foreground font-medium"
                : "border-transparent text-muted-foreground hover:text-foreground hover:border-border",
            )}
          >
            {t.label}
          </Link>
        ))}
      </nav>
    </div>
  );
}
