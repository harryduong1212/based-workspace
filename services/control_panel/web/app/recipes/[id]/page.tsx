import Link from "next/link";
import { notFound } from "next/navigation";
import { ChevronLeft, Sparkles } from "lucide-react";

import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { FeatureActionButtons } from "@/components/feature-action-buttons";
import { FeatureStatusBadge } from "@/components/feature-status-badge";
import { InstallStateNotice } from "@/components/install-state-notice";
import { RecipeActions } from "@/components/recipe-actions";
import { api, type Feature, type FeatureDetail } from "@/lib/api";

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

  // The recipe content (frontmatter + body) comes from /api/v1/recipes/<id>.
  // The install-side state (synced to .claude/ + .agents/, status, plus the
  // editorial about/highlights/examples we author in frontmatter) lives on
  // the feature endpoint. We fetch both — the feature lookup is cheap and
  // lets us merge the two views into one page. If it 404s we soldier on
  // without the install controls (older recipes without a registry entry).
  let featureDetail: FeatureDetail | null = null;
  try {
    featureDetail = await api.feature("recipe", id);
  } catch {
    featureDetail = null;
  }
  const feature: Feature | null = featureDetail?.feature ?? null;
  const unmetPrereqs = featureDetail?.unmet_prereqs ?? [];
  const unmetPrereqsDetail = featureDetail?.unmet_prereqs_detail;

  return (
    <div className="space-y-6">
      <div>
        <Link
          href="/recipes"
          className="inline-flex items-center gap-1 text-xs text-muted-foreground hover:text-foreground"
        >
          <ChevronLeft className="h-3 w-3" /> Recipes
        </Link>
        <div className="mt-2 flex items-center justify-between gap-3">
          <div className="min-w-0">
            <div className="flex items-baseline gap-2">
              <h1 className="text-2xl font-semibold tracking-tight">{recipe.name}</h1>
              <span className="text-sm text-muted-foreground">recipe</span>
            </div>
            <p className="text-sm text-muted-foreground mt-1">
              {recipe.description || "(no description)"}
            </p>
          </div>
          {feature && <FeatureStatusBadge status={feature.status} />}
        </div>
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

      <div className="mt-6">
        <RecipeActions recipeId={recipe.id} />
      </div>

      {/* Install / Uninstall / Verify lives next to Run/Edit so the page
        * carries both flows. Hidden when the feature lookup failed (e.g. a
        * recipe present on disk but not registered yet). */}
      {feature && (
        <Card>
          <CardHeader className="pb-3">
            <CardTitle className="text-base">Install state</CardTitle>
          </CardHeader>
          <CardContent>
            <InstallStateNotice status={feature.status} />
            <FeatureActionButtons
              feature={feature}
              unmetPrereqs={unmetPrereqs}
              unmetPrereqsDetail={unmetPrereqsDetail}
              allowUninstall={true}
            />
          </CardContent>
        </Card>
      )}

      <div className="grid lg:grid-cols-[minmax(0,3fr)_minmax(0,1fr)] gap-6">
        <article className="min-w-0 space-y-6">
          {/* Editorial cards — about / highlights / examples — sit ABOVE
            * the rendered recipe body so a reader gets the "what / why /
            * how" before the long prompt-style instructions. */}
          {feature?.about && (
            <Card>
              <CardHeader className="pb-3">
                <CardTitle className="text-base">About</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-sm leading-relaxed text-foreground/90 whitespace-pre-line">
                  {feature.about}
                </p>
              </CardContent>
            </Card>
          )}

          {feature && feature.highlights.length > 0 && (
            <Card>
              <CardHeader className="pb-3">
                <CardTitle className="text-base flex items-center gap-2">
                  <Sparkles className="h-4 w-4 text-primary/80" />
                  Highlights
                </CardTitle>
              </CardHeader>
              <CardContent>
                <ul className="space-y-1.5 text-sm leading-relaxed">
                  {feature.highlights.map((h, i) => (
                    <li key={i} className="flex gap-2">
                      <span className="text-primary/70 mt-0.5">•</span>
                      <span className="text-foreground/90">{h}</span>
                    </li>
                  ))}
                </ul>
              </CardContent>
            </Card>
          )}

          {feature && feature.examples.length > 0 && (
            <Card>
              <CardHeader className="pb-3">
                <CardTitle className="text-base">Examples</CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                {feature.examples.map((ex, i) => (
                  <div key={i} className="space-y-1.5">
                    {ex.label && (
                      <div className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
                        {ex.label}
                      </div>
                    )}
                    <pre className="rounded-md border bg-muted/30 p-2.5 text-xs overflow-x-auto leading-relaxed">
                      {ex.code}
                    </pre>
                  </div>
                ))}
              </CardContent>
            </Card>
          )}

          <article
            className="min-w-0 prose-body"
            dangerouslySetInnerHTML={{ __html: recipe.rendered_body }}
          />
        </article>

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

          {/* Sync state moved from the old Components/Recipe page — surfaces
            * which provider directories the recipe is installed into. */}
          {feature && (
            <Card>
              <CardHeader className="pb-3">
                <CardTitle className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
                  Sync targets
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-1.5 text-sm">
                <Row label=".claude/">
                  {feature.detail?.in_claude ? (
                    <Badge variant="success">synced</Badge>
                  ) : (
                    <Badge variant="secondary">not synced</Badge>
                  )}
                </Row>
                <Row label=".agents/">
                  {feature.detail?.in_agents ? (
                    <Badge variant="success">synced</Badge>
                  ) : (
                    <Badge variant="secondary">not synced</Badge>
                  )}
                </Row>
              </CardContent>
            </Card>
          )}

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
                <ListRow label="connectors" items={recipe.requires_connectors} linkPrefix="/components/connector/" />
                <ListRow label="workflows" items={recipe.requires_workflows} />
                <ListRow label="mcp" items={recipe.requires_mcp} linkPrefix="/components/mcp/" />
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
