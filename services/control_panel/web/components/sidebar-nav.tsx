"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { Boxes, LayoutGrid, Play, Clock, Package } from "lucide-react";

import { cn } from "@/lib/utils";
import { useSidebarCollapsed } from "@/components/sidebar-context";

const NAV = [
  { href: "/", label: "Overview", icon: LayoutGrid },
  { href: "/components", label: "Components", icon: Package },
  { href: "/recipes", label: "Recipes", icon: Boxes },
  { href: "/routines", label: "Routines", icon: Clock },
  { href: "/runs", label: "Runs", icon: Play },
];

export function SidebarNav() {
  const pathname = usePathname();
  const collapsed = useSidebarCollapsed();
  return (
    <nav
      className={cn(
        "flex-1 py-4 space-y-0.5 text-sm",
        collapsed ? "px-2" : "px-3",
      )}
    >
      {NAV.map((item) => {
        const active =
          item.href === "/" ? pathname === "/" : pathname === item.href || pathname.startsWith(`${item.href}/`);
        const Icon = item.icon;
        return (
          <Link
            key={item.href}
            href={item.href}
            title={collapsed ? item.label : undefined}
            className={cn(
              "flex items-center rounded-md transition-colors",
              collapsed ? "justify-center px-0 py-2.5" : "gap-2.5 px-3 py-2",
              active
                ? "bg-primary/10 text-foreground font-medium"
                : "text-muted-foreground hover:bg-accent hover:text-foreground",
            )}
          >
            <Icon className="h-4 w-4 shrink-0" />
            {!collapsed && <span>{item.label}</span>}
          </Link>
        );
      })}
    </nav>
  );
}
