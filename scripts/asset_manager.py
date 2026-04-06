#!/usr/bin/env python3
"""
Asset Manager CLI 🛠️
Unified interface for managing registry assets (skills, workflows, tags).
"""

import sys
import os

# Add lib to path so we can import the sub-modules
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "lib"))

def print_help():
    print("usage: asset_manager.py {tags, reorganize_skills, reorganize_workflows} ...")
    print("\nUnified interface for managing workspace assets. Now supports AI-driven metadata generation.")
    print("\nCommands:")
    print("  tags                  Extract operational tags. Supports --force-llm for AI synthesis.")
    print("  reorganize_skills     Sync skills with filesystem. Supports ingestion and AI metadata generation.")
    print("  reorganize_workflows  Sync workflows with filesystem. Supports ingestion and AI metadata generation.")
    print("\nCommon Flags (for subcommands):")
    print("  --force-llm           Connect to LM Studio/Ollama to regenerate or synthesize metadata using AI.")
    print("  --target <path>       Ingest and insert a single skill/workflow folder from /tmp/ without rebuilding the entire system.")
    print("\nRun a command with --help for its specific usage.")

def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print_help()
        sys.exit(0 if "-h" in sys.argv or "--help" in sys.argv else 1)

    cmd = sys.argv.pop(1)

    if cmd == "tags":
        import tags_generator
        tags_generator.main()
    elif cmd == "reorganize_skills":
        import skills_reorganizer
        skills_reorganizer.main()
    elif cmd == "reorganize_workflows":
        import workflows_reorganizer
        workflows_reorganizer.main()
    else:
        print(f"Error: Unknown command '{cmd}'\n")
        print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()
