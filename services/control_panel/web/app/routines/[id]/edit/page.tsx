"use client";

import { useState, useEffect, use } from "react";
import { useRouter } from "next/navigation";
import { api, Routine } from "@/lib/api";
import { Button } from "@/components/ui/button";
import { RoutineForm } from "@/components/routine-form";

export default function RoutineEditPage({ params }: { params: Promise<{ id: string }> }) {
  const router = useRouter();
  const { id } = use(params);
  
  const [routine, setRoutine] = useState<Routine | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [deleting, setDeleting] = useState(false);

  useEffect(() => {
    api.routines().then(routines => {
      const r = routines.find(r => r.id === id);
      if (r) setRoutine(r);
      else setError("Routine not found");
    });
  }, [id]);

  const handleDelete = async () => {
    if (!confirm("Are you sure you want to delete this routine?")) return;
    setDeleting(true);
    try {
      await api.deleteRoutine(id);
      router.push("/routines");
    } catch (err: any) {
      setError(err.message);
      setDeleting(false);
    }
  };

  if (error) {
    return <div className="text-sm text-rose-500 p-8">{error}</div>;
  }

  if (!routine) {
    return <div className="text-sm text-muted-foreground p-8">Loading routine...</div>;
  }

  return (
    <div className="max-w-3xl">
      <div className="mb-6 flex justify-between items-start">
        <div>
          <h1 className="text-2xl font-semibold tracking-tight">Edit Routine</h1>
          <p className="mt-1 text-sm font-mono text-zinc-500">
            {id}
          </p>
        </div>
        <Button variant="destructive" size="sm" onClick={handleDelete} disabled={deleting}>
          {deleting ? "Deleting..." : "Delete Routine"}
        </Button>
      </div>

      <RoutineForm initialData={routine} />
    </div>
  );
}
