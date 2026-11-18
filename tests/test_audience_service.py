import pytest
from app.services.audience_service import analyze_target_audience


@pytest.mark.asyncio
async def test_missing_api_key(monkeypatch):
    monkeypatch.setattr(
        "app.services.audience_service.OPENAI_API_KEY",
        ""
    )
    with pytest.raises(RuntimeError):
        await analyze_target_audience({
            "url": "https://example.com",
            "title": "Example",
            "description": "",
            "headings": [],
            "content": "Example website content"
        })
