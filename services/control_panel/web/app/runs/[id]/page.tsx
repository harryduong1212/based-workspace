"use client";

import { use, useEffect, useState, useRef } from "react";
import Link from "next/link";
import { api, RunDetail } from "@/lib/api";

export default function RunViewPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = use(params);
  
  const [run, setRun] = useState<RunDetail | null>(null);
  const [streamedOutput, setStreamedOutput] = useState("");
  const [streamedError, setStreamedError] = useState<string | null>(null);
  const [streamStatus, setStreamStatus] = useState<string>("");
  const sseRef = useRef<EventSource | null>(null);

  useEffect(() => {
    api.run(id).then((r) => {
      setRun(r);
      setStreamedOutput(r.output);
      setStreamedError(r.error);
      setStreamStatus(r.status);
      
      if (r.status === "running") {
        const sse = new EventSource(`/api/runs/${r.id}/stream`);
        sseRef.current = sse;
        
        sse.addEventListener("chunk", (e) => {
          try {
            const piece = JSON.parse(e.data);
            setStreamedOutput((prev) => prev + piece);
          } catch (err) { /* ignore */ }
        });
        
        sse.addEventListener("done", (e) => {
          sse.close();
          sseRef.current = null;
          try {
            const payload = JSON.parse(e.data);
            setStreamStatus(payload.status || "done");
            if (payload.error) setStreamedError(payload.error);
          } catch (err) {
            setStreamStatus("done");
          }
        });
        
        sse.onerror = () => { /* browser retry */ };
      }
    }).catch(console.error);

    return () => {
      if (sseRef.current) {
        sseRef.current.close();
      }
    };
  }, [id]);

  if (!run) {
    return <div className="p-8 text-zinc-500">Loading run...</div>;
  }

  return (
    <div className="space-y-6">
      <nav className="text-sm">
        <Link href="/" className="hover:text-zinc-700 dark:hover:text-zinc-300">Recipes</Link>
        <span className="mx-1.5 text-zinc-400">/</span>
        <Link href={`/recipes/${run.recipe_id}`} className="hover:text-zinc-700 dark:hover:text-zinc-300">
          {run.recipe_id}
        </Link>
        <span className="mx-1.5 text-zinc-400">/</span>
        <span className="font-medium text-zinc-700 dark:text-zinc-300">run</span>
      </nav>

      <div className="mb-5">
        <div className="flex items-center gap-3">
          <h1 className="text-2xl font-semibold tracking-tight">Run · {run.recipe_id}</h1>
          <span className={`inline-flex items-center gap-1.5 rounded-full px-2 py-0.5 text-xs font-medium ring-1 ring-inset ${
            streamStatus === "done" ? "bg-emerald-50 text-emerald-700 ring-emerald-600/20 dark:bg-emerald-500/10 dark:text-emerald-300 dark:ring-emerald-500/30" :
            streamStatus === "error" ? "bg-rose-50 text-rose-700 ring-rose-600/20 dark:bg-rose-500/10 dark:text-rose-300 dark:ring-rose-500/30" :
            "bg-amber-50 text-amber-700 ring-amber-600/20 dark:bg-amber-500/10 dark:text-amber-300 dark:ring-amber-500/30"
          }`}>
            {streamStatus === "running" && <span className="h-1.5 w-1.5 animate-pulse rounded-full bg-amber-500"></span>}
            {streamStatus}
          </span>
        </div>
        <p className="mt-1 text-sm text-zinc-500">
          Model: <code className="font-mono">{run.model_ref}</code>
          {" · "}Started: <span className="font-mono">{new Date(run.started_at).toLocaleString()}</span>
          {" · "}Run ID: <code className="font-mono">{run.id}</code>
        </p>
      </div>

      <div className="rounded-lg border border-zinc-200 bg-zinc-900 text-zinc-100 shadow-sm dark:border-zinc-800 dark:bg-zinc-950">
        <div className="flex items-center gap-2 border-b border-zinc-800 px-4 py-2 text-xs text-zinc-400">
          <span className="flex gap-1">
            <span className="h-2.5 w-2.5 rounded-full bg-rose-500/70"></span>
            <span className="h-2.5 w-2.5 rounded-full bg-amber-500/70"></span>
            <span className="h-2.5 w-2.5 rounded-full bg-emerald-500/70"></span>
          </span>
          <span className="ml-2">output</span>
        </div>
        <pre className="m-0 min-h-[8rem] max-h-[70vh] overflow-y-auto whitespace-pre-wrap break-words p-4 font-mono text-sm leading-relaxed">
          {streamedOutput}
        </pre>
      </div>

      {streamedError && (
        <div className="mt-4 rounded-md border border-rose-300 bg-rose-50 p-4 text-sm dark:border-rose-700 dark:bg-rose-500/10">
          <p className="font-medium text-rose-800 dark:text-rose-200">Error</p>
          <pre className="mt-1 whitespace-pre-wrap font-mono text-xs text-rose-700 dark:text-rose-300/90">{streamedError}</pre>
        </div>
      )}

      <details className="group mt-6">
        <summary className="cursor-pointer select-none text-sm text-zinc-600 hover:text-zinc-900 dark:text-zinc-400 dark:hover:text-zinc-100">
          <span className="inline-block transition group-open:rotate-90">▸</span> Inputs
        </summary>
        <dl className="mt-3 space-y-3">
          {Object.entries(run.inputs).map(([k, v]) => (
            <div key={k} className="rounded-md border border-zinc-200 bg-white p-3 dark:border-zinc-800 dark:bg-zinc-900">
              <dt className="mb-1 text-xs font-semibold text-zinc-500"><code className="font-mono">{k}</code></dt>
              <dd><pre className="m-0 whitespace-pre-wrap font-mono text-xs text-zinc-700 dark:text-zinc-300">{v}</pre></dd>
            </div>
          ))}
        </dl>
      </details>
    </div>
  );
}
