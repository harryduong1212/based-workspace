import type { Metadata } from "next";

import { ThemeProvider } from "@/components/theme-provider";
import { ThemeToggle } from "@/components/theme-toggle";
import { HealthIndicator } from "@/components/health-indicator";
import { Sidebar } from "@/components/sidebar";
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
            <Sidebar />

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
