import Link from "next/link";
import { CheckCircle2, Loader2, Play, XCircle, AlertCircle } from "lucide-react";

import { Badge } from "@/components/ui/badge";
import { Card, CardContent } from "@/components/ui/card";
import { api, type RunSummary } from "@/lib/api";

export const dynamic = "force-dynamic";
export const metadata = { title: "Runs — Control Panel" };

export default async function RunsPage() {
  const runs = await api.runs({ limit: 100 }).catch(() => []);

  return (
    <div className="space-y-6">
      <div>
        <div className="text-xs font-semibold uppercase tracking-wider text-primary/70 mb-1.5">
          Runs
        </div>
        <h1 className="text-2xl font-semibold tracking-tight">Run history</h1>
        <p className="text-sm text-muted-foreground mt-1">
          {runs.length === 0
            ? "No runs yet."
            : `Last ${runs.length} run${runs.length === 1 ? "" : "s"}, persisted in SQLite at .cache/control_panel.db.`}
        </p>
      </div>

      {runs.length === 0 ? (
        <Card>
          <CardContent className="py-16 text-center">
            <Play className="h-10 w-10 mx-auto text-muted-foreground/40 mb-3" />
            <p className="text-sm text-muted-foreground">Nothing here yet.</p>
            <p className="text-xs text-muted-foreground/70 mt-1">
              Open a recipe and hit Run — completed runs survive a server restart.
            </p>
          </CardContent>
        </Card>
      ) : (
        <div className="rounded-xl border bg-card/40 backdrop-blur divide-y overflow-hidden">
          {runs.map((r) => (
            <RunRow key={r.id} run={r} />
          ))}
        </div>
      )}
    </div>
  );
}

function RunRow({ run }: { run: RunSummary }) {
  const duration = formatDuration(run.started_at, run.ended_at);
  return (
    <Link
      href={`/runs/${run.id}`}
      className="grid grid-cols-[auto_1fr_auto_auto] sm:grid-cols-[auto_2fr_1.5fr_auto_auto] items-center gap-3 px-4 py-3 hover:bg-accent/50 transition-colors"
    >
      <StatusIcon status={run.status} />
      <div className="min-w-0">
        <div className="text-sm font-medium truncate">{run.recipe_id}</div>
        <div className="text-[11px] text-muted-foreground font-mono truncate">{run.id}</div>
      </div>
      <div className="hidden sm:block text-xs text-muted-foreground font-mono truncate">
        {run.model_ref}
      </div>
      <div className="text-xs text-muted-foreground tabular-nums whitespace-nowrap">
        {duration}
      </div>
      {statusBadge(run.status)}
    </Link>
  );
}

function StatusIcon({ status }: { status: string }) {
  if (status === "running") return <Loader2 className="h-4 w-4 animate-spin text-indigo-500" />;
  if (status === "done") return <CheckCircle2 className="h-4 w-4 text-emerald-500" />;
  if (status === "error") return <XCircle className="h-4 w-4 text-rose-500" />;
  return <AlertCircle className="h-4 w-4 text-amber-500" />;
}

function statusBadge(status: string) {
  if (status === "done") return <Badge variant="success">done</Badge>;
  if (status === "running") return <Badge variant="info">running</Badge>;
  if (status === "error") return <Badge variant="destructive">error</Badge>;
  return <Badge variant="secondary">{status}</Badge>;
}

function formatDuration(startedAt: string, endedAt: string | null): string {
  const start = new Date(startedAt).getTime();
  const end = endedAt ? new Date(endedAt).getTime() : Date.now();
  const ms = end - start;
  if (ms < 1000) return `${ms}ms`;
  const sec = Math.floor(ms / 1000);
  if (sec < 60) return `${sec}s`;
  const min = Math.floor(sec / 60);
  const remSec = sec % 60;
  return `${min}m ${remSec}s`;
}
