import os
import re
import shutil
import json
import argparse
from datetime import datetime
from pathlib import Path
import tags_generator
import llm_utils
import utils

# Configuration
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
SKILLS_MD = ROOT_DIR / "docs" / "SKILLS.md"
SKILLS_DIR = ROOT_DIR / ".archived" / "skills"
NEW_SKILLS_DIR = ROOT_DIR / ".archived" / "skills_reorganized"
ROOT_REGISTRY_JSON = SKILLS_DIR / "registry.json"
DOMAIN_MAPPING_FILE = ROOT_DIR / "scripts" / "resources" / "domain_to_skills_mapping.json"
BASED_SKILLS_FILE = ROOT_DIR / "scripts" / "resources" / "based_skills_registry.json"

def get_desc(folder_path):
    md_path = Path(folder_path) / "SKILL.md"
    if md_path.exists():
        try:
            content = md_path.read_text(encoding="utf-8")
            desc_match = re.search(r"^description:\s*(.+)$", content, re.MULTILINE)
            if desc_match:
                return desc_match.group(1).strip().strip("'\"")
        except:
            pass
    return Path(folder_path).name.replace("-", " ").title()

def score_skill(skill_name, skill_desc, category):
    text = f"{skill_name.lower().replace('-', ' ')} {skill_desc.lower()}"
    words = set(re.findall(r'\b\w+\b', text))
    
    score = 0
    cat_id = category["category_id"]
    
    # Exact tag matches are weighted heavily
    for tag in category.get("category_tags", []):
        tag_lower = tag.lower()
        if tag_lower in text:
            score += 5
        if tag_lower in words:
            score += 3
            
    # Keywords from the category name also help
    cat_words = set(re.findall(r'\b\w+\b', category["category_name"].lower()))
    for cw in cat_words:
        if len(cw) > 3 and cw in words:
            score += 2
            
    # Sub-string match for category ID just in case
    if cat_id in text or cat_id.replace("-", " ") in text:
        score += 4
        
    return score

def generate_category_registry(cat_slug, cat_name, skills, staging_path, based_skills_lookup=None, force_llm=False):
    if based_skills_lookup is None:
        based_skills_lookup = {}
        
    registry = {
        "category_id": cat_slug,
        "category_name": cat_name,
        "skills": []
    }
    
    domain = cat_slug
    sub_domain = ""
    parts = cat_slug.split('-')
    if len(parts) > 1:
        sub_domain = parts[-1]
        domain = "-".join(parts[:-1])
        
    for skill in sorted(skills, key=lambda x: x["name"]):
        if "new_path" not in skill: continue
        skill_id = skill["name"]
        
        llm_meta = None
        if force_llm or skill_id not in based_skills_lookup:
            # Attempt LM Studio generation if forced or missing
            skill_folder = skill.get("path")
            if skill_folder and (skill_folder / "SKILL.md").exists():
                print(f"    [LLM] Extracting skill metadata for {skill_id}...")
                try:
                    content = (skill_folder / "SKILL.md").read_text(encoding="utf-8", errors="replace")
                    llm_meta = llm_utils.generate_skill_metadata(content)
                    if llm_meta:
                        print(f"    [LLM] Success!")
                except Exception as e:
                    print(f"    [LLM] Failed to read or generate LLM metadata for {skill_id}: {e}")

        if not force_llm and skill_id in based_skills_lookup:
            meta = based_skills_lookup[skill_id]
            desc = meta.get("description", skill.get("desc", ""))
            tags = meta.get("tags", [])
            trigger_conditions = meta.get("trigger_conditions", [])
            anti_triggers = meta.get("anti_triggers", [])
            dependencies = meta.get("dependencies", [])
            mcp_tools = meta.get("mcp_tools", [])
        else:
            # Start with basic parsing as fallback
            desc = skill.get("desc", "")
            triggers = []
            if "Triggers:" in desc:
                triggers = [t.strip().strip("'\"") for t in desc.split("Triggers:")[1].split(",")]
            elif "Use when" in desc:
                triggers = [w.strip(",") for w in desc.split() if len(w) > 4][:5]
                
            tags = skill.get("tags", [])
            trigger_conditions = triggers
            anti_triggers = skill.get("anti_triggers", [])
            dependencies = skill.get("dependencies", [])
            mcp_tools = skill.get("mcp_tools", [])
            
            # If LLM succeeded, overwrite fallbacks with smart data
            if llm_meta:
                desc = llm_meta.get("description", desc)
                tags = llm_meta.get("tags", tags)
                trigger_conditions = llm_meta.get("trigger_conditions", trigger_conditions)
                anti_triggers = llm_meta.get("anti_triggers", anti_triggers)
                mcp_tools = llm_meta.get("mcp_tools", mcp_tools)
            
        registry["skills"].append({
            "id": skill_id,
            "description": desc,
            "path": f"{skill_id}/SKILL.md",  # Local path within category
            "tags": tags,
            "trigger_conditions": trigger_conditions,
            "anti_triggers": anti_triggers,
            "dependencies": dependencies,
            "mcp_tools": mcp_tools
        })
        
    registry_file = Path(staging_path) / "registry.json"
    registry_file.write_text(json.dumps(registry, indent=2, ensure_ascii=False), encoding="utf-8")

def rebuild_skills_md():
    if not ROOT_REGISTRY_JSON.exists():
        print("Root registry missing, cannot rebuild SKILLS.md")
        return

    registry_data = json.loads(ROOT_REGISTRY_JSON.read_text(encoding="utf-8"))
    categories = registry_data.get("categories", [])
    
    total_count = 0
    new_md_lines = []
    
    for cat in categories:
        cat_id = cat["category_id"]
        cat_name = cat["category_name"]
        
        cat_registry_path = SKILLS_DIR / cat_id / "registry.json"
        if not cat_registry_path.exists(): continue
        
        try:
            cat_reg = json.loads(cat_registry_path.read_text(encoding="utf-8"))
        except: continue
        
        skills = cat_reg.get("skills", [])
        if not skills: continue
        
        total_count += len(skills)
        
        new_md_lines.append(f"### {cat_name}\n\n")
        new_md_lines.append("<details>\n")
        new_md_lines.append(f"<summary><b>{cat_name} (Click to expand)</b></summary>\n\n")
        new_md_lines.append("| Skill | Description |\n")
        new_md_lines.append("|---|---|\n")
        for s in sorted(skills, key=lambda x: x.get("id", "")):
            new_path = f"../.archived/skills/{cat_id}/{s.get('path', '')}"
            new_md_lines.append(f"| [{s.get('id', '')}]({new_path}) | {s.get('description', '')} |\n")
        new_md_lines.append("\n</details>\n\n")

    full_text = SKILLS_MD.read_text(encoding="utf-8")
    start_match = re.search(r"## .*Skills by Category\n+", full_text)
    end_match = re.search(r"## Finding Skills\n+", full_text)
    
    if start_match and end_match:
        print(f"Updated SKILLS.md with {total_count} skills natively.")
    else:
        print("Error: Could not find markers in SKILLS.md")

def process_target(target_path, force_llm=False):
    target = Path(target_path)
    if not target.exists() or not target.is_dir() or not (target / "SKILL.md").exists():
        print(f"Error: Target {target_path} is not a valid skill folder (must contain SKILL.md).")
        return

    name = target.name
    desc = get_desc(target)

    registry_data = json.loads(ROOT_REGISTRY_JSON.read_text(encoding="utf-8"))
    categories = registry_data.get("categories", [])
    
    # Determine the category
    best_score = -1
    best_cat = None

    # 1. Check mapping file first (Prioritize explicit mapping)
    if DOMAIN_MAPPING_FILE.exists():
        mapping = json.loads(DOMAIN_MAPPING_FILE.read_text(encoding="utf-8"))
        for cat_id, skills_list in mapping.items():
            if name in skills_list:
                best_cat = cat_id
                best_score = 100
                break

    # 2. Falling back to scoring if not explicitly mapped
    if best_score < 100:
        for cat in categories:
            score = score_skill(name, desc, cat)
            if score > best_score:
                best_score = score
                best_cat = cat["category_id"]
            
    target_cat = best_cat if best_score > 0 and best_cat else "miscellaneous-other"
    dest_path = SKILLS_DIR / target_cat / name

    # Check if target and destination are the same physical path
    if target.resolve() == dest_path.resolve():
        print(f"Skill {name} is already in the correct category ({target_cat}). No move needed.")
    else:
        if dest_path.exists():
            print(f"Update: Skill {name} already exists in {target_cat}. Replacing it.")
            shutil.rmtree(dest_path)
            
        shutil.move(str(target), str(dest_path))
        print(f"Moved new skill '{name}' to '{target_cat}'.")
    
    cat_registry_path = SKILLS_DIR / target_cat / "registry.json"
    if cat_registry_path.exists():
        cat_reg = json.loads(cat_registry_path.read_text(encoding="utf-8"))
        
        based_skills_lookup = {}
        if BASED_SKILLS_FILE.exists():
            based_data = json.loads(BASED_SKILLS_FILE.read_text(encoding="utf-8"))
            for s in based_data.get("skills", []):
                based_skills_lookup[s["id"]] = s
                
        # Remove old entry if replacing
        cat_reg["skills"] = [s for s in cat_reg.get("skills", []) if s.get("id") != name]
        
        domain = target_cat
        sub_domain = ""
        parts = target_cat.split('-')
        if len(parts) > 1:
            sub_domain = parts[-1]
            domain = "-".join(parts[:-1])

        llm_meta = None
        if force_llm or name not in based_skills_lookup:
            print(f"  [LLM] Extracting skill metadata for {name}...")
            try:
                content = (target / "SKILL.md").read_text(encoding="utf-8", errors="replace")
                llm_meta = llm_utils.generate_skill_metadata(content)
                if llm_meta:
                        print(f"  [LLM] Success!")
            except Exception as e:
                print(f"  [LLM] Failed to read or generate LLM metadata for {name}: {e}")

        if not force_llm and name in based_skills_lookup:
            meta = based_skills_lookup[name]
            updated_desc = meta.get("description", desc)
            tags = meta.get("tags", [])
            trigger_conditions = meta.get("trigger_conditions", [])
            anti_triggers = meta.get("anti_triggers", [])
            dependencies = meta.get("dependencies", [])
            mcp_tools = meta.get("mcp_tools", [])
        else:
            updated_desc = desc
            triggers = []
            if "Triggers:" in desc:
                triggers = [t.strip().strip("'\"") for t in desc.split("Triggers:")[1].split(",")]
            elif "Use when" in desc:
                triggers = [w.strip(",") for w in desc.split() if len(w) > 4][:5]
                
            tags = []
            trigger_conditions = triggers
            anti_triggers = []
            dependencies = []
            mcp_tools = []
            
            if llm_meta:
                updated_desc = llm_meta.get("description", updated_desc)
                tags = llm_meta.get("tags", tags)
                trigger_conditions = llm_meta.get("trigger_conditions", trigger_conditions)
                anti_triggers = llm_meta.get("anti_triggers", anti_triggers)
                mcp_tools = llm_meta.get("mcp_tools", mcp_tools)
            
        cat_reg["skills"].append({
            "id": name,
            "description": updated_desc,
            "path": f"{name}/SKILL.md",
            "tags": tags,
            "trigger_conditions": trigger_conditions,
            "anti_triggers": anti_triggers,
            "dependencies": dependencies,
            "mcp_tools": mcp_tools
        })
        cat_reg["skills"] = sorted(cat_reg["skills"], key=lambda x: x.get("id", ""))
        cat_registry_path.write_text(json.dumps(cat_reg, indent=2, ensure_ascii=False), encoding="utf-8")
        
    rebuild_skills_md()
    print("Targeted ingestion complete.")

def reorganize_full(force_llm=False):
    if not SKILLS_DIR.exists():
        print(f"Error: Skills directory not found at {SKILLS_DIR}")
        return

    based_skills_lookup = {}
    if BASED_SKILLS_FILE.exists():
        based_data = json.loads(BASED_SKILLS_FILE.read_text(encoding="utf-8"))
        for skill in based_data.get("skills", []):
            based_skills_lookup[skill["id"]] = skill

    explicit_map = {}
    categorized_skills = {}
    if DOMAIN_MAPPING_FILE.exists():
        domain_mapping = json.loads(DOMAIN_MAPPING_FILE.read_text(encoding="utf-8"))
        for cat_id, skills_list in domain_mapping.items():
            categorized_skills[cat_id] = {
                "details": {"category_id": cat_id, "category_name": utils.format_label(cat_id)},
                "skills": []
            }
            for skill in skills_list:
                explicit_map[skill] = cat_id
    
    if "miscellaneous-other" not in categorized_skills:
        categorized_skills["miscellaneous-other"] = {
            "details": {"category_id": "miscellaneous-other", "category_name": "Miscellaneous Other"},
            "skills": []
        }

    all_skill_folders = {}
    for item in SKILLS_DIR.iterdir():
        if not item.is_dir() or item.name in [".git", "node_modules"]:
            continue
            
        if (item / "SKILL.md").exists():
            all_skill_folders[item.name] = item
        else:
            for sub in item.iterdir():
                if sub.is_dir() and (sub / "SKILL.md").exists():
                    all_skill_folders[sub.name] = sub

    for name, path in all_skill_folders.items():
        desc = get_desc(path)
        target_cat = "miscellaneous-other"
        
        if name in explicit_map and explicit_map[name] in categorized_skills:
            target_cat = explicit_map[name]
        else:
            # Fallback to miscellaneous-other if not in mapping, since categories are dynamically driven
            target_cat = "miscellaneous-other"
                
        categorized_skills[target_cat]["skills"].append({"name": name, "desc": desc, "path": path})

    if NEW_SKILLS_DIR.exists(): shutil.rmtree(NEW_SKILLS_DIR)
    NEW_SKILLS_DIR.mkdir(parents=True)

    total_count = 0
    reorganized_count = 0
    for cat_id, data in categorized_skills.items():
        if not data["skills"]:
            continue
            
        cat_staging_path = NEW_SKILLS_DIR / cat_id
        cat_staging_path.mkdir(parents=True, exist_ok=True)
        
        for skill in data["skills"]:
            name = skill["name"]
            if name in all_skill_folders:
                current_path = all_skill_folders[name]
                # Determine current category: relative to SKILLS_DIR, first parent
                try:
                    rel_parent = current_path.parent.relative_to(SKILLS_DIR)
                    current_cat = rel_parent.parts[0] if rel_parent.parts else None
                except ValueError:
                    current_cat = None # Skill was likely at root or outside SKILLS_DIR
                
                if current_cat != cat_id:
                    print(f"  [MOVE] {name:<40} {current_cat or 'ROOT'} -> {cat_id}")
                    reorganized_count += 1
                
                shutil.copytree(current_path, cat_staging_path / name, dirs_exist_ok=True)
                total_count += 1
                skill["new_path"] = f".archived/skills/{cat_id}/{name}/SKILL.md"

        generate_category_registry(cat_id, data["details"]["category_name"], data["skills"], cat_staging_path, based_skills_lookup, force_llm)

    for item in SKILLS_DIR.iterdir():
        if item.is_file():
            shutil.copy2(item, NEW_SKILLS_DIR / item.name)

    if total_count == 0:
        print("Error: No skills found. Aborting swap.")
        return

    backup_path = ROOT_DIR / "tmp" / "skills_backup"
    if not (ROOT_DIR / "tmp").exists():
        (ROOT_DIR / "tmp").mkdir(parents=True, exist_ok=True)
        
    if not backup_path.exists():
        os.rename(SKILLS_DIR, backup_path)
    else:
        import time
        alt_backup = ROOT_DIR / "tmp" / f"skills_backup_{int(time.time())}"
        os.rename(SKILLS_DIR, alt_backup)
        
    os.rename(NEW_SKILLS_DIR, SKILLS_DIR)
    
    # Rebuild ROOT_REGISTRY_JSON to reflect new categories
    new_categories = []
    for cat_id, data in categorized_skills.items():
        if not data["skills"]:
            continue
        new_categories.append({
            "category_id": cat_id,
            "category_name": data["details"]["category_name"],
            "registry_path": f".archived/skills/{cat_id}/registry.json",
            "category_tags": []
        })
        
    new_root_registry = {
        "version": "1.0.0",
        "type": "skill_registry",
        "last_updated": datetime.utcnow().isoformat() + "Z",
        "categories": sorted(new_categories, key=lambda x: x["category_id"])
    }
    
    ROOT_REGISTRY_JSON.write_text(json.dumps(new_root_registry, indent=2, ensure_ascii=False), encoding="utf-8")
    
    print(f"Success! {total_count} skills processed, {reorganized_count} newly reallocated. Now rebuilding MD.")
    rebuild_skills_md()
    
    # Automatically restore tags
    print("\nRunning Deep Tag Extraction...")
    tags_args = argparse.Namespace(dry_run=False, category=None, type="skills", force_llm=force_llm)
    tags_generator.run_tag_extraction("skills", tags_args)

def main():
    parser = argparse.ArgumentParser(description="Clean up and sync the skills registry with the file system. Now supports AI-driven metadata generation via LM Studio/Ollama.")
    parser.add_argument("--target", type=str, help="Path to a single skill folder inside /tmp/ to ingest and insert without reorganizing the whole ecosystem.")
    parser.add_argument("--force-llm", action="store_true", help="Connect to LM Studio/Ollama to force-regenerate metadata (description, tags, triggers) for all processed skills.")
    args = parser.parse_args()
    
    if args.target:
        process_target(args.target, args.force_llm)
    else:
        reorganize_full(args.force_llm)

if __name__ == "__main__":
    main()
