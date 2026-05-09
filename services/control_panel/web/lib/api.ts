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

export type EnvSaveResult = {
  ok: boolean;
  saved_keys: string[];
  message: string;
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
  saveConnectorEnv: (id: string, values: Record<string, string>) =>
    getJson<EnvSaveResult>(`/api/v1/connectors/${id}/env`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ values }),
    }),
  runs: (params?: { limit?: number; recipe_id?: string }) => {
    const q = new URLSearchParams();
    if (params?.limit) q.set("limit", String(params.limit));
    if (params?.recipe_id) q.set("recipe_id", params.recipe_id);
    const qs = q.toString();
    return getJson<RunSummary[]>(`/api/v1/runs${qs ? `?${qs}` : ""}`);
  },
  run: (id: string) => getJson<RunDetail>(`/api/v1/runs/${id}`),
};
