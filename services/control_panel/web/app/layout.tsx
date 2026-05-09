import type { Metadata } from "next";
import Link from "next/link";

import { ThemeProvider } from "@/components/theme-provider";
import { ThemeToggle } from "@/components/theme-toggle";
import { HealthIndicator } from "@/components/health-indicator";
import { SidebarNav } from "@/components/sidebar-nav";
import { SidebarRecentRuns } from "@/components/sidebar-recent-runs";
import { Toaster } from "@/components/ui/sonner";

import "./globals.css";

export const metadata: Metadata = {
  title: "Control Panel — based-workspace",
  description: "Browse and manage recipes, connectors, and routines.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className="min-h-screen antialiased">
        <ThemeProvider attribute="class" defaultTheme="system" enableSystem>
          <div className="flex min-h-screen">
            <aside className="hidden md:flex md:flex-col w-64 shrink-0 border-r bg-muted/30">
              <Link href="/" className="flex items-center gap-2.5 px-5 h-14 border-b border-border/50 hover:bg-muted/50 transition-colors">
                <span className="flex h-8 w-8 items-center justify-center rounded-md bg-gradient-to-br from-indigo-500 to-violet-600 text-white shadow-sm">
                  <svg viewBox="0 0 20 20" fill="currentColor" className="h-4 w-4">
                    <path d="M10 2 2 6l8 4 8-4-8-4Zm0 6.4L2 4.4v8l8 4 8-4v-8l-8 4Z" />
                  </svg>
                </span>
                <span className="flex flex-col leading-tight">
                  <span className="text-sm font-semibold">based-workspace</span>
                  <span className="text-[10px] uppercase tracking-wider text-muted-foreground">
                    control panel
                  </span>
                </span>
              </Link>

              <SidebarNav />
              <SidebarRecentRuns />

              <div className="px-5 py-3 border-t border-border/50 text-[10px] text-muted-foreground flex items-center justify-between bg-muted/10">
                <span>v0.2 · next.js</span>
                <span className="text-[9px] uppercase tracking-wider">local</span>
              </div>
            </aside>

            <div className="flex-1 flex flex-col min-w-0">
              {/* Transparent Floating Header for Utility Icons */}
              <header className="absolute top-0 right-0 z-10 h-14 px-4 sm:px-6 flex items-center gap-3">
                <HealthIndicator />
                <ThemeToggle />
              </header>
              <main className="flex-1 overflow-x-hidden pt-10">
                <div className="mx-auto max-w-6xl px-4 sm:px-6 py-8">{children}</div>
              </main>
            </div>
          </div>
          <Toaster richColors closeButton position="bottom-right" />
        </ThemeProvider>
      </body>
    </html>
  );
}
