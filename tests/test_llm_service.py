import pytest
from app.services.llm_service import analyze_website


@pytest.mark.asyncio
async def test_missing_api_key(monkeypatch):
    monkeypatch.setattr(
        "app.services.llm_service.OPENAI_API_KEY",
        ""
    )
    with pytest.raises((RuntimeError, ValueError)):
        await analyze_website({
            "url": "https://example.com",
            "title": "Example",
            "description": "",
            "headings": [],
            "content": "Sample website content"
        })
