"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import cronstrue from "cronstrue";
import { api, Routine, RecipeSummary, RecipeDetail } from "@/lib/api";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Switch } from "@/components/ui/switch";
import { Card, CardContent } from "@/components/ui/card";

interface RoutineFormProps {
  initialData?: Routine;
}

export function RoutineForm({ initialData }: RoutineFormProps) {
  const router = useRouter();
  
  const [recipes, setRecipes] = useState<RecipeSummary[]>([]);
  const [selectedRecipe, setSelectedRecipe] = useState<RecipeDetail | null>(null);
  
  const [formData, setFormData] = useState({
    id: initialData?.id || "",
    recipe_id: initialData?.recipe_id || "",
    model_ref: initialData?.model_ref || "",
    schedule: initialData?.schedule || "0 8 * * *",
    enabled: initialData?.enabled ?? true,
    inputs: initialData?.inputs || {},
  });
  
  const [error, setError] = useState<string | null>(null);
  const [saving, setSaving] = useState(false);
  const [cronString, setCronString] = useState("");

  useEffect(() => {
    api.dashboard().then(data => {
      setRecipes(data.recipes);
      if (data.recipes.length > 0 && !formData.recipe_id) {
        handleRecipeChange(data.recipes[0].id);
      } else if (formData.recipe_id) {
        // Fetch inputs for initial recipe
        api.recipe(formData.recipe_id).then(r => setSelectedRecipe(r));
      }
    });
  }, []);

  useEffect(() => {
    try {
      setCronString(cronstrue.toString(formData.schedule));
    } catch {
      setCronString("Invalid cron expression");
    }
  }, [formData.schedule]);

  const handleRecipeChange = async (recipeId: string) => {
    setFormData(prev => ({ ...prev, recipe_id: recipeId, inputs: {} }));
    try {
      const recipe = await api.recipe(recipeId);
      setSelectedRecipe(recipe);
    } catch (e) {
      console.error(e);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSaving(true);
    setError(null);
    try {
      await api.saveRoutine(formData);
      router.push("/routines");
    } catch (err: any) {
      setError(err.message);
      setSaving(false);
    }
  };

  const handleInputChange = (name: string, value: string) => {
    setFormData(prev => ({
      ...prev,
      inputs: { ...prev.inputs, [name]: value }
    }));
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      {error && (
        <div className="rounded-md border border-rose-300 bg-rose-50 p-4 text-sm dark:border-rose-700 dark:bg-rose-500/10">
          <p className="font-medium text-rose-800 dark:text-rose-200">Couldn't save:</p>
          <p className="mt-0.5 text-rose-700 dark:text-rose-300/80">{error}</p>
        </div>
      )}

      <Card>
        <CardContent className="p-6 space-y-5">
          <div className="flex items-center justify-between pb-2 border-b border-zinc-100 dark:border-zinc-800">
            <div>
              <h3 className="font-medium text-lg">General Settings</h3>
              <p className="text-sm text-muted-foreground">Configure the core routine properties.</p>
            </div>
            <div className="flex items-center gap-2">
              <Label htmlFor="enabled" className="text-sm cursor-pointer">
                {formData.enabled ? "Enabled" : "Disabled"}
              </Label>
              <Switch 
                id="enabled"
                checked={formData.enabled} 
                onCheckedChange={(c) => setFormData(prev => ({ ...prev, enabled: c }))} 
              />
            </div>
          </div>

          {!initialData && (
            <div>
              <Label htmlFor="id" className="mb-1.5 block">
                ID (Optional)
              </Label>
              <Input
                id="id"
                value={formData.id}
                onChange={e => setFormData(prev => ({ ...prev, id: e.target.value }))}
                pattern="[a-zA-Z0-9][a-zA-Z0-9_-]*"
                placeholder="Auto-generated if left blank"
                className="font-mono bg-zinc-50/50 dark:bg-zinc-900/50"
              />
            </div>
          )}

          <div className="grid sm:grid-cols-2 gap-5">
            <div>
              <Label htmlFor="recipe_id" className="mb-1.5 block">
                Recipe <span className="text-rose-500">*</span>
              </Label>
              <select
                id="recipe_id"
                value={formData.recipe_id}
                onChange={e => handleRecipeChange(e.target.value)}
                required
                className="block w-full rounded-md border-zinc-300 bg-white text-sm shadow-sm focus:border-primary focus:ring-primary dark:border-zinc-700 dark:bg-zinc-900 h-9 px-3"
              >
                {recipes.map(r => (
                  <option key={r.id} value={r.id}>{r.name} ({r.id})</option>
                ))}
              </select>
            </div>

            <div>
              <Label htmlFor="model_ref" className="mb-1.5 block">
                Model Override
              </Label>
              <Input
                id="model_ref"
                value={formData.model_ref}
                onChange={e => setFormData(prev => ({ ...prev, model_ref: e.target.value }))}
                placeholder="Leave blank for recipe default"
                className="font-mono bg-zinc-50/50 dark:bg-zinc-900/50"
              />
            </div>
          </div>

          <div>
            <Label htmlFor="schedule" className="mb-1.5 flex justify-between items-center">
              <span>Schedule (Cron) <span className="text-rose-500">*</span></span>
              <span className="text-xs text-primary font-medium">{cronString}</span>
            </Label>
            <Input
              id="schedule"
              value={formData.schedule}
              onChange={e => setFormData(prev => ({ ...prev, schedule: e.target.value }))}
              required
              placeholder="0 8 * * *"
              className="font-mono bg-zinc-50/50 dark:bg-zinc-900/50"
            />
          </div>
        </CardContent>
      </Card>

      {selectedRecipe && selectedRecipe.inputs.length > 0 && (
        <Card>
          <CardContent className="p-6 space-y-5">
            <div className="pb-2 border-b border-zinc-100 dark:border-zinc-800">
              <h3 className="font-medium text-lg">Recipe Inputs</h3>
              <p className="text-sm text-muted-foreground">Dynamic variables required by {selectedRecipe.name}.</p>
            </div>
            
            <div className="space-y-4">
              {selectedRecipe.inputs.map(input => (
                <div key={input.name}>
                  <Label className="mb-1.5 block">
                    {input.name} {input.required && <span className="text-rose-500">*</span>}
                  </Label>
                  <Input
                    value={formData.inputs[input.name] || ""}
                    onChange={e => handleInputChange(input.name, e.target.value)}
                    required={input.required}
                    placeholder={input.description}
                    className="bg-zinc-50/50 dark:bg-zinc-900/50"
                  />
                  {input.description && (
                    <p className="mt-1 text-xs text-zinc-500">{input.description}</p>
                  )}
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}

      <div className="flex gap-3 pt-2">
        <Button type="button" variant="outline" onClick={() => router.push("/routines")}>
          Cancel
        </Button>
        <Button type="submit" disabled={saving}>
          {saving ? "Saving..." : "Save Routine"}
        </Button>
      </div>
    </form>
  );
}
