import pytest
from app.services.service_recommendation import recommend_services


@pytest.mark.asyncio
async def test_missing_api_key(monkeypatch):
    monkeypatch.setattr(
        "app.services.service_recommendation.OPENAI_API_KEY",
        ""
    )
    with pytest.raises(RuntimeError):
        await recommend_services({
            "url": "https://example.com",
            "title": "Example",
            "description": "",
            "headings": [],
            "content": "Example website content"
        })
