import os
from collections import defaultdict

FILE_1 = "skill_inventory.md"
FILE_2 = "llama_skill_inventory.md"
OUTPUT_FILE = "merged_skill_inventory.md"

def parse_inventory(filepath, db):
    """Parses a markdown inventory file and extracts skills into the database."""
    if not os.path.exists(filepath):
        print(f"[!] Warning: {filepath} not found. Skipping.")
        return

    current_domain = None
    current_subdomain = None

    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            
            # Match Domain (e.g., ## Ai Ml)
            if line.startswith('## '):
                # Use .title() to normalize casing and prevent duplicates 
                current_domain = line[3:].strip().title()
                current_subdomain = None
            
            # Match Subdomain (e.g., ### Evaluation)
            elif line.startswith('### '):
                if current_domain:
                    current_subdomain = line[4:].strip().title()
            
            # Match Table Row
            elif line.startswith('|') and current_domain and current_subdomain:
                # Skip table headers and alignment separators
                if 'Skill Name' in line or '|:---' in line or '|---' in line:
                    continue
                
                parts = line.split('|')
                if len(parts) >= 3:
                    # Extract skill name (Column 1) and strip backticks for clean deduplication
                    skill_name_raw = parts[1].strip()
                    skill_name = skill_name_raw.replace('`', '')
                    
                    if skill_name:
                        # Save the entire markdown row string to the nested dictionary
                        db[current_domain][current_subdomain][skill_name] = line

def get_score(row_str):
    """Extracts the evaluation score from the markdown row for sorting."""
    try:
        # The last element after splitting by '|' is an empty string, so the score is at index -2
        parts = row_str.split('|')
        score_str = parts[-2].strip()
        return float(score_str)
    except (ValueError, IndexError):
        return 0.0

def generate_merged_markdown(db, output_file):
    """Generates the final merged markdown file."""
    with open(output_file, 'w', encoding='utf-8') as md:
        # Write Frontmatter
        md.write("---\n")
        md.write("title: Merged Skill Inventory\n")
        md.write("description: Comprehensive and deduplicated directory of skills mapped by domain and subdomain.\n")
        md.write("---\n\n")
        md.write("# Skill Inventory\n\n")

        # Iterate through alphabetically sorted domains
        for domain in sorted(db.keys()):
            md.write(f"## {domain}\n\n")
            
            # Iterate through alphabetically sorted subdomains
            for subdomain in sorted(db[domain].keys()):
                md.write(f"### {subdomain}\n\n")
                
                # Write Table Headers
                headers = [
                    "Skill Name", "File", "Summary", "Tags", 
                    "Trigger Conditions", "Anti-Triggers", "Dependencies", 
                    "MCP Tools", "Complexity", "Score"
                ]
                md.write("| " + " | ".join(headers) + " |\n")
                md.write("|" + "|".join([":---"] * len(headers)) + "|\n")
                
                # Get all rows for this subdomain and sort them by score (descending)
                skills = db[domain][subdomain].values()
                sorted_skills = sorted(skills, key=lambda x: get_score(x), reverse=True)
                
                # Write rows
                for row in sorted_skills:
                    md.write(f"{row}\n")
                
                md.write("\n")

def main():
    # Nested dictionary to hold: db[Domain][Subdomain][SkillName] = MarkdownRow
    merged_db = defaultdict(lambda: defaultdict(dict))

    print(f"[*] Parsing {FILE_1}...")
    parse_inventory(FILE_1, merged_db)
    
    print(f"[*] Parsing {FILE_2}...")
    parse_inventory(FILE_2, merged_db)

    print(f"[*] Generating merged output to {OUTPUT_FILE}...")
    generate_merged_markdown(merged_db, OUTPUT_FILE)
    
    # Calculate total unique skills processed
    total_skills = sum(len(skills) for subdomains in merged_db.values() for skills in subdomains.values())
    print(f"[+] Done! Successfully merged {total_skills} unique skills.")

if __name__ == "__main__":
    main()