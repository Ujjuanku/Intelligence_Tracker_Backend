import re

def preprocess_text(text: str) -> str:
    """
    Clean text content by removing dynamic noise like timestamps, 
    vote counts, and common navigation elements.
    """
    if not text:
        return ""

    lines = text.splitlines()
    cleaned_lines = []

    # Regex patterns to ignore
    patterns = [
        r'\b\d+\s+(points?|comments?|hours?|minutes?|days?|seconds?|years?|months?)\s+ago\b', # timestamps/counts
        r'^\d+\s+(points?|comments?)$', # standalone counts
        r'^\s*\|\s*hide\s*\|\s*$', # HN specific
        r'^\s*past\s*\|\s*comments\s*\|\s*ask\s*\|\s*show\s*\|\s*jobs\s*\|\s*submit\s*$', # HN header
        r'^\s*(login|sign\s*up|search|menu|help|guidelines|faq|legal|security|terms|privacy|contact|apply\s*to\s*yc)\s*$', # common nav
        r'^\s*search\s*:', # search bar
        r'^\d{4}-\d{2}-\d{2}', # raw dates
        r'©\s*\d{4}', # copyright years
    ]
    
    combined_pattern = re.compile('|'.join(patterns), re.IGNORECASE)

    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # Skip if matches noise pattern
        if combined_pattern.search(line):
            continue

        # Skip short numeric lines (likely pagination or counts)
        if line.isdigit() and len(line) < 5:
            continue

        cleaned_lines.append(line)

    return "\n".join(cleaned_lines)

def normalize_whitespace(text: str) -> str:
    """Replace multiple spaces/newlines with single ones."""
    return re.sub(r'\s+', ' ', text).strip()
