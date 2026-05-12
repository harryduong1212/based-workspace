import Link from "next/link";
import { ArrowRight, Boxes, Network, Play } from "lucide-react";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { InfraStatusWidget } from "@/components/infra-status-widget";
import { api } from "@/lib/api";

export const dynamic = "force-dynamic";

function statusBadge(status: string) {
  switch (status) {
    case "done":
      return <Badge variant="success">done</Badge>;
    case "running":
      return <Badge variant="info">running</Badge>;
    case "error":
      return <Badge variant="destructive">error</Badge>;
    default:
      return <Badge variant="secondary">{status}</Badge>;
  }
}

export default async function OverviewPage() {
  const [dash, runs, features] = await Promise.all([
    api.dashboard(),
    api.runs({ limit: 8 }).catch(() => []),
    api.features().catch(() => ({ features: [], kinds: [] })),
  ]);
  const containers = features.features.filter((f) => f.kind === "container");

  return (
    <div className="space-y-10">
      {/* Hero */}
      <div className="relative overflow-hidden rounded-2xl border bg-card/40 backdrop-blur p-8">
        <div className="absolute inset-0 dot-grid opacity-50 pointer-events-none" />
        <div className="relative">
          <div className="text-xs font-semibold uppercase tracking-wider text-primary/70 mb-2">
            Workspace
          </div>
          <h1 className="text-3xl font-semibold tracking-tight">based-workspace</h1>
          <p className="text-sm text-muted-foreground mt-2 max-w-xl">
            Run AI recipes against your tools. Configure connectors once, schedule routines, watch outputs stream live.
          </p>
          <div className="mt-5 flex flex-wrap gap-2">
            <Button asChild size="sm">
              <Link href="/recipes">
                <Boxes className="h-4 w-4" /> Browse recipes
              </Link>
            </Button>
            <Button asChild size="sm" variant="outline">
              <Link href="/connectors">
                <Network className="h-4 w-4" /> Connectors
              </Link>
            </Button>
          </div>
        </div>
      </div>

      {/* Infrastructure quick controls — sits above stats because "is my stack ready?"
          is the most actionable question at start-of-day. */}
      <InfraStatusWidget initial={containers} />

      {/* Stats */}
      <div className="grid sm:grid-cols-3 gap-4">
        <StatCard icon={Boxes} label="Recipes" value={dash.recipes.length} href="/recipes" />
        <StatCard icon={Network} label="Connectors" value={dash.connectors.length} href="/connectors" />
        <StatCard icon={Play} label="Runs" value={runs.length} href="/runs" />
      </div>

      {/* Recent runs */}
      <section>
        <div className="flex items-baseline justify-between mb-3">
          <h2 className="text-sm font-semibold uppercase tracking-wider text-muted-foreground">
            Recent runs
          </h2>
          <Link href="/runs" className="text-xs text-primary hover:underline inline-flex items-center gap-1">
            View all <ArrowRight className="h-3 w-3" />
          </Link>
        </div>
        {runs.length === 0 ? (
          <Card>
            <CardContent className="py-12 text-center">
              <Play className="h-8 w-8 mx-auto text-muted-foreground/50 mb-3" />
              <p className="text-sm text-muted-foreground">No runs yet.</p>
              <p className="text-xs text-muted-foreground/70 mt-1">
                Open a recipe and hit Run to see history here.
              </p>
            </CardContent>
          </Card>
        ) : (
          <div className="rounded-xl border bg-card/40 backdrop-blur divide-y">
            {runs.map((r) => (
              <Link
                key={r.id}
                href={`/runs/${r.id}`}
                className="flex items-center gap-3 px-4 py-3 hover:bg-accent/50 transition-colors"
              >
                <div className="flex-1 min-w-0">
                  <div className="text-sm font-medium truncate">{r.recipe_id}</div>
                  <div className="text-xs text-muted-foreground truncate font-mono">
                    {r.model_ref}
                  </div>
                </div>
                <div className="text-xs text-muted-foreground tabular-nums">
                  {new Date(r.started_at).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}
                </div>
                {statusBadge(r.status)}
              </Link>
            ))}
          </div>
        )}
      </section>
    </div>
  );
}

function StatCard({
  icon: Icon,
  label,
  value,
  href,
}: {
  icon: React.ComponentType<{ className?: string }>;
  label: string;
  value: number;
  href: string;
}) {
  return (
    <Link href={href} className="block group">
      <Card className="card-lift border-border/60">
        <CardHeader className="pb-2">
          <div className="flex items-center justify-between">
            <span className="inline-flex h-8 w-8 items-center justify-center rounded-md bg-primary/10 text-primary">
              <Icon className="h-4 w-4" />
            </span>
            <ArrowRight className="h-3.5 w-3.5 text-muted-foreground opacity-0 group-hover:opacity-100 transition-opacity" />
          </div>
          <CardDescription className="text-[11px] uppercase tracking-wider mt-2">
            {label}
          </CardDescription>
        </CardHeader>
        <CardContent>
          <CardTitle className="text-3xl font-semibold tabular-nums">{value}</CardTitle>
        </CardContent>
      </Card>
    </Link>
  );
}
