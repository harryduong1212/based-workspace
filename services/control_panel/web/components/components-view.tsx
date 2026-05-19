"use client";

import { useMemo, useState } from "react";
import { LayoutGrid, List } from "lucide-react";

import { FeatureCard } from "@/components/feature-card";
import { SearchInput } from "@/components/search-input";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";
import { useIsomorphicLayoutEffect } from "@/lib/use-isomorphic-layout-effect";
import type { Feature, FeatureKind } from "@/lib/api";

// One UI-visible "kind" → label + blurb (kept compact).
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
  mcp: "MCP servers from .mcp.json.example. Install copies into .mcp.json (workspace) or ~/.claude.json (global) and runs a spawn-and-list_tools smoke.",
  recipe: "Recipes from recipes/. Install syncs to .claude/commands/ + .agents/workflows/; uninstall removes the synced copies (source preserved).",
  connector: "External data sources (Jira, Bitbucket, GitHub, n8n). Install writes required env vars via env_writer; secrets never echo back.",
};

const KIND_ORDER: FeatureKind[] = ["system", "container", "mcp", "recipe", "connector"];

// Layer = the 3-tab grouping (the "by layer" view the user picked). Each tab
// covers one or more kinds. Order here is the tab order shown in the UI.
type Layer = "runtime" | "tools" | "workflows";
const LAYERS: { id: Layer; label: string; blurb: string; kinds: FeatureKind[] }[] = [
  {
    id: "runtime",
    label: "Runtime",
    blurb: "The base everything else depends on — host binaries (T1) and the containerised services (T2) they orchestrate.",
    kinds: ["system", "container"],
  },
  {
    id: "tools",
    label: "Tools",
    blurb: "MCP servers — recipes and agents call these as tools (memory, code search, notebooks, …).",
    kinds: ["mcp"],
  },
  {
    id: "workflows",
    label: "Workflows",
    blurb: "Reusable units of work (recipes) plus the external data sources they reach into (connectors).",
    kinds: ["recipe", "connector"],
  },
];

type ViewMode = "tabs" | "list";
const STORAGE_KEY_VIEW = "componentsViewMode";
const STORAGE_KEY_TAB = "componentsActiveTab";

export function ComponentsView({ features }: { features: Feature[] }) {
  // Tab view is the default; user can switch to list. Persist in localStorage
  // so the toggle sticks across reloads. SSR safety: start with the default,
  // sync from storage in an effect (hydration would otherwise mismatch).
  const [viewMode, setViewMode] = useState<ViewMode>("tabs");
  const [activeTab, setActiveTab] = useState<Layer>("runtime");
  const [hydrated, setHydrated] = useState(false);

  // Layout effect (not plain effect): apply the stored view/tab before the
  // browser paints so the default never flashes first.
  useIsomorphicLayoutEffect(() => {
    try {
      const v = localStorage.getItem(STORAGE_KEY_VIEW);
      if (v === "tabs" || v === "list") setViewMode(v);
      const t = localStorage.getItem(STORAGE_KEY_TAB);
      if (t === "runtime" || t === "tools" || t === "workflows") setActiveTab(t);
    } catch {
      // localStorage can throw in private-mode iframes — best-effort only.
    }
    setHydrated(true);
  }, []);

  const updateViewMode = (m: ViewMode) => {
    setViewMode(m);
    try {
      localStorage.setItem(STORAGE_KEY_VIEW, m);
    } catch {
      // no-op
    }
  };
  const updateActiveTab = (t: Layer) => {
    setActiveTab(t);
    try {
      localStorage.setItem(STORAGE_KEY_TAB, t);
    } catch {
      // no-op
    }
  };

  const [query, setQuery] = useState("");
  const q = query.trim().toLowerCase();
  const searching = q.length > 0;

  // Smoke recipes are dispatcher fixtures, not user-facing tasks — always
  // hide them on this page. The Recipes page has an opt-in toggle for
  // intentional browsing.
  const visible = useMemo(
    () =>
      features.filter(
        (f) =>
          !(
            f.kind === "recipe" &&
            ((f.detail?.tags as string[] | undefined) ?? []).includes("smoke")
          ),
      ),
    [features],
  );

  const filtered = useMemo(
    () =>
      searching
        ? visible.filter((f) =>
            `${f.id} ${f.name} ${f.description} ${f.kind}`
              .toLowerCase()
              .includes(q),
          )
        : visible,
    [visible, q, searching],
  );

  const grouped = groupByKind(filtered);
  const totalInstalled = visible.filter((f) => f.status === "installed").length;
  const totalCount = visible.length;

  return (
    <div className="space-y-6">
      <div className="flex items-start justify-between gap-4">
        <div>
          <div className="text-xs font-semibold uppercase tracking-wider text-primary/70 mb-1.5">
            Components
          </div>
          <h1 className="text-2xl font-semibold tracking-tight">Install &amp; manage</h1>
          <p className="text-sm text-muted-foreground mt-1">
            {totalInstalled} of {totalCount} components installed. Click any card to
            install, configure, or remove it.
          </p>
        </div>
        <ViewToggle mode={viewMode} onChange={updateViewMode} />
      </div>

      <SearchInput
        value={query}
        onChange={setQuery}
        placeholder="Search components by name, id, or kind…"
      />

      {/* When searching, flatten to a single grouped list — tabs would hide
       * matches behind an inactive tab. Otherwise keep the tab/list view the
       * user picked. Render tab view only AFTER hydration so the initial
       * paint matches saved preference (no flicker). */}
      {searching ? (
        filtered.length === 0 ? (
          <div className="rounded-md border bg-card/40 px-4 py-10 text-center text-sm text-muted-foreground">
            No components match <span className="font-medium text-foreground">“{query}”</span>.
          </div>
        ) : (
          <div className="space-y-2">
            <p className="text-sm text-muted-foreground">
              {filtered.length} match{filtered.length === 1 ? "" : "es"} for{" "}
              <span className="font-medium text-foreground">“{query}”</span>
            </p>
            <ListView grouped={grouped} />
          </div>
        )
      ) : !hydrated ? (
        <TabbedView
          grouped={grouped}
          activeTab="runtime"
          onTabChange={() => {}}
        />
      ) : viewMode === "tabs" ? (
        <TabbedView grouped={grouped} activeTab={activeTab} onTabChange={updateActiveTab} />
      ) : (
        <ListView grouped={grouped} />
      )}
    </div>
  );
}

function ViewToggle({
  mode,
  onChange,
}: {
  mode: ViewMode;
  onChange: (m: ViewMode) => void;
}) {
  return (
    <div className="inline-flex rounded-md border bg-card/40 p-0.5">
      <button
        type="button"
        onClick={() => onChange("tabs")}
        className={cn(
          "inline-flex items-center gap-1.5 px-2.5 py-1 rounded-[5px] text-xs transition-colors",
          mode === "tabs"
            ? "bg-primary/10 text-foreground"
            : "text-muted-foreground hover:text-foreground",
        )}
        aria-pressed={mode === "tabs"}
      >
        <LayoutGrid className="h-3.5 w-3.5" />
        Tabs
      </button>
      <button
        type="button"
        onClick={() => onChange("list")}
        className={cn(
          "inline-flex items-center gap-1.5 px-2.5 py-1 rounded-[5px] text-xs transition-colors",
          mode === "list"
            ? "bg-primary/10 text-foreground"
            : "text-muted-foreground hover:text-foreground",
        )}
        aria-pressed={mode === "list"}
      >
        <List className="h-3.5 w-3.5" />
        List
      </button>
    </div>
  );
}

function TabbedView({
  grouped,
  activeTab,
  onTabChange,
}: {
  grouped: Record<FeatureKind, Feature[]>;
  activeTab: Layer;
  onTabChange: (t: Layer) => void;
}) {
  const current = LAYERS.find((l) => l.id === activeTab) ?? LAYERS[0];
  return (
    <div className="space-y-5">
      <div className="border-b">
        <div className="flex gap-1 -mb-px overflow-x-auto">
          {LAYERS.map((layer) => {
            const count = layer.kinds.reduce((acc, k) => acc + grouped[k].length, 0);
            const active = layer.id === activeTab;
            return (
              <button
                key={layer.id}
                type="button"
                onClick={() => onTabChange(layer.id)}
                className={cn(
                  "px-4 py-2 text-sm border-b-2 transition-colors whitespace-nowrap",
                  active
                    ? "border-primary text-foreground font-medium"
                    : "border-transparent text-muted-foreground hover:text-foreground hover:border-muted",
                )}
                aria-current={active ? "page" : undefined}
              >
                {layer.label}
                <span className="ml-1.5 text-xs text-muted-foreground">{count}</span>
              </button>
            );
          })}
        </div>
      </div>

      <p className="text-sm text-muted-foreground">{current.blurb}</p>

      {current.kinds.map((kind) => {
        const items = grouped[kind];
        if (items.length === 0) return null;
        return <KindSection key={kind} kind={kind} items={items} />;
      })}
    </div>
  );
}

function ListView({ grouped }: { grouped: Record<FeatureKind, Feature[]> }) {
  return (
    <div className="space-y-8">
      {KIND_ORDER.map((kind) => {
        const items = grouped[kind];
        if (items.length === 0) return null;
        return <KindSection key={kind} kind={kind} items={items} />;
      })}
    </div>
  );
}

function KindSection({ kind, items }: { kind: FeatureKind; items: Feature[] }) {
  return (
    <section className="space-y-3">
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
}

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
