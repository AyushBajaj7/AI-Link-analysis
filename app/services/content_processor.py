"""Content processing and semantic cleaning service."""

import re


def clean_text(text: str) -> str:
    """Remove extra whitespace and sanitize text characters while preserving semantic tokens."""
    if not text:
        return ""
    text = re.sub(r"\s+", " ", text)
    # Preserve alphanumeric, common punctuation, currencies ($€£¥) and brackets
    text = re.sub(r"[^\w\s.,!?;:'\"()&/@#%+\-$€£¥\[\]]", " ", text)
    return text.strip()


def process_website_data(data: dict) -> dict:
    """Clean and structure extracted website information and check for sufficient content."""
    content = clean_text(data.get("content", ""))

    headings = []
    seen = set()
    for heading in data.get("headings", []):
        heading_text = clean_text(heading.get("text", ""))
        if heading_text and heading_text.lower() not in seen:
            headings.append({
                "tag": heading.get("tag", ""),
                "text": heading_text
            })
            seen.add(heading_text.lower())

    words = content.split()
    if len(words) < 15:
        raise ValueError("Website does not contain enough readable content")

    return {
        "url": data.get("url", ""),
        "title": clean_text(data.get("title", "")),
        "description": clean_text(data.get("description", "")),
        "headings": headings[:50],
        "content": content[:15000],
        "word_count": len(words)
    }
