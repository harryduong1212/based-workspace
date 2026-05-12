import { FeatureCard } from "@/components/feature-card";
import { api, type Feature, type FeatureKind } from "@/lib/api";

export const dynamic = "force-dynamic";
export const metadata = { title: "Features — Control Panel" };

const KIND_LABEL: Record<FeatureKind, string> = {
  system: "System runtime",
  container: "Infrastructure containers",
  mcp: "MCP servers",
  recipe: "Recipes",
  connector: "Connectors",
};

const KIND_BLURB: Record<FeatureKind, string> = {
  system: "Host binaries — Podman, Python, Node, Git, gitleaks. Detect-only; the wizard prints install commands, never runs sudo.",
  container: "podman-compose services — Postgres, n8n, Qdrant, llama-swap. Install brings the container up; uninstall stops + removes (volumes preserved).",
  mcp: "MCP servers from .mcp.json.example. Install copies into .mcp.json and runs a spawn-and-list_tools smoke.",
  recipe: "Recipes from recipes/. Install syncs to .claude/commands/ + .agents/workflows/; uninstall removes the synced copies (source preserved).",
  connector: "External data sources (Jira, Bitbucket, GitHub, n8n). Install writes required env vars via env_writer; secrets never echo back.",
};

const KIND_ORDER: FeatureKind[] = ["system", "container", "mcp", "recipe", "connector"];

function groupByKind(features: Feature[]): Record<FeatureKind, Feature[]> {
  const out: Record<FeatureKind, Feature[]> = {
    system: [],
    container: [],
    mcp: [],
    recipe: [],
    connector: [],
  };
  for (const f of features) out[f.kind].push(f);
  for (const k of Object.keys(out) as FeatureKind[]) {
    out[k].sort((a, b) => a.id.localeCompare(b.id));
  }
  return out;
}

export default async function FeaturesPage() {
  const data = await api.features();
  const grouped = groupByKind(data.features);

  const totalInstalled = data.features.filter((f) => f.status === "installed").length;
  const totalCount = data.features.length;

  return (
    <div className="space-y-8">
      <div>
        <div className="text-xs font-semibold uppercase tracking-wider text-primary/70 mb-1.5">
          Features
        </div>
        <h1 className="text-2xl font-semibold tracking-tight">Install &amp; manage</h1>
        <p className="text-sm text-muted-foreground mt-1">
          {totalInstalled} of {totalCount} features installed. Click any feature to
          install, configure, or remove it.
        </p>
      </div>

      {KIND_ORDER.map((kind) => {
        const items = grouped[kind];
        if (items.length === 0) return null;
        return (
          <section key={kind} className="space-y-3">
            <div>
              <h2 className="text-lg font-medium">{KIND_LABEL[kind]}</h2>
              <p className="text-sm text-muted-foreground mt-0.5">{KIND_BLURB[kind]}</p>
            </div>
            <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
              {items.map((f) => (
                <FeatureCard key={`${f.kind}:${f.id}`} feature={f} />
              ))}
            </div>
          </section>
        );
      })}
    </div>
  );
}
