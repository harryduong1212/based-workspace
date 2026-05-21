import { AlertTriangle, Info } from "lucide-react";

import { cn } from "@/lib/utils";
import type { FeatureStatus } from "@/lib/api";

// Only states worth surfacing get a banner. `installed` and `available`
// are "clean" — the status badge already says it plainly, so a banner
// there would just be noise. The rest carry an actionable hint.
const NOTICE: Partial<
  Record<FeatureStatus, { tone: "warn" | "info"; text: string }>
> = {
  partial: {
    tone: "warn",
    text: "Installed, but the verification check is failing — try Verify, or reinstall.",
  },
  error: {
    tone: "warn",
    text: "In an error state — an uninstall followed by a reinstall usually clears it.",
  },
  stopped: {
    tone: "info",
    text: "Installed but not running — Start it to bring it back up.",
  },
  unavailable: {
    tone: "info",
    text: "Not available on this system — the install hint may be missing for your platform.",
  },
  unknown: {
    tone: "info",
    text: "Status couldn't be determined — try Verify.",
  },
};

// A banner shown above the install-state action buttons ONLY when the
// status is noteworthy. Renders nothing for clean states.
export function InstallStateNotice({ status }: { status: FeatureStatus }) {
  const notice = NOTICE[status];
  if (!notice) return null;
  const Icon = notice.tone === "warn" ? AlertTriangle : Info;
  return (
    <div
      className={cn(
        "mb-3 flex items-start gap-2 rounded-md border px-3 py-2 text-xs",
        notice.tone === "warn"
          ? "border-amber-500/40 bg-amber-500/10 text-amber-700 dark:text-amber-300"
          : "border-border bg-muted/40 text-muted-foreground",
      )}
    >
      <Icon className="mt-0.5 h-3.5 w-3.5 shrink-0" />
      <span>{notice.text}</span>
    </div>
  );
}
