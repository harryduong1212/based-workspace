"use client";

import { useRouter } from "next/navigation";
import { useState, useTransition } from "react";
import { Loader2, Pencil } from "lucide-react";
import { toast } from "sonner";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Sheet,
  SheetClose,
  SheetContent,
  SheetDescription,
  SheetFooter,
  SheetHeader,
  SheetTitle,
  SheetTrigger,
} from "@/components/ui/sheet";
import { api, type EnvVarStatus } from "@/lib/api";

type Props = {
  connectorId: string;
  connectorName: string;
  requiresEnv: EnvVarStatus[];
  safeToWrite: boolean;
  host: string;
};

export function ConnectorEnvSheet({ connectorId, connectorName, requiresEnv, safeToWrite, host }: Props) {
  const router = useRouter();
  const [open, setOpen] = useState(false);
  const [values, setValues] = useState<Record<string, string>>({});
  const [submitting, setSubmitting] = useState(false);
  const [, startTransition] = useTransition();

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!safeToWrite) return;
    setSubmitting(true);
    try {
      const result = await api.saveConnectorEnv(connectorId, values);
      if (result.saved_keys.length === 0) {
        toast.info(result.message);
      } else {
        toast.success(result.message, { description: result.saved_keys.join(", ") });
        setValues({});
        setOpen(false);
        // Refresh the server component so env-status pills update.
        startTransition(() => router.refresh());
      }
    } catch (err) {
      toast.error("Save failed", {
        description: err instanceof Error ? err.message : String(err),
      });
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <Sheet open={open} onOpenChange={setOpen}>
      <SheetTrigger asChild>
        <Button className="w-full" variant="default">
          <Pencil /> Set env
        </Button>
      </SheetTrigger>
      <SheetContent className="flex flex-col gap-5 overflow-y-auto">
        <SheetHeader>
          <SheetTitle>Environment for {connectorName}</SheetTitle>
          <SheetDescription>
            {requiresEnv.length} variable{requiresEnv.length === 1 ? "" : "s"} declared. Empty fields are skipped — they don&apos;t clear existing values.
          </SheetDescription>
        </SheetHeader>

        {!safeToWrite && (
          <div className="rounded-md border border-rose-300 bg-rose-50 dark:border-rose-700 dark:bg-rose-500/10 p-3 text-sm text-rose-800 dark:text-rose-200">
            <strong>Disabled:</strong> the Control Panel is bound to <code className="font-mono">{host}</code>, not <code className="font-mono">127.0.0.1</code>. Editing env vars is local-only by policy.
          </div>
        )}

        <form onSubmit={onSubmit} className="flex-1 space-y-4">
          {requiresEnv.map((v) => (
            <div key={v.name} className="space-y-1.5">
              <div className="flex items-center justify-between gap-2">
                <Label htmlFor={`env__${v.name}`} className="font-mono text-sm">
                  {v.name}
                </Label>
                <span
                  className={`inline-flex items-center gap-1 px-2 py-0.5 text-[11px] rounded-full font-medium ${
                    v.present
                      ? "bg-emerald-500/15 text-emerald-700 dark:text-emerald-300"
                      : "bg-rose-500/15 text-rose-700 dark:text-rose-300"
                  }`}
                >
                  <span className={`h-1.5 w-1.5 rounded-full ${v.present ? "bg-emerald-500" : "bg-rose-500"}`} />
                  {v.present ? "set" : "missing"}
                </span>
              </div>
              <Input
                id={`env__${v.name}`}
                name={v.name}
                type={isSecret(v.name) ? "password" : "text"}
                autoComplete="off"
                spellCheck={false}
                disabled={!safeToWrite}
                placeholder={v.present ? "•••••• (currently set — leave blank to keep)" : "enter value…"}
                className="font-mono"
                value={values[v.name] ?? ""}
                onChange={(e) => setValues((s) => ({ ...s, [v.name]: e.target.value }))}
              />
            </div>
          ))}
          <SheetFooter className="pt-2">
            <SheetClose asChild>
              <Button type="button" variant="ghost">
                Cancel
              </Button>
            </SheetClose>
            <Button type="submit" disabled={!safeToWrite || submitting}>
              {submitting ? (
                <>
                  <Loader2 className="animate-spin" /> Saving…
                </>
              ) : (
                "Save"
              )}
            </Button>
          </SheetFooter>
        </form>
      </SheetContent>
    </Sheet>
  );
}

function isSecret(name: string): boolean {
  const upper = name.toUpperCase();
  return upper.includes("PASSWORD") || upper.includes("TOKEN") || upper.includes("SECRET") || upper.includes("KEY");
}
