/**
 * Typed fetch wrappers for the FastAPI backend.
 *
 * In dev, requests go to /api/v1/* on :3000, which next.config.ts rewrites
 * to http://127.0.0.1:8765/api/v1/*. Server Components fetch with absolute
 * URLs are also supported (set INTERNAL_API_BASE for SSR).
 */

const SSR_BASE = process.env.INTERNAL_API_BASE ?? "http://127.0.0.1:8765";
const isServer = typeof window === "undefined";

function url(path: string): string {
  return isServer ? `${SSR_BASE}${path}` : path;
}

export type RecipeSummary = {
  id: string;
  name: string;
  description: string;
  audience: string;
  status: string;
  tags: string[];
  execution_type: string;
  execution_model: string | null;
};

export type ConnectorSummary = {
  id: string;
  name: string;
  description: string;
};

export type DashboardData = {
  recipes: RecipeSummary[];
  connectors: ConnectorSummary[];
};

export type EnvVarStatus = { name: string; present: boolean };

export type RecipeInput = {
  name: string;
  type?: string;
  required?: boolean;
  description?: string;
};

export type RecipeOutput = {
  name: string;
  type?: string;
  description?: string;
};

export type RecipeDetail = {
  id: string;
  name: string;
  description: string;
  status: string;
  version: string;
  audience: string;
  cost: string;
  tags: string[];
  execution_type: string;
  execution_model: string | null;
  requires_skills: string[];
  requires_workflows: string[];
  requires_connectors: string[];
  requires_mcp: string[];
  requires_env: string[];
  triggers: Record<string, unknown>;
  inputs: RecipeInput[];
  outputs: RecipeOutput[];
  rendered_body: string;
  relative_path: string;
  raw_content?: string;
};

export type ConnectorDetail = {
  id: string;
  name: string;
  description: string;
  status: string;
  auth_type: string;
  tags: string[];
  provides: string[];
  embed_collection: string;
  n8n_workflow: string;
  requires_env: EnvVarStatus[];
  rendered_body: string;
  relative_path: string;
  probe_registered: boolean;
  host: string;
  safe_to_write_env: boolean;
};

export type ProbeOutcome = { ok: boolean; message: string };

export type ConnectorTestResult = {
  env_check: { all_present: boolean; missing: string[] };
  probe: ProbeOutcome | null;
  probe_registered: boolean;
};

export type HealthStatus = { name: string; ok: boolean; detail: string };

export type RunSummary = {
  id: string;
  recipe_id: string;
  model_ref: string;
  status: "running" | "done" | "error" | "abandoned" | string;
  error: string | null;
  started_at: string;
  ended_at: string | null;
};

export type RunDetail = RunSummary & {
  inputs: Record<string, string>;
  output: string;
};

export type ProviderOption = {
  provider: string;
  models: string[];
  available: boolean;
};

export type ProvidersResponse = {
  options: ProviderOption[];
  default_model: string;
};

export type RunResponse = {
  id: string;
};

// ---- features (install/uninstall/verify wizard) ---------------------------

export type FeatureKind = "system" | "container" | "mcp" | "recipe" | "connector";

export type FeatureStatus =
  | "available"
  | "installed"
  | "partial"
  | "stopped"
  | "error"
  | "unavailable"
  | "unknown";

export type Feature = {
  id: string;
  kind: FeatureKind;
  name: string;
  description: string;
  status: FeatureStatus;
  requires: string[];
  detail: Record<string, unknown>;
};

export type FeaturesList = { features: Feature[]; kinds: FeatureKind[] };

export type FeatureDetail = { feature: Feature; unmet_prereqs: string[] };

export type FeatureActionResult = {
  ok: boolean;
  noop?: boolean;
  error?: string;
  command?: string;
  message?: string;
  feature?: Feature;
  unmet_prereqs?: string[];
  // Connector-specific
  wrote_keys?: string[];
  rejected?: string[];
  cleared?: string[];
  kept_shared?: string[];
  // System / T2 extras
  kind?: string;
  distro?: string;
  stdout?: string;
};

export type FeatureSideEffect = {
  kind: string;
  summary: string;
  detail: string;
};

export type FeaturePreview = {
  ok: boolean;
  error?: string;
  feature?: Feature;
  would_be_noop?: boolean;
  side_effects?: FeatureSideEffect[];
  warnings?: string[];
  unmet_prereqs?: string[];
};

export type InstallJobStart = {
  ok: boolean;
  job_id: string;
};

export type InstallJobStatus = {
  id: string;
  kind: string;
  feature_id: string;
  status: "running" | "done" | "error";
  started_at: string;
  ended_at: string | null;
  output: string;
  error: string | null;
  result: FeatureActionResult | null;
};

export type Routine = {
  id: string;
  recipe_id: string;
  model_ref: string;
  inputs: Record<string, string>;
  schedule: string;
  enabled: boolean;
  created_at: string;
  updated_at: string;
};

async function getJson<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(url(path), {
    ...init,
    cache: "no-store",
    headers: { Accept: "application/json", ...(init?.headers ?? {}) },
  });
  if (!res.ok) {
    const body = await res.text().catch(() => "");
    throw new Error(`${init?.method ?? "GET"} ${path} → ${res.status}: ${body || res.statusText}`);
  }
  return (await res.json()) as T;
}

export const api = {
  dashboard: () => getJson<DashboardData>("/api/v1/dashboard"),
  health: () => getJson<HealthStatus[]>("/api/v1/health"),
  recipe: (id: string) => getJson<RecipeDetail>(`/api/v1/recipes/${id}`),
  connector: (id: string) => getJson<ConnectorDetail>(`/api/v1/connectors/${id}`),
  testConnector: (id: string) =>
    getJson<ConnectorTestResult>(`/api/v1/connectors/${id}/test`, { method: "POST" }),
  runs: (params?: { limit?: number; recipe_id?: string }) => {
    const q = new URLSearchParams();
    if (params?.limit) q.set("limit", String(params.limit));
    if (params?.recipe_id) q.set("recipe_id", params.recipe_id);
    const qs = q.toString();
    return getJson<RunSummary[]>(`/api/v1/runs${qs ? `?${qs}` : ""}`);
  },
  run: (id: string) => getJson<RunDetail>(`/api/v1/runs/${id}`),
  providers: (recipe_default?: string) => {
    const q = new URLSearchParams();
    if (recipe_default) q.set("recipe_default", recipe_default);
    const qs = q.toString();
    return getJson<ProvidersResponse>(`/api/v1/providers${qs ? `?${qs}` : ""}`);
  },
  lastInputs: (id: string) => getJson<Record<string, string>>(`/api/v1/recipes/${id}/last-inputs`),
  startRun: (id: string, model_ref: string, inputs: Record<string, string>) =>
    getJson<RunResponse>(`/api/v1/recipes/${id}/run`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ model_ref, inputs }),
    }),
  createRecipe: (data: Record<string, string>) =>
    getJson<{ id: string }>(`/api/v1/recipes/new`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    }),
  saveRecipe: (id: string, content: string) =>
    getJson<{ ok: boolean; message: string; warnings: string[] }>(`/api/v1/recipes/${id}/edit`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ content }),
    }),
  routines: () => getJson<Routine[]>("/api/v1/routines"),
  saveRoutine: (routine: Partial<Routine> & { recipe_id: string; schedule: string }) =>
    getJson<{ id: string }>("/api/v1/routines", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(routine),
    }),
  deleteRoutine: (id: string) =>
    getJson<{ ok: boolean }>(`/api/v1/routines/${id}`, {
      method: "DELETE",
    }),
  features: () => getJson<FeaturesList>("/api/v1/features"),
  feature: (kind: FeatureKind, id: string) =>
    getJson<FeatureDetail>(`/api/v1/features/${kind}/${id}`),
  installFeature: (kind: FeatureKind, id: string, inputs?: Record<string, unknown>) =>
    getJson<InstallJobStart>(`/api/v1/features/${kind}/${id}/install`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(inputs ?? {}),
    }),
  installJobStatus: (job_id: string) =>
    getJson<InstallJobStatus>(`/api/v1/features/install/${job_id}`),
  uninstallFeature: (kind: FeatureKind, id: string) =>
    getJson<FeatureActionResult>(`/api/v1/features/${kind}/${id}/uninstall`, {
      method: "POST",
    }),
  verifyFeature: (kind: FeatureKind, id: string) =>
    getJson<FeatureActionResult>(`/api/v1/features/${kind}/${id}/verify`, {
      method: "POST",
    }),
  previewFeature: (kind: FeatureKind, id: string, inputs?: Record<string, unknown>) =>
    getJson<FeaturePreview>(`/api/v1/features/${kind}/${id}/preview`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(inputs ?? {}),
    }),
};
