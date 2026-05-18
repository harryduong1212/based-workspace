"use client";

import Link from "next/link";
import { useState } from "react";
import { PanelLeftClose, PanelLeftOpen } from "lucide-react";

import { cn } from "@/lib/utils";
import { useIsomorphicLayoutEffect } from "@/lib/use-isomorphic-layout-effect";
import { SidebarNav } from "@/components/sidebar-nav";
import { SidebarRecentRuns } from "@/components/sidebar-recent-runs";
import { SidebarCollapsedContext } from "@/components/sidebar-context";

const STORAGE_KEY = "sidebarCollapsed";

// Owns the collapse state for the whole left rail. Collapsed = icon-only
// (w-16). State persists in localStorage; we start expanded on the server
// and only apply the stored value after hydration to avoid a width mismatch.
export function Sidebar() {
  const [collapsed, setCollapsed] = useState(false);
  const [hydrated, setHydrated] = useState(false);

  // Layout effect so the rail width is correct on first paint (no expand→
  // collapse flash for users who saved the collapsed preference).
  useIsomorphicLayoutEffect(() => {
    try {
      setCollapsed(localStorage.getItem(STORAGE_KEY) === "1");
    } catch {
      // localStorage can throw in locked-down iframes — stay expanded.
    }
    setHydrated(true);
  }, []);

  const toggle = () =>
    setCollapsed((c) => {
      const next = !c;
      try {
        localStorage.setItem(STORAGE_KEY, next ? "1" : "0");
      } catch {
        // no-op
      }
      return next;
    });

  const isCollapsed = hydrated && collapsed;

  return (
    <SidebarCollapsedContext.Provider value={isCollapsed}>
      <aside
        className={cn(
          "relative hidden md:flex md:flex-col shrink-0 border-r bg-muted/30 transition-[width] duration-200",
          isCollapsed ? "w-16" : "w-64",
        )}
      >
        <div
          className={cn(
            "flex items-center h-14 border-b border-border/50",
            isCollapsed ? "justify-center px-0" : "px-5",
          )}
        >
          <Link
            href="/"
            className="flex items-center gap-2.5 min-w-0 hover:opacity-80 transition-opacity"
            title="based-workspace control panel"
          >
            <span className="flex h-8 w-8 items-center justify-center rounded-md bg-gradient-to-br from-indigo-500 to-violet-600 text-white shadow-sm shrink-0">
              <svg viewBox="0 0 20 20" fill="currentColor" className="h-4 w-4">
                <path d="M10 2 2 6l8 4 8-4-8-4Zm0 6.4L2 4.4v8l8 4 8-4v-8l-8 4Z" />
              </svg>
            </span>
            {!isCollapsed && (
              <span className="flex flex-col leading-tight min-w-0">
                <span className="text-sm font-semibold truncate">based-workspace</span>
                <span className="text-[10px] uppercase tracking-wider text-muted-foreground">
                  control panel
                </span>
              </span>
            )}
          </Link>
        </div>

        {/* Floating pill on the right divider, vertically centered. Sits half
         * outside the aside (-right-3) so the border line runs through it. */}
        <button
          type="button"
          onClick={toggle}
          aria-label={isCollapsed ? "Expand sidebar" : "Collapse sidebar"}
          title={isCollapsed ? "Expand sidebar" : "Collapse sidebar"}
          className="absolute top-1/2 -right-3 -translate-y-1/2 z-20 flex h-6 w-6 items-center justify-center rounded-full border bg-background text-muted-foreground hover:text-foreground hover:bg-accent shadow-sm transition-colors"
        >
          {isCollapsed ? (
            <PanelLeftOpen className="h-3.5 w-3.5" />
          ) : (
            <PanelLeftClose className="h-3.5 w-3.5" />
          )}
        </button>

        <SidebarNav />
        <SidebarRecentRuns />

        {!isCollapsed && (
          <div className="px-5 py-3 border-t border-border/50 text-[10px] text-muted-foreground flex items-center justify-between bg-muted/10">
            <span>v0.2 · next.js</span>
            <span className="text-[9px] uppercase tracking-wider">local</span>
          </div>
        )}
      </aside>
    </SidebarCollapsedContext.Provider>
  );
}
