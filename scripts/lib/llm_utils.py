import json
import urllib.request
import urllib.error
from typing import Dict, List, Optional, Any

LLM_BASE_URL = "http://localhost:11434/v1"
_IS_AVAILABLE: Optional[bool] = None

def is_lm_studio_available() -> bool:
    """Proactively checks if the LLM server is reachable."""
    global _IS_AVAILABLE
    if _IS_AVAILABLE is not None:
        return _IS_AVAILABLE
        
    try:
        models_url = f"{LLM_BASE_URL}/models"
        req = urllib.request.Request(models_url)
        with urllib.request.urlopen(req, timeout=1.5):
            pass
        _IS_AVAILABLE = True
        return True
    except Exception as e:
        print(f"  [LLM] Server unreachable. Operating in offline local fallback mode.")
        _IS_AVAILABLE = False
        return False

def call_lm_studio(system_prompt: str, user_prompt: str, timeout: int = 15) -> Optional[Dict[str, Any]]:
    """Calls LLM API and safely attempts to parse a JSON response."""
    if not is_lm_studio_available():
        return None
        
    data = {
        "model": "local-model",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.0,
        "stream": False
    }
    
    req = urllib.request.Request(
        f"{LLM_BASE_URL}/chat/completions",
        data=json.dumps(data).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            result = json.loads(response.read().decode('utf-8'))
            content = result["choices"][0]["message"]["content"]
            
            # Simple cleanup in case model wrapped it in markdown code blocks
            content = content.replace("```json", "").replace("```", "").strip()
            return json.loads(content)
            
    except urllib.error.HTTPError as e:
        print(f"  [LLM] HTTP Error {e.code}: {e.reason} - {e.read().decode('utf-8')}")
        return None
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, KeyError) as e:
        print(f"  [LLM] LM Studio unreachable or invalid response: {e}")
        return None

def generate_skill_metadata(content: str) -> Optional[Dict[str, Any]]:
    """
    Given the content of a SKILL.md file, query LM Studio for 
    structured metadata (description, tags, triggers, mcp_tools, etc.)
    """
    system_prompt = """You are an expert developer assistant analyzing an AI system skill module.
Respond ONLY with a valid JSON object. Do not wrap it in markdown block quotes. Use this format:
{
  "description": "A concise 1-2 sentence description",
  "tags": ["cloud", "api", "security", "python"],
  "trigger_conditions": ["Use when needing...", "User asks for..."],
  "anti_triggers": ["Do not use for UI elements"],
  "mcp_tools": ["postgres-memory", "github"]
}
If a field is not applicable, return an empty array or empty string, but keep the keys.
"""
    
    user_prompt = f"Analyze the following SKILL.md content and extract metadata into the required JSON format.\n\nCONTENT:\n{content[:4000]}" # Truncate to avoid context window issues
    
    return call_lm_studio(system_prompt, user_prompt)

def generate_category_tags(tags_list: List[str]) -> Optional[List[str]]:
    """
    Given a list of tags belonging to a category, queries LM studio 
    to synthesize 6-8 high-level conceptual domain tags representing the category.
    """
    if not tags_list:
        return []
        
    system_prompt = """You are a domain-mapping AI assigning high-level categories to directories based on their files' metadata.
Respond ONLY with a valid JSON object. Do not wrap it in markdown block quotes. Use this format:
{
  "category_tags": ["domain1", "domain2"]
}
"""

    tags_str = ", ".join(tags_list)
    user_prompt = f"I have a directory of skills with the following tags: [{tags_str}]. Synthesize exactly 5-8 high-level fundamental domain tags that best summarize this category."
    
    result = call_lm_studio(system_prompt, user_prompt)
    if result and "category_tags" in result:
        return result["category_tags"]
    return None

def generate_workflow_metadata(content: str) -> Optional[Dict[str, Any]]:
    """
    Given the content of a workflow file, query LM Studio for 
    structured metadata (description, tags, triggers, entry_point).
    """
    system_prompt = """You are an expert developer assistant analyzing an AI system workflow module.
Respond ONLY with a valid JSON object. Do not wrap it in markdown block quotes. Use this format:
{
  "description": "A concise 1-2 sentence description",
  "tags": ["automation", "git", "testing"],
  "triggers": ["workflow-slug-name", "git-commit-hook"],
  "entry_point": "None"
}
If a field is not applicable, return an empty array or empty string, but keep the keys.
"""
    
    user_prompt = f"Analyze the following workflow content and extract metadata into the required JSON format.\n\nCONTENT:\n{content[:4000]}"
    
    return call_lm_studio(system_prompt, user_prompt)

