import json
import os
import re

# Centralized Paths
SCRIPTS_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(SCRIPTS_DIR)
PROFILES_FILE = os.path.join(SCRIPTS_DIR, "profiles.json")
SKILLS_MD = os.path.join(BASE_DIR, "docs", "SKILLS.md")
WORKFLOWS_MD = os.path.join(BASE_DIR, "docs", "WORKFLOWS.md")
TMP_DIR = os.path.join(BASE_DIR, "tmp")

def load_json(file_path):
    if not os.path.exists(file_path):
        return {}
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json(file_path, data):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def get_effective_set(p_name, profiles, key, visited=None):
    """Recursively resolves inherited skills or workflows."""
    if visited is None: visited = set()
    if p_name in visited: return set()
    visited.add(p_name)
    
    prof = profiles.get(p_name, {})
    res = set(prof.get(key, []))
    for parent in prof.get("extends", []):
        res.update(get_effective_set(parent, profiles, key, visited))
    return res

def get_root_ids(file_path, pattern):
    """Extracts IDs from a markdown table based on a regex pattern."""
    ids = set()
    if not os.path.exists(file_path):
        return ids
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
        ids.update(re.findall(pattern, content))
    return ids

def get_valid_skills():
    return get_root_ids(SKILLS_MD, r"\| \[([a-zA-Z0-9_-]+)\]\(\.?\.?/?\.archived/skills/")

def get_valid_workflows():
    return get_root_ids(WORKFLOWS_MD, r"\| \[([a-zA-Z0-9_-]+)\]\(\.?\.?/?\.archived/workflows/")
def format_label(text):
    """Standardizes casing for technical acronyms (e.g., Ai Ml -> AI ML, Api -> API)."""
    if not text:
        return text
    
    # Process the text: replace dashes with spaces and title case it first
    formatted = text.replace("-", " ").title()
    
    # Map of lower-case words to their standardized upper/proper case versions
    acronyms = {
        # A - C
        "abac": "ABAC",
        "adr": "ADR",         # Architecture Decision Record
        "ai": "AI",
        "api": "API",
        "arr": "ARR",         # Annual Recurring Revenue
        "aws": "AWS",
        "b2b": "B2B",
        "b2c": "B2C",
        "cac": "CAC",         # Customer Acquisition Cost
        "cd": "CD",
        "ci": "CI",
        "cli": "CLI",
        "cls": "CLS",         # Cumulative Layout Shift (SEO)
        "cors": "CORS",
        "cpc": "CPC",         # Cost Per Click (SEO/Marketing)
        "cqrs": "CQRS",
        "cro": "CRO",         # Conversion Rate Optimization
        "crud": "CRUD",
        "csrf": "CSRF",
        "css": "CSS",
        "ctr": "CTR",         # Click-Through Rate
        "cv": "CV",
        "cwv": "CWV",         # Core Web Vitals (SEO)
        "cx": "CX",           # Customer Experience

        # D - G
        "db": "DB",
        "dbaas": "DBaaS",
        "ddd": "DDD",
        "ddos": "DDoS",
        "docs": "Docs",
        "dom": "DOM",
        "eat": "E-A-T",       # Expertise, Authoritativeness, Trustworthiness (SEO)
        "eeat": "E-E-A-T",    # Experience, Expertise, Authoritativeness, Trustworthiness
        "elt": "ELT",
        "etl": "ETL",
        "faq": "FAQ",
        "fid": "FID",         # First Input Delay (SEO)
        "gcp": "GCP",
        "github": "GitHub",
        "gitlab": "GitLab",
        "graphql": "GraphQL",
        "grpc": "gRPC",

        # H - L
        "hig": "HIG",
        "html": "HTML",
        "http": "HTTP",
        "https": "HTTPS",
        "iac": "IaC",
        "icp": "ICP",         # Ideal Customer Profile (PM/Marketing)
        "idor": "IDOR",
        "inp": "INP",         # Interaction to Next Paint (SEO)
        "ios": "iOS",
        "ip": "IP",
        "json": "JSON",
        "jwt": "JWT",
        "k8s": "K8s",
        "kpi": "KPI",
        "lcp": "LCP",         # Largest Contentful Paint (SEO)
        "llm": "LLM",
        "lsi": "LSI",         # Latent Semantic Indexing (SEO)
        "ltv": "LTV",         # Life Time Value

        # M - O
        "mac": "Mac",
        "macos": "macOS",
        "mcp": "MCP",
        "mfa": "MFA",
        "ml": "ML",
        "mrr": "MRR",         # Monthly Recurring Revenue
        "mvc": "MVC",
        "mvp": "MVP",         # Minimum Viable Product
        "mysql": "MySQL",
        "n8n": "n8n",         # Ensure lowercase
        "nlp": "NLP",
        "nosql": "NoSQL",
        "npm": "npm",
        "okr": "OKR",
        "olap": "OLAP",
        "oltp": "OLTP",
        "orm": "ORM",
        "owasp": "OWASP",

        # P - S
        "paas": "PaaS",
        "pdf": "PDF",
        "pm": "PM",           # Product Management / Manager
        "postgres": "Postgres",
        "postgresql": "PostgreSQL",
        "pr": "PR",
        "prd": "PRD",         # Product Requirements Document
        "pwa": "PWA",
        "rag": "RAG",
        "rbac": "RBAC",
        "rest": "REST",
        "rfc": "RFC",         # Request for Comments
        "roi": "ROI",
        "saas": "SaaS",       # Special case
        "sam": "SAM",         # Serviceable Available Market
        "sdk": "SDK",
        "seo": "SEO",
        "serp": "SERP",       # Search Engine Results Page
        "sla": "SLA",
        "sli": "SLI",
        "slo": "SLO",
        "sme": "SME",         # Subject Matter Expert
        "som": "SOM",         # Serviceable Obtainable Market
        "spa": "SPA",
        "sql": "SQL",
        "ssh": "SSH",
        "ssl": "SSL",
        "sso": "SSO",

        # T - Z
        "tam": "TAM",         # Total Addressable Market
        "tcp": "TCP",
        "tldr": "TL;DR",
        "tls": "TLS",
        "toc": "TOC",         # Table of Contents
        "tpu": "TPU",
        "ui": "UI",
        "uri": "URI",
        "url": "URL",
        "ux": "UX",
        "vm": "VM",
        "vpc": "VPC",
        "waf": "WAF",
        "xml": "XML",
        "xss": "XSS"
    }
    
    # Split into words and replace based on the acronyms dictionary
    words = formatted.split()
    standardized_words = []
    for word in words:
        low_word = word.lower()
        if low_word in acronyms:
            standardized_words.append(acronyms[low_word])
        else:
            standardized_words.append(word)
            
    return " ".join(standardized_words)
