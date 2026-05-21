import Link from "next/link";
import { notFound } from "next/navigation";
import { ChevronLeft, ExternalLink, Sparkles } from "lucide-react";

import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { CollapsibleSection } from "@/components/collapsible-section";
import { ConnectorFeatureEnvForm } from "@/components/connector-feature-env-form";
import { ConnectorTestButton } from "@/components/connector-test-button";
import { FeatureActionButtons } from "@/components/feature-action-buttons";
import { FeatureStatusBadge } from "@/components/feature-status-badge";
import { InstallStateNotice } from "@/components/install-state-notice";
import { api, type ConnectorDetail, type Feature, type FeatureKind } from "@/lib/api";

export const dynamic = "force-dynamic";

// Recipe-kind URLs are redirected to /recipes/:id by next.config.ts (the run-
// flavoured page is canonical there). We still list "recipe" here so that
// other internal links typed against /components/recipe/... resolve before
// the redirect fires.
const VALID_KINDS: FeatureKind[] = ["system", "container", "mcp", "recipe", "connector"];

export default async function ComponentDetailPage(props: {
  params: Promise<{ kind: string; id: string }>;
}) {
  const { kind, id } = await props.params;
  if (!VALID_KINDS.includes(kind as FeatureKind)) notFound();

  let data;
  try {
    data = await api.feature(kind as FeatureKind, id);
  } catch {
    notFound();
  }

  const { feature, unmet_prereqs } = data;
  const unmetPrereqsDetail = data.unmet_prereqs_detail ?? [];

  let connectorDetail: ConnectorDetail | null = null;
  if (feature.kind === "connector") {
    try {
      connectorDetail = await api.connector(feature.id);
    } catch {
      connectorDetail = null;
    }
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <Link
          href="/components"
          className="inline-flex items-center gap-1 text-xs text-muted-foreground hover:text-foreground"
        >
          <ChevronLeft className="h-3 w-3" /> Components
        </Link>
        <div className="mt-2 flex items-center justify-between gap-3">
          <div className="min-w-0">
            <div className="flex items-baseline gap-2 flex-wrap">
              <h1 className="text-2xl font-semibold tracking-tight">{feature.name}</h1>
              <span className="text-sm text-muted-foreground">{feature.kind}</span>
            </div>
            <p className="text-sm text-muted-foreground mt-1">
              {feature.description || "(no description)"}
            </p>
          </div>
          <FeatureStatusBadge status={feature.status} />
        </div>
        <HeaderTagBadges feature={feature} connectorDetail={connectorDetail} />
      </div>

      {/* Action row — no "Install state" card. Any action error and the
        * status-notice banner render directly under the buttons. */}
      <div className="border-b border-border pb-4">
        <FeatureActionButtons
          feature={feature}
          unmetPrereqs={unmet_prereqs}
          unmetPrereqsDetail={unmetPrereqsDetail}
          allowUninstall={feature.kind !== "system"}
        />
        <InstallStateNotice status={feature.status} />
      </div>

      <div className="grid lg:grid-cols-[minmax(0,3fr)_minmax(0,1fr)] gap-6">
        <article className="min-w-0 space-y-6">
          {feature.about && (
            <Card>
              <CardHeader className="pb-3">
                <CardTitle className="text-base">About</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-sm leading-relaxed text-foreground/90 whitespace-pre-line">
                  {feature.about}
                </p>
              </CardContent>
            </Card>
          )}

          {feature.highlights.length > 0 && (
            <Card>
              <CardHeader className="pb-3">
                <CardTitle className="text-base flex items-center gap-2">
                  <Sparkles className="h-4 w-4 text-primary/80" />
                  Highlights
                </CardTitle>
              </CardHeader>
              <CardContent>
                <ul className="space-y-1.5 text-sm leading-relaxed">
                  {feature.highlights.map((h, i) => (
                    <li key={i} className="flex gap-2">
                      <span className="text-primary/70 mt-0.5">•</span>
                      <span className="text-foreground/90">{h}</span>
                    </li>
                  ))}
                </ul>
              </CardContent>
            </Card>
          )}

          {feature.examples.length > 0 && (
            <Card>
              <CardHeader className="pb-3">
                <CardTitle className="text-base">Examples</CardTitle>
                <CardDescription>Concrete uses — copy, adapt to your case.</CardDescription>
              </CardHeader>
              <CardContent className="space-y-3">
                {feature.examples.map((ex, i) => (
                  <div key={i} className="space-y-1.5">
                    {ex.label && (
                      <div className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
                        {ex.label}
                      </div>
                    )}
                    <pre className="rounded-md border bg-muted/30 p-2.5 text-xs overflow-x-auto leading-relaxed">
                      {ex.code}
                    </pre>
                  </div>
                ))}
              </CardContent>
            </Card>
          )}

          {/* Connector-only: rendered markdown body */}
          {feature.kind === "connector" && connectorDetail?.rendered_body && (
            <Card>
              <CardHeader className="pb-3">
                <CardTitle className="text-base">Documentation</CardTitle>
                <CardDescription>
                  Setup notes from <code>{connectorDetail.relative_path}</code>.
                </CardDescription>
              </CardHeader>
              <CardContent>
                <CollapsibleSection previewMaxHeight={220} expandLabel="Show full docs" collapseLabel="Show less">
                  <article
                    className="prose-body"
                    dangerouslySetInnerHTML={{ __html: connectorDetail.rendered_body }}
                  />
                </CollapsibleSection>
              </CardContent>
            </Card>
          )}

          {feature.docs && (
            <a
              href={feature.docs}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-1.5 text-sm text-primary hover:underline"
            >
              <ExternalLink className="h-3.5 w-3.5" />
              Source / documentation
            </a>
          )}
        </article>

        <aside className="space-y-4">
          {/* Kind-specific details */}
          <Card>
            <CardHeader className="pb-3">
              <CardTitle className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
                Details
              </CardTitle>
            </CardHeader>
            <CardContent>
              <KindDetailBlock feature={feature} />
            </CardContent>
          </Card>

          {/* Connector env-form */}
          {feature.kind === "connector" && (
            <Card>
              <CardHeader className="pb-3">
                <CardTitle className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
                  Environment variables
                </CardTitle>
                <CardDescription className="text-xs">
                  Written to <code>.env</code> via env_writer. Values never echo back.
                </CardDescription>
              </CardHeader>
              <CardContent>
                <ConnectorFeatureEnvForm feature={feature} />
              </CardContent>
            </Card>
          )}

          {/* Connector live-probe */}
          {feature.kind === "connector" && connectorDetail && (
            <Card>
              <CardHeader className="pb-3">
                <CardTitle className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
                  Live check
                </CardTitle>
                <CardDescription className="text-xs">
                  Hits the real API with the env vars in <code>.env</code>.
                </CardDescription>
              </CardHeader>
              <CardContent>
                <ConnectorTestButton connectorId={connectorDetail.id} />
              </CardContent>
            </Card>
          )}

          {/* Connector metadata */}
          {feature.kind === "connector" && connectorDetail && (
            <ConnectorMetadataCard detail={connectorDetail} />
          )}
        </aside>
      </div>
    </div>
  );
}

function HeaderTagBadges({
  feature,
  connectorDetail,
}: {
  feature: Feature;
  connectorDetail: ConnectorDetail | null;
}) {
  const chips: { label: string; variant: "info" | "outline" | "warn" }[] = [];
  if (feature.kind === "connector" && connectorDetail?.auth_type) {
    chips.push({ label: connectorDetail.auth_type, variant: "info" });
  }
  if (feature.kind === "mcp") {
    const scopes = Array.isArray(feature.detail?.installed_scopes)
      ? (feature.detail.installed_scopes as string[])
      : [];
    if (scopes.length === 2) chips.push({ label: "workspace + global", variant: "info" });
    else if (scopes.length === 1) chips.push({ label: scopes[0], variant: "info" });
  }
  if (feature.kind === "container" && typeof feature.detail?.profile === "string") {
    chips.push({ label: `profile: ${feature.detail.profile as string}`, variant: "outline" });
  }
  const tags = (connectorDetail?.tags ?? []) as string[];
  for (const t of tags) chips.push({ label: t, variant: "outline" });

  if (chips.length === 0) return null;
  return (
    <div className="flex flex-wrap gap-1.5 mt-3">
      {chips.map((c, i) => (
        <Badge key={i} variant={c.variant}>
          {c.label}
        </Badge>
      ))}
    </div>
  );
}

function KindDetailBlock({ feature }: { feature: Feature }) {
  const d = feature.detail;
  if (feature.kind === "system") {
    return (
      <div className="space-y-1.5 text-sm">
        <Row label="binary" value={String(d.binary ?? "—")} mono />
        <Row label="min version" value={String(d.min_version ?? "any")} />
        {d.version != null && <Row label="detected" value={String(d.version)} />}
        {d.binary_path != null && <Row label="path" value={String(d.binary_path)} mono />}
        {d.install_command != null && (
          <Row label="install cmd" value={String(d.install_command)} mono />
        )}
        <Row label="distro" value={String(d.distro ?? "—")} />
      </div>
    );
  }
  if (feature.kind === "container") {
    return (
      <div className="space-y-1.5 text-sm">
        <Row label="compose file" value={String(d.compose_file ?? "—")} mono />
        <Row label="service" value={String(d.compose_service ?? "—")} mono />
        <Row label="container" value={String(d.container_name ?? "—")} mono />
        {(d.health as Record<string, unknown> | undefined)?.url != null && (
          <Row label="health url" value={String((d.health as Record<string, unknown>).url)} mono />
        )}
        {d.health_error != null && (
          <Row label="health error" value={String(d.health_error)} mono />
        )}
      </div>
    );
  }
  if (feature.kind === "mcp") {
    const services = Array.isArray(d.requires_services)
      ? (d.requires_services as string[])
      : [];
    const scopes = Array.isArray(d.installed_scopes)
      ? (d.installed_scopes as string[])
      : [];
    const scopeLabel =
      scopes.length === 0
        ? "not installed"
        : scopes.length === 2
          ? "workspace + global"
          : scopes[0];
    return (
      <div className="space-y-1.5 text-sm">
        <Row label="command" value={String(d.command ?? "—")} mono />
        <Row label="args" value={Array.isArray(d.args) ? d.args.join(" ") : "—"} mono />
        {d.cwd != null && <Row label="working dir" value={String(d.cwd)} mono />}
        {services.length > 0 && (
          <Row label="needs" value={services.join(", ")} mono />
        )}
        <Row label="in example" value={d.in_example ? "yes" : "no"} />
        <Row label="installed in" value={scopeLabel} />
        <Row label="spawn-probed" value={d.probed ? "yes" : "no (list view)"} />
        {d.probe_error != null && (
          <Row label="probe error" value={String(d.probe_error)} mono />
        )}
      </div>
    );
  }
  if (feature.kind === "connector") {
    const requiresEnv = Array.isArray(d.requires_env) ? (d.requires_env as string[]) : [];
    const envMissing = Array.isArray(d.env_missing) ? (d.env_missing as string[]) : [];
    return (
      <div className="space-y-1.5 text-sm">
        <Row label="path" value={String(d.path ?? "—")} mono />
        <Row label="requires env" value={requiresEnv.join(", ") || "—"} mono />
        <Row
          label="missing env"
          value={envMissing.length > 0 ? envMissing.join(", ") : "(none)"}
          mono
        />
        {Array.isArray(d.provides) && (d.provides as string[]).length > 0 && (
          <Row label="provides" value={(d.provides as string[]).join(", ")} />
        )}
      </div>
    );
  }
  if (feature.kind === "recipe") {
    return (
      <div className="space-y-1.5 text-sm">
        <Row label="source" value={String(d.source ?? "—")} mono />
        <Row label="execution" value={String(d.execution_type ?? "—")} />
        <Row label="synced .claude/" value={d.in_claude ? "yes" : "no"} />
        <Row label="synced .agents/" value={d.in_agents ? "yes" : "no"} />
      </div>
    );
  }
  return <p className="text-sm text-muted-foreground">No details for this kind.</p>;
}

function Row({ label, value, mono }: { label: string; value: string; mono?: boolean }) {
  return (
    <div className="grid grid-cols-[max-content_1fr] gap-x-3 items-baseline">
      <dt className="text-[11px] uppercase tracking-wider text-muted-foreground">{label}</dt>
      <dd className={mono ? "font-mono text-xs break-all" : "text-sm"}>{value}</dd>
    </div>
  );
}

function ConnectorMetadataCard({ detail }: { detail: ConnectorDetail }) {
  if (
    detail.provides.length === 0 &&
    !detail.embed_collection &&
    !detail.n8n_workflow &&
    !detail.relative_path
  ) {
    return null;
  }
  return (
    <Card>
      <CardHeader className="pb-3">
        <CardTitle className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
          Metadata
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-1.5 text-sm">
        {detail.provides.length > 0 && (
          <Row label="provides" value={detail.provides.join(", ")} />
        )}
        {detail.embed_collection && (
          <Row label="embed coll." value={detail.embed_collection} mono />
        )}
        {detail.n8n_workflow && (
          <Row label="n8n flow" value={detail.n8n_workflow} mono />
        )}
        <Row label="file" value={detail.relative_path} mono />
      </CardContent>
    </Card>
  );
}
