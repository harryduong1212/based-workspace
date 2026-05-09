import { ConnectorCard } from "@/components/connector-card";
import { api } from "@/lib/api";

export const dynamic = "force-dynamic";
export const metadata = { title: "Connectors — Control Panel" };

export default async function ConnectorsPage() {
  const data = await api.dashboard();
  const connectors = [...data.connectors].sort((a, b) => a.id.localeCompare(b.id));

  return (
    <div className="space-y-6">
      <div>
        <div className="text-xs font-semibold uppercase tracking-wider text-emerald-600/80 dark:text-emerald-400/80 mb-1.5">
          Connectors
        </div>
        <h1 className="text-2xl font-semibold tracking-tight">All connectors</h1>
        <p className="text-sm text-muted-foreground mt-1">
          {connectors.length} declared. Click any card to configure env vars and run a live test.
        </p>
      </div>

      <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
        {connectors.map((c) => (
          <ConnectorCard key={c.id} connector={c} />
        ))}
      </div>
    </div>
  );
}
