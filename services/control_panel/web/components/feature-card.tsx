import Link from "next/link";
import { ArrowUpRight, Cpu, Database, FileBox, Network, Server } from "lucide-react";

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { FeatureStatusBadge } from "@/components/feature-status-badge";
import type { Feature, FeatureKind } from "@/lib/api";

const KIND_ICON: Record<FeatureKind, React.ComponentType<{ className?: string }>> = {
  system: Server,
  container: Database,
  mcp: Cpu,
  recipe: FileBox,
  connector: Network,
};

export function FeatureCard({ feature }: { feature: Feature }) {
  const Icon = KIND_ICON[feature.kind] ?? Server;
  return (
    <Link
      href={`/features/${feature.kind}/${feature.id}`}
      className="block group focus:outline-hidden"
    >
      <Card className="h-full card-lift border-border/60 group-focus-visible:ring-2 group-focus-visible:ring-ring">
        <CardHeader className="pb-3">
          <div className="flex items-center justify-between gap-2 mb-1">
            <span className="inline-flex h-7 w-7 items-center justify-center rounded-md bg-primary/10 text-primary">
              <Icon className="h-3.5 w-3.5" />
            </span>
            <FeatureStatusBadge status={feature.status} />
          </div>
          <CardTitle className="text-base flex items-center gap-1 truncate">
            {feature.name}
            <ArrowUpRight className="h-3.5 w-3.5 opacity-0 group-hover:opacity-100 text-muted-foreground transition-opacity" />
          </CardTitle>
          <CardDescription className="line-clamp-2 min-h-[2.5rem]">
            {feature.description || "(no description)"}
          </CardDescription>
        </CardHeader>
        <CardContent className="pt-0">
          <div className="flex items-center justify-between text-[11px]">
            <code className="font-mono text-muted-foreground truncate">{feature.id}</code>
          </div>
          {feature.requires.length > 0 && (
            <div className="mt-2 text-[11px] text-muted-foreground">
              requires: <code className="font-mono">{feature.requires.join(", ")}</code>
            </div>
          )}
        </CardContent>
      </Card>
    </Link>
  );
}
