import Link from "next/link";
import { notFound } from "next/navigation";
import { ChevronLeft } from "lucide-react";

import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { ConnectorEnvSheet } from "@/components/connector-env-sheet";
import { ConnectorTestButton } from "@/components/connector-test-button";
import { api } from "@/lib/api";

export const dynamic = "force-dynamic";

export default async function ConnectorDetailPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;
  let connector;
  try {
    connector = await api.connector(id);
  } catch (e) {
    if (e instanceof Error && e.message.includes("404")) notFound();
    throw e;
  }

  return (
    <div className="space-y-6">
      <div>
        <Link
          href="/"
          className="inline-flex items-center gap-1 text-xs text-muted-foreground hover:text-foreground"
        >
          <ChevronLeft className="h-3 w-3" /> Dashboard
        </Link>
        <div className="mt-2 flex items-baseline gap-2">
          <h1 className="text-2xl font-semibold tracking-tight">{connector.name}</h1>
          <span className="text-sm text-muted-foreground">connector</span>
        </div>
        <p className="text-sm text-muted-foreground mt-1">
          {connector.description || "(no description)"}
        </p>
        <div className="flex flex-wrap gap-1.5 mt-3">
          <Badge variant={connector.status === "stable" ? "success" : "warn"}>
            {connector.status || "unknown"}
          </Badge>
          {connector.auth_type && <Badge variant="info">{connector.auth_type}</Badge>}
          {connector.tags.map((t) => (
            <Badge key={t} variant="outline">
              {t}
            </Badge>
          ))}
        </div>
      </div>

      <div className="grid lg:grid-cols-[minmax(0,3fr)_minmax(0,1fr)] gap-6">
        <article
          className="min-w-0 prose-body"
          dangerouslySetInnerHTML={{ __html: connector.rendered_body }}
        />

        <aside className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
                Frontmatter
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-2 text-sm">
              <Row label="id"><code className="font-mono text-xs">{connector.id}</code></Row>
              {connector.auth_type && <Row label="auth">{connector.auth_type}</Row>}
              {connector.provides.length > 0 && (
                <Row label="provides">
                  <span className="font-mono text-xs">{connector.provides.join(", ")}</span>
                </Row>
              )}
              {connector.embed_collection && (
                <Row label="embed">
                  <code className="font-mono text-xs">{connector.embed_collection}</code>
                </Row>
              )}
              {connector.n8n_workflow && (
                <Row label="n8n">
                  <code className="font-mono text-xs break-all">{connector.n8n_workflow}</code>
                </Row>
              )}
            </CardContent>
          </Card>

          {connector.requires_env.length > 0 && (
            <Card>
              <CardHeader>
                <CardTitle className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
                  Environment
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                <div className="space-y-2">
                  {connector.requires_env.map((e) => (
                    <div key={e.name} className="flex items-center justify-between gap-2 text-sm">
                      <code className="font-mono text-xs">{e.name}</code>
                      <Badge variant={e.present ? "success" : "destructive"}>
                        {e.present ? "set" : "missing"}
                      </Badge>
                    </div>
                  ))}
                </div>
                <div className="grid grid-cols-1 gap-2 pt-1">
                  <ConnectorTestButton connectorId={connector.id} />
                  <ConnectorEnvSheet
                    connectorId={connector.id}
                    connectorName={connector.name}
                    requiresEnv={connector.requires_env}
                    safeToWrite={connector.safe_to_write_env}
                    host={connector.host}
                  />
                </div>
              </CardContent>
            </Card>
          )}

          <Card>
            <CardHeader>
              <CardTitle className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
                File
              </CardTitle>
            </CardHeader>
            <CardContent>
              <code className="font-mono text-xs text-muted-foreground break-all">
                {connector.relative_path}
              </code>
            </CardContent>
          </Card>
        </aside>
      </div>
    </div>
  );
}

function Row({ label, children }: { label: string; children: React.ReactNode }) {
  return (
    <div className="grid grid-cols-[max-content_1fr] gap-x-3 items-baseline">
      <dt className="text-muted-foreground">{label}</dt>
      <dd>{children}</dd>
    </div>
  );
}
