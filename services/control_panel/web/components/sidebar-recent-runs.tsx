"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { CheckCircle2, Loader2, XCircle, AlertCircle } from "lucide-react";

import { api, type RunSummary } from "@/lib/api";
import { useSidebarCollapsed } from "@/components/sidebar-context";

export function SidebarRecentRuns() {
  const [runs, setRuns] = useState<RunSummary[] | null>(null);
  const collapsed = useSidebarCollapsed();

  useEffect(() => {
    let cancelled = false;
    const tick = async () => {
      try {
        const data = await api.runs({ limit: 5 });
        if (!cancelled) setRuns(data);
      } catch {
        if (!cancelled) setRuns([]);
      }
    };
    tick();
    const id = setInterval(tick, 5_000);
    return () => {
      cancelled = true;
      clearInterval(id);
    };
  }, []);

  // Recent runs is a label/time list — meaningless as icon-only. Drop it
  // entirely when the rail is collapsed.
  if (collapsed) return null;
  if (runs === null) return null;
  if (runs.length === 0) {
    return (
      <div className="px-5 py-3 border-t text-[11px] text-muted-foreground">
        No runs yet — open a recipe and hit Run.
      </div>
    );
  }
  return (
    <div className="px-3 py-3 border-t space-y-0.5">
      <div className="px-2 pb-1.5 text-[10px] font-semibold uppercase tracking-wider text-muted-foreground">
        Recent runs
      </div>
      {runs.map((r) => (
        <Link
          key={r.id}
          href={`/runs/${r.id}`}
          className="flex items-center gap-2 px-2 py-1.5 rounded-md text-xs hover:bg-accent transition-colors"
        >
          <StatusIcon status={r.status} />
          <span className="truncate flex-1 text-foreground">{r.recipe_id}</span>
          <span className="text-[10px] font-mono text-muted-foreground">
            {timeAgo(r.started_at)}
          </span>
        </Link>
      ))}
    </div>
  );
}

function StatusIcon({ status }: { status: string }) {
  if (status === "running") {
    return <Loader2 className="h-3 w-3 animate-spin text-indigo-500 shrink-0" />;
  }
  if (status === "done") {
    return <CheckCircle2 className="h-3 w-3 text-emerald-500 shrink-0" />;
  }
  if (status === "error") {
    return <XCircle className="h-3 w-3 text-rose-500 shrink-0" />;
  }
  return <AlertCircle className="h-3 w-3 text-amber-500 shrink-0" />;
}

function timeAgo(iso: string): string {
  const then = new Date(iso).getTime();
  const diffSec = Math.floor((Date.now() - then) / 1000);
  if (diffSec < 60) return `${diffSec}s`;
  if (diffSec < 3600) return `${Math.floor(diffSec / 60)}m`;
  if (diffSec < 86400) return `${Math.floor(diffSec / 3600)}h`;
  return `${Math.floor(diffSec / 86400)}d`;
}
