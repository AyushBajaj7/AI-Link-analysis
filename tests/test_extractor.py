import pytest
from app.services.website_extractor import extract_website


@pytest.mark.asyncio
async def test_extract_website():
    result = await extract_website("https://example.com")
    assert result["url"]
    assert result["title"]
    assert result["content"]
    assert isinstance(result["headings"], list)
