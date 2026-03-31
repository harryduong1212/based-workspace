#!/usr/bin/env python3
import argparse
import sys
import os
import re
import json

# Add lib to path
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "lib"))
import utils

def cmd_stats(args):
    data = utils.load_json(utils.PROFILES_FILE)
    profiles = data.get("profiles", {})
    
    print(f"| {'Profile Name':<25} | {'Atomic S/W':<12} | {'Effective S/W':<14} |")
    print("|" + "-"*27 + "|" + "-"*14 + "|" + "-"*16 + "|")
    
    for name, details in sorted(profiles.items()):
        atomic_s = len(details.get("skills", []))
        atomic_w = len(details.get("workflows", []))
        eff_s = len(utils.get_effective_set(name, profiles, "skills"))
        eff_w = len(utils.get_effective_set(name, profiles, "workflows"))
        print(f"| {name:<25} | {atomic_s:<2}/{atomic_w:<2}        | {eff_s:<3}/{eff_w:<2}          |")

def cmd_audit(args):
    data = utils.load_json(utils.PROFILES_FILE)
    profiles = data.get("profiles", {})
    all_skills = utils.get_valid_skills()
    all_workflows = utils.get_valid_workflows()
    
    audit_log = []
    def out(msg):
        print(msg)
        audit_log.append(msg)

    total_issues = 0
    for name, prof in sorted(profiles.items()):
        out(f"\n{'='*70}\nPROFILE: {name}\n{'='*70}")
        eff_s = utils.get_effective_set(name, profiles, "skills")
        eff_w = utils.get_effective_set(name, profiles, "workflows")
        
        issues = []
        for sid in eff_s:
            if sid not in all_skills: issues.append(f"MISSING SKILL: {sid}")
        for wid in eff_w:
            if wid not in all_workflows: issues.append(f"MISSING WORKFLOW: {wid}")
            
        if not issues:
            out("  ✅ ALL CLEAR")
        else:
            for iss in issues: out(f"  ❌ {iss}")
            total_issues += len(issues)

    # Save results to tmp
    os.makedirs(utils.TMP_DIR, exist_ok=True)
    with open(os.path.join(utils.TMP_DIR, "audit_results.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(audit_log))
    
    print(f"\nAudit complete. Total issues: {total_issues}")
    print(f"Results saved to {os.path.join(utils.TMP_DIR, 'audit_results.txt')}")

def cmd_fix(args):
    audit_file = os.path.join(utils.TMP_DIR, "audit_results.txt")
    if not os.path.exists(audit_file):
        print(f"Error: {audit_file} not found. Run 'audit' first.")
        return

    valid_skills = utils.get_valid_skills()
    valid_workflows = utils.get_valid_workflows()
    
    with open(audit_file, "r", encoding="utf-8") as f:
        content = f.read()

    with open(utils.PROFILES_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    profiles = data.get("profiles", {})
    
    sections = re.split(r'={70}', content)
    total_added_skills = 0
    total_added_workflows = 0
    skipped_ids = set()
    
    for section in sections:
        profile_match = re.search(r'PROFILE:\s+([a-zA-Z0-9_-]+)', section)
        if not profile_match:
            continue
        pname = profile_match.group(1).strip()
        if pname not in profiles:
            continue
            
        eff_skills = utils.get_effective_set(pname, profiles, "skills")
        eff_workflows = utils.get_effective_set(pname, profiles, "workflows")

        # Extract missing skills
        skill_matches = re.findall(r"MISSING SKILL:\s+([a-zA-Z0-9_-]+)", section)
        for sid in skill_matches:
            if sid in valid_skills:
                if sid not in eff_skills:
                    profiles[pname].setdefault("skills", []).append(sid)
                    eff_skills.add(sid)
                    print(f"[{pname}] + Added skill: {sid}")
                    total_added_skills += 1
            else:
                skipped_ids.add(f"Skill '{sid}' (not in SKILLS.md)")
        
        # Extract missing workflows
        workflow_matches = re.findall(r"MISSING WORKFLOW:\s+([a-zA-Z0-9_-]+)", section)
        for wid in workflow_matches:
            if wid in valid_workflows:
                if wid not in eff_workflows:
                    profiles[pname].setdefault("workflows", []).append(wid)
                    eff_workflows.add(wid)
                    print(f"[{pname}] + Added workflow: {wid}")
                    total_added_workflows += 1
            else:
                skipped_ids.add(f"Workflow '{wid}' (not in WORKFLOWS.md)")

    if skipped_ids:
        print("\nSkipped IDs (not found in root docs):")
        for skipped in sorted(list(skipped_ids)):
            print(f"  - {skipped}")

    if total_added_skills > 0 or total_added_workflows > 0:
        for p in profiles.values():
            if "skills" in p: p["skills"].sort()
            if "workflows" in p: p["workflows"].sort()

        with open(utils.PROFILES_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        
        print("\n" + "="*50)
        print(f"SUCCESS: Added {total_added_skills} skills and {total_added_workflows} workflows.")
        print("="*50)
    else:
        print("\nNo new validated dependencies found to add.")

def main():
    parser = argparse.ArgumentParser(description="Workspace Maintenance CLI")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("stats", help="Display profile statistics (Inherited counts)")
    subparsers.add_parser("audit", help="Audit profiles for missing IDs or broken references")
    subparsers.add_parser("fix", help="Fix missing profile dependencies based on audit output")

    args = parser.parse_args()

    if args.command == "stats": cmd_stats(args)
    elif args.command == "audit": cmd_audit(args)
    elif args.command == "fix": cmd_fix(args)
    else: parser.print_help()

if __name__ == "__main__":
    main()
