import os
import json
import requests
import time
import argparse
import re

# --- Configuration ---
LM_STUDIO_BASE_URL = "http://localhost:11434/v1"
BASE_SKILLS_DIR = ".archived/skills"
DOMAIN_MAPPING_FILE = os.path.join("scripts", "resources", "domain_to_skills_mapping.json")

# --- Model Routing Maps ---
QWEN_CATEGORIES = [
    "backend-api", "backend-arch", "backend-core",
    "data-admin", "data-nosql", "data-orm", "data-pipelines", "data-sql",
    "devops-cicd", "devops-cli", "devops-cloud", "devops-containers", 
    "devops-iac", "devops-os-scripting", "devops-quality",
    "mobile-gaming-debugging", "mobile-gaming-gaming", "mobile-gaming-mobile",
    "quality-code-review", "quality-debugging", "quality-documentation", 
    "quality-observability", "quality-testing",
    "security-compliance", "security-defensive", "security-offensive", "security-testing"
]

LLAMA_CATEGORIES = [
    "ai-ml-agents", "ai-ml-evaluation", "ai-ml-mcp", "ai-ml-memory", 
    "ai-ml-prompting", "ai-ml-science",
    "automation-bots", "automation-n8n", "automation-scraping", "automation-workflows",
    "frontend-3d-anim", "frontend-core", "frontend-security", "frontend-seo", "frontend-ui",
    "design-apple-hig", "design-core", "design-ux-ui", "design-visuals",
    "business-content", "business-health", "business-product", "business-seo",
    "documentation-planning", "documentation-writing",
    "productivity-office"
]

SYSTEM_PROMPT = """You are an expert technical auditor for `based-workspace`. Your task is to analyze a raw AI skill file, extract metadata, and rigorously calculate a quality score.

Analyze the provided file content and extract the following:
1. "summary": A concise, 1-2 sentence description of the skill.
2. "tags": An array of 3-9 technical keywords.
3. "trigger_conditions": An array of 2-3 specific scenarios to use this skill.
4. "anti_triggers": An array of 1-2 scenarios where this skill should NOT be used.
5. "dependencies": Required external infrastructure (e.g., "n8n", "postgres", "docker"). Do not list npm packages.
6. "mcp_tools": Model Context Protocol tools EXPLICITLY named (e.g., "postgres-memory", "atom8n"). STRICT RULE: Do NOT include standard frameworks (React, Three.js) or languages. If none, output [].
7. "depends_on": An array of other INTERNAL workspace skills or workflows explicitly mentioned as prerequisites or closely related requirements (e.g., "python-pro", "workspace-configurator"). If none are mentioned, output [].
8. "execution_complexity": Exactly one of: "low", "medium", or "high".
9. "evaluation_ledger": You MUST act as a deterministic scoring engine. Calculate the score step-by-step using ONLY this rubric.
   - "base_score": Always starts at 30.
   - "points_for_code": Add 20 if the file contains explicit code blocks, CLI commands, or YAML configs. Otherwise 0.
   - "points_for_boundaries": Add 20 if the file explicitly details "Anti-Patterns" or what NOT to do. Otherwise 0.
   - "points_for_actionability": Add 20 if the file contains step-by-step pipelines, workflows, or decision trees. Otherwise 0.
   - "points_for_dependencies": Add 10 if the file explicitly states hardware, tool, or environment dependencies. Otherwise 0.
   - "penalty_for_fluff": Subtract 20 if the file is purely theoretical and lacks practical implementation details. Otherwise 0.
   - "final_score": Sum the values above (Min 0, Max 100).

CRITICAL RULE: Output ONLY valid JSON. Do not include markdown formatting like ```json.

Format template:
{
  "summary": "...",
  "tags": ["..."],
  "trigger_conditions": ["..."],
  "anti_triggers": ["..."],
  "dependencies": ["..."],
  "mcp_tools": ["..."],
  "depends_on": ["..."],
  "execution_complexity": "...",
  "evaluation_ledger": {
    "base_score": 30,
    "points_for_code": 20,
    "points_for_boundaries": 20,
    "points_for_actionability": 0,
    "points_for_dependencies": 10,
    "penalty_for_fluff": 0,
    "final_score": 80
  }
}
"""

def check_connection():
    try:
        response = requests.get(f"{LM_STUDIO_BASE_URL}/models", timeout=5)
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException:
        return False

def is_valid_md_skill(file_path):
    if os.path.basename(file_path) != 'SKILL.md':
        return False
    if not os.path.exists(file_path):
        return False
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            first_line = f.readline().strip()
            return first_line == '---'
    except Exception:
        return False

def load_existing_mapping(output_file):
    if os.path.exists(output_file):
        with open(output_file, 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    return {}

def save_mapping(mapping, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(mapping, f, indent=4)

def load_valid_workspace_skills(mapping_file):
    """Loads all valid skill IDs into a single flat set. No domain checking."""
    valid_skills = set()
    if os.path.exists(mapping_file):
        with open(mapping_file, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
                for category, skills in data.items():
                    valid_skills.update([s.lower() for s in skills])
                print(f"[+] Loaded {len(valid_skills)} valid skills from domain mapping.")
            except json.JSONDecodeError:
                print(f"  [!] Failed to parse {mapping_file}")
    else:
        print(f"  [!] Warning: {mapping_file} not found. Validation will be bypassed.")
    return valid_skills

def call_lm_studio(file_content):
    payload = {
        "model": "local-model",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"File Content:\n\n{file_content}"}
        ],
        "temperature": 0.0,
        "stream": False
    }
    
    try:
        response = requests.post(f"{LM_STUDIO_BASE_URL}/chat/completions", json=payload, timeout=90)
        response.raise_for_status()
        data = response.json()
        raw_text = data["choices"][0]["message"]["content"].strip()
        if "<think>" in raw_text:
            raw_text = re.sub(r'<think>.*?</think>', '', raw_text, flags=re.DOTALL).strip()
        if raw_text.startswith("```json"):
            raw_text = raw_text[7:-3].strip()
        elif raw_text.startswith("```"):
            raw_text = raw_text[3:-3].strip()
        return json.loads(raw_text)
    except Exception as e:
        print(f"  [!] Error parsing LM Studio response: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description="Extract skill metadata using LM Studio.")
    parser.add_argument("--model", type=str, choices=["qwen", "llama", "both"], default="both", help="Target model categories (qwen, llama, or both)")
    parser.add_argument("--retry-errors", action="store_true", help="Process files with 'error' in JSON")
    args = parser.parse_args()

    print("=== Checking Connection ===")
    lm_studio_available = check_connection()
    if not lm_studio_available:
        print(f"[!] WARNING: Cannot connect to server at {LM_STUDIO_BASE_URL}")
        print("[!] Operating in OFFLINE mode. Statically parsing dependencies and marking for later LLM review.\n")
    else:
        print("[+] Connected successfully.\n")

    valid_skills_set = load_valid_workspace_skills(DOMAIN_MAPPING_FILE)

    if args.model == "qwen":
        target_categories = QWEN_CATEGORIES
    elif args.model == "llama":
        target_categories = LLAMA_CATEGORIES
    else:
        target_categories = QWEN_CATEGORIES + LLAMA_CATEGORIES

    output_file = f"{args.model}_stack_skill_mapping.json"
    mapping = load_existing_mapping(output_file)
    all_files = []
    
    if args.retry_errors:
        for json_path, metadata in mapping.items():
            if isinstance(metadata, dict) and "error" in metadata:
                if any(cat in json_path for cat in target_categories):
                    all_files.append(json_path)
    else:
        for category in target_categories:
            category_path = os.path.join(BASE_SKILLS_DIR, category)
            if not os.path.exists(category_path):
                continue
            for root, _, files in os.walk(category_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    if is_valid_md_skill(file_path):
                        all_files.append(file_path.replace("\\", "/"))

    total_files = len(all_files)
    if total_files == 0:
        print("No files to process. Exiting.")
        return
        
    print(f"Processing {total_files} files.\nOutput saved to: {output_file}\n")
    
    for i, file_path in enumerate(all_files):
        normalized_path = file_path
        
        # Skip successfully processed files
        if not args.retry_errors and normalized_path in mapping and "error" not in mapping[normalized_path]:
            print(f"[{i+1:04d}/{total_files}] Skipping (Already successfully processed): {normalized_path}")
            continue
            
        print(f"[{i+1:04d}/{total_files}] Analyzing: {normalized_path}")
        
        try:
            os_friendly_path = os.path.normpath(normalized_path)
            with open(os_friendly_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception:
            print("  [!] File unreadable. Skipping.")
            continue
            
        current_skill_id = os.path.basename(os.path.dirname(os_friendly_path)).lower()
        
        # PRE-FILTER: Exact Token Match (Case-Insensitive)
        # Convert content to lowercase to ensure skills written as "API-Documentation" match "api-documentation"
        content_tokens = set(re.findall(r'[a-z0-9_\-]+', content.lower()))
        
        text_matched_dependencies = []
        if valid_skills_set:
            for skill_candidate in valid_skills_set:
                if skill_candidate != current_skill_id:
                    # EXACT MATCH: The candidate must exist exactly in the parsed tokens.
                    if skill_candidate in content_tokens:
                        text_matched_dependencies.append(skill_candidate)

        # FAST-PATH
        if len(text_matched_dependencies) == 0:
            print("  [~] Fast-Path: No internal dependencies found (Exact Match). Excluded from output.")
            if normalized_path in mapping:
                del mapping[normalized_path]
                save_mapping(mapping, output_file)
            continue

        print(f"  [>] Static Scan found {len(text_matched_dependencies)} explicit dependencies.")
        
        # Baseline result using the statically parsed dependencies
        final_result = {
            "depends_on": text_matched_dependencies
        }

        if lm_studio_available:
            print("  [>] LM Studio online. Passing to LLM for contextual analysis...")
            if len(content) > 20000:
                content = content[:20000] 
                
            llm_result = call_lm_studio(content)
            
            if llm_result:
                filtered_depends = []
                if "depends_on" in llm_result and isinstance(llm_result["depends_on"], list):
                    for dep in llm_result["depends_on"]:
                        dep_lower = str(dep).lower()
                        if dep_lower in valid_skills_set and dep_lower != current_skill_id:
                            filtered_depends.append(dep_lower)
                        else:
                            print(f"  [~] Filtered invalid/self dependency from LLM: '{dep}'")
                
                llm_result["depends_on"] = filtered_depends
                final_result = llm_result
                
                # HIGHLIGHT LOGIC
                if len(filtered_depends) == 0:
                    final_result["depends_on"] = ["Dependency candidate found."]
                    final_result["error"] = "Needs manual review: Text exactly matches valid skills, but LLM extracted none."
                    print("  [!] HIGHLIGHT: Text exactly matches skills, but LLM extracted none. Saved placeholder for review.")
                else:
                    print(f"  [+] Success. LLM extracted {len(filtered_depends)} dependencies.")
            else:
                final_result["error"] = "Failed to extract metadata via LLM"
                print("  [-] Failed LLM extraction")
        else:
            print("  [-] LM Studio is offline. Saving static scan results.")
            final_result["error"] = "Offline Mode: Dependencies extracted via exact text-match only. Run again to generate missing metadata."

        mapping[normalized_path] = final_result
        save_mapping(mapping, output_file)
        
        time.sleep(0.5)

if __name__ == "__main__":
    main()