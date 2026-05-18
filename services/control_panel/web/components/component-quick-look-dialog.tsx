"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useState, useTransition } from "react";
import { ArrowUpRight, CheckCircle2, Loader2, XCircle } from "lucide-react";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { FeatureStatusBadge } from "@/components/feature-status-badge";
import { InstallConfirmDialog } from "@/components/install-confirm-dialog";
import { VerifyIconButton } from "@/components/verify-icon-button";
import { ContainerLogsDialog } from "@/components/container-logs-dialog";
import { api, type Feature, type FeatureActionResult, type FeatureStatus } from "@/lib/api";

// Friendly one-liners per status — the "what does this mean for me" line.
const STATUS_HINT: Record<FeatureStatus, string> = {
  installed: "Up and running.",
  partial: "Installed but verification is failing — try Verify or reinstall.",
  stopped: "Installed but not running — click Start to bring it back up.",
  available: "Not installed yet.",
  unavailable: "Not available on this system — install hint may be missing for your distro.",
  error: "In an error state — uninstall + reinstall usually clears it.",
  unknown: "Status couldn't be determined — try Verify.",
};

// Recipe-kind detail lives at /recipes/:id (the canonical, run-flavoured
// page). All other kinds keep their detail under /components/:kind/:id.
function detailHref(feature: Feature): string {
  if (feature.kind === "recipe") return `/recipes/${feature.id}`;
  return `/components/${feature.kind}/${feature.id}`;
}

type Props = {
  feature: Feature;
  open: boolean;
  onOpenChange: (open: boolean) => void;
};

export function ComponentQuickLookDialog({ feature, open, onOpenChange }: Props) {
  const router = useRouter();
  const [pending, startTransition] = useTransition();
  const [actionResult, setActionResult] = useState<FeatureActionResult | null>(null);
  const [actionError, setActionError] = useState<string | null>(null);

  // Which uninstall buttons to show — mirrors the rules in feature-action-buttons
  // but trimmed for the quick-look context. MCP can sit in two scopes; everyone
  // else has at most one.
  const isMcp = feature.kind === "mcp";
  const isConnector = feature.kind === "connector";
  const installedScopes: string[] =
    isMcp && Array.isArray(feature.detail?.installed_scopes)
      ? (feature.detail.installed_scopes as string[])
      : [];
  const notInstalled = feature.status === "available" || feature.status === "unavailable";
  const fullyInstalled = feature.status === "installed";
  const showInstall = (!fullyInstalled || isMcp) && !isConnector;
  const showUninstall = feature.kind !== "system" && !notInstalled;
  const canShowLogs =
    feature.kind === "container" &&
    (feature.status === "installed" || feature.status === "partial");

  const runAction = (action: () => Promise<FeatureActionResult>) => {
    setActionError(null);
    setActionResult(null);
    startTransition(async () => {
      try {
        const result = await action();
        setActionResult(result);
        router.refresh();
      } catch (e) {
        setActionError(e instanceof Error ? e.message : String(e));
      }
    });
  };

  const firstExample = feature.examples[0];

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-lg overflow-hidden">
        <DialogHeader>
          {/* pr-8 keeps the title clear of the absolute close ✕ (right-4).
           * The status badge sits on its own line so it never collides with
           * the ✕ and never wraps mid-label ("not installed"). */}
          <div className="min-w-0 pr-8">
            <div className="flex items-center gap-2">
              <div className="text-[10px] font-semibold uppercase tracking-wider text-primary/70">
                {feature.kind}
              </div>
              <span className="shrink-0 whitespace-nowrap">
                <FeatureStatusBadge status={feature.status} />
              </span>
            </div>
            <DialogTitle className="text-lg mt-1">{feature.name}</DialogTitle>
            <DialogDescription className="mt-1">
              {feature.description || "(no description)"}
            </DialogDescription>
          </div>
        </DialogHeader>

        <div className="min-w-0 space-y-4">
          <div className="rounded-md border bg-card/40 px-3 py-2.5 text-sm">
            <span className="text-muted-foreground">{STATUS_HINT[feature.status]}</span>
          </div>

          {/* Quick actions row — Install / Uninstall / Verify. Mirrors the
           * detail page's action buttons but condensed for the dialog. */}
          <div className="flex flex-wrap items-center gap-2">
            {showInstall && (
              <InstallConfirmDialog
                feature={feature}
                onInstalled={(result) => {
                  setActionResult(result);
                  router.refresh();
                }}
                trigger={
                  <Button size="sm" disabled={pending}>
                    {pending ? (
                      <Loader2 className="h-3.5 w-3.5 animate-spin mr-1" />
                    ) : null}
                    {feature.kind === "container" && feature.status === "stopped" ? "Start" : "Install"}
                  </Button>
                }
              />
            )}
            {showUninstall && (
              <Button
                size="sm"
                variant="outline"
                disabled={pending}
                onClick={() => runAction(() => api.uninstallFeature(feature.kind, feature.id))}
              >
                Uninstall
                {isMcp && installedScopes.length === 1 && (
                  <span className="ml-1 text-[10px] uppercase tracking-wider text-muted-foreground">
                    ({installedScopes[0]})
                  </span>
                )}
              </Button>
            )}
            {canShowLogs && <ContainerLogsDialog feature={feature} size="sm" />}
            <VerifyIconButton
              featureKind={feature.kind}
              featureId={feature.id}
              onVerified={() => router.refresh()}
              size="sm"
            />
          </div>

          {actionResult && <ActionResultLine result={actionResult} />}
          {actionError && (
            <div className="rounded-md border border-destructive/40 bg-destructive/10 px-3 py-2 text-xs">
              {actionError}
            </div>
          )}

          {/* First example only — the dialog stays scannable. The full
           * Examples list lives on the detail page. */}
          {firstExample && (
            <div className="min-w-0 space-y-1.5">
              <div className="flex items-baseline justify-between gap-3">
                <div className="text-[10px] font-semibold uppercase tracking-wider text-muted-foreground shrink-0">
                  Example {feature.examples.length > 1 ? `1 of ${feature.examples.length}` : ""}
                </div>
                {firstExample.label && (
                  <div className="text-[11px] text-muted-foreground italic truncate min-w-0">
                    {firstExample.label}
                  </div>
                )}
              </div>
              <pre className="max-w-full rounded-md border bg-muted/30 p-2.5 text-[11px] overflow-x-auto leading-relaxed">
                {firstExample.code}
              </pre>
            </div>
          )}

          {feature.requires.length > 0 && (
            <div className="flex flex-wrap items-baseline gap-1.5 text-xs">
              <span className="text-muted-foreground">requires:</span>
              {feature.requires.map((r) => (
                <Badge key={r} variant="outline" className="font-mono">
                  {r}
                </Badge>
              ))}
            </div>
          )}
        </div>

        <DialogFooter className="sm:justify-between">
          <Button
            variant="ghost"
            size="sm"
            onClick={() => onOpenChange(false)}
          >
            Close
          </Button>
          <Button asChild size="sm" variant="outline">
            <Link href={detailHref(feature)}>
              View full details
              <ArrowUpRight className="h-3.5 w-3.5 ml-1" />
            </Link>
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}

function ActionResultLine({ result }: { result: FeatureActionResult }) {
  if (result.ok) {
    return (
      <div className="flex items-center gap-2 text-xs text-emerald-700 dark:text-emerald-400">
        <CheckCircle2 className="h-3.5 w-3.5" />
        {result.noop ? "Already in the desired state" : result.message ?? "Done"}
      </div>
    );
  }
  return (
    <div className="flex items-center gap-2 text-xs text-destructive">
      <XCircle className="h-3.5 w-3.5" />
      {result.error ?? "Action did not succeed"}
    </div>
  );
}
