"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import cronstrue from "cronstrue";
import { api, Routine } from "@/lib/api";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Switch } from "@/components/ui/switch";
import { Clock, Play, ExternalLink } from "lucide-react";
import { toast } from "sonner";

export default function RoutinesPage() {
  const [routines, setRoutines] = useState<Routine[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchRoutines = async () => {
    try {
      const data = await api.routines();
      setRoutines(data);
    } catch (e) {
      toast.error("Failed to fetch routines.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchRoutines();
  }, []);

  const handleToggle = async (routine: Routine, enabled: boolean) => {
    // Optimistic update
    setRoutines(prev => prev.map(r => r.id === routine.id ? { ...r, enabled } : r));
    try {
      await api.saveRoutine({ ...routine, enabled });
      toast.success(`Routine ${enabled ? "enabled" : "disabled"}`);
    } catch (e: any) {
      // Revert on failure
      setRoutines(prev => prev.map(r => r.id === routine.id ? { ...r, enabled: !enabled } : r));
      toast.error("Failed to toggle routine.");
    }
  };

  const handleRunNow = async (routine: Routine) => {
    try {
      toast.info(`Starting routine: ${routine.recipe_id}...`);
      const res = await api.startRun(routine.recipe_id, routine.model_ref, routine.inputs);
      toast.success("Run started successfully!", {
        action: { label: "View", onClick: () => window.open(`/runs/${res.id}`, "_blank") }
      });
    } catch (e: any) {
      toast.error(`Failed to run: ${e.message}`);
    }
  };

  if (loading) {
    return <div className="p-8 text-sm text-muted-foreground">Loading routines...</div>;
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <div className="text-xs font-semibold uppercase tracking-wider text-primary/70 mb-1.5 flex items-center gap-1">
            <Clock className="w-3.5 h-3.5" /> Routines
          </div>
          <h1 className="text-2xl font-semibold tracking-tight">Scheduled Automation</h1>
          <p className="text-sm text-muted-foreground mt-1">
            Manage recurring recipe executions driven by APScheduler.
          </p>
        </div>
        <Button asChild>
          <Link href="/routines/new">New Routine</Link>
        </Button>
      </div>

      {routines.length === 0 ? (
        <div className="rounded-md border border-dashed border-zinc-300 p-12 text-center dark:border-zinc-800">
          <p className="text-sm text-zinc-500">No routines defined yet.</p>
        </div>
      ) : (
        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {routines.map((r) => {
            let humanCron = r.schedule;
            try {
              humanCron = cronstrue.toString(r.schedule);
            } catch {}

            return (
              <Card key={r.id} className="relative overflow-hidden group">
                <div className={`absolute left-0 top-0 bottom-0 w-1 ${r.enabled ? "bg-emerald-500" : "bg-zinc-300 dark:bg-zinc-700"}`} />
                <CardHeader className="pb-3 pl-5">
                  <div className="flex items-center justify-between">
                    <span className="text-xs font-medium text-emerald-600 dark:text-emerald-400">
                      {humanCron}
                    </span>
                    <Switch checked={r.enabled} onCheckedChange={(c) => handleToggle(r, c)} />
                  </div>
                  <CardTitle className="text-base mt-2 flex items-center gap-2">
                    <Link href={`/recipes/${r.recipe_id}`} className="hover:underline flex items-center gap-1">
                      {r.recipe_id} <ExternalLink className="w-3 h-3 text-muted-foreground" />
                    </Link>
                  </CardTitle>
                  <CardDescription className="font-mono text-xs truncate" title={r.schedule}>
                    {r.schedule}
                  </CardDescription>
                </CardHeader>
                <CardContent className="pl-5">
                  <div className="text-xs text-muted-foreground bg-zinc-50 dark:bg-zinc-900/50 p-2 rounded border border-zinc-100 dark:border-zinc-800 space-y-1 mb-4">
                    <p><span className="font-medium text-zinc-700 dark:text-zinc-300">Model:</span> {r.model_ref || "Default"}</p>
                    <p className="truncate"><span className="font-medium text-zinc-700 dark:text-zinc-300">Inputs:</span> {Object.keys(r.inputs).length > 0 ? JSON.stringify(r.inputs) : "None"}</p>
                  </div>
                  <div className="flex gap-2">
                    <Button variant="outline" size="sm" asChild className="flex-1">
                      <Link href={`/routines/${r.id}/edit`}>Edit</Link>
                    </Button>
                    <Button variant="secondary" size="sm" onClick={() => handleRunNow(r)} className="flex-1" title="Run immediately">
                      <Play className="w-3.5 h-3.5 mr-1" /> Run Now
                    </Button>
                  </div>
                </CardContent>
              </Card>
            );
          })}
        </div>
      )}
    </div>
  );
}
