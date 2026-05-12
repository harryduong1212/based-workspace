"use client";

import { useState } from "react";
import { ChevronDown, ChevronRight } from "lucide-react";

import { Button } from "@/components/ui/button";

/**
 * Collapsible section with a preview slice when collapsed.
 *
 * `previewMaxHeight` clips the body in CSS (with a fade-out gradient) so the
 * user can sample the content before deciding to expand. Expand toggles to
 * the full body. This keeps long markdown bodies (e.g. connector setup docs)
 * from dominating the detail page while still being one click away.
 */
export function CollapsibleSection({
  children,
  previewMaxHeight = 200,
  expandLabel = "Show more",
  collapseLabel = "Show less",
  defaultExpanded = false,
}: {
  children: React.ReactNode;
  previewMaxHeight?: number;
  expandLabel?: string;
  collapseLabel?: string;
  defaultExpanded?: boolean;
}) {
  const [expanded, setExpanded] = useState(defaultExpanded);

  return (
    <div className="space-y-2">
      <div
        className="relative overflow-hidden transition-[max-height]"
        style={{
          maxHeight: expanded ? "none" : `${previewMaxHeight}px`,
        }}
      >
        {children}
        {!expanded && (
          <div className="pointer-events-none absolute inset-x-0 bottom-0 h-16 bg-gradient-to-t from-background to-transparent" />
        )}
      </div>
      <Button
        variant="ghost"
        size="sm"
        className="text-xs gap-1"
        onClick={() => setExpanded((e) => !e)}
      >
        {expanded ? (
          <>
            <ChevronDown className="h-3.5 w-3.5" /> {collapseLabel}
          </>
        ) : (
          <>
            <ChevronRight className="h-3.5 w-3.5" /> {expandLabel}
          </>
        )}
      </Button>
    </div>
  );
}
