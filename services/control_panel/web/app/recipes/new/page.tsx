"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { api } from "@/lib/api";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

export default function RecipeNewPage() {
  const router = useRouter();
  
  const [formData, setFormData] = useState({
    id: "",
    name: "",
    description: "",
    audience: "tech",
    execution_type: "prompt",
    tags: "",
  });
  
  const [error, setError] = useState<string | null>(null);
  const [creating, setCreating] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setCreating(true);
    setError(null);
    try {
      const res = await api.createRecipe(formData);
      router.push(`/recipes/${res.id}/edit`);
    } catch (err: any) {
      setError(err.message);
      setCreating(false);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  return (
    <div className="max-w-2xl">
      <div className="mb-6">
        <h1 className="text-2xl font-semibold tracking-tight">New recipe</h1>
        <p className="mt-1 text-sm text-zinc-500">
          Scaffolds a recipe with valid frontmatter and TODO-marked body sections. You'll land in the editor right after.
        </p>
      </div>

      {error && (
        <div className="mb-5 rounded-md border border-rose-300 bg-rose-50 p-4 text-sm dark:border-rose-700 dark:bg-rose-500/10">
          <p className="font-medium text-rose-800 dark:text-rose-200">Couldn't create:</p>
          <p className="mt-0.5 text-rose-700 dark:text-rose-300/80">{error}</p>
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-5">
        <div>
          <Label htmlFor="id" className="mb-1.5 block">
            id <span className="text-rose-500">*</span>
          </Label>
          <Input
            id="id"
            name="id"
            value={formData.id}
            onChange={handleChange}
            required
            pattern="[a-zA-Z0-9][a-zA-Z0-9_-]*"
            placeholder="kebab-case-id"
            className="font-mono"
          />
          <p className="mt-1 text-xs text-zinc-500">Lowercase letters, digits, dash, underscore. Becomes the file name.</p>
        </div>

        <div>
          <Label htmlFor="name" className="mb-1.5 block">
            name <span className="text-rose-500">*</span>
          </Label>
          <Input
            id="name"
            name="name"
            value={formData.name}
            onChange={handleChange}
            required
            placeholder="Human-readable Title"
          />
        </div>

        <div>
          <Label htmlFor="description" className="mb-1.5 block">
            description <span className="text-rose-500">*</span>
          </Label>
          <textarea
            id="description"
            name="description"
            rows={2}
            value={formData.description}
            onChange={handleChange}
            required
            placeholder="One sentence on what this recipe does and the moment it's useful."
            className="block w-full rounded-md border-zinc-300 bg-white text-sm shadow-sm placeholder:text-zinc-400 focus:border-indigo-500 focus:ring-indigo-500 dark:border-zinc-700 dark:bg-zinc-900"
          />
        </div>

        <div>
          <Label htmlFor="audience" className="mb-1.5 block">
            audience
          </Label>
          <select
            id="audience"
            name="audience"
            value={formData.audience}
            onChange={handleChange}
            className="block w-full rounded-md border-zinc-300 bg-white text-sm shadow-sm focus:border-indigo-500 focus:ring-indigo-500 dark:border-zinc-700 dark:bg-zinc-900"
          >
            <option value="tech">tech</option>
            <option value="ops">ops</option>
            <option value="exec">exec</option>
          </select>
        </div>

        <fieldset className="rounded-md border border-zinc-200 p-4 dark:border-zinc-800">
          <legend className="px-1 text-sm font-medium">
            execution type <span className="text-rose-500">*</span>
          </legend>
          
          <label className="flex items-start gap-2 py-1">
            <input
              type="radio"
              name="execution_type"
              value="prompt"
              checked={formData.execution_type === "prompt"}
              onChange={handleChange}
              className="mt-0.5 text-indigo-600 focus:ring-indigo-500"
            />
            <span className="text-sm">
              <span className="font-medium">prompt</span> — single LLM call
            </span>
          </label>
          
          <label className="flex items-start gap-2 py-1">
            <input
              type="radio"
              name="execution_type"
              value="agent"
              checked={formData.execution_type === "agent"}
              onChange={handleChange}
              className="mt-0.5 text-indigo-600 focus:ring-indigo-500"
            />
            <span className="text-sm">
              <span className="font-medium">agent</span> — multi-step LLM loop with tools
            </span>
          </label>
          
          <label className="flex items-start gap-2 py-1">
            <input
              type="radio"
              name="execution_type"
              value="workflow"
              checked={formData.execution_type === "workflow"}
              onChange={handleChange}
              className="mt-0.5 text-indigo-600 focus:ring-indigo-500"
            />
            <span className="text-sm">
              <span className="font-medium">workflow</span> — n8n orchestration
            </span>
          </label>
        </fieldset>

        <div>
          <Label htmlFor="tags" className="mb-1.5 block">
            tags
          </Label>
          <Input
            id="tags"
            name="tags"
            value={formData.tags}
            onChange={handleChange}
            placeholder="comma, separated, tags"
          />
          <p className="mt-1 text-xs text-zinc-500">Optional. Comma-separated.</p>
        </div>

        <div className="pt-2">
          <Button type="submit" disabled={creating}>
            {creating ? "Creating..." : "Create & open editor"}
          </Button>
        </div>
      </form>
    </div>
  );
}
