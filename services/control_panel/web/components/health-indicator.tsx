"use client";

import { useEffect, useState } from "react";
import { api, type HealthStatus } from "@/lib/api";

export function HealthIndicator() {
  const [statuses, setStatuses] = useState<HealthStatus[] | null>(null);

  useEffect(() => {
    let cancelled = false;
    const tick = async () => {
      try {
        const data = await api.health();
        if (!cancelled) setStatuses(data);
      } catch {
        if (!cancelled) setStatuses([]);
      }
    };
    tick();
    const id = setInterval(tick, 30_000);
    return () => {
      cancelled = true;
      clearInterval(id);
    };
  }, []);

  if (statuses === null) {
    return <span className="text-xs text-muted-foreground">checking…</span>;
  }
  if (statuses.length === 0) {
    return <span className="text-xs text-muted-foreground">health: unavailable</span>;
  }
  return (
    <div className="flex items-center gap-3 text-xs">
      {statuses.map((s) => (
        <div key={s.name} className="flex items-center gap-1.5" title={s.detail}>
          <span
            className={`h-1.5 w-1.5 rounded-full ${
              s.ok ? "bg-emerald-500" : "bg-rose-500"
            }`}
          />
          <span className="text-muted-foreground">{s.name}</span>
        </div>
      ))}
    </div>
  );
}
