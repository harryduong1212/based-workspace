"use client";

import { Search, X } from "lucide-react";

import { cn } from "@/lib/utils";

// Small controlled search box. Parent owns the query string so it can filter
// its own list however it likes. Shows a clear (✕) affordance when non-empty.
export function SearchInput({
  value,
  onChange,
  placeholder = "Search…",
  className,
}: {
  value: string;
  onChange: (v: string) => void;
  placeholder?: string;
  className?: string;
}) {
  return (
    <div className={cn("relative w-full max-w-sm", className)}>
      <Search className="pointer-events-none absolute left-2.5 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
      <input
        type="text"
        role="searchbox"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder={placeholder}
        className="w-full rounded-md border bg-background pl-8 pr-8 py-1.5 text-sm outline-none transition-colors focus:border-primary focus:ring-1 focus:ring-primary/40"
      />
      {value && (
        <button
          type="button"
          onClick={() => onChange("")}
          aria-label="Clear search"
          className="absolute right-2 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground"
        >
          <X className="h-3.5 w-3.5" />
        </button>
      )}
    </div>
  );
}
