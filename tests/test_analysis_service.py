import pytest
from unittest.mock import patch, AsyncMock
from app.services.analysis_service import run_complete_analysis


@pytest.mark.asyncio
async def test_run_complete_analysis():
    dummy_data = {
        "url": "https://example.com",
        "title": "Example",
        "description": "",
        "headings": [],
        "content": "Sample content"
    }

    with patch("app.services.analysis_service.analyze_website", new_callable=AsyncMock) as m1, \
         patch("app.services.analysis_service.analyze_competitors", new_callable=AsyncMock) as m2, \
         patch("app.services.analysis_service.generate_search_queries", new_callable=AsyncMock) as m3, \
         patch("app.services.analysis_service.generate_seo_recommendations", new_callable=AsyncMock) as m4, \
         patch("app.services.analysis_service.recommend_services", new_callable=AsyncMock) as m5, \
         patch("app.services.analysis_service.analyze_target_audience", new_callable=AsyncMock) as m6:
        m1.return_value = {"overview": "1"}
        m2.return_value = {"competitors": []}
        m3.return_value = {"queries": []}
        m4.return_value = {"keywords": []}
        m5.return_value = {"services": []}
        m6.return_value = {"audience": []}

        res = await run_complete_analysis(dummy_data)
        assert "analysis" in res
        assert "competitor_analysis" in res
        assert "search_query_analysis" in res
        assert "seo_analysis" in res
        assert "service_analysis" in res
        assert "audience_analysis" in res
