import pytest
from app.services.content_processor import (
    clean_text,
    process_website_data
)


def test_clean_text():
    result = clean_text("  Hello   World!  ")
    assert result == "Hello World!"


def test_process_website_data():
    data = {
        "url": "https://example.com",
        "title": "Example Website",
        "description": "A sample website",
        "headings": [
            {"tag": "h1", "text": "Welcome"},
            {"tag": "h2", "text": "About"},
            {"tag": "h2", "text": "About"}
        ],
        "content": "This is a sample website with enough readable content to test the content processing functionality successfully."
    }
    result = process_website_data(data)
    assert result["title"] == "Example Website"
    assert len(result["headings"]) == 2
    assert result["word_count"] > 0
    assert result["content"]


def test_insufficient_content():
    data = {
        "url": "https://example.com",
        "title": "Example",
        "description": "",
        "headings": [],
        "content": "Too short"
    }
    with pytest.raises(ValueError):
        process_website_data(data)
