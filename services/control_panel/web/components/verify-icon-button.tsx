"use client";

import { useEffect, useRef, useState } from "react";
import { CheckCircle2, Loader2, RefreshCw, XCircle } from "lucide-react";

import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";
import { api, type FeatureKind } from "@/lib/api";

type VerifyState = "idle" | "running" | "ok" | "fail";

type Props = {
  featureKind: FeatureKind;
  featureId: string;
  // `message` carries the failure text on a failed verify (null on success)
  // so the caller can surface it inline — the button only shows a tooltip.
  onVerified?: (ok: boolean, message: string | null) => void;
  size?: "default" | "sm";
};

// Verify re-runs the detection / health probe without changing state. We
// render it as a normal outline button (matching Install/Uninstall) with the
// icon morphing through states. Result chip lingers a few seconds then
// fades back so the row doesn't accumulate noise.
const RESULT_AUTO_CLEAR_MS = 6_000;

export function VerifyIconButton({ featureKind, featureId, onVerified, size = "default" }: Props) {
  const [state, setState] = useState<VerifyState>("idle");
  const [message, setMessage] = useState<string | null>(null);
  const clearTimer = useRef<ReturnType<typeof setTimeout> | null>(null);

  useEffect(() => {
    return () => {
      if (clearTimer.current) clearTimeout(clearTimer.current);
    };
  }, []);

  const onClick = async () => {
    if (state === "running") return;
    if (clearTimer.current) clearTimeout(clearTimer.current);
    setState("running");
    setMessage(null);
    try {
      const result = await api.verifyFeature(featureKind, featureId);
      const ok = !!result.ok;
      const failMsg = result.error ?? "Verification failed";
      setState(ok ? "ok" : "fail");
      setMessage(ok ? "Verified" : failMsg);
      onVerified?.(ok, ok ? null : failMsg);
    } catch (e) {
      const msg = e instanceof Error ? e.message : String(e);
      setState("fail");
      setMessage(msg);
      onVerified?.(false, msg);
    } finally {
      clearTimer.current = setTimeout(() => {
        setState("idle");
        setMessage(null);
      }, RESULT_AUTO_CLEAR_MS);
    }
  };

  const Icon =
    state === "running" ? Loader2 :
    state === "ok" ? CheckCircle2 :
    state === "fail" ? XCircle :
    RefreshCw;

  // Only colour the button after a result lands — idle/running keep the
  // standard outline look so it's visually consistent with the other action
  // buttons in the row. Coloured state is a temporary signal, not a permanent
  // pill.
  const tone =
    state === "ok" ? "text-emerald-700 dark:text-emerald-400 border-emerald-500/50 bg-emerald-500/10 hover:bg-emerald-500/15" :
    state === "fail" ? "text-destructive border-destructive/50 bg-destructive/10 hover:bg-destructive/15" :
    "";

  const label =
    state === "running" ? "Verifying…" :
    state === "ok" ? "Verified" :
    state === "fail" ? "Verify failed" :
    "Verify";

  return (
    <Button
      type="button"
      variant="outline"
      onClick={onClick}
      disabled={state === "running"}
      title={message ?? label}
      className={cn(
        "transition-colors",
        size === "sm" ? "h-8 w-8 p-0" : "h-9 w-9 p-0",
        tone,
      )}
      aria-label={label}
    >
      <Icon className={cn("h-3.5 w-3.5", state === "running" && "animate-spin")} />
    </Button>
  );
}
