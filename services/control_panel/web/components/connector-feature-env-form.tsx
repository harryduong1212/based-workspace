"use client";

import { useRouter } from "next/navigation";
import { useState, useTransition } from "react";
import { CheckCircle2, Loader2 } from "lucide-react";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { api, type Feature, type FeatureActionResult } from "@/lib/api";

/**
 * Per-connector env input form. Reads requires_env / env_present /
 * env_missing from feature.detail; renders a labelled password input for
 * each var, with "Already set" indicator when the value is already in .env
 * (the actual secret is never sent to the browser).
 *
 * On submit, posts only the keys the user filled in — empty values are
 * dropped client-side (backend also drops them). Secrets travel one-way:
 * input → POST body → env_writer → .env. Never echoed back.
 */
export function ConnectorFeatureEnvForm({ feature }: { feature: Feature }) {
  const router = useRouter();
  const [pending, startTransition] = useTransition();
  const [values, setValues] = useState<Record<string, string>>({});
  const [result, setResult] = useState<FeatureActionResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  const requiresEnv = (feature.detail.requires_env as string[] | undefined) ?? [];
  const envPresent = new Set((feature.detail.env_present as string[] | undefined) ?? []);

  if (requiresEnv.length === 0) {
    return (
      <p className="text-sm text-muted-foreground">
        This connector declares no required env vars — it is considered installed
        as soon as its definition file is present.
      </p>
    );
  }

  const onSubmit = () => {
    const filled: Record<string, string> = {};
    for (const [k, v] of Object.entries(values)) {
      if (v && v.trim() !== "") filled[k] = v;
    }
    setError(null);
    startTransition(async () => {
      try {
        const r = await api.installFeature(feature.kind, feature.id, { env: filled });
        setResult(r);
        if (r.ok) setValues({});
        router.refresh();
      } catch (e) {
        setError(e instanceof Error ? e.message : String(e));
      }
    });
  };

  return (
    <div className="space-y-3">
      <div className="space-y-3">
        {requiresEnv.map((key) => {
          const isSet = envPresent.has(key);
          return (
            <div key={key} className="space-y-1.5">
              <div className="flex items-center justify-between">
                <Label htmlFor={`env-${key}`} className="font-mono text-xs">
                  {key}
                </Label>
                {isSet ? (
                  <span className="inline-flex items-center gap-1 text-[11px] text-emerald-500">
                    <CheckCircle2 className="h-3 w-3" />
                    already set
                  </span>
                ) : (
                  <span className="text-[11px] text-muted-foreground">not set</span>
                )}
              </div>
              <Input
                id={`env-${key}`}
                type="password"
                autoComplete="off"
                placeholder={isSet ? "(leave blank to keep current)" : "paste value"}
                value={values[key] ?? ""}
                onChange={(e) => setValues({ ...values, [key]: e.target.value })}
                disabled={pending}
              />
            </div>
          );
        })}
      </div>

      <div className="flex items-center gap-2">
        <Button onClick={onSubmit} disabled={pending || Object.values(values).every((v) => !v)}>
          {pending ? <Loader2 className="h-3.5 w-3.5 animate-spin mr-1" /> : null}
          Save to .env
        </Button>
        <p className="text-[11px] text-muted-foreground">
          Values are written to <code>.env</code> via env_writer and are never echoed back.
        </p>
      </div>

      {error && (
        <div className="rounded-md border border-destructive/40 bg-destructive/10 p-3 text-sm">
          <pre className="text-xs whitespace-pre-wrap break-all">{error}</pre>
        </div>
      )}

      {result && result.ok && (
        <div className="rounded-md border border-emerald-500/40 bg-emerald-500/10 p-3 text-sm">
          <div className="font-medium flex items-center gap-2">
            <CheckCircle2 className="h-4 w-4" />
            Saved
          </div>
          {result.wrote_keys && result.wrote_keys.length > 0 && (
            <div className="text-xs text-muted-foreground mt-1">
              Wrote: <code>{result.wrote_keys.join(", ")}</code>
            </div>
          )}
          {result.rejected && result.rejected.length > 0 && (
            <div className="text-xs text-muted-foreground mt-1">
              Rejected unknown keys: <code>{result.rejected.join(", ")}</code>
            </div>
          )}
        </div>
      )}

      {result && !result.ok && (
        <div className="rounded-md border border-destructive/40 bg-destructive/10 p-3 text-sm">
          <div className="font-medium">Save failed</div>
          <pre className="text-xs mt-1 whitespace-pre-wrap break-all">{result.error}</pre>
        </div>
      )}
    </div>
  );
}
