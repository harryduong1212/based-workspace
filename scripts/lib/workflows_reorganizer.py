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
WORKFLOWS_DIR = ROOT_DIR / ".archived" / "workflows"
STAGING_DIR = ROOT_DIR / ".archived" / "workflows_reorganized"
WORKFLOWS_MD = ROOT_DIR / "docs" / "WORKFLOWS.md"
ROOT_REGISTRY_JSON = WORKFLOWS_DIR / "registry.json"

def slugify(text):
    text = re.sub(r'[^\w\s-]', '', text).strip().lower()
    return re.sub(r'[-\s]+', '-', text)

def get_desc(file_path):
    md_path = Path(file_path)
    if md_path.exists() and md_path.is_file():
        try:
            content = md_path.read_text(encoding="utf-8")
            desc_match = re.search(r"^description:\s*(.+)$", content, re.MULTILINE)
            if desc_match:
                return desc_match.group(1).strip().strip("'\"")
        except:
            pass
    return utils.format_label(Path(file_path).stem)

def score_workflow(workflow_name, desc, category):
    text = f"{workflow_name.lower().replace('-', ' ')} {desc.lower()}"
    words = set(re.findall(r'\b\w+\b', text))
    
    score = 0
    cat_id = category.get("category_id", "")
    
    for tag in category.get("domain_tags", []):
        tag_lower = tag.lower()
        if tag_lower in text: score += 5
        if tag_lower in words: score += 3
            
    cat_words = set(re.findall(r'\b\w+\b', category.get("category_name", "").lower()))
    for cw in cat_words:
        if len(cw) > 3 and cw in words: score += 2
            
    if cat_id in text or cat_id.replace("-", " ") in text: score += 4
        
    return score

def get_workflows_mapping():
    if not WORKFLOWS_MD.exists():
        return {}
    full_content = WORKFLOWS_MD.read_text(encoding="utf-8")
    mapping = {} 
    sections = re.split(r'^### (.*)$', full_content, flags=re.MULTILINE)
    for i in range(1, len(sections), 2):
        cat_name = sections[i].strip()
        body = sections[i+1]
        links = re.findall(r'\[([^\]]+)\]\(\.(?:archived/workflows/|archived_workflows/)(.*?)\)', body)
        if links:
            ids = []
            for name, relative_path in links:
                path_parts = relative_path.strip("/\\").replace("\\", "/").split("/")
                if path_parts[-1].endswith(".md"):
                    if path_parts[-1] == "WORKFLOW.md" and len(path_parts) >= 2:
                        ids.append(path_parts[-2] + ".md")
                    else:
                        ids.append(path_parts[-1])
                else:
                    ids.append(path_parts[-1] + ".md")
            mapping[cat_name] = ids
    return mapping

def generate_category_registry(cat_slug, cat_name, file_list, staging_path, original_content, force_llm=False):
    registry = {
        "category_id": cat_slug,
        "category_name": cat_name,
        "workflows": []
    }
    for filename in sorted(file_list):
        workflow_id = filename.replace(".md", "")
        esc_id = re.escape(workflow_id)
        row_pattern = rf'\| \[([^\]]+)\]\(\.(?:archived/workflows/|archived_workflows/)(?:.*?){esc_id}(?:[/\\]WORKFLOW\.md|\.md)\) \| ([^|]+) \| ([^|]*?) \| ([^|]*?)? \|'
        match = re.search(row_pattern, original_content)
        description = ""
        triggers = []
        if match:
            slash = match.group(2).strip()
            desc = match.group(4).strip() if match.group(4) else match.group(3).strip()
            triggers = [slash.replace("/", "").replace("`", "")]
            description = desc
        
        # Read the file for required skills matching and LLM expansion
        wf_path = Path(staging_path) / filename
        req_skills = []
        tags = []
        entry_point = None
        if wf_path.exists() and wf_path.is_file():
            content = wf_path.read_text(encoding="utf-8", errors="replace")
            
            if force_llm or not description:
                print(f"    [LLM] Extracting triggers and metadata for {workflow_id}...")
                try:
                    llm_meta = llm_utils.generate_workflow_metadata(content)
                    if llm_meta:
                        print(f"    [LLM] Extracted metadata successfully.")
                        description = llm_meta.get("description", description)
                        if llm_meta.get("triggers"):
                            triggers = llm_meta.get("triggers")
                        tags = llm_meta.get("tags", [])
                        entry_point = llm_meta.get("entry_point", entry_point)
                except Exception as e:
                    print(f"Failed LLM gen for {workflow_id}: {e}")

            # We assume root skills registry exists
            skills_dir = ROOT_DIR / ".archived" / "skills"
            if (skills_dir / "registry.json").exists():
                 try:
                     s_reg = json.loads((skills_dir / "registry.json").read_text(encoding="utf-8"))
                     known_skills = []
                     for c in s_reg.get("categories", []):
                         c_path = skills_dir / c["category_id"] / "registry.json"
                         if c_path.exists():
                             cr = json.loads(c_path.read_text(encoding="utf-8"))
                             known_skills.extend([s["id"] for s in cr.get("skills", [])])
                     
                     found_skills = set()
                     for s_id in known_skills:
                         if re.search(r'(?i)@' + re.escape(s_id) + r'(?![a-zA-Z0-9_\-])', content):
                             found_skills.add(s_id)
                     req_skills = sorted(list(found_skills))
                 except: pass

        registry["workflows"].append({
            "id": workflow_id,
            "description": description,
            "path": filename,
            "triggers": triggers if triggers else [workflow_id],
            "required_skills": req_skills,
            "entry_point": entry_point,
            "tags": tags
        })
    registry_file = Path(staging_path) / "registry.json"
    registry_file.write_text(json.dumps(registry, indent=2, ensure_ascii=False), encoding="utf-8")

def rebuild_workflows_md():
    if not ROOT_REGISTRY_JSON.exists():
        print("Root registry missing, cannot rebuild WORKFLOWS.md")
        return

    registry_data = json.loads(ROOT_REGISTRY_JSON.read_text(encoding="utf-8"))
    categories = registry_data.get("categories", [])
    
    total_workflows = 0
    new_sections = []
    
    for cat in sorted(categories, key=lambda x: x.get("category_name", "")):
        cat_id = cat["category_id"]
        cat_name = cat["category_name"]
        
        cat_registry_path = WORKFLOWS_DIR / cat_id / "registry.json"
        if not cat_registry_path.exists(): continue
        
        try:
            cat_reg = json.loads(cat_registry_path.read_text(encoding="utf-8"))
        except: continue
        
        workflows = cat_reg.get("workflows", [])
        if not workflows: continue
        
        total_workflows += len(workflows)
        
        section = f"\n### {cat_name}\n<details>\n\n"
        section += "| Workflow | Command | Status | Description |\n|---|---|---|---|\n"
        
        for wf in sorted(workflows, key=lambda x: x.get("id", "")):
            w_id = wf.get("id", "")
            desc = wf.get("description", "")
            trigger = wf.get("triggers", [w_id])[0] if wf.get("triggers") else w_id
            cmd = f"/{trigger}"
            status = "🚧 Custom" if w_id.startswith("custom-") else "✅ Ready"
            link = f".archived/workflows/{cat_id}/{w_id}.md"
            section += f"| [{w_id}]({link}) | {cmd} | {status} | {desc} |\n"
            
        section += "\n</details>\n"
        new_sections.append(section)

    full_text = WORKFLOWS_MD.read_text(encoding="utf-8")
    header_end_idx = full_text.find("## 📂 Available Workflows")
    
    if header_end_idx != -1:
        # Rebuild the dynamic header with the count
        lines_before = full_text[:header_end_idx].splitlines()
        header = "\n".join(lines_before) + f"\n## 📂 Available Workflows ({total_workflows})\n"
        
        footer = """
---

## 🤝 Contributing

To add a new workflow:
1. Develop it in `/tmp/my-workflow.md`
2. Run `python scripts/reorganize_workflows_safe.py --target /tmp/my-workflow.md` to auto-categorize.

---

> **Repo:** [github.com/harikrishna8121999/antigravity-workflows](https://github.com/harikrishna8121999/antigravity-workflows)
"""
        WORKFLOWS_MD.write_text(header + "".join(new_sections) + footer, encoding="utf-8")
        print(f"Updated WORKFLOWS.md with {total_workflows} strictly sourced workflows.")
    else:
        print("Error: Could not find ## 📂 Available Workflows marker in WORKFLOWS.md")

def process_target(target_path, force_llm=False):
    target = Path(target_path)
    if not target.exists() or not target.is_file() or target.suffix != ".md":
        print(f"Error: Target {target_path} is not a valid workflow file (must end in .md).")
        return

    name = target.stem
    desc = get_desc(target)
    
    triggers = [name]
    req_skills = []
    tags = []
    entry = None

    if target.exists() and target.is_file():
        content = target.read_text(encoding="utf-8", errors="replace")
        if force_llm or not desc or desc == name.replace("-", " ").title():
            print(f"  [LLM] Extracting triggers and metadata for {name}...")
            try:
                llm_meta = llm_utils.generate_workflow_metadata(content)
                if llm_meta:
                    print(f"  [LLM] Extracted metadata successfully.")
                    desc = llm_meta.get("description", desc)
                    if llm_meta.get("triggers"):
                        triggers = llm_meta.get("triggers")
                    tags = llm_meta.get("tags", [])
                    entry = llm_meta.get("entry_point", None)
            except Exception as e:
                print(f"Failed LLM gen for {name}: {e}")

    # Need root registry for NLP scoring
    if not ROOT_REGISTRY_JSON.exists():
        print("Root workflows registry missing! Run build_workflow_registries.py first.")
        return
        
    registry_data = json.loads(ROOT_REGISTRY_JSON.read_text(encoding="utf-8"))
    categories = registry_data.get("categories", [])
    
    best_score = -1
    best_cat = None
    for cat in categories:
        score = score_workflow(name, desc, cat)
        if score > best_score:
            best_score = score
            best_cat = cat["category_id"]
            
    target_cat = best_cat if best_score > 0 and best_cat else "miscellaneous"
    
    dest_path = WORKFLOWS_DIR / target_cat / (name + ".md")
    
    if dest_path.exists():
        print(f"Update: Workflow {name} already exists in {target_cat}. Replacing it.")
        dest_path.unlink()
        
    shutil.copy2(str(target), str(dest_path))
    print(f"Moved new workflow '{name}' to '{target_cat}'.")
    
    cat_registry_path = WORKFLOWS_DIR / target_cat / "registry.json"
    if cat_registry_path.exists():
        cat_reg = json.loads(cat_registry_path.read_text(encoding="utf-8"))
        
        # Remove old entry if updating
        cat_reg["workflows"] = [w for w in cat_reg.get("workflows", []) if w.get("id") != name]
        
        # Find explicit skills if any
        content = dest_path.read_text(encoding="utf-8")
        skills_dir = ROOT_DIR / ".archived" / "skills"
        req_skills = []
        if (skills_dir / "registry.json").exists():
             try:
                 s_reg = json.loads((skills_dir / "registry.json").read_text(encoding="utf-8"))
                 known_skills = []
                 for c in s_reg.get("categories", []):
                     c_path = skills_dir / c["category_id"] / "registry.json"
                     if c_path.exists():
                         cr = json.loads(c_path.read_text(encoding="utf-8"))
                         known_skills.extend([s["id"] for s in cr.get("skills", [])])
                 
                 found_skills = set()
                 for s_id in known_skills:
                     if re.search(r'(?i)@' + re.escape(s_id) + r'(?![a-zA-Z0-9_\-])', content):
                         found_skills.add(s_id)
                 req_skills = sorted(list(found_skills))
             except: pass
             
        cat_reg["workflows"].append({
            "id": name,
            "description": desc,
            "path": f"{name}.md",
            "triggers": triggers,
            "required_skills": req_skills,
            "entry_point": entry,
            "tags": tags
        })
        cat_reg["workflows"] = sorted(cat_reg["workflows"], key=lambda x: x.get("id", ""))
        cat_registry_path.write_text(json.dumps(cat_reg, indent=2, ensure_ascii=False), encoding="utf-8")
        
    rebuild_workflows_md()
    print("Targeted ingestion complete.")

def reorganize_full(force_llm=False):
    mapping = get_workflows_mapping()
    
    explicit_map = {
        "feature-deep-dive.md": "custom-workflows",
        "prepare-test-environment.md": "custom-workflows"
    }

    if STAGING_DIR.exists():
        shutil.rmtree(STAGING_DIR)
    STAGING_DIR.mkdir(parents=True)
    
    all_files = {} 
    for r, d, files in os.walk(WORKFLOWS_DIR):
        root = Path(r)
        if root.name == ".git": continue
        for f in files:
            if f.endswith(".md") and " copy" not in f:
                if f == "WORKFLOW.md":
                    wf_id = root.name
                    all_files[wf_id + ".md"] = root / f
                else:
                    all_files[f] = root / f
    
    original_content = WORKFLOWS_MD.read_text(encoding="utf-8")
    moved_filenames = set()
    
    reorganized_count = 0
    reorganized_count = 0
    
    # 1. Update mapping with explicit overrides
    for wf_filename, target_cat_id in explicit_map.items():
        # Find if it's currently in any category in the mapping
        found = False
        for cat_name, file_list in mapping.items():
            if wf_filename in file_list:
                file_list.remove(wf_filename)
                found = True
        
        # Add to the target category (create category if needed by searching the registry)
        # However, for simplicity and since we slugify cat names, we'll just add it to a new section entry
        # But wait, the script expects cat_name, not cat_id as keys in mapping.
        # Let's find the cat_name for this cat_id from the root registry.
        target_cat_name = utils.format_label(target_cat_id)
        if ROOT_REGISTRY_JSON.exists():
            root_reg = json.loads(ROOT_REGISTRY_JSON.read_text(encoding="utf-8"))
            for cat in root_reg.get("categories", []):
                if cat["category_id"] == target_cat_id:
                    target_cat_name = cat["category_name"]
                    break
        
        if target_cat_name not in mapping:
            mapping[target_cat_name] = []
        mapping[target_cat_name].append(wf_filename)

    for cat_name, file_list in mapping.items():
        cat_slug = slugify(cat_name)
        cat_staging_path = STAGING_DIR / cat_slug
        cat_staging_path.mkdir(parents=True, exist_ok=True)
        
        valid_files_in_cat = []
        for filename in file_list:
            if filename in all_files:
                current_path = all_files[filename]
                try:
                    rel_parent = current_path.parent.relative_to(WORKFLOWS_DIR)
                    current_cat = rel_parent.parts[0] if rel_parent.parts else None
                except ValueError:
                    current_cat = None

                if current_cat != cat_slug:
                    print(f"  [MOVE] {filename:<40} {current_cat or 'ROOT'} -> {cat_slug}")
                    reorganized_count += 1
                
                shutil.copy2(current_path, cat_staging_path / filename)
                moved_filenames.add(filename)
                valid_files_in_cat.append(filename)
        
        if valid_files_in_cat:
            generate_category_registry(cat_slug, cat_name, valid_files_in_cat, cat_staging_path, original_content, force_llm)
                
    misc_path = STAGING_DIR / "miscellaneous"
    misc_files = []
    for filename, full_path in all_files.items():
        if filename not in moved_filenames:
            if not misc_path.exists(): misc_path.mkdir(parents=True)
            workflow_id = filename.replace(".md", "")
            shutil.copy2(full_path, misc_path / filename)
            misc_files.append(filename)
    
    if misc_files:
        generate_category_registry("miscellaneous", "📦 Miscellaneous", misc_files, misc_path, original_content, force_llm)

    total_wf_files = sum(1 for _, _, files in os.walk(STAGING_DIR) for f in files if f.endswith(".md"))

    if total_wf_files == 0:
        print("Error: Staging directory contains no workflows. Aborting swap.")
        return

    # To preserve registry structures generated by build_workflow_registries.py, copy over any registry files
    # not overridden by generation.
    for r, d, files in os.walk(WORKFLOWS_DIR):
        if "registry.json" in files:
            rel = Path(r).relative_to(WORKFLOWS_DIR)
            st_path = STAGING_DIR / rel / "registry.json"
            if not st_path.exists() and (STAGING_DIR / rel).exists():
                shutil.copy2(Path(r) / "registry.json", st_path)
    
    if (WORKFLOWS_DIR / "registry.json").exists():
        shutil.copy2(WORKFLOWS_DIR / "registry.json", STAGING_DIR / "registry.json")

    final_backup = ROOT_DIR / "tmp" / "workflows_backup"
    if not (ROOT_DIR / "tmp").exists():
        (ROOT_DIR / "tmp").mkdir(parents=True, exist_ok=True)
        
    if final_backup.exists(): shutil.rmtree(final_backup)
    
    os.rename(WORKFLOWS_DIR, final_backup)
    os.rename(STAGING_DIR, WORKFLOWS_DIR)
    
    print(f"Reorganization success! {total_wf_files} workflows processed, {reorganized_count} newly reallocated.")
    rebuild_workflows_md()
    
    # Automatically restore tags
    print("\nRunning Deep Tag Extraction...")
    tags_args = argparse.Namespace(dry_run=False, category=None, type="workflows", force_llm=force_llm)
    tags_generator.run_tag_extraction("workflows", tags_args)

def main():
    parser = argparse.ArgumentParser(description="Clean up and sync the workflows registry with the file system. Now supports AI-driven metadata generation via LM Studio/Ollama.")
    parser.add_argument("--target", type=str, help="Path to a single workflow file inside /tmp/ to ingest and insert without reorganizing the whole ecosystem.")
    parser.add_argument("--force-llm", action="store_true", help="Connect to LM Studio/Ollama to force-regenerate metadata (description, tags, triggers) for all processed workflows.")
    args = parser.parse_args()
    
    if args.target:
        process_target(args.target, args.force_llm)
    else:
        reorganize_full(args.force_llm)

if __name__ == "__main__":
    main()
