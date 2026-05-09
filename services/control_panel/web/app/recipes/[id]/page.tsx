import Link from "next/link";
import { notFound } from "next/navigation";
import { ChevronLeft } from "lucide-react";

import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { RecipeTabs } from "@/components/recipe-tabs";
import { api } from "@/lib/api";

export const dynamic = "force-dynamic";

export default async function RecipeOverviewPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;
  let recipe;
  try {
    recipe = await api.recipe(id);
  } catch (e) {
    if (e instanceof Error && e.message.includes("404")) notFound();
    throw e;
  }

  return (
    <div className="space-y-6">
      <div>
        <Link
          href="/recipes"
          className="inline-flex items-center gap-1 text-xs text-muted-foreground hover:text-foreground"
        >
          <ChevronLeft className="h-3 w-3" /> Recipes
        </Link>
        <div className="mt-2 flex items-baseline gap-2">
          <h1 className="text-2xl font-semibold tracking-tight">{recipe.name}</h1>
          <span className="text-sm text-muted-foreground">recipe</span>
        </div>
        <p className="text-sm text-muted-foreground mt-1">
          {recipe.description || "(no description)"}
        </p>
        <div className="flex flex-wrap gap-1.5 mt-3">
          <Badge variant={recipe.status === "stable" ? "success" : "warn"}>
            {recipe.status || "n/a"}
          </Badge>
          {recipe.audience && <Badge variant="info">{recipe.audience}</Badge>}
          <Badge variant="info">{recipe.execution_type}</Badge>
          {recipe.tags.map((t) => (
            <Badge key={t} variant="outline">
              {t}
            </Badge>
          ))}
        </div>
      </div>

      <RecipeTabs recipeId={recipe.id} active="overview" />

      <div className="grid lg:grid-cols-[minmax(0,3fr)_minmax(0,1fr)] gap-6">
        <article
          className="min-w-0 prose-body"
          dangerouslySetInnerHTML={{ __html: recipe.rendered_body }}
        />

        <aside className="space-y-4">
          <Card>
            <CardHeader className="pb-3">
              <CardTitle className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
                Execution
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-2 text-sm">
              <Row label="type"><Badge variant="info">{recipe.execution_type}</Badge></Row>
              {recipe.execution_model && (
                <Row label="default model">
                  <code className="font-mono text-xs">{recipe.execution_model}</code>
                </Row>
              )}
              {recipe.cost && <Row label="cost">{recipe.cost}</Row>}
              {recipe.version && (
                <Row label="version">
                  <code className="font-mono text-xs">{recipe.version}</code>
                </Row>
              )}
            </CardContent>
          </Card>

          {(recipe.requires_skills.length > 0 ||
            recipe.requires_connectors.length > 0 ||
            recipe.requires_workflows.length > 0 ||
            recipe.requires_mcp.length > 0 ||
            recipe.requires_env.length > 0) && (
            <Card>
              <CardHeader className="pb-3">
                <CardTitle className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
                  Requires
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-3 text-sm">
                <ListRow label="skills" items={recipe.requires_skills} />
                <ListRow label="connectors" items={recipe.requires_connectors} linkPrefix="/connectors/" />
                <ListRow label="workflows" items={recipe.requires_workflows} />
                <ListRow label="mcp" items={recipe.requires_mcp} />
                <ListRow label="env" items={recipe.requires_env} mono />
              </CardContent>
            </Card>
          )}

          {recipe.inputs.length > 0 && (
            <Card>
              <CardHeader className="pb-3">
                <CardTitle className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
                  Inputs
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-2.5 text-sm">
                {recipe.inputs.map((inp) => (
                  <div key={inp.name}>
                    <div className="flex items-center gap-1.5">
                      <code className="font-mono text-xs">{inp.name}</code>
                      {inp.required && <span className="text-rose-500 text-xs">*</span>}
                      {inp.type && (
                        <span className="text-[10px] text-muted-foreground">({inp.type})</span>
                      )}
                    </div>
                    {inp.description && (
                      <p className="text-xs text-muted-foreground mt-0.5">{inp.description}</p>
                    )}
                  </div>
                ))}
              </CardContent>
            </Card>
          )}

          <Card>
            <CardHeader className="pb-3">
              <CardTitle className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
                File
              </CardTitle>
            </CardHeader>
            <CardContent>
              <code className="font-mono text-xs text-muted-foreground break-all">
                {recipe.relative_path}
              </code>
            </CardContent>
          </Card>
        </aside>
      </div>
    </div>
  );
}

function Row({ label, children }: { label: string; children: React.ReactNode }) {
  return (
    <div className="grid grid-cols-[max-content_1fr] gap-x-3 items-baseline">
      <dt className="text-muted-foreground">{label}</dt>
      <dd>{children}</dd>
    </div>
  );
}

function ListRow({
  label,
  items,
  linkPrefix,
  mono,
}: {
  label: string;
  items: string[];
  linkPrefix?: string;
  mono?: boolean;
}) {
  if (items.length === 0) return null;
  return (
    <div>
      <div className="text-[11px] uppercase tracking-wider text-muted-foreground mb-1">
        {label}
      </div>
      <div className="flex flex-wrap gap-1">
        {items.map((it) =>
          linkPrefix ? (
            <Link
              key={it}
              href={`${linkPrefix}${it}`}
              className="inline-flex items-center px-2 py-0.5 text-[11px] rounded-full bg-emerald-500/15 text-emerald-700 dark:text-emerald-300 hover:bg-emerald-500/25 transition-colors"
            >
              {it}
            </Link>
          ) : (
            <span
              key={it}
              className={`inline-flex items-center px-2 py-0.5 text-[11px] rounded-full bg-muted text-foreground/80 ${
                mono ? "font-mono" : ""
              }`}
            >
              {it}
            </span>
          ),
        )}
      </div>
    </div>
  );
}
