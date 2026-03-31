import json
import os
import re

# Centralized Paths
SCRIPTS_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(SCRIPTS_DIR)
PROFILES_FILE = os.path.join(SCRIPTS_DIR, "profiles.json")
SKILLS_MD = os.path.join(BASE_DIR, "SKILLS.md")
WORKFLOWS_MD = os.path.join(BASE_DIR, "WORKFLOWS.md")
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
    return get_root_ids(SKILLS_MD, r"\| \[([a-zA-Z0-9_-]+)\]\(.archived/skills/")

def get_valid_workflows():
    return get_root_ids(WORKFLOWS_MD, r"\| \[([a-zA-Z0-9_-]+)\]\(.archived/workflows/")
