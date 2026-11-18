import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
from app.main import app

client = TestClient(app)


def test_api_home():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "active"


def test_api_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_api_missing_url():
    response = client.post("/link-analysis", json={})
    assert response.status_code == 422


def test_api_malformed_url():
    response = client.post("/link-analysis", json={"url": "not-a-valid-url"})
    assert response.status_code == 422


def test_api_extra_fields_rejected():
    response = client.post(
        "/link-analysis",
        json={"url": "https://example.com", "unexpected": "field"}
    )
    assert response.status_code == 422


def test_api_ssrf_blocked():
    response = client.post("/link-analysis", json={"url": "http://127.0.0.1"})
    assert response.status_code == 400


def test_api_successful_analysis():
    mock_results = {
        "analysis": {"business_overview": "Overview", "business_category": "Tech", "products_services": [], "target_customers": [], "strengths": [], "weaknesses": [], "inferences": []},
        "competitor_analysis": {"competitors": [], "competitive_advantages": [], "gaps": [], "opportunities": [], "evidence": [], "inferences": []},
        "search_query_analysis": {"queries": [], "research_note": "AI"},
        "seo_analysis": {"primary_keywords": [], "secondary_keywords": [], "long_tail_keywords": [], "seo_title": "", "meta_description": "", "content_recommendations": [], "optimization_notes": [], "research_note": ""},
        "service_analysis": {"top_services": [], "research_note": "AI"},
        "audience_analysis": {"primary_audience": "Audience", "secondary_audience": "", "industries": [], "business_types": [], "customer_profiles": [], "geographic_markets": [], "customer_needs": [], "customer_challenges": [], "customer_interests": [], "marketing_segments": [], "evidence": [], "inferences": []}
    }

    with patch("app.main.run_complete_analysis", new_callable=AsyncMock) as mock_run:
        mock_run.return_value = mock_results
        response = client.post("/link-analysis", json={"url": "https://example.com"})
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "analysis" in data
        assert "competitor_analysis" in data
        assert "search_query_analysis" in data
        assert "seo_analysis" in data
        assert "service_analysis" in data
        assert "audience_analysis" in data
