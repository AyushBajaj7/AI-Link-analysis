import pytest
from app.services.competitor_service import analyze_competitors


@pytest.mark.asyncio
async def test_competitor_service_missing_api_key(monkeypatch):
    monkeypatch.setattr(
        "app.services.competitor_service.OPENAI_API_KEY",
        ""
    )
    with pytest.raises(RuntimeError):
        await analyze_competitors({
            "url": "https://example.com",
            "title": "Example",
            "description": "",
            "headings": [],
            "content": "Sample website content"
        })
