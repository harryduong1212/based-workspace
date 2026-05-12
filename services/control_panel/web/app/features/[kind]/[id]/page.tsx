import Link from "next/link";
import { notFound } from "next/navigation";
import { ChevronLeft } from "lucide-react";

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { FeatureActionButtons } from "@/components/feature-action-buttons";
import { FeatureStatusBadge } from "@/components/feature-status-badge";
import { ConnectorFeatureEnvForm } from "@/components/connector-feature-env-form";
import { api, type FeatureKind } from "@/lib/api";

export const dynamic = "force-dynamic";

const VALID_KINDS: FeatureKind[] = ["system", "container", "mcp", "recipe", "connector"];

export default async function FeatureDetailPage(props: {
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

  return (
    <div className="space-y-6 max-w-3xl">
      <div>
        <Link
          href="/features"
          className="inline-flex items-center gap-1 text-xs text-muted-foreground hover:text-foreground transition-colors mb-2"
        >
          <ChevronLeft className="h-3.5 w-3.5" />
          All features
        </Link>
        <div className="flex items-center justify-between gap-3">
          <div>
            <div className="text-xs font-semibold uppercase tracking-wider text-primary/70 mb-1">
              {feature.kind}
            </div>
            <h1 className="text-2xl font-semibold tracking-tight">{feature.name}</h1>
            <p className="text-sm text-muted-foreground mt-1">
              {feature.description || "(no description)"}
            </p>
          </div>
          <FeatureStatusBadge status={feature.status} />
        </div>
      </div>

      <Card>
        <CardHeader className="pb-3">
          <CardTitle className="text-base">Actions</CardTitle>
          <CardDescription>
            Install adds this feature to your setup; Uninstall reverses it. Verify
            re-runs the detection check without changing anything.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <FeatureActionButtons
            feature={feature}
            unmetPrereqs={unmet_prereqs}
            allowUninstall={feature.kind !== "system"}
          />
        </CardContent>
      </Card>

      {feature.kind === "connector" && (
        <Card>
          <CardHeader className="pb-3">
            <CardTitle className="text-base">Environment variables</CardTitle>
            <CardDescription>
              This connector needs the following vars to be set in <code>.env</code>.
              Values are written via env_writer and never echoed back.
            </CardDescription>
          </CardHeader>
          <CardContent>
            <ConnectorFeatureEnvForm feature={feature} />
          </CardContent>
        </Card>
      )}

      <Card>
        <CardHeader className="pb-3">
          <CardTitle className="text-base">Details</CardTitle>
        </CardHeader>
        <CardContent>
          <KindDetailBlock feature={data.feature} />
        </CardContent>
      </Card>
    </div>
  );
}

function KindDetailBlock({ feature }: { feature: { kind: FeatureKind; detail: Record<string, unknown> } }) {
  const d = feature.detail;
  if (feature.kind === "system") {
    return (
      <div className="space-y-2 text-sm">
        <Row label="Binary" value={String(d.binary ?? "—")} />
        <Row label="Minimum version" value={String(d.min_version ?? "any")} />
        {d.version != null && <Row label="Detected version" value={String(d.version)} />}
        {d.binary_path != null && <Row label="Path" value={String(d.binary_path)} mono />}
        {d.install_command != null && (
          <Row label="Install command" value={String(d.install_command)} mono />
        )}
        <Row label="Distro detected" value={String(d.distro ?? "—")} />
      </div>
    );
  }
  if (feature.kind === "container") {
    return (
      <div className="space-y-2 text-sm">
        <Row label="Compose file" value={String(d.compose_file ?? "—")} mono />
        <Row label="Service" value={String(d.compose_service ?? "—")} mono />
        <Row label="Container name" value={String(d.container_name ?? "—")} mono />
        {d.profile != null && <Row label="Profile" value={String(d.profile)} mono />}
        {(d.health as Record<string, unknown> | undefined)?.url != null && (
          <Row label="Health URL" value={String((d.health as Record<string, unknown>).url)} mono />
        )}
        {d.health_error != null && (
          <Row label="Health error" value={String(d.health_error)} mono />
        )}
      </div>
    );
  }
  if (feature.kind === "mcp") {
    return (
      <div className="space-y-2 text-sm">
        <Row label="Command" value={String(d.command ?? "—")} mono />
        <Row label="Args" value={Array.isArray(d.args) ? d.args.join(" ") : "—"} mono />
        {d.cwd != null && <Row label="Working dir" value={String(d.cwd)} mono />}
        <Row label="In example" value={d.in_example ? "yes" : "no"} />
        <Row label="In .mcp.json" value={d.in_installed ? "yes" : "no"} />
        <Row label="Spawn-probed" value={d.probed ? "yes" : "no (list view)"} />
        {d.probe_error != null && (
          <Row label="Probe error" value={String(d.probe_error)} mono />
        )}
      </div>
    );
  }
  if (feature.kind === "recipe") {
    const reqLine = (label: string, items: unknown) =>
      Array.isArray(items) && items.length > 0
        ? <Row key={label} label={label} value={items.join(", ")} mono /> : null;
    return (
      <div className="space-y-2 text-sm">
        <Row label="Source" value={String(d.source ?? "—")} mono />
        <Row label="Execution type" value={String(d.execution_type ?? "—")} />
        <Row label="Synced to .claude/" value={d.in_claude ? "yes" : "no"} />
        <Row label="Synced to .agents/" value={d.in_agents ? "yes" : "no"} />
        {reqLine("requires_skills", d.requires_skills)}
        {reqLine("requires_connectors", d.requires_connectors)}
        {reqLine("requires_mcp", d.requires_mcp)}
        {reqLine("requires_env", d.requires_env)}
      </div>
    );
  }
  if (feature.kind === "connector") {
    return (
      <div className="space-y-2 text-sm">
        <Row label="Path" value={String(d.path ?? "—")} mono />
        <Row
          label="requires_env"
          value={Array.isArray(d.requires_env) ? (d.requires_env as string[]).join(", ") : "—"}
          mono
        />
        <Row
          label="env_missing"
          value={Array.isArray(d.env_missing) ? (d.env_missing as string[]).join(", ") || "(none)" : "—"}
          mono
        />
        {Array.isArray(d.provides) && (d.provides as string[]).length > 0 && (
          <Row label="Provides" value={(d.provides as string[]).join(", ")} />
        )}
      </div>
    );
  }
  return <p className="text-sm text-muted-foreground">No details for this kind.</p>;
}

function Row({ label, value, mono }: { label: string; value: string; mono?: boolean }) {
  return (
    <div className="flex gap-3 items-baseline">
      <div className="w-40 shrink-0 text-xs uppercase tracking-wider text-muted-foreground">
        {label}
      </div>
      <div className={mono ? "font-mono text-xs break-all" : "text-sm"}>{value}</div>
    </div>
  );
}
