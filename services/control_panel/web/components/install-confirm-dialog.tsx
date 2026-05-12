"use client";

import { useEffect, useState } from "react";
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
  /** Called after install resolves (success OR failure). UI refresh is the parent's job. */
  onInstalled?: (result: FeatureActionResult) => void;
};

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
  const [preview, setPreview] = useState<FeaturePreview | null>(null);
  const [previewError, setPreviewError] = useState<string | null>(null);
  const [previewing, setPreviewing] = useState(false);
  const [installing, setInstalling] = useState(false);

  useEffect(() => {
    if (!open) {
      // Reset state when the dialog closes so reopening always re-fetches.
      setPreview(null);
      setPreviewError(null);
      return;
    }
    let cancelled = false;
    setPreviewing(true);
    api
      .previewFeature(feature.kind, feature.id, installInputs)
      .then((p) => {
        if (cancelled) return;
        setPreview(p);
      })
      .catch((e) => {
        if (cancelled) return;
        setPreviewError(e instanceof Error ? e.message : String(e));
      })
      .finally(() => {
        if (cancelled) return;
        setPreviewing(false);
      });
    return () => {
      cancelled = true;
    };
  }, [open, feature.kind, feature.id, installInputs]);

  const blocked = (preview?.unmet_prereqs?.length ?? 0) > 0;
  const wouldBeNoop = preview?.would_be_noop === true;

  const onConfirm = async () => {
    setInstalling(true);
    try {
      const r = await api.installFeature(feature.kind, feature.id, installInputs);
      onInstalled?.(r);
      setOpen(false);
    } catch (e) {
      setPreviewError(e instanceof Error ? e.message : String(e));
    } finally {
      setInstalling(false);
    }
  };

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <div onClick={() => setOpen(true)} className="inline-flex">
        {trigger}
      </div>
      <DialogContent className="sm:max-w-xl">
        <DialogHeader>
          <DialogTitle>Install {feature.name}</DialogTitle>
          <DialogDescription>
            Review what this install will do before confirming. Nothing has changed yet.
          </DialogDescription>
        </DialogHeader>

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

        <DialogFooter>
          <Button variant="outline" onClick={() => setOpen(false)} disabled={installing}>
            Cancel
          </Button>
          <Button
            onClick={onConfirm}
            disabled={installing || previewing || blocked || !preview?.ok}
          >
            {installing ? <Loader2 className="h-3.5 w-3.5 animate-spin mr-1" /> : null}
            {wouldBeNoop ? "Re-run anyway" : blocked ? "Install (blocked)" : "Confirm install"}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
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
