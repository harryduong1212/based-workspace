"use client";

import { useEffect, useRef, useState } from "react";
import { ScrollText, Loader2 } from "lucide-react";

import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { LogViewer } from "@/components/log-viewer";
import type { Feature } from "@/lib/api";

// Live `podman logs -f` for a running container, streamed over the same SSE
// chunk/done framing the install job uses — so it reuses <LogViewer>. The
// stream is a continuous tail (no terminal success/failure), so banners are
// off; "done" only fires if the container stops or the 10-min cap hits.
export function ContainerLogsDialog({
  feature,
  size = "default",
}: {
  feature: Feature;
  size?: "default" | "sm";
}) {
  const [open, setOpen] = useState(false);
  const [log, setLog] = useState("");
  const [ended, setEnded] = useState(false);
  const sseRef = useRef<EventSource | null>(null);
  const logRef = useRef<HTMLPreElement | null>(null);

  useEffect(() => {
    if (!open) {
      sseRef.current?.close();
      sseRef.current = null;
      const t = setTimeout(() => {
        setLog("");
        setEnded(false);
      }, 200);
      return () => clearTimeout(t);
    }
    setLog("");
    setEnded(false);
    const es = new EventSource(
      `/api/v1/features/container/${feature.id}/logs/stream`,
    );
    sseRef.current = es;
    es.addEventListener("chunk", (ev) => {
      try {
        const text = JSON.parse((ev as MessageEvent).data) as string;
        setLog((prev) => prev + text);
      } catch {
        // ignore malformed frame
      }
    });
    es.addEventListener("done", () => {
      setEnded(true);
      es.close();
      sseRef.current = null;
    });
    es.addEventListener("error", () => {
      setEnded(true);
      es.close();
      sseRef.current = null;
    });
    return () => {
      es.close();
      sseRef.current = null;
    };
  }, [open, feature.id]);

  // Pin to the bottom as new lines arrive.
  useEffect(() => {
    const el = logRef.current;
    if (el) el.scrollTop = el.scrollHeight;
  }, [log]);

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <div onClick={() => setOpen(true)} className="inline-flex">
        <Button type="button" variant="outline" size={size}>
          <ScrollText className="h-3.5 w-3.5 mr-1" />
          Logs
        </Button>
      </div>
      <DialogContent className="sm:max-w-2xl overflow-hidden">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2">
            {!ended && <Loader2 className="h-4 w-4 animate-spin" />}
            Logs — {feature.name}
          </DialogTitle>
          <DialogDescription>
            Live tail of <code className="font-mono">podman logs -f</code> (last
            200 lines + follow). Closing this stops the follow.
            {ended && " Stream ended (container stopped or follow timed out)."}
          </DialogDescription>
        </DialogHeader>

        <LogViewer
          ref={logRef}
          log={log}
          status={null}
          error={null}
          showBanners={false}
          placeholder="(connecting to container logs…)"
        />

        <DialogFooter>
          <Button variant="outline" onClick={() => setOpen(false)}>
            Close
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
