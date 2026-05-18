import { Badge } from "@/components/ui/badge";
import type { FeatureStatus } from "@/lib/api";

const VARIANT: Record<FeatureStatus, "success" | "warn" | "destructive" | "secondary" | "info"> = {
  installed: "success",
  partial: "warn",
  stopped: "info",
  available: "secondary",
  unavailable: "secondary",
  error: "destructive",
  unknown: "info",
};

const LABEL: Record<FeatureStatus, string> = {
  installed: "installed",
  partial: "partial",
  stopped: "stopped",
  available: "not installed",
  unavailable: "unavailable",
  error: "error",
  unknown: "unknown",
};

export function FeatureStatusBadge({ status }: { status: FeatureStatus }) {
  return <Badge variant={VARIANT[status]}>{LABEL[status]}</Badge>;
}
