"use client";

import { useEffect, useRef, useState } from "react";
import {
  AlertTriangle,
  Box,
  CheckCircle2,
  FileText,
  KeyRound,
  Loader2,
  Network,
  Plug,
  Terminal,
  XCircle,
} from "lucide-react";

import { Button } from "@/components/ui/button";
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
} from "@/lib/api";

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
    }, 200);
    return () => clearTimeout(t);
  }, [open]);

  // Auto-scroll the log to the bottom as new chunks arrive.
  useEffect(() => {
    if (phase !== "streaming" && phase !== "done") return;
    const el = logRef.current;
    if (el) el.scrollTop = el.scrollHeight;
  }, [log, phase]);

  // Fetch preview when entering the preview phase.
  useEffect(() => {
    if (!open || phase !== "preview") return;
    let cancelled = false;
    setPreviewing(true);
    api
      .previewFeature(feature.kind, feature.id, installInputs)
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
  }, [open, phase, feature.kind, feature.id, installInputs]);

  const blocked = (preview?.unmet_prereqs?.length ?? 0) > 0;
  const wouldBeNoop = preview?.would_be_noop === true;

  const onConfirm = async () => {
    try {
      const start = await api.installFeature(feature.kind, feature.id, installInputs);
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
            {phase === "preview" && `Install ${feature.name}`}
            {phase === "streaming" && `Installing ${feature.name}…`}
            {phase === "done" && (finalStatus === "done" ? "Install complete" : "Install failed")}
          </DialogTitle>
          <DialogDescription>
            {phase === "preview" &&
              "Review what this install will do before confirming. Nothing has changed yet."}
            {phase === "streaming" && "Live log from the install job. Closing the dialog does not abort the job."}
            {phase === "done" &&
              (finalStatus === "done"
                ? "All done. You can close this dialog."
                : "Install reported an error. Check the log below for details.")}
          </DialogDescription>
        </DialogHeader>

        {phase === "preview" && (
          <PreviewBody
            previewing={previewing}
            preview={preview}
            previewError={previewError}
            blocked={blocked}
            wouldBeNoop={wouldBeNoop}
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
                disabled={previewing || blocked || !preview?.ok}
              >
                {wouldBeNoop ? "Re-run anyway" : blocked ? "Install (blocked)" : "Confirm install"}
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
  blocked,
  wouldBeNoop,
}: {
  previewing: boolean;
  preview: FeaturePreview | null;
  previewError: string | null;
  blocked: boolean;
  wouldBeNoop: boolean;
}) {
  return (
    <div className="space-y-4">
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
          <SideEffectsList items={preview.side_effects ?? []} noop={wouldBeNoop} />
          <WarningsList items={preview.warnings ?? []} blocked={blocked} />
        </>
      )}
    </div>
  );
}

const LogViewer = ({
  ref,
  log,
  status,
  error,
}: {
  ref: React.Ref<HTMLPreElement>;
  log: string;
  status: "done" | "error" | null;
  error: string | null;
}) => (
  <div className="space-y-3">
    <pre
      ref={ref}
      className="rounded-md border bg-black/80 text-green-300 p-3 text-[11px] font-mono max-h-80 overflow-auto whitespace-pre-wrap break-all leading-relaxed"
    >
      {log || "(waiting for first chunk…)"}
    </pre>
    {status === "done" && (
      <div className="rounded-md border border-emerald-500/40 bg-emerald-500/10 p-3 text-sm flex items-start gap-2">
        <CheckCircle2 className="h-4 w-4 mt-0.5 shrink-0" />
        <span>Install finished successfully.</span>
      </div>
    )}
    {status === "error" && (
      <div className="rounded-md border border-destructive/40 bg-destructive/10 p-3 text-sm flex items-start gap-2">
        <XCircle className="h-4 w-4 mt-0.5 shrink-0" />
        <div className="space-y-1">
          <div className="font-medium">Install failed</div>
          {error && <pre className="text-xs whitespace-pre-wrap break-all">{error}</pre>}
        </div>
      </div>
    )}
  </div>
);

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

function WarningsList({ items, blocked }: { items: string[]; blocked: boolean }) {
  if (items.length === 0) return null;
  return (
    <div className="space-y-1.5">
      <div className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
        Heads up
      </div>
      <ul
        className={
          "rounded-md border p-3 space-y-1.5 text-sm " +
          (blocked
            ? "border-destructive/40 bg-destructive/10"
            : "border-amber-500/40 bg-amber-500/10")
        }
      >
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
