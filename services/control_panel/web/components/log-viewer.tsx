import { CheckCircle2, XCircle } from "lucide-react";

// Shared terminal-style streaming log box. Used by the install dialog and the
// container "Logs" viewer — both consume the same SSE chunk/done framing, so
// they render identically. The success/failure banners are optional: a live
// log tail (no terminal outcome) just passes status=null.
export const LogViewer = ({
  ref,
  log,
  status,
  error,
  successText = "Install finished successfully.",
  failTitle = "Install failed",
  showBanners = true,
  placeholder = "(waiting for first chunk…)",
}: {
  ref: React.Ref<HTMLPreElement>;
  log: string;
  status: "done" | "error" | null;
  error: string | null;
  successText?: string;
  failTitle?: string;
  showBanners?: boolean;
  placeholder?: string;
}) => (
  <div className="space-y-3">
    <pre
      ref={ref}
      className="rounded-md border bg-black/80 text-green-300 p-3 text-[11px] font-mono max-h-80 overflow-auto whitespace-pre-wrap break-all leading-relaxed"
    >
      {log || placeholder}
    </pre>
    {showBanners && status === "done" && (
      <div className="rounded-md border border-emerald-500/40 bg-emerald-500/10 p-3 text-sm flex items-start gap-2">
        <CheckCircle2 className="h-4 w-4 mt-0.5 shrink-0" />
        <span>{successText}</span>
      </div>
    )}
    {showBanners && status === "error" && (
      <div className="rounded-md border border-destructive/40 bg-destructive/10 p-3 text-sm flex items-start gap-2">
        <XCircle className="h-4 w-4 mt-0.5 shrink-0" />
        <div className="space-y-1">
          <div className="font-medium">{failTitle}</div>
          {error && <pre className="text-xs whitespace-pre-wrap break-all">{error}</pre>}
        </div>
      </div>
    )}
  </div>
);
