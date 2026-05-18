"use client";

import { useRouter } from "next/navigation";
import { useState, useTransition } from "react";
import Link from "next/link";
import {
  Brain,
  Database,
  Loader2,
  Power,
  PowerOff,
  RefreshCw,
  Server,
  Sparkles,
  Workflow,
} from "lucide-react";

import { Button } from "@/components/ui/button";
import { FeatureStatusBadge } from "@/components/feature-status-badge";
import { InstallConfirmDialog } from "@/components/install-confirm-dialog";
import type { Feature, FeatureKind } from "@/lib/api";
import { api } from "@/lib/api";

/**
 * Dashboard widget: shows the four infrastructure containers (Postgres,
 * llama-swap, n8n, Qdrant) with start/stop controls and a refresh button.
 * Server passes initial state; the widget re-fetches on click.
 *
 * The two the user typically cares about (Postgres + llama-swap) get
 * primary visual weight; n8n + Qdrant sit alongside as secondary.
 */

const ICON: Record<string, React.ComponentType<{ className?: string }>> = {
  postgres: Database,
  "llama-swap": Sparkles,
  n8n: Workflow,
  qdrant: Brain,
};

const PRIMARY_ORDER = ["llama-swap", "postgres", "n8n", "qdrant"];

export function InfraStatusWidget({ initial }: { initial: Feature[] }) {
  const router = useRouter();
  const [features, setFeatures] = useState<Feature[]>(initial);
  const [pending, startTransition] = useTransition();
  const [actingId, setActingId] = useState<string | null>(null);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  const refetch = async () => {
    const data = await api.features();
    setFeatures(data.features.filter((f) => f.kind === "container"));
  };

  const onRefresh = () => {
    setErrorMsg(null);
    startTransition(async () => {
      try {
        await refetch();
        router.refresh();
      } catch (e) {
        setErrorMsg(e instanceof Error ? e.message : String(e));
      }
    });
  };

  const onUninstall = (kind: FeatureKind, id: string) => {
    setErrorMsg(null);
    setActingId(id);
    startTransition(async () => {
      try {
        await api.uninstallFeature(kind, id);
        await refetch();
        router.refresh();
      } catch (e) {
        setErrorMsg(e instanceof Error ? e.message : String(e));
      } finally {
        setActingId(null);
      }
    });
  };

  const onInstalled = async () => {
    setErrorMsg(null);
    startTransition(async () => {
      try {
        await refetch();
        router.refresh();
      } catch (e) {
        setErrorMsg(e instanceof Error ? e.message : String(e));
      }
    });
  };

  // Sort by primary order then by id (anything else not in PRIMARY_ORDER appended).
  const sorted = [...features].sort((a, b) => {
    const ai = PRIMARY_ORDER.indexOf(a.id);
    const bi = PRIMARY_ORDER.indexOf(b.id);
    if (ai === -1 && bi === -1) return a.id.localeCompare(b.id);
    if (ai === -1) return 1;
    if (bi === -1) return -1;
    return ai - bi;
  });

  return (
    <section>
      <div className="flex items-baseline justify-between mb-3">
        <h2 className="text-sm font-semibold uppercase tracking-wider text-muted-foreground">
          Infrastructure
        </h2>
        <Button
          variant="ghost"
          size="sm"
          onClick={onRefresh}
          disabled={pending}
          className="text-xs"
        >
          <RefreshCw className={`h-3.5 w-3.5 ${pending ? "animate-spin" : ""}`} />
          Refresh
        </Button>
      </div>

      <div className="grid grid-cols-2 lg:grid-cols-4 gap-3">
        {sorted.map((f) => {
          const Icon = ICON[f.id] ?? Server;
          const running = f.status === "installed";
          const partial = f.status === "partial";
          const acting = pending && actingId === f.id;
          return (
            <div
              key={f.id}
              className="rounded-lg border bg-card/40 backdrop-blur p-3 space-y-2"
            >
              <div className="flex items-start justify-between gap-2">
                <div className="flex items-center gap-2 min-w-0">
                  <span className="inline-flex h-7 w-7 shrink-0 items-center justify-center rounded-md bg-primary/10 text-primary">
                    <Icon className="h-3.5 w-3.5" />
                  </span>
                  <div className="min-w-0">
                    <div className="text-sm font-medium truncate">{f.name}</div>
                    <code className="text-[10px] text-muted-foreground font-mono">
                      {f.id}
                    </code>
                  </div>
                </div>
                <FeatureStatusBadge status={f.status} />
              </div>

              <div className="flex items-center gap-1.5">
                {running || partial ? (
                  <Button
                    size="sm"
                    variant="outline"
                    onClick={() => onUninstall("container", f.id)}
                    disabled={pending}
                    className="h-7 text-xs flex-1"
                  >
                    {acting ? (
                      <Loader2 className="h-3 w-3 animate-spin" />
                    ) : (
                      <PowerOff className="h-3 w-3" />
                    )}
                    Stop
                  </Button>
                ) : (
                  <InstallConfirmDialog
                    feature={f}
                    onInstalled={() => onInstalled()}
                    trigger={
                      <Button
                        size="sm"
                        disabled={pending}
                        className="h-7 text-xs flex-1"
                      >
                        {acting ? (
                          <Loader2 className="h-3 w-3 animate-spin" />
                        ) : (
                          <Power className="h-3 w-3" />
                        )}
                        Start
                      </Button>
                    }
                  />
                )}
                <Button asChild size="sm" variant="ghost" className="h-7 text-xs px-2">
                  <Link href={`/components/container/${f.id}`}>Details</Link>
                </Button>
              </div>
            </div>
          );
        })}
      </div>

      {errorMsg && (
        <div className="mt-2 rounded-md border border-destructive/40 bg-destructive/10 p-2 text-xs">
          <pre className="whitespace-pre-wrap break-all">{errorMsg}</pre>
        </div>
      )}
    </section>
  );
}
