import json
import os
import re

RAW_DATA_FILE = "llama_stack_skill_mapping.json"
MAPPING_FILE = "llama_subdomain_mapping.json"
OUTPUT_FILE = "llama_skill_inventory.md"
TMP_INVENTORY_FILE = "llama_skill_inventory_tmp.md"

def load_json(filepath):
    if not os.path.exists(filepath):
        print(f"Error: {filepath} not found.")
        return {}
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def clean_text(text):
    """Sanitize strings and arrays for Markdown table compatibility."""
    if not text:
        return ""
    if isinstance(text, list):
        text = ", ".join(str(i) for i in text)
    return str(text).replace('\n', ' ').replace('|', '&#124;')

def load_valid_skills(filepath):
    """Parses the tmp markdown inventory to extract a set of valid file paths."""
    valid_skills = set()
    if not os.path.exists(filepath):
        print(f"Warning: {filepath} not found. Processing ALL skills without filtering.")
        return None

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        # Matches markdown links ending in .md: [Name](path/to/SKILL.md)
        matches = re.findall(r'\]\(([^)]+\.md)\)', content)
        for match in matches:
            valid_skills.add(match.strip())
            
    print(f"Loaded {len(valid_skills)} valid skills from {filepath}")
    return valid_skills

def generate_markdown():
    raw_data = load_json(RAW_DATA_FILE)
    mapping_data = load_json(MAPPING_FILE)

    if not raw_data or not mapping_data:
        print("Missing required JSON data. Please ensure both files exist.")
        return

    # Load the allowed skills from the temporary inventory
    valid_skills = load_valid_skills(TMP_INVENTORY_FILE)

    # Pre-filter the mapping data to exclude skills not in the valid_skills list
    # This also prevents printing empty Domain/Subdomain headers
    filtered_mapping = {}
    for domain, subdomains in mapping_data.items():
        filtered_subdomains = {}
        for subdomain, file_paths in subdomains.items():
            valid_paths = [fp for fp in file_paths if valid_skills is None or fp in valid_skills]
            if valid_paths:
                filtered_subdomains[subdomain] = valid_paths
        if filtered_subdomains:
            filtered_mapping[domain] = filtered_subdomains

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as md:
        md.write("---\n")
        md.write("title: Skill Inventory\n")
        md.write("description: Comprehensive directory of skills mapped by domain and subdomain.\n")
        md.write("---\n\n")
        md.write("# Skill Inventory\n\n")

        # Iterate over the filtered domains
        for domain, subdomains in filtered_mapping.items():
            formatted_domain = domain.replace('_', ' ').title()
            md.write(f"## {formatted_domain}\n\n")

            # Iterate over the filtered subdomains
            for subdomain, file_paths in subdomains.items():
                formatted_subdomain = subdomain.replace('_', ' ').title()
                md.write(f"### {formatted_subdomain}\n\n")
                
                headers = [
                    "Skill Name", "File", "Summary", "Tags", 
                    "Trigger Conditions", "Anti-Triggers", "Dependencies", 
                    "MCP Tools", "Complexity", "Score"
                ]
                md.write("| " + " | ".join(headers) + " |\n")
                md.write("|" + "|".join([":---"] * len(headers)) + "|\n")

                skills_list = []
                for file_path in file_paths:
                    details = raw_data.get(file_path)
                    
                    if not details:
                        # Fallback if a mapped path is missing from raw data
                        details = {}

                    # Extract skill name from path (folder name or filename without extension)
                    parts = file_path.split('/')
                    if parts[-1] == 'SKILL.md' and len(parts) >= 2:
                        skill_name = parts[-2]
                    else:
                        skill_name = parts[-1].replace('.md', '')
                        
                    file_link = f"[{parts[-1]}]({file_path})"
                    
                    eval_ledger = details.get("evaluation_ledger", {})
                    score = eval_ledger.get("final_score", 0)
                    
                    skills_list.append({
                        "name": f"`{skill_name}`",
                        "file_link": file_link,
                        "summary": clean_text(details.get("summary")),
                        "tags": clean_text(details.get("tags")),
                        "triggers": clean_text(details.get("trigger_conditions")),
                        "anti_triggers": clean_text(details.get("anti_triggers")),
                        "dependencies": clean_text(details.get("dependencies")),
                        "mcp_tools": clean_text(details.get("mcp_tools")),
                        "complexity": str(details.get("execution_complexity", "N/A")).title(),
                        "score": score
                    })
                
                # Sort skills by final_score descending within their subcategory
                skills_list.sort(key=lambda x: int(x['score']) if str(x['score']).isdigit() else 0, reverse=True)

                # Write rows to the table
                for skill in skills_list:
                    row = [
                        skill["name"],
                        skill["file_link"],
                        skill["summary"], 
                        skill["tags"],
                        skill["triggers"],
                        skill["anti_triggers"], 
                        skill["dependencies"],
                        skill["mcp_tools"], 
                        skill["complexity"],
                        str(skill["score"])
                    ]
                    md.write("| " + " | ".join(row) + " |\n")
                
                md.write("\n")

    print(f"Success: {OUTPUT_FILE} has been generated.")

if __name__ == "__main__":
    generate_markdown()