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
};

export default config;
