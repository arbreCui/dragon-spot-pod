"""UNREADY source-only function candidate; not installed or a production resource admission."""
from pathlib import Path

def validate_history_roots(values, artifacts_root):
    base = Path(artifacts_root).resolve(strict=True)
    if not isinstance(values, list) or not values:
        raise ValueError("explicit complete-history resource roots required")
    roots = []
    overlap_trie = {}
    for value in values:
        if not isinstance(value, str):
            raise ValueError("resource roots must be absolute directory paths")
        path = Path(value)
        if (not path.is_absolute() or ".." in path.parts or path == base or not path.is_relative_to(base)):
            raise ValueError("resource roots must be strict validation/artifacts descendants")
        cursor = path
        while cursor != base:
            if cursor.is_symlink() or (cursor.exists() and not cursor.is_dir()):
                raise ValueError("resource root or ancestor is a symlink/non-directory")
            cursor = cursor.parent
        branch = overlap_trie
        for part in path.parts:
            if None in branch:
                raise ValueError("resource roots overlap or repeat")
            branch = branch.setdefault(part, {})
        if branch:
            raise ValueError("resource roots overlap or repeat")
        branch[None] = None
        roots.append(path)
    return roots
