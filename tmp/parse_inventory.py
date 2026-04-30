import json
import re

def to_snake_case(text):
    """
    Converts a string to snake_case by lowering case, 
    replacing spaces/hyphens with underscores, and removing non-alphanumeric characters.
    """
    # Remove backticks and trim
    text = text.replace('`', '').strip()
    # Replace spaces and hyphens with underscores
    text = re.sub(r'[-\s]+', '_', text.lower())
    # Remove any remaining non-alphanumeric characters except underscores
    return re.sub(r'[^\w_]', '', text)

def generate_snake_case_skills_json(input_file, output_file):
    """
    Parses the Markdown inventory, flattens the structure, 
    and converts keys to snake_case for the JSON output.
    """
    all_skills = []
    snake_headers = []

    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()

                # Process only table rows
                if not (line.startswith('|') and line.endswith('|')):
                    continue

                # Extract raw columns from the pipe-separated line
                raw_columns = [col.strip() for col in line.split('|')][1:-1]

                # 1. Identify and Transform Header Row
                if "Skill Name" in line:
                    # Map headers like "Skill Name" to "skill_name"
                    snake_headers = [to_snake_case(h) for h in raw_columns]
                    continue

                # 2. Skip Separator Rows
                if all(re.match(r'^[:\s-]*$', col) for col in raw_columns):
                    continue

                # 3. Map Data Rows to snake_case Headers
                if snake_headers and len(raw_columns) == len(snake_headers):
                    skill_entry = {}
                    for i in range(len(snake_headers)):
                        key = snake_headers[i]
                        # Remove backticks from values (e.g., in skill_name or file columns)
                        value = raw_columns[i].replace('`', '')
                        skill_entry[key] = value
                    
                    all_skills.append(skill_entry)

        # Write the final JSON
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(all_skills, f, indent=4, ensure_ascii=False)

        print(f"Successfully processed {len(all_skills)} skills into {output_file}.")

    except Exception as e:
        print(f"Error during processing: {e}")

if __name__ == "__main__":
    # Assuming the input file is named skill_inventory.md
    generate_snake_case_skills_json('skill_inventory.md', 'skills_snake.json')