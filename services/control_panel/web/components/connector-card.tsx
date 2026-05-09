import Link from "next/link";
import { ArrowUpRight, Plug } from "lucide-react";

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import type { ConnectorSummary } from "@/lib/api";

export function ConnectorCard({ connector }: { connector: ConnectorSummary }) {
  return (
    <Link href={`/connectors/${connector.id}`} className="block group focus:outline-hidden">
      <Card className="h-full card-lift border-border/60 group-focus-visible:ring-2 group-focus-visible:ring-ring">
        <CardHeader className="pb-3">
          <div className="flex items-center justify-between gap-2 mb-1">
            <span className="inline-flex h-7 w-7 items-center justify-center rounded-md bg-emerald-500/10 text-emerald-600 dark:text-emerald-400">
              <Plug className="h-3.5 w-3.5" />
            </span>
            <ArrowUpRight className="h-3.5 w-3.5 opacity-0 group-hover:opacity-100 text-muted-foreground transition-opacity" />
          </div>
          <CardTitle className="text-base truncate">{connector.name}</CardTitle>
          <CardDescription className="line-clamp-2 min-h-[2.5rem]">
            {connector.description || "(no description)"}
          </CardDescription>
        </CardHeader>
        <CardContent className="pt-0">
          <code className="font-mono text-[11px] text-muted-foreground">{connector.id}</code>
        </CardContent>
      </Card>
    </Link>
  );
}
