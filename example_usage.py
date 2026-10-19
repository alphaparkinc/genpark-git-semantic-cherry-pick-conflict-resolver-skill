"""Example usage for Git Semantic Cherry-Pick Conflict Resolver."""
from client import GitSemanticCherryPickConflictResolver

if __name__ == "__main__":
    base = "import os\ndef init(): pass"
    ours = "import os\nimport sys\ndef init(): pass\ndef helper_a(): return 1"
    theirs = "import os\nimport math\ndef init(): pass\ndef helper_b(): return 2"

    res = GitSemanticCherryPickConflictResolver.resolve_conflicts(base, ours, theirs)
    print("Resolved conflicts successfully:")
    print(res)
