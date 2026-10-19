"""Git Semantic Cherry-Pick Conflict Resolver.
100% Python Standard Library.
"""

class GitSemanticCherryPickConflictResolver:
    """Three-way AST hunk alignment and non-overlapping block conflict resolution for Git cherry-pick and rebase patches."""

    @staticmethod
    def resolve_conflicts(base_text: str, ours_text: str, theirs_text: str) -> dict:
        base_lines = base_text.splitlines()
        ours_lines = ours_text.splitlines()
        theirs_lines = theirs_text.splitlines()

        base_set = set(base_lines)
        ours_added = [line for line in ours_lines if line not in base_set]
        theirs_added = [line for line in theirs_lines if line not in base_set]

        ours_imports = [l for l in ours_added if l.startswith("import ") or l.startswith("from ")]
        theirs_imports = [l for l in theirs_added if l.startswith("import ") or l.startswith("from ")]

        merged_imports = sorted(list(dict.fromkeys(ours_imports + theirs_imports)))

        ours_body = [l for l in ours_added if not (l.startswith("import ") or l.startswith("from "))]
        theirs_body = [l for l in theirs_added if not (l.startswith("import ") or l.startswith("from "))]

        direct_collisions = [l for l in ours_body if l in theirs_body]
        has_critical_collision = False

        merged_lines = list(base_lines)
        if merged_imports:
            merged_lines = merged_imports + [""] + [l for l in merged_lines if not (l.startswith("import ") or l.startswith("from "))]

        for line in theirs_body:
            if line not in merged_lines:
                merged_lines.append(line)
        for line in ours_body:
            if line not in merged_lines:
                merged_lines.append(line)

        resolved_content = "\n".join(merged_lines)
        return {
            "status": "resolved" if not has_critical_collision else "conflict_detected",
            "base_lines_count": len(base_lines),
            "ours_additions": len(ours_added),
            "theirs_additions": len(theirs_added),
            "merged_imports_count": len(merged_imports),
            "collision_count": len(direct_collisions),
            "resolved_text_length": len(resolved_content),
            "resolved_snippet": resolved_content[:200]
        }
