import type { NextConfig } from "next";

const FASTAPI_BASE = process.env.FASTAPI_BASE ?? "http://127.0.0.1:8765";

const config: NextConfig = {
  // Same-origin proxy: browser hits /api/* on :3000, Next forwards to FastAPI
  // on :8765. Avoids CORS entirely and lets Server Components fetch /api/*
  // without needing absolute URLs.
  // beforeFiles: precedence over Next.js routes — used for paths where a
  // dynamic Next.js segment would otherwise win (e.g. /recipes/[id] would
  // match /recipes/new and 404 looking for a recipe named "new").
  // afterFiles: only fires when no Next.js page matches. Drop entries
  // one-by-one as each section gets a real Next.js page.
  async rewrites() {
    return {
      beforeFiles: [],
      afterFiles: [
        { source: "/api/:path*", destination: `${FASTAPI_BASE}/api/:path*` },
      ],
      fallback: [],
    };
  },
  // Page route was renamed /features → /components. Keep old bookmarks
  // working with a permanent redirect. Backend API path stays /api/v1/features.
  async redirects() {
    return [
      { source: "/features", destination: "/components", permanent: true },
      { source: "/features/:path*", destination: "/components/:path*", permanent: true },
      // Recipe detail is canonical at /recipes/:id (the run-flavoured page).
      // The Components/Recipe subtree was merged in; this keeps inbound links
      // working and the Components page's recipe-kind cards land where the
      // full content lives. Order matters — this must come AFTER the broader
      // /features/:path* rule, but Next evaluates these top-to-bottom so the
      // /features/recipe path will still be matched by the broader rule.
      // We also redirect from the new /components/recipe/:id path explicitly.
      { source: "/components/recipe/:id", destination: "/recipes/:id", permanent: true },
    ];
  },
};

export default config;
