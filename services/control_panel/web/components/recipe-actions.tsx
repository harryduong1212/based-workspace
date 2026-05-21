"use client";

import { useState, useEffect, useRef } from "react";
import CodeMirror from "@uiw/react-codemirror";
import { markdown, markdownLanguage } from "@codemirror/lang-markdown";
import { languages } from "@codemirror/language-data";
import { useTheme } from "next-themes";
import { Play, Pencil, Save, RefreshCw, X } from "lucide-react";
import { api, RecipeDetail, ProvidersResponse } from "@/lib/api";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";

export function RecipeActions({ recipeId }: { recipeId: string }) {
  // No divider/spacing of its own — the detail page composes this into a
  // shared action row alongside the Install/Uninstall/Verify buttons.
  return (
    <div className="flex items-center gap-3">
      <RunSheet recipeId={recipeId} />
      <EditSheet recipeId={recipeId} />
    </div>
  );
}

function RunSheet({ recipeId }: { recipeId: string }) {
  const [open, setOpen] = useState(false);
  const [recipe, setRecipe] = useState<RecipeDetail | null>(null);
  const [providers, setProviders] = useState<ProvidersResponse | null>(null);
  const [lastInputs, setLastInputs] = useState<Record<string, string>>({});
  
  const [modelRef, setModelRef] = useState("");
  const [modelOverride, setModelOverride] = useState("");
  const [inputs, setInputs] = useState<Record<string, string>>({});
  
  const [runningId, setRunningId] = useState<string | null>(null);
  const [output, setOutput] = useState("");
  const [runStatus, setRunStatus] = useState<string>("");
  const [runError, setRunError] = useState<string | null>(null);
  const sseRef = useRef<EventSource | null>(null);
  
  const [refreshing, setRefreshing] = useState(false);

  const loadData = async () => {
    try {
      const [r, li] = await Promise.all([
        api.recipe(recipeId),
        api.lastInputs(recipeId),
      ]);
      setRecipe(r);
      setLastInputs(li);
      
      const defaults: Record<string, string> = {};
      for (const inp of r.inputs) {
        defaults[inp.name] = li[inp.name] || "";
      }
      setInputs(defaults);
      
      await loadProviders(r.execution_model || undefined);
    } catch (e) {
      console.error(e);
    }
  };

  const loadProviders = async (defaultModel?: string) => {
    setRefreshing(true);
    try {
      const p = await api.providers(defaultModel);
      setProviders(p);
      
      let validDefault = "";
      if (p.default_model) {
        const provPrefix = p.default_model.split("/")[0];
        const provOpt = p.options.find(o => o.provider === provPrefix);
        if (provOpt && provOpt.available) {
          validDefault = p.default_model;
        }
      }
      
      if (!validDefault) {
        const firstAvail = p.options.find(o => o.available && o.models.length > 0);
        if (firstAvail) {
          validDefault = `${firstAvail.provider}/${firstAvail.models[0]}`;
        }
      }

      setModelRef(validDefault);
    } catch (e) {
      console.error(e);
    } finally {
      setRefreshing(false);
    }
  };

  useEffect(() => {
    if (open && !recipe) {
      loadData();
    }
  }, [open, recipeId]);

  const handleRun = async (e: React.FormEvent) => {
    e.preventDefault();
    if (sseRef.current) return;

    const ref = modelOverride.trim() || modelRef;
    setOutput("");
    setRunStatus("running");
    setRunError(null);

    try {
      const res = await api.startRun(recipeId, ref, inputs);
      setRunningId(res.id);
      
      const sse = new EventSource(`/api/runs/${res.id}/stream`);
      sseRef.current = sse;

      sse.addEventListener("chunk", (e) => {
        try {
          const piece = JSON.parse(e.data);
          setOutput((prev) => prev + piece);
        } catch (err) { /* ignore */ }
      });

      sse.addEventListener("done", (e) => {
        sse.close();
        sseRef.current = null;
        try {
          const payload = JSON.parse(e.data);
          setRunStatus(payload.status || "done");
          if (payload.error) setRunError(payload.error);
        } catch (err) {
          setRunStatus("done");
        }
      });

      sse.onerror = () => {
        // let the browser auto-retry or close if done
      };
    } catch (err: any) {
      setRunStatus("error");
      setRunError(err.message);
    }
  };

  const handleStop = () => {
    if (sseRef.current) {
      sseRef.current.close();
      sseRef.current = null;
      setRunStatus("stopped");
    }
  };

  const hasProviders = providers?.options.some((o) => o.available && o.models.length > 0) ?? false;

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button className="gap-2" size="sm">
          <Play className="h-4 w-4" /> Run Recipe
        </Button>
      </DialogTrigger>
      <DialogContent className="sm:max-w-[700px] max-h-[85vh] overflow-y-auto">
        <DialogHeader className="mb-2">
          <DialogTitle>Run &middot; {recipe?.name || "Loading..."}</DialogTitle>
        </DialogHeader>
        
        {!recipe || !providers ? (
          <div className="text-muted-foreground text-sm flex items-center gap-2">
            <RefreshCw className="h-4 w-4 animate-spin" /> Loading...
          </div>
        ) : (
          <div className="space-y-6">
            <form onSubmit={handleRun} className="space-y-5">
              {!hasProviders && (
                <div className="rounded-md border border-amber-300 bg-amber-50 dark:border-amber-700 dark:bg-amber-500/10 p-4 text-sm">
                  <p className="font-medium text-amber-800 dark:text-amber-200">No providers available.</p>
                  <p className="text-amber-700 dark:text-amber-300/80 mt-1">
                    Set at least one provider API key in your <code className="font-mono">.env</code> and refresh.
                  </p>
                </div>
              )}

              <div>
                <div className="flex items-center justify-between mb-1.5">
                  <Label htmlFor="model_ref">Provider / model</Label>
                  <Button 
                    type="button" 
                    variant="ghost" 
                    size="icon" 
                    className="h-6 w-6" 
                    onClick={() => loadProviders(recipe.execution_model || undefined)}
                    disabled={refreshing}
                  >
                    <RefreshCw className={`h-3.5 w-3.5 text-muted-foreground ${refreshing ? "animate-spin" : ""}`} />
                  </Button>
                </div>
                <select
                  id="model_ref"
                  className="block w-full rounded-md border-input bg-zinc-50 px-3 py-2 text-sm shadow-sm focus:border-primary focus:ring-primary dark:bg-zinc-900/50 dark:text-foreground disabled:opacity-50 disabled:cursor-not-allowed"
                  value={modelRef}
                  onChange={(e) => setModelRef(e.target.value)}
                  disabled={!hasProviders}
                >
                  {!hasProviders ? (
                    <option value="">No provider available</option>
                  ) : (
                    providers.options.map((opt) => {
                      if (opt.models.length > 0) {
                        return (
                          <optgroup
                            key={opt.provider}
                            label={`${opt.provider}${!opt.available ? " (no key set)" : ""}`}
                            disabled={!opt.available}
                          >
                            {opt.models.map((m) => {
                              const ref = `${opt.provider}/${m}`;
                              return <option key={ref} value={ref}>{m}</option>;
                            })}
                          </optgroup>
                        );
                      } else if (opt.provider === "local") {
                        return (
                          <optgroup key="local" label="local (daemon offline)" disabled>
                            <option value="local-offline" disabled>—</option>
                          </optgroup>
                        );
                      }
                      return null;
                    })
                  )}
                </select>
                <p className="mt-1 text-xs text-muted-foreground">
                  Recipe declares <code className="font-mono">{recipe.execution_model || "(none)"}</code>.
                </p>
              </div>

              <div>
                <Label htmlFor="model_override" className="mb-1.5 block">Or model id (free-text override)</Label>
                <Input
                  id="model_override"
                  placeholder="local/qwen2.5-coder-14b &middot; anthropic/claude-opus-4-7"
                  value={modelOverride}
                  onChange={(e) => setModelOverride(e.target.value)}
                  className="font-mono bg-zinc-50 dark:bg-zinc-900/50 dark:text-foreground placeholder:text-zinc-400 dark:placeholder:text-zinc-600"
                />
              </div>

              {recipe.inputs.length > 0 ? (
                <div className="space-y-4">
                  {recipe.inputs.map((inp) => (
                    <div key={inp.name}>
                      <Label htmlFor={`input_${inp.name}`} className="mb-1.5 block">
                        {inp.name}
                        {inp.required && <span className="text-destructive ml-1">*</span>}
                        {inp.type && <span className="ml-1 text-xs font-normal text-muted-foreground">({inp.type})</span>}
                      </Label>
                      <textarea
                        id={`input_${inp.name}`}
                        rows={3}
                        required={inp.required}
                        placeholder={inp.description || ""}
                        value={inputs[inp.name]}
                        onChange={(e) => setInputs({ ...inputs, [inp.name]: e.target.value })}
                        className="block w-full rounded-md border-input bg-zinc-50 px-3 py-2 text-sm font-mono shadow-sm placeholder:text-zinc-400 dark:placeholder:text-zinc-600 focus:border-primary focus:ring-primary dark:bg-zinc-900/50 dark:text-foreground"
                      />
                    </div>
                  ))}
                </div>
              ) : (
                <p className="text-sm italic text-muted-foreground">This recipe declares no inputs.</p>
              )}

              <div className="pt-2 flex gap-2">
                <Button type="submit" disabled={runStatus === "running"}>
                  {runStatus === "running" ? "Running..." : "Start Run"}
                </Button>
                {runStatus === "running" && (
                  <Button type="button" variant="destructive" onClick={handleStop}>
                    Stop
                  </Button>
                )}
              </div>
            </form>

            {runStatus && (
              <div className="mb-4 flex items-center gap-3">
                <span className={`inline-flex items-center gap-1.5 rounded-full px-2 py-0.5 text-xs font-medium ring-1 ring-inset ${
                  runStatus === "done" ? "bg-emerald-50 text-emerald-700 ring-emerald-600/20 dark:bg-emerald-500/10 dark:text-emerald-300 dark:ring-emerald-500/30" :
                  runStatus === "error" ? "bg-rose-50 text-rose-700 ring-rose-600/20 dark:bg-rose-500/10 dark:text-rose-300 dark:ring-rose-500/30" :
                  "bg-amber-50 text-amber-700 ring-amber-600/20 dark:bg-amber-500/10 dark:text-amber-300 dark:ring-amber-500/30"
                }`}>
                  {runStatus === "running" && <span className="h-1.5 w-1.5 animate-pulse rounded-full bg-amber-500"></span>}
                  {runStatus}
                </span>
                {runningId && <span className="text-xs text-muted-foreground font-mono">ID: {runningId}</span>}
              </div>
            )}

            {(runStatus || output) && (
              <div className="rounded-lg border border-border bg-zinc-900 text-zinc-100 shadow-sm dark:bg-zinc-950">
                <div className="flex items-center gap-2 border-b border-zinc-800 px-4 py-2 text-xs text-zinc-400">
                  <span className="flex gap-1">
                    <span className="h-2.5 w-2.5 rounded-full bg-rose-500/70"></span>
                    <span className="h-2.5 w-2.5 rounded-full bg-amber-500/70"></span>
                    <span className="h-2.5 w-2.5 rounded-full bg-emerald-500/70"></span>
                  </span>
                  <span className="ml-2">output</span>
                </div>
                <pre className="m-0 min-h-[8rem] max-h-[50vh] overflow-y-auto whitespace-pre-wrap break-words p-4 font-mono text-sm leading-relaxed">
                  {output}
                </pre>
              </div>
            )}

            {runError && (
              <div className="mt-4 rounded-md border border-destructive bg-destructive/10 p-4 text-sm">
                <p className="font-medium text-destructive">Error</p>
                <pre className="mt-1 whitespace-pre-wrap font-mono text-xs text-destructive/90">{runError}</pre>
              </div>
            )}
          </div>
        )}
      </DialogContent>
    </Dialog>
  );
}

function EditSheet({ recipeId }: { recipeId: string }) {
  const [open, setOpen] = useState(false);
  const { theme, systemTheme } = useTheme();

  const [recipe, setRecipe] = useState<RecipeDetail | null>(null);
  const [content, setContent] = useState("");
  const [saving, setSaving] = useState(false);
  const [saveResult, setSaveResult] = useState<{ ok: boolean; message: string; warnings: string[] } | null>(null);

  useEffect(() => {
    if (open && !recipe) {
      api.recipe(recipeId).then((r) => {
        setRecipe(r);
        setContent(r.raw_content || "");
      }).catch(console.error);
    }
  }, [open, recipeId, recipe]);

  const handleSave = async () => {
    setSaving(true);
    setSaveResult(null);
    try {
      const res = await api.saveRecipe(recipeId, content);
      setSaveResult(res);
      if (res.ok) {
        setRecipe((prev) => prev ? { ...prev, raw_content: content } : null);
      }
    } catch (err: any) {
      setSaveResult({ ok: false, message: err.message, warnings: [] });
    } finally {
      setSaving(false);
    }
  };

  const isDark = theme === "dark" || (theme === "system" && systemTheme === "dark");

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button variant="secondary" className="gap-2" size="sm">
          <Pencil className="h-4 w-4" /> Edit Recipe
        </Button>
      </DialogTrigger>
      <DialogContent className="sm:max-w-[900px] max-h-[90vh] overflow-hidden flex flex-col">
        <DialogHeader className="shrink-0 mb-2">
          <DialogTitle>Edit &middot; {recipe?.name || "Loading..."}</DialogTitle>
        </DialogHeader>

        {!recipe ? (
          <div className="text-muted-foreground text-sm flex items-center gap-2">
            <RefreshCw className="h-4 w-4 animate-spin" /> Loading...
          </div>
        ) : (
          <div className="flex flex-col gap-4 flex-1 overflow-y-auto pb-4 pr-1">
            <div className="rounded-md border border-border overflow-hidden shadow-sm flex-1 min-h-[50vh]">
              <CodeMirror
                value={content}
                height="100%"
                theme={isDark ? "dark" : "light"}
                extensions={[markdown({ base: markdownLanguage, codeLanguages: languages })]}
                onChange={(val) => setContent(val)}
                className="text-sm font-mono h-full"
              />
            </div>

            <div className="flex items-center gap-4">
              <Button onClick={handleSave} disabled={saving} className="gap-2">
                <Save className="h-4 w-4" />
                {saving ? "Saving..." : "Save"}
              </Button>
              <p className="text-xs text-muted-foreground">
                Saves automatically reload in the workspace.
              </p>
            </div>

            {saveResult && (
              <div className={`rounded-md border p-4 text-sm ${saveResult.ok ? "border-emerald-300 bg-emerald-50 dark:border-emerald-800 dark:bg-emerald-500/10 text-emerald-800 dark:text-emerald-200" : "border-rose-300 bg-rose-50 dark:border-rose-800 dark:bg-rose-500/10 text-rose-800 dark:text-rose-200"}`}>
                <p className="font-medium">{saveResult.message}</p>
                {saveResult.warnings && saveResult.warnings.length > 0 && (
                  <ul className="mt-2 list-inside list-disc text-amber-600 dark:text-amber-400">
                    {saveResult.warnings.map((w, i) => (
                      <li key={i}>{w}</li>
                    ))}
                  </ul>
                )}
              </div>
            )}
          </div>
        )}
      </DialogContent>
    </Dialog>
  );
}
