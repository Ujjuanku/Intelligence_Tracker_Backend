import difflib
from typing import Dict, Any

def generate_diff(old_text: str, new_text: str) -> Dict[str, Any]:
    """
    Compare two texts at a paragraph level and return structured diff.
    Filters out small numeric changes and short lines.
    """
    if not old_text:
        return {"added": new_text, "removed": "", "full_diff": "New Content", "lines_added_count": len(new_text.splitlines()), "lines_removed_count": 0}
    
    # Split into paragraphs (chunks separated by blank lines)
    old_paragraphs = [p.strip() for p in old_text.split('\n\n') if p.strip()]
    new_paragraphs = [p.strip() for p in new_text.split('\n\n') if p.strip()]

    d = difflib.Differ()
    diff = list(d.compare(old_paragraphs, new_paragraphs))

    added = []
    removed = []

    for line in diff:
        content = line[2:]
        if len(content) < 30: # Ignore short segments (increased threshold)
            continue

        if line.startswith('+ '):
            added.append(content)
        elif line.startswith('- '):
            removed.append(content)

    return {
        "added": "\n\n".join(added),
        "removed": "\n\n".join(removed),
        "lines_added_count": len(added),
        "lines_removed_count": len(removed)
    }
