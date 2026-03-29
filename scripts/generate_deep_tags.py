"""
Deep Tag Extraction & Registry Update
======================================
Reads actual SKILL.md instruction files to extract operational tags
(technologies, protocols, core actions) and updates category registry.json files.

Usage:
    python scripts/generate_deep_tags.py
    python scripts/generate_deep_tags.py --dry-run       # Preview without writing
    python scripts/generate_deep_tags.py --category ai-llm-agent-development  # Single category
"""

import json
import re
import sys
import time
from collections import Counter
from pathlib import Path
from argparse import ArgumentParser

# ─── Configuration ────────────────────────────────────────────────────────────
SKILLS_ROOT = Path(__file__).resolve().parent.parent / ".archived" / "skills"
MIN_TAGS = 4
MAX_TAGS = 8

# ─── Stop Words ───────────────────────────────────────────────────────────────
# Broad set of filler words that carry no operational signal.
STOP_WORDS = frozenset([
    # English articles, prepositions, conjunctions
    "the", "a", "an", "and", "or", "but", "of", "to", "in", "on", "at", "by",
    "for", "with", "from", "as", "is", "it", "be", "are", "was", "were", "been",
    "has", "have", "had", "do", "does", "did", "not", "no", "if", "so", "that",
    "this", "these", "those", "than", "then", "when", "what", "which", "who",
    "how", "where", "why", "can", "could", "will", "would", "shall", "should",
    "may", "might", "must", "am", "its", "your", "our", "their", "my",
    "also", "just", "about", "each", "every", "all", "any", "some", "such",
    "more", "most", "other", "into", "over", "between", "through", "during",
    "before", "after", "above", "below", "up", "down", "out", "off", "only",
    "both", "either", "neither", "while", "since", "until", "because",
    "very", "too", "here", "there", "now", "well", "still", "even",
    # Common AI-boilerplate words that appear everywhere
    "you", "use", "using", "used", "user", "users",
    "skill", "skills", "expert", "specialist", "tool", "tools",
    "system", "systems", "based", "level", "approach", "following",
    "create", "creating", "build", "building", "make", "making",
    "implement", "implementing", "implementation", "implementations",
    "provide", "providing", "provides", "support", "supports", "supporting",
    "include", "includes", "including", "work", "working", "works",
    "ensure", "ensures", "ensuring", "maintain", "maintaining",
    "manage", "managing", "management", "handle", "handling",
    "design", "designing", "develop", "developing", "development",
    "apply", "applying", "example", "examples", "like", "etc",
    "key", "best", "practice", "practices", "common", "step",
    "need", "needs", "new", "first", "one", "two", "three",
    "see", "note", "file", "files", "code", "project",
    "specific", "general", "guide", "run", "set", "get",
    "type", "types", "data", "way", "ways", "case", "cases",
    "good", "bad", "important", "required", "optional",
    "section", "description", "name", "path", "value", "values",
    "line", "lines", "end", "start", "begin", "check",
    "right", "left", "true", "false", "yes", "default",
    "production", "ready", "comprehensive", "automated", "autonomous",
    # YAML frontmatter noise
    "risk", "safe", "unknown", "community", "self", "source", "date_added",
])

# ─── Known Technology / Framework Tokens ──────────────────────────────────────
# These are high-signal keywords that should always be promoted when found.
KNOWN_TECH = frozenset([
    # Languages
    "python", "typescript", "javascript", "rust", "golang", "java", "csharp",
    "ruby", "swift", "kotlin", "php", "dart", "elixir", "scala", "lua",
    "solidity", "haskell", "zig", "cpp", "sql", "graphql", "html", "css",
    # Frontend
    "react", "nextjs", "angular", "vue", "svelte", "nuxt", "astro", "remix",
    "gatsby", "tailwind", "tailwindcss", "bootstrap", "shadcn", "radix",
    "storybook", "webpack", "vite", "esbuild", "rollup", "turbopack",
    # Backend / Runtime
    "nodejs", "deno", "bun", "express", "fastapi", "django", "flask",
    "spring", "nestjs", "rails", "laravel", "gin", "echo", "actix",
    "fastify", "hono", "elysia", "koa",
    # Database
    "postgres", "postgresql", "mysql", "sqlite", "mongodb", "redis",
    "dynamodb", "cassandra", "neo4j", "supabase", "firebase", "prisma",
    "drizzle", "typeorm", "sequelize", "knex", "sqlalchemy", "mongoose",
    # Cloud / Infra
    "aws", "azure", "gcp", "docker", "podman", "kubernetes", "k8s",
    "terraform", "pulumi", "ansible", "nginx", "caddy", "traefik",
    "cloudflare", "vercel", "netlify", "heroku", "digitalocean", "fly",
    # AI / ML
    "openai", "anthropic", "claude", "gemini", "llama", "mistral",
    "langchain", "langgraph", "langfuse", "crewai", "autogen",
    "huggingface", "pytorch", "tensorflow", "jax", "onnx", "mlflow",
    "ollama", "vllm", "chromadb", "pinecone", "weaviate", "qdrant",
    "pydantic", "llamaindex",
    # Auth / Security
    "oauth", "jwt", "saml", "oidc", "clerk", "auth0", "keycloak",
    "owasp", "nmap", "burp", "metasploit", "ghidra", "wireshark",
    # Protocols / Standards
    "rest", "grpc", "websocket", "mqtt", "amqp", "http", "https",
    "smtp", "snmp", "ssh", "ftp", "dns", "tcp", "udp",
    "json", "yaml", "toml", "xml", "protobuf", "avro", "parquet",
    "wcag", "aria",
    # Testing
    "jest", "vitest", "playwright", "cypress", "pytest", "mocha",
    "selenium", "puppeteer",
    # CI/CD / Tools
    "github", "gitlab", "bitbucket", "jenkins", "circleci",
    "npm", "pnpm", "yarn", "pip", "cargo", "maven", "gradle",
    # Payments
    "stripe", "plaid", "paypal", "braintree",
    # Blockchain
    "ethereum", "solana", "hardhat", "foundry", "ethers", "web3",
    # Data / ETL
    "airflow", "dbt", "spark", "kafka", "rabbitmq", "celery",
    "pandas", "numpy", "polars", "dask",
    # Mobile
    "flutter", "swiftui", "jetpack", "expo", "capacitor", "ionic",
    # MCP / Agent
    "mcp", "rag", "embeddings", "vector", "chunking",
    # Automation
    "n8n", "zapier", "make", "workato",
    # Game
    "unity", "unreal", "godot", "pygame", "phaser",
])

# ─── Extraction Patterns ─────────────────────────────────────────────────────
# Regex to pull technology-like tokens from code blocks, headings, and prose.
RE_BACKTICK_TOKEN = re.compile(r"`([A-Za-z][\w.\-/]+)`")       # `fastapi`, `npm run build`
RE_HEADING_WORDS  = re.compile(r"^#{1,4}\s+(.+)$", re.MULTILINE)
RE_CAPITALIZED    = re.compile(r"\b([A-Z][a-zA-Z]{2,})\b")     # PascalCase words
RE_WORD           = re.compile(r"\b[a-z][a-z0-9\-]{2,}\b")     # lowercase hyphenated tokens
RE_ACTIONS        = re.compile(                                 # high-signal verbs/nouns
    r"\b(scraping|fuzzing|load[- ]testing|benchmarking|profiling|monitoring|"
    r"scaffolding|refactoring|migrating|deploying|provisioning|orchestrating|"
    r"containerizing|caching|indexing|pagination|throttling|rate[- ]limiting|"
    r"authentication|authorization|serialization|deserialization|"
    r"encryption|decryption|hashing|signing|tokenization|"
    r"validation|sanitization|normalization|interpolation|"
    r"observability|tracing|logging|alerting|"
    r"code[- ]splitting|tree[- ]shaking|lazy[- ]loading|"
    r"hydration|prerendering|streaming|"
    r"fine[- ]tuning|inference|embedding|retrieval|"
    r"crawling|parsing|templating|rendering|routing|"
    r"mocking|stubbing|snapshot[- ]testing|"
    r"linting|formatting|bundling|transpiling|compiling)\b",
    re.IGNORECASE
)

# ─── Strip boilerplate from YAML frontmatter ──────────────────────────────────
RE_FRONTMATTER = re.compile(r"^---\s*\n.*?\n---\s*\n", re.DOTALL)


def strip_boilerplate(text: str) -> str:
    """Remove YAML frontmatter and generic AI intro sentences."""
    text = RE_FRONTMATTER.sub("", text)
    # Remove common boilerplate opening lines
    boilerplate_patterns = [
        r"^You are an? .*?(?:expert|specialist|assistant).*?\.\s*",
        r"^This skill (?:should be|is) used when.*?\.\s*",
        r"^## When to Use This Skill\s*\n(?:- .*\n)*",
    ]
    for pat in boilerplate_patterns:
        text = re.sub(pat, "", text, flags=re.MULTILINE | re.IGNORECASE)
    return text


def extract_tags_from_content(content: str, skill_id: str) -> list[str]:
    """
    Extract high-signal tags from SKILL.md content using lightweight NLP.
    Returns a deduplicated list of 4-8 tags sorted by relevance score.
    """
    content = strip_boilerplate(content)
    scores: Counter = Counter()

    # ── 1. Known tech tokens from backtick mentions (highest signal) ──────
    for match in RE_BACKTICK_TOKEN.finditer(content):
        token = match.group(1).lower().split("/")[0].split(".")[0]  # `@angular/core` → angular
        token = token.strip("-").strip("@")
        if token in KNOWN_TECH:
            scores[token] += 5
        elif len(token) > 2 and token not in STOP_WORDS:
            scores[token] += 2

    # ── 2. Headings carry strong signal ───────────────────────────────────
    for match in RE_HEADING_WORDS.finditer(content):
        heading = match.group(1)
        for word in RE_WORD.findall(heading.lower()):
            if word not in STOP_WORDS:
                if word in KNOWN_TECH:
                    scores[word] += 4
                else:
                    scores[word] += 3

    # ── 3. PascalCase names (class names, framework names) ────────────────
    for match in RE_CAPITALIZED.finditer(content):
        token = match.group(1).lower()
        if token in KNOWN_TECH:
            scores[token] += 4
        elif token not in STOP_WORDS and len(token) > 2:
            scores[token] += 1

    # ── 4. Action/operation verbs (specific, operational signal) ──────────
    for match in RE_ACTIONS.finditer(content):
        action = match.group(1).lower().replace(" ", "-")
        scores[action] += 4

    # ── 5. Repeated lowercase tokens in prose (frequency signal) ──────────
    all_words = RE_WORD.findall(content.lower())
    word_freq = Counter(w for w in all_words if w not in STOP_WORDS and len(w) > 2)
    for word, freq in word_freq.items():
        if freq >= 3:
            bonus = 2 if word in KNOWN_TECH else 1
            scores[word] += bonus

    # ── 6. Inject tokens from the skill ID itself ─────────────────────────
    for part in skill_id.split("-"):
        if part and part not in STOP_WORDS and len(part) > 1:
            if part in KNOWN_TECH:
                scores[part] += 3
            else:
                scores[part] += 2

    # ── 7. Clean, deduplicate, sort by score, and return top N ────────────
    # Remove very short or numeric-only tokens
    scores = Counter({
        k: v for k, v in scores.items()
        if len(k) > 1 and not k.isdigit() and k not in STOP_WORDS
    })

    top_tags = [tag for tag, _ in scores.most_common(MAX_TAGS)]

    # Ensure minimum tags by padding from skill_id parts
    if len(top_tags) < MIN_TAGS:
        for part in skill_id.split("-"):
            if part and part not in top_tags and part not in STOP_WORDS and len(part) > 1:
                top_tags.append(part)
            if len(top_tags) >= MIN_TAGS:
                break

    return top_tags[:MAX_TAGS]


def process_category(category_dir: Path, dry_run: bool = False) -> dict:
    """Process a single category directory. Returns stats dict."""
    registry_file = category_dir / "registry.json"
    stats = {"category": category_dir.name, "total": 0, "tagged": 0, "missing": 0, "errors": 0}

    if not registry_file.exists():
        print(f"  ⚠ No registry.json in {category_dir.name}, skipping.")
        return stats

    with open(registry_file, "r", encoding="utf-8") as f:
        registry = json.load(f)

    skills = registry.get("skills", [])
    stats["total"] = len(skills)

    for i, skill in enumerate(skills):
        skill_id = skill["id"]
        skill_md_path = category_dir / skill_id / "SKILL.md"

        progress = f"  [{i+1:3d}/{len(skills)}]"

        if not skill_md_path.exists():
            print(f"{progress} ⚠ MISSING: {skill_id}/SKILL.md")
            stats["missing"] += 1
            continue

        try:
            content = skill_md_path.read_text(encoding="utf-8", errors="replace")
            tags = extract_tags_from_content(content, skill_id)
            skill["tags"] = tags
            stats["tagged"] += 1
            tag_str = ", ".join(tags[:5])
            ellipsis = "..." if len(tags) > 5 else ""
            print(f"{progress} ✓ {skill_id:<45s} → [{tag_str}{ellipsis}]")
        except Exception as e:
            print(f"{progress} ✗ ERROR {skill_id}: {e}")
            stats["errors"] += 1

    if not dry_run:
        with open(registry_file, "w", encoding="utf-8") as f:
            json.dump(registry, f, indent=2, ensure_ascii=False)
        print(f"  💾 Wrote {registry_file}")

    return stats


def main():
    parser = ArgumentParser(description="Deep Tag Extraction for Skills Registry")
    parser.add_argument("--dry-run", action="store_true", help="Preview without writing JSON files")
    parser.add_argument("--category", type=str, default=None, help="Process only a specific category folder")
    args = parser.parse_args()

    print("=" * 72)
    print("  Deep Tag Extraction & Registry Update")
    print(f"  Skills root: {SKILLS_ROOT}")
    print(f"  Mode: {'DRY RUN (no writes)' if args.dry_run else 'LIVE (will overwrite registry.json files)'}")
    print("=" * 72)
    print()

    if not SKILLS_ROOT.exists():
        print(f"ERROR: Skills directory not found: {SKILLS_ROOT}")
        sys.exit(1)

    start_time = time.time()
    all_stats = []

    # Collect category directories
    if args.category:
        target = SKILLS_ROOT / args.category
        if not target.is_dir():
            print(f"ERROR: Category directory not found: {target}")
            sys.exit(1)
        categories = [target]
    else:
        categories = sorted([
            d for d in SKILLS_ROOT.iterdir()
            if d.is_dir() and (d / "registry.json").exists()
        ])

    total_categories = len(categories)
    print(f"Found {total_categories} categories to process.\n")

    for idx, cat_dir in enumerate(categories):
        print(f"━━━ [{idx+1}/{total_categories}] {cat_dir.name} ━━━")
        stats = process_category(cat_dir, dry_run=args.dry_run)
        all_stats.append(stats)
        print()

    # ── Summary ───────────────────────────────────────────────────────────
    elapsed = time.time() - start_time
    total_skills = sum(s["total"] for s in all_stats)
    total_tagged = sum(s["tagged"] for s in all_stats)
    total_missing = sum(s["missing"] for s in all_stats)
    total_errors = sum(s["errors"] for s in all_stats)

    print("=" * 72)
    print("  SUMMARY")
    print("=" * 72)
    print(f"  Categories processed : {total_categories}")
    print(f"  Total skills         : {total_skills}")
    print(f"  Successfully tagged  : {total_tagged}")
    print(f"  Missing SKILL.md     : {total_missing}")
    print(f"  Errors               : {total_errors}")
    print(f"  Elapsed time         : {elapsed:.1f}s")
    print("=" * 72)

    if args.dry_run:
        print("\n  ℹ DRY RUN complete. No files were modified.")
        print("  Re-run without --dry-run to apply changes.\n")


if __name__ == "__main__":
    main()
