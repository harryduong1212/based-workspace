import os
import json
import urllib.request

def resolve_path(entrypoint):
    if entrypoint.endswith(".n8n"):
        return "webhook/" + os.path.basename(entrypoint)[:-4]
    return "webhook/" + entrypoint.lstrip("/")
print(resolve_path("n8n-workflows/daily-briefing.n8n"))
