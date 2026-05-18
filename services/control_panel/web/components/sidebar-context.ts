"use client";

import { createContext, useContext } from "react";

// Whether the sidebar is in icon-only (collapsed) mode. Provided by <Sidebar>,
// consumed by SidebarNav / SidebarRecentRuns so they can drop their labels.
export const SidebarCollapsedContext = createContext(false);

export const useSidebarCollapsed = () => useContext(SidebarCollapsedContext);
