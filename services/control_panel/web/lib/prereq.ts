import type { InstallStep, PrereqDetail } from "@/lib/api";

/**
 * Human phrasing for a prerequisite's state + what the cascade will do about
 * it. A STOPPED container is "installed but not started" — saying "not
 * installed" there (the old behaviour) was just wrong.
 */
export function prereqHint(status: string): string {
  switch (status) {
    case "stopped":
      return "installed but not started — will be started";
    case "available":
    case "unavailable":
      return "not installed — will be installed";
    case "partial":
      return "partially installed — will be completed";
    case "error":
      return "in an error state — install will attempt to repair it";
    case "missing":
      return "not found in any catalog — install it manually first";
    default:
      return status;
  }
}

/** "qdrant (not installed → will be installed)" style label. */
export function prereqLabel(p: PrereqDetail | InstallStep): string {
  return `${p.id} — ${prereqHint(p.status)}`;
}
