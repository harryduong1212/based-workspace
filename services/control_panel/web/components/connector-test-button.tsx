"use client";

import { useState } from "react";
import { Loader2, AlertTriangle, CheckCircle2, XCircle } from "lucide-react";

import { Button } from "@/components/ui/button";
import { api, type ConnectorTestResult } from "@/lib/api";

type Outcome =
  | { kind: "idle" }
  | { kind: "loading" }
  | { kind: "result"; data: ConnectorTestResult }
  | { kind: "error"; message: string };

export function ConnectorTestButton({ connectorId }: { connectorId: string }) {
  const [outcome, setOutcome] = useState<Outcome>({ kind: "idle" });

  const run = async () => {
    setOutcome({ kind: "loading" });
    try {
      const data = await api.testConnector(connectorId);
      setOutcome({ kind: "result", data });
    } catch (e) {
      setOutcome({ kind: "error", message: e instanceof Error ? e.message : String(e) });
    }
  };

  return (
    <div className="space-y-3">
      <Button variant="secondary" className="w-full" onClick={run} disabled={outcome.kind === "loading"}>
        {outcome.kind === "loading" ? (
          <>
            <Loader2 className="animate-spin" /> Testing…
          </>
        ) : (
          "Test"
        )}
      </Button>
      <TestOutcome outcome={outcome} />
    </div>
  );
}

function TestOutcome({ outcome }: { outcome: Outcome }) {
  if (outcome.kind === "idle" || outcome.kind === "loading") return null;
  if (outcome.kind === "error") {
    return (
      <Banner variant="error" icon={<AlertTriangle className="h-4 w-4" />}>
        Request failed: {outcome.message}
      </Banner>
    );
  }
  const { env_check, probe } = outcome.data;
  if (!env_check.all_present) {
    return (
      <Banner variant="error" icon={<XCircle className="h-4 w-4" />}>
        <div className="font-medium">Missing env vars</div>
        <div className="text-xs font-mono mt-1">{env_check.missing.join(", ")}</div>
        <div className="text-xs mt-2 opacity-80">Click <em>Set env</em> and fill them in.</div>
      </Banner>
    );
  }
  if (probe === null) {
    return (
      <Banner variant="success" icon={<CheckCircle2 className="h-4 w-4" />}>
        <div className="font-medium">All required env vars are set.</div>
        <div className="text-xs mt-1 opacity-80">
          No live probe is registered for this connector — the live API check is deferred.
        </div>
      </Banner>
    );
  }
  if (probe.ok) {
    return (
      <Banner variant="success" icon={<CheckCircle2 className="h-4 w-4" />}>
        <div className="font-medium">Live connection succeeded.</div>
        <div className="text-xs mt-1">{probe.message}</div>
      </Banner>
    );
  }
  return (
    <Banner variant="error" icon={<XCircle className="h-4 w-4" />}>
      <div className="font-medium">Live connection failed.</div>
      <div className="text-xs mt-1 break-words">{probe.message}</div>
      <div className="text-xs mt-2 opacity-80">
        Env vars are present but the credentials didn&apos;t authenticate. Re-check the value and re-test.
      </div>
    </Banner>
  );
}

function Banner({
  variant,
  icon,
  children,
}: {
  variant: "success" | "error";
  icon: React.ReactNode;
  children: React.ReactNode;
}) {
  const colors =
    variant === "success"
      ? "border-emerald-300 bg-emerald-50 text-emerald-800 dark:border-emerald-700 dark:bg-emerald-500/10 dark:text-emerald-200"
      : "border-rose-300 bg-rose-50 text-rose-800 dark:border-rose-700 dark:bg-rose-500/10 dark:text-rose-200";
  return (
    <div className={`rounded-md border p-3 text-sm flex items-start gap-2 ${colors}`}>
      <span className="mt-0.5 shrink-0">{icon}</span>
      <div className="min-w-0">{children}</div>
    </div>
  );
}
