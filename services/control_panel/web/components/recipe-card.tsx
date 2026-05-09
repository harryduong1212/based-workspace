import Link from "next/link";
import { ArrowUpRight, Cpu, Network, Sparkles, Workflow } from "lucide-react";

import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import type { RecipeSummary } from "@/lib/api";

const TYPE_ICON: Record<string, React.ComponentType<{ className?: string }>> = {
  prompt: Sparkles,
  agent: Cpu,
  workflow: Workflow,
};

function statusVariant(status: string) {
  if (status === "stable") return "success" as const;
  if (status === "experimental") return "warn" as const;
  return "secondary" as const;
}

export function RecipeCard({ recipe }: { recipe: RecipeSummary }) {
  const Icon = TYPE_ICON[recipe.execution_type] ?? Network;
  return (
    <Link href={`/recipes/${recipe.id}`} className="block group focus:outline-hidden">
      <Card className="h-full card-lift border-border/60 group-focus-visible:ring-2 group-focus-visible:ring-ring">
        <CardHeader className="pb-3">
          <div className="flex items-center justify-between gap-2 mb-1">
            <span className="inline-flex h-7 w-7 items-center justify-center rounded-md bg-primary/10 text-primary">
              <Icon className="h-3.5 w-3.5" />
            </span>
            <Badge variant={statusVariant(recipe.status)}>{recipe.status || "n/a"}</Badge>
          </div>
          <CardTitle className="text-base flex items-center gap-1 truncate">
            {recipe.name}
            <ArrowUpRight className="h-3.5 w-3.5 opacity-0 group-hover:opacity-100 text-muted-foreground transition-opacity" />
          </CardTitle>
          <CardDescription className="line-clamp-2 min-h-[2.5rem]">
            {recipe.description || "(no description)"}
          </CardDescription>
        </CardHeader>
        <CardContent className="pt-0">
          <div className="flex items-center justify-between text-[11px]">
            <code className="font-mono text-muted-foreground truncate">{recipe.id}</code>
            <Badge variant="info">{recipe.execution_type}</Badge>
          </div>
          {recipe.tags.length > 0 && (
            <div className="flex flex-wrap gap-1 mt-3">
              {recipe.tags.slice(0, 4).map((t) => (
                <Badge key={t} variant="secondary" className="text-[10px] font-normal hover:bg-secondary/60 transition-colors">
                  {t}
                </Badge>
              ))}
              {recipe.tags.length > 4 && (
                <span className="text-[10px] text-muted-foreground">+{recipe.tags.length - 4}</span>
              )}
            </div>
          )}
        </CardContent>
      </Card>
    </Link>
  );
}
