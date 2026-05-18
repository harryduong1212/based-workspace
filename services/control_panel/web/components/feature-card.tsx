"use client";

import { useState } from "react";
import { ArrowUpRight, Cpu, Database, FileBox, Network, Server, Sparkles } from "lucide-react";

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { FeatureStatusBadge } from "@/components/feature-status-badge";
import { ComponentQuickLookDialog } from "@/components/component-quick-look-dialog";
import type { Feature, FeatureKind } from "@/lib/api";

const KIND_ICON: Record<FeatureKind, React.ComponentType<{ className?: string }>> = {
  system: Server,
  container: Database,
  mcp: Cpu,
  recipe: FileBox,
  connector: Network,
};

// Default card click opens a small preview dialog (no navigation). To reach
// the full detail page, the user clicks the explicit "View full details"
// link inside the dialog — so default-clicking a card never yanks them to a
// new page unexpectedly.
export function FeatureCard({ feature }: { feature: Feature }) {
  const [open, setOpen] = useState(false);
  const Icon = KIND_ICON[feature.kind] ?? Server;
  return (
    <>
      <button
        type="button"
        onClick={() => setOpen(true)}
        className="block group focus:outline-hidden text-left w-full"
        aria-label={`Preview ${feature.name}`}
      >
        <Card className="h-full card-lift border-border/60 group-focus-visible:ring-2 group-focus-visible:ring-ring relative">
          <CardHeader className="pb-3">
            <div className="flex items-center justify-between gap-2 mb-1">
              <span className="inline-flex h-7 w-7 items-center justify-center rounded-md bg-primary/10 text-primary">
                <Icon className="h-3.5 w-3.5" />
              </span>
              <FeatureStatusBadge status={feature.status} />
            </div>
            <CardTitle className="text-base flex items-center gap-1 truncate">
              {feature.name}
              {/* Subtle hint that clicking does something. The "Quick look"
                * affordance is reinforced by the icon swap on hover. */}
              <Sparkles className="h-3 w-3 opacity-40 group-hover:opacity-100 text-primary/70 transition-opacity" />
            </CardTitle>
            <CardDescription className="line-clamp-2 min-h-[2.5rem]">
              {feature.description || "(no description)"}
            </CardDescription>
          </CardHeader>
          <CardContent className="pt-0">
            <div className="flex items-center justify-between text-[11px]">
              <code className="font-mono text-muted-foreground truncate">{feature.id}</code>
              <span className="inline-flex items-center gap-0.5 text-[10px] text-muted-foreground opacity-0 group-hover:opacity-100 transition-opacity">
                quick look
                <ArrowUpRight className="h-3 w-3" />
              </span>
            </div>
            {feature.requires.length > 0 && (
              <div className="mt-2 text-[11px] text-muted-foreground">
                requires: <code className="font-mono">{feature.requires.join(", ")}</code>
              </div>
            )}
          </CardContent>
        </Card>
      </button>
      <ComponentQuickLookDialog
        feature={feature}
        open={open}
        onOpenChange={setOpen}
      />
    </>
  );
}
