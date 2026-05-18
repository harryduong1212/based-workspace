"use client";

import { useRouter } from "next/navigation";
import { useState, useTransition } from "react";
import { CheckCircle2, AlertTriangle, Loader2 } from "lucide-react";

import { Button } from "@/components/ui/button";
import { InstallConfirmDialog } from "@/components/install-confirm-dialog";
import { api, type Feature, type FeatureActionResult, type PrereqDetail } from "@/lib/api";
import { prereqLabel } from "@/lib/prereq";

type Props = {
  feature: Feature;
  unmetPrereqs: string[];
  unmetPrereqsDetail?: PrereqDetail[];
  installInputs?: Record<string, unknown>;
  // Whether the system uninstall button is shown (defaults to false for T1).
  allowUninstall?: boolean;
};

export function FeatureActionButtons({
  feature,
  unmetPrereqs,
  unmetPrereqsDetail,
  installInputs,
  allowUninstall = true,
}: Props) {
  const router = useRouter();
  const [pending, startTransition] = useTransition();
  const [lastResult, setLastResult] = useState<FeatureActionResult | null>(null);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  // Unmet prereqs no longer block — they trigger an auto-cascade the dialog
  // explains step by step. We only use this to surface an informational note.
  const hasUnmetPrereqs = unmetPrereqs.length > 0;
  const prereqDetail: PrereqDetail[] =
    unmetPrereqsDetail ??
    unmetPrereqs.map((id) => ({ id, kind: null, status: "missing" as const }));

  // Status-aware action visibility:
  //  - not installed (available/unavailable): Install only — Uninstall is moot.
  //  - fully installed: Uninstall only — Install would be a confusing no-op.
  //  - needs-action (partial/stopped/error/unknown): both — Install repairs/
  //    starts, Uninstall tears down.
  // Verify is always available (it never changes anything).
  //
  // Connector exception: a connector install means writing env vars, which
  // requires per-feature inputs the generic button can't supply — that path
  // lives in ConnectorFeatureEnvForm (rendered separately on the detail
  // page). So the generic Install is suppressed for connectors to avoid a
  // guaranteed no-op; Uninstall (clear env) + Verify still apply.
  const isConnector = feature.kind === "connector";
  const notInstalled = feature.status === "available" || feature.status === "unavailable";
  const fullyInstalled = feature.status === "installed";
  const showInstall = !fullyInstalled && !isConnector;
  const showUninstall = allowUninstall && !notInstalled;

  const runAction = (action: () => Promise<FeatureActionResult>) => {
    setErrorMessage(null);
    startTransition(async () => {
      try {
        const result = await action();
        setLastResult(result);
        router.refresh();
      } catch (e) {
        setErrorMessage(e instanceof Error ? e.message : String(e));
      }
    });
  };

  const handleInstalled = (result: FeatureActionResult) => {
    setLastResult(result);
    router.refresh();
  };

  return (
    <div className="space-y-3">
      <div className="flex flex-wrap gap-2">
        {showInstall && (
          <InstallConfirmDialog
            feature={feature}
            installInputs={installInputs}
            onInstalled={handleInstalled}
            trigger={
              <Button disabled={pending}>
                {pending ? <Loader2 className="h-3.5 w-3.5 animate-spin mr-1" /> : null}
                Install
              </Button>
            }
          />
        )}
        {showUninstall && (
          <Button
            variant="outline"
            onClick={() => runAction(() => api.uninstallFeature(feature.kind, feature.id))}
            disabled={pending}
          >
            Uninstall
          </Button>
        )}
        <Button
          variant="ghost"
          onClick={() => runAction(() => api.verifyFeature(feature.kind, feature.id))}
          disabled={pending}
        >
          Verify
        </Button>
      </div>

      {hasUnmetPrereqs && showInstall && (
        <div className="rounded-md border border-amber-500/40 bg-amber-500/10 p-3 text-sm">
          <div className="flex items-center gap-2 font-medium">
            <AlertTriangle className="h-4 w-4" />
            Prerequisites will be set up first
          </div>
          <p className="mt-1 text-xs text-muted-foreground">
            Install isn&apos;t blocked — clicking it walks you through a plan
            that installs these in order, then {feature.name}:
          </p>
          <ul className="mt-1.5 text-xs text-muted-foreground list-disc list-inside space-y-0.5">
            {prereqDetail.map((p) => (
              <li key={p.id}>
                <code className="font-mono">{p.id}</code> — {prereqLabel(p).split(" — ")[1]}
              </li>
            ))}
          </ul>
        </div>
      )}

      {errorMessage && (
        <div className="rounded-md border border-destructive/40 bg-destructive/10 p-3 text-sm">
          <div className="font-medium">Action failed</div>
          <pre className="text-xs mt-1 whitespace-pre-wrap break-all">{errorMessage}</pre>
        </div>
      )}

      {lastResult && <ActionResult result={lastResult} />}
    </div>
  );
}

function ActionResult({ result }: { result: FeatureActionResult }) {
  if (result.ok) {
    return (
      <div className="rounded-md border border-emerald-500/40 bg-emerald-500/10 p-3 text-sm space-y-1">
        <div className="flex items-center gap-2 font-medium">
          <CheckCircle2 className="h-4 w-4" />
          {result.noop ? "Already installed" : result.message ?? "Action succeeded"}
        </div>
        {result.command && (
          <div>
            <div className="text-xs text-muted-foreground mb-1">
              Run this command, then click Verify:
            </div>
            <pre className="rounded bg-background/60 p-2 text-xs overflow-x-auto">
              {result.command}
            </pre>
          </div>
        )}
        {result.wrote_keys && result.wrote_keys.length > 0 && (
          <div className="text-xs text-muted-foreground">
            Wrote keys: <code>{result.wrote_keys.join(", ")}</code>
          </div>
        )}
        {result.rejected && result.rejected.length > 0 && (
          <div className="text-xs text-muted-foreground">
            Rejected unknown keys: <code>{result.rejected.join(", ")}</code>
          </div>
        )}
        {result.cleared && result.cleared.length > 0 && (
          <div className="text-xs text-muted-foreground">
            Cleared: <code>{result.cleared.join(", ")}</code>
          </div>
        )}
        {result.kept_shared && result.kept_shared.length > 0 && (
          <div className="text-xs text-muted-foreground">
            Preserved (shared with other installed features):{" "}
            <code>{result.kept_shared.join(", ")}</code>
          </div>
        )}
      </div>
    );
  }
  return (
    <div className="rounded-md border border-destructive/40 bg-destructive/10 p-3 text-sm">
      <div className="font-medium">Action did not succeed</div>
      <pre className="text-xs mt-1 whitespace-pre-wrap break-all">
        {result.error ?? "(no error message)"}
      </pre>
      {result.unmet_prereqs && result.unmet_prereqs.length > 0 && (
        <div className="text-xs text-muted-foreground mt-2">
          Unmet prereqs: <code>{result.unmet_prereqs.join(", ")}</code>
        </div>
      )}
    </div>
  );
}
