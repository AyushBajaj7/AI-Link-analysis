import pytest
from app.services.keyword_service import generate_search_queries


@pytest.mark.asyncio
async def test_missing_api_key(monkeypatch):
    monkeypatch.setattr(
        "app.services.keyword_service.OPENAI_API_KEY",
        ""
    )
    with pytest.raises(RuntimeError):
        await generate_search_queries({
            "url": "https://example.com",
            "title": "Example",
            "description": "",
            "headings": [],
            "content": "Example website content"
        })
