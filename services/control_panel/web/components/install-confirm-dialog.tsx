"use client";

import { useEffect, useRef, useState } from "react";
import {
  AlertTriangle,
  Box,
  CheckCircle2,
  FileText,
  KeyRound,
  ListOrdered,
  Loader2,
  Network,
  Plug,
  Terminal,
} from "lucide-react";

import { Button } from "@/components/ui/button";
import { LogViewer } from "@/components/log-viewer";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import {
  api,
  type Feature,
  type FeatureActionResult,
  type FeaturePreview,
  type FeatureSideEffect,
  type InstallStep,
  type McpScope,
} from "@/lib/api";
import { prereqHint } from "@/lib/prereq";

type Props = {
  feature: Feature;
  installInputs?: Record<string, unknown>;
  /** Trigger button — caller supplies it so it can be styled per context. */
  trigger: React.ReactNode;
  /** Called after the install job finishes. The job's final result dict is
   * forwarded so the parent can decide whether to refresh / show errors. */
  onInstalled?: (result: FeatureActionResult) => void;
};

type Phase = "preview" | "streaming" | "done";

const ICON_MAP: Record<string, React.ComponentType<{ className?: string }>> = {
  print_command: Terminal,
  run_command: Terminal,
  run_script: Terminal,
  container_image: Box,
  port_bind: Network,
  volume_use: Box,
  config_write: FileText,
  file_write: FileText,
  env_write: KeyRound,
  env_read: KeyRound,
  mcp_spawn: Plug,
  noop: CheckCircle2,
};

function sideEffectIcon(kind: string) {
  const Icon = ICON_MAP[kind] ?? FileText;
  return <Icon className="h-4 w-4 text-muted-foreground shrink-0 mt-0.5" />;
}

export function InstallConfirmDialog({ feature, installInputs, trigger, onInstalled }: Props) {
  const [open, setOpen] = useState(false);
  const [phase, setPhase] = useState<Phase>("preview");
  const [preview, setPreview] = useState<FeaturePreview | null>(null);
  const [previewError, setPreviewError] = useState<string | null>(null);
  const [previewing, setPreviewing] = useState(false);
  // Scope toggle: only meaningful for MCP. The handler defaults to workspace
  // server-side, but we mirror that here so the toggle starts on a real value.
  // Caller-supplied `installInputs.scope` wins (e.g. a future deep-link).
  const isMcp = feature.kind === "mcp";
  // A stopped container isn't a fresh install — `compose up` just brings the
  // existing container (image + volume) back. Same backend path, but the
  // user clicked "Start" and expects Start wording, not Install wording.
  const isStart = feature.kind === "container" && feature.status === "stopped";
  const verbDone = isStart ? "Started" : "Install complete";
  const verbFailed = isStart ? "Start failed" : "Install failed";
  const initialScope: McpScope =
    typeof installInputs?.scope === "string" && installInputs.scope === "global"
      ? "global"
      : "workspace";
  const [scope, setScope] = useState<McpScope>(initialScope);
  // "Other location" mode: backend scope stays "workspace" but we send a
  // `path` so the entry lands in <path>/.mcp.json instead of this project's.
  const [useCustom, setUseCustom] = useState(false);
  const [customPath, setCustomPath] = useState("");

  const [log, setLog] = useState<string>("");
  const [finalStatus, setFinalStatus] = useState<"done" | "error" | null>(null);
  const [finalResult, setFinalResult] = useState<FeatureActionResult | null>(null);
  const [finalError, setFinalError] = useState<string | null>(null);
  const sseRef = useRef<EventSource | null>(null);
  const logRef = useRef<HTMLPreElement | null>(null);

  // Reset everything when the dialog closes — but only after closing animation.
  useEffect(() => {
    if (open) return;
    sseRef.current?.close();
    sseRef.current = null;
    const t = setTimeout(() => {
      setPhase("preview");
      setPreview(null);
      setPreviewError(null);
      setLog("");
      setFinalStatus(null);
      setFinalResult(null);
      setFinalError(null);
      setUseCustom(false);
      setCustomPath("");
    }, 200);
    return () => clearTimeout(t);
  }, [open]);

  // Auto-scroll the log to the bottom as new chunks arrive.
  useEffect(() => {
    if (phase !== "streaming" && phase !== "done") return;
    const el = logRef.current;
    if (el) el.scrollTop = el.scrollHeight;
  }, [log, phase]);

  // Compose inputs for preview/install: caller's inputs + scope (MCP only).
  // For non-MCP kinds the handler ignores scope, so passing it is harmless,
  // but we omit it to keep the network payload honest.
  const trimmedPath = customPath.trim();
  const effectiveInputs = isMcp
    ? {
        ...(installInputs ?? {}),
        scope,
        ...(useCustom && trimmedPath ? { path: trimmedPath } : {}),
      }
    : installInputs;

  // Fetch preview when entering the preview phase OR when scope changes.
  useEffect(() => {
    if (!open || phase !== "preview") return;
    let cancelled = false;
    setPreviewing(true);
    setPreviewError(null);
    api
      .previewFeature(feature.kind, feature.id, effectiveInputs)
      .then((p) => {
        if (!cancelled) setPreview(p);
      })
      .catch((e) => {
        if (!cancelled) setPreviewError(e instanceof Error ? e.message : String(e));
      })
      .finally(() => {
        if (!cancelled) setPreviewing(false);
      });
    return () => {
      cancelled = true;
    };
    // effectiveInputs changes whenever scope changes, which is exactly when we want
    // to re-preview. We intentionally don't depend on installInputs/scope directly
    // because effectiveInputs already captures both.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [open, phase, feature.kind, feature.id, scope, useCustom, trimmedPath, installInputs]);

  // The cascade plan = prereqs (deps-first) + the target as the final step.
  // Everything but the last entry is an auto-pulled prerequisite. This is
  // informational now — never a block.
  const plan = preview?.install_plan ?? [];
  const prereqSteps = plan.length > 1 ? plan.slice(0, -1) : [];
  const wouldBeNoop = preview?.would_be_noop === true && prereqSteps.length === 0;

  const onConfirm = async () => {
    try {
      const start = await api.installFeature(feature.kind, feature.id, effectiveInputs);
      setPhase("streaming");
      // Open SSE stream against the job_id.
      const url = `/api/v1/features/install/${start.job_id}/stream`;
      const es = new EventSource(url);
      sseRef.current = es;
      es.addEventListener("chunk", (ev) => {
        try {
          const text = JSON.parse((ev as MessageEvent).data) as string;
          setLog((prev) => prev + text);
        } catch {
          // Ignore malformed frames; the next done frame still finalizes state.
        }
      });
      es.addEventListener("done", (ev) => {
        try {
          const payload = JSON.parse((ev as MessageEvent).data) as {
            status: "done" | "error";
            error: string | null;
            result: FeatureActionResult | null;
          };
          setFinalStatus(payload.status);
          setFinalError(payload.error);
          setFinalResult(payload.result);
          if (payload.result) onInstalled?.(payload.result);
        } catch (e) {
          setFinalStatus("error");
          setFinalError(e instanceof Error ? e.message : String(e));
        } finally {
          setPhase("done");
          es.close();
          sseRef.current = null;
        }
      });
      es.addEventListener("error", () => {
        // Browser fires `error` on normal stream close too — only treat it as
        // an actual failure if we haven't yet reached the `done` frame.
        if (phase === "streaming") {
          setFinalStatus("error");
          setFinalError("stream interrupted");
          setPhase("done");
          es.close();
          sseRef.current = null;
        }
      });
    } catch (e) {
      setPreviewError(e instanceof Error ? e.message : String(e));
    }
  };

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <div onClick={() => setOpen(true)} className="inline-flex">
        {trigger}
      </div>
      <DialogContent className="sm:max-w-2xl">
        <DialogHeader>
          <DialogTitle>
            {phase === "preview" && `${isStart ? "Start" : "Install"} ${feature.name}`}
            {phase === "streaming" && `${isStart ? "Starting" : "Installing"} ${feature.name}…`}
            {phase === "done" && (finalStatus === "done" ? verbDone : verbFailed)}
          </DialogTitle>
          <DialogDescription>
            {phase === "preview" &&
              (isStart
                ? "Review what starting this container will do before confirming. Nothing has changed yet."
                : "Review what this install will do before confirming. Nothing has changed yet.")}
            {phase === "streaming" &&
              `Live log from the ${isStart ? "start" : "install"} job. Closing the dialog does not abort the job.`}
            {phase === "done" &&
              (finalStatus === "done"
                ? "All done. You can close this dialog."
                : `${isStart ? "Start" : "Install"} reported an error. Check the log below for details.`)}
          </DialogDescription>
        </DialogHeader>

        {phase === "preview" && (
          <PreviewBody
            previewing={previewing}
            preview={preview}
            previewError={previewError}
            prereqSteps={prereqSteps}
            targetName={feature.name}
            wouldBeNoop={wouldBeNoop}
            isMcp={isMcp}
            scope={scope}
            onScopeChange={setScope}
            useCustom={useCustom}
            onUseCustomChange={setUseCustom}
            customPath={customPath}
            onCustomPathChange={setCustomPath}
            feature={feature}
          />
        )}

        {(phase === "streaming" || phase === "done") && (
          <LogViewer ref={logRef} log={log} status={finalStatus} error={finalError} />
        )}

        <DialogFooter>
          {phase === "preview" && (
            <>
              <Button variant="outline" onClick={() => setOpen(false)}>
                Cancel
              </Button>
              <Button
                onClick={onConfirm}
                disabled={previewing || !preview?.ok || (useCustom && !trimmedPath)}
              >
                {wouldBeNoop
                  ? "Re-run anyway"
                  : prereqSteps.length > 0
                    ? `Confirm — set up ${prereqSteps.length} prereq${prereqSteps.length > 1 ? "s" : ""} + ${feature.name}`
                    : isStart
                      ? "Confirm start"
                      : "Confirm install"}
              </Button>
            </>
          )}
          {phase === "streaming" && (
            <Button variant="outline" onClick={() => setOpen(false)}>
              Hide (job keeps running)
            </Button>
          )}
          {phase === "done" && (
            <Button onClick={() => setOpen(false)}>Close</Button>
          )}
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}

function PreviewBody({
  previewing,
  preview,
  previewError,
  prereqSteps,
  targetName,
  wouldBeNoop,
  isMcp,
  scope,
  onScopeChange,
  useCustom,
  onUseCustomChange,
  customPath,
  onCustomPathChange,
  feature,
}: {
  previewing: boolean;
  preview: FeaturePreview | null;
  previewError: string | null;
  prereqSteps: InstallStep[];
  targetName: string;
  wouldBeNoop: boolean;
  isMcp: boolean;
  scope: McpScope;
  onScopeChange: (s: McpScope) => void;
  useCustom: boolean;
  onUseCustomChange: (v: boolean) => void;
  customPath: string;
  onCustomPathChange: (v: string) => void;
  feature: Feature;
}) {
  return (
    <div className="space-y-4">
      {isMcp && (
        <ScopeToggle
          scope={scope}
          onChange={onScopeChange}
          useCustom={useCustom}
          onUseCustomChange={onUseCustomChange}
          customPath={customPath}
          onCustomPathChange={onCustomPathChange}
          feature={feature}
        />
      )}

      {previewing && (
        <div className="flex items-center gap-2 text-sm text-muted-foreground py-4">
          <Loader2 className="h-4 w-4 animate-spin" /> Generating preview…
        </div>
      )}

      {previewError && (
        <div className="rounded-md border border-destructive/40 bg-destructive/10 p-3 text-sm">
          <div className="font-medium">Preview failed</div>
          <pre className="text-xs mt-1 whitespace-pre-wrap break-all">{previewError}</pre>
        </div>
      )}

      {preview && !preview.ok && (
        <div className="rounded-md border border-destructive/40 bg-destructive/10 p-3 text-sm">
          <div className="font-medium">Cannot preview</div>
          <pre className="text-xs mt-1 whitespace-pre-wrap break-all">
            {preview.error ?? "(no error)"}
          </pre>
        </div>
      )}

      {preview?.ok && (
        <>
          {prereqSteps.length > 0 && (
            <InstallPlanList steps={prereqSteps} targetName={targetName} />
          )}
          <SideEffectsList items={preview.side_effects ?? []} noop={wouldBeNoop} />
          <WarningsList items={preview.warnings ?? []} />
        </>
      )}
    </div>
  );
}

function ScopeToggle({
  scope,
  onChange,
  useCustom,
  onUseCustomChange,
  customPath,
  onCustomPathChange,
  feature,
}: {
  scope: McpScope;
  onChange: (s: McpScope) => void;
  useCustom: boolean;
  onUseCustomChange: (v: boolean) => void;
  customPath: string;
  onCustomPathChange: (v: string) => void;
  feature: Feature;
}) {
  const installedScopes = Array.isArray(feature.detail?.installed_scopes)
    ? (feature.detail.installed_scopes as string[])
    : [];
  const wsName =
    (typeof feature.detail?.workspace_name === "string" &&
      feature.detail.workspace_name) ||
    "Workspace";
  const knownLocations = Array.isArray(feature.detail?.known_locations)
    ? (feature.detail.known_locations as string[])
    : [];

  // Three modes: this project's workspace, machine-global, or a custom dir.
  // Custom maps to backend scope "workspace" + a `path`.
  const mode: "workspace" | "global" | "custom" = useCustom
    ? "custom"
    : scope;
  const here = !useCustom && installedScopes.includes(scope);

  return (
    <div className="rounded-md border bg-card/40 p-3 space-y-2">
      <div className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
        Install scope
      </div>
      <div className="flex gap-2">
        <ScopePill
          active={mode === "workspace"}
          installed={installedScopes.includes("workspace")}
          onClick={() => {
            onUseCustomChange(false);
            onChange("workspace");
          }}
          label={wsName}
          sub="./.mcp.json"
        />
        <ScopePill
          active={mode === "global"}
          installed={installedScopes.includes("global")}
          onClick={() => {
            onUseCustomChange(false);
            onChange("global");
          }}
          label="Global"
          sub="~/.claude.json"
        />
        <ScopePill
          active={mode === "custom"}
          installed={false}
          onClick={() => {
            onChange("workspace");
            onUseCustomChange(true);
          }}
          label="Other location…"
          sub="<dir>/.mcp.json"
        />
      </div>

      {mode === "custom" ? (
        <div className="space-y-2 pt-1">
          <input
            type="text"
            value={customPath}
            onChange={(e) => onCustomPathChange(e.target.value)}
            placeholder="/abs/path/to/another/project"
            spellCheck={false}
            className="w-full rounded-md border bg-background px-2.5 py-1.5 text-sm font-mono outline-none transition-colors focus:border-primary focus:ring-1 focus:ring-primary/40"
          />
          {knownLocations.length > 0 && (
            <div className="space-y-1">
              <div className="text-[10px] uppercase tracking-wider text-muted-foreground">
                Used before
              </div>
              <div className="flex flex-wrap gap-1.5">
                {knownLocations.map((loc) => (
                  <button
                    key={loc}
                    type="button"
                    onClick={() => onCustomPathChange(loc)}
                    className={
                      "rounded border px-2 py-1 text-[11px] font-mono transition-colors " +
                      (customPath === loc
                        ? "border-primary bg-primary/10"
                        : "border-input bg-background hover:bg-accent")
                    }
                  >
                    {loc}
                  </button>
                ))}
              </div>
            </div>
          )}
          <p className="text-xs text-muted-foreground leading-relaxed">
            Writes <code className="font-mono">{customPath.trim() || "<dir>"}/.mcp.json</code>.
            The directory must already exist. Its status won&apos;t show on this
            card (detection scans only this project + global), but the path is
            remembered for next time.
          </p>
        </div>
      ) : (
        <p className="text-xs text-muted-foreground leading-relaxed">
          {scope === "workspace"
            ? `Only ${wsName} sees this MCP. Best for project-specific servers (cwd, env, requires_services).`
            : "Every Claude Code session on this machine sees this MCP. Best for project-agnostic tools (e.g. public-API wrappers). `cwd` is dropped on install."}
          {here && (
            <>
              {" "}
              <span className="font-medium text-foreground/80">Currently installed here.</span>
            </>
          )}
        </p>
      )}
    </div>
  );
}

function ScopePill({
  active,
  installed,
  onClick,
  label,
  sub,
}: {
  active: boolean;
  installed: boolean;
  onClick: () => void;
  label: string;
  sub: string;
}) {
  return (
    <button
      type="button"
      onClick={onClick}
      className={
        "flex-1 rounded-md border px-3 py-2 text-left transition-colors " +
        (active
          ? "border-primary bg-primary/10"
          : "border-input bg-background hover:bg-accent")
      }
    >
      <div className="flex items-center gap-2 text-sm font-medium">
        {label}
        {installed && (
          <span className="text-[10px] uppercase tracking-wider rounded bg-emerald-500/15 text-emerald-700 dark:text-emerald-400 px-1.5 py-0.5">
            installed
          </span>
        )}
      </div>
      <div className="text-[11px] font-mono text-muted-foreground mt-0.5">{sub}</div>
    </button>
  );
}


function SideEffectsList({ items, noop }: { items: FeatureSideEffect[]; noop: boolean }) {
  if (noop) {
    return (
      <div className="rounded-md border border-emerald-500/40 bg-emerald-500/10 p-3 text-sm flex items-start gap-2">
        <CheckCircle2 className="h-4 w-4 mt-0.5 shrink-0" />
        <div>
          <div className="font-medium">No changes needed</div>
          <div className="text-xs text-muted-foreground mt-0.5">
            Confirming would be a no-op — this feature is already in the desired state.
          </div>
        </div>
      </div>
    );
  }
  if (items.length === 0) {
    return (
      <div className="text-sm text-muted-foreground italic">
        No side effects reported.
      </div>
    );
  }
  return (
    <div className="space-y-1.5">
      <div className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
        What will happen
      </div>
      <ul className="rounded-md border bg-card/40 divide-y">
        {items.map((s, i) => (
          <li key={i} className="flex items-start gap-3 px-3 py-2 text-sm">
            {sideEffectIcon(s.kind)}
            <div className="min-w-0 flex-1">
              <div className="font-medium">{s.summary}</div>
              <div className="text-xs text-muted-foreground font-mono break-all mt-0.5">
                {s.detail}
              </div>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}

function WarningsList({ items }: { items: string[] }) {
  if (items.length === 0) return null;
  return (
    <div className="space-y-1.5">
      <div className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
        Heads up
      </div>
      <ul className="rounded-md border border-amber-500/40 bg-amber-500/10 p-3 space-y-1.5 text-sm">
        {items.map((w, i) => (
          <li key={i} className="flex items-start gap-2">
            <AlertTriangle className="h-3.5 w-3.5 mt-0.5 shrink-0" />
            <span>{w}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}

function InstallPlanList({
  steps,
  targetName,
}: {
  steps: InstallStep[];
  targetName: string;
}) {
  return (
    <div className="space-y-1.5">
      <div className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
        Install plan
      </div>
      <div className="rounded-md border border-indigo-500/40 bg-indigo-500/10 p-3 text-sm space-y-2">
        <div className="flex items-start gap-2">
          <ListOrdered className="h-4 w-4 mt-0.5 shrink-0" />
          <span>
            {targetName} needs {steps.length} prerequisite
            {steps.length > 1 ? "s" : ""}. They&apos;ll be set up first, in
            order, then {targetName} — all in one run with live logs.
          </span>
        </div>
        <ol className="list-decimal list-inside space-y-1 text-xs">
          {steps.map((s) => (
            <li key={s.id}>
              <code className="font-mono">{s.id}</code>{" "}
              <span className="text-muted-foreground">— {prereqHint(s.status)}</span>
            </li>
          ))}
          <li>
            <code className="font-mono">{targetName}</code>{" "}
            <span className="text-muted-foreground">— installed last</span>
          </li>
        </ol>
      </div>
    </div>
  );
}
