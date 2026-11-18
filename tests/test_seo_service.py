import pytest
from app.services.seo_service import generate_seo_recommendations


@pytest.mark.asyncio
async def test_missing_api_key(monkeypatch):
    monkeypatch.setattr(
        "app.services.seo_service.OPENAI_API_KEY",
        ""
    )
    with pytest.raises(RuntimeError):
        await generate_seo_recommendations({
            "url": "https://example.com",
            "title": "Example",
            "description": "",
            "headings": [],
            "content": "Example website content"
        })
