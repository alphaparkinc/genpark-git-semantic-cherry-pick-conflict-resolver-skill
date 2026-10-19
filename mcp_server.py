"""MCP Server wrapper for Git Semantic Cherry-Pick Conflict Resolver."""
import json
import sys
from client import GitSemanticCherryPickConflictResolver

def handle_request(req):
    method = req.get("method")
    if method == "tools/list":
        return {
            "tools": [
                {
                    "name": "resolve_cherry_pick_conflicts",
                    "description": "Align three-way hunks and resolve non-colliding imports and code additions for Git cherry-pick and rebase",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "base_text": {"type": "string"},
                            "ours_text": {"type": "string"},
                            "theirs_text": {"type": "string"}
                        },
                        "required": ["base_text", "ours_text", "theirs_text"]
                    }
                }
            ]
        }
    elif method == "tools/call":
        args = req.get("params", {}).get("arguments", {})
        res = GitSemanticCherryPickConflictResolver.resolve_conflicts(
            args.get("base_text", ""),
            args.get("ours_text", ""),
            args.get("theirs_text", "")
        )
        return {
            "content": [
                {
                    "type": "text",
                    "text": json.dumps(res, indent=2)
                }
            ]
        }
    return {}

if __name__ == "__main__":
    for line in sys.stdin:
        if line.strip():
            try:
                r = json.loads(line)
                out = handle_request(r)
                print(json.dumps(out), flush=True)
            except Exception as e:
                print(json.dumps({"error": str(e)}), flush=True)
