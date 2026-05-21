"use client";

import { useRouter } from "next/navigation";
import { useState, useTransition } from "react";
import { CheckCircle2, AlertTriangle, Loader2 } from "lucide-react";

import { Button } from "@/components/ui/button";
import { ConfirmButton } from "@/components/confirm-button";
import { InstallConfirmDialog } from "@/components/install-confirm-dialog";
import { VerifyIconButton } from "@/components/verify-icon-button";
import { ContainerLogsDialog } from "@/components/container-logs-dialog";
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
  const isMcp = feature.kind === "mcp";
  // MCP scope wrinkle: an MCP feature can be installed in two scopes.
  // We always show Install (you may want to add it to the *other* scope)
  // and we offer per-scope Uninstall buttons when both hold the entry.
  const installedScopes: string[] =
    isMcp && Array.isArray(feature.detail?.installed_scopes)
      ? (feature.detail.installed_scopes as string[])
      : [];
  const installedInBothScopes = isMcp && installedScopes.length === 2;
  // A running container (up — health passing OR failing) has logs worth
  // tailing. stopped/available/unavailable have nothing to follow.
  const canShowLogs =
    feature.kind === "container" &&
    (feature.status === "installed" || feature.status === "partial");
  const notInstalled = feature.status === "available" || feature.status === "unavailable";
  const fullyInstalled = feature.status === "installed";
  // For MCP, keep Install visible even when "fully installed" so the user can
  // add the entry to the *other* scope. For non-MCP that'd be a no-op.
  const showInstall = (!fullyInstalled || isMcp) && !isConnector;
  const showUninstall = allowUninstall && !notInstalled;

  const runAction = (action: () => Promise<FeatureActionResult>) => {
    // De-stack: any new action wipes the prior log boxes (error + result)
    // before it starts, so old verify failures and old success messages
    // don't pile up under fresh clicks.
    setErrorMessage(null);
    setLastResult(null);
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

  // The outer wrapper uses `display: contents` so the button-row and the
  // logs panel become direct siblings in whatever layout the parent
  // imposes. On the recipe page action row (a flex-wrap), this lets the
  // logs (basis-full) wrap to a new full-width line BELOW the buttons —
  // left-aligned with Run Recipe instead of crammed under the right side
  // of the row. In block-flow parents (components page, quick-look) the
  // logs simply stack below the buttons as normal block children.
  const hasLogs =
    (hasUnmetPrereqs && showInstall) || !!errorMessage || !!lastResult;

  return (
    <div className="contents">
      <div className="flex flex-wrap gap-2">
        {showInstall && (
          <InstallConfirmDialog
            feature={feature}
            installInputs={installInputs}
            onInstalled={handleInstalled}
            trigger={
              <Button size="sm" disabled={pending}>
                {pending ? <Loader2 className="h-3.5 w-3.5 animate-spin mr-1" /> : null}
                {feature.kind === "container" && feature.status === "stopped" ? "Start" : "Install"}
              </Button>
            }
          />
        )}
        {showUninstall && !installedInBothScopes && (
          <ConfirmButton
            title={`Uninstall ${feature.name}?`}
            description="This removes the component from your setup. You can reinstall it later from the same page."
            confirmLabel="Uninstall"
            disabled={pending}
            onConfirm={() => runAction(() => api.uninstallFeature(feature.kind, feature.id))}
          >
            Uninstall
            {isMcp && installedScopes.length === 1 && (
              <span className="ml-1.5 text-[10px] uppercase tracking-wider text-muted-foreground">
                ({installedScopes[0]})
              </span>
            )}
          </ConfirmButton>
        )}
        {showUninstall && installedInBothScopes && (
          <>
            <ConfirmButton
              title={`Uninstall ${feature.name} (workspace)?`}
              description="Removes only the workspace-scoped entry. The global entry stays in place."
              confirmLabel="Uninstall"
              disabled={pending}
              onConfirm={() =>
                runAction(() =>
                  api.uninstallFeature(feature.kind, feature.id, { scope: "workspace" }),
                )
              }
            >
              Uninstall (workspace)
            </ConfirmButton>
            <ConfirmButton
              title={`Uninstall ${feature.name} (global)?`}
              description="Removes only the global entry. The workspace entry stays in place."
              confirmLabel="Uninstall"
              disabled={pending}
              onConfirm={() =>
                runAction(() =>
                  api.uninstallFeature(feature.kind, feature.id, { scope: "global" }),
                )
              }
            >
              Uninstall (global)
            </ConfirmButton>
          </>
        )}
        {canShowLogs && <ContainerLogsDialog feature={feature} size="sm" />}
        <VerifyIconButton
          featureKind={feature.kind}
          featureId={feature.id}
          size="sm"
          onVerified={(ok, message) => {
            // Same inline area as Install/Uninstall results: success shows
            // a green ActionResult box, failure the red error block. Each
            // branch clears the other so logs never stack.
            if (ok) {
              setErrorMessage(null);
              setLastResult({ ok: true, message: "Verification passed" });
            } else {
              setLastResult(null);
              setErrorMessage(message ?? "Verification failed");
            }
            router.refresh();
          }}
        />
      </div>

      {hasLogs && (
        /* basis-full makes this panel claim its own line and span full
         * width when the parent is a flex-wrap (the recipe page action
         * row) — so logs sit under Run Recipe on the left, not crammed
         * under the right side. In block-flow parents the basis-full is
         * a harmless no-op. */
        <div className="basis-full w-full mt-2 space-y-3">
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
      )}
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
