import httpx
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock, MagicMock
from openai import APITimeoutError, APIConnectionError, APIError
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
        "search_query_analysis": {"queries": [{"query": "q1", "platform": "Google", "search_intent": "Info"}], "research_note": "AI"},
        "seo_analysis": {"primary_keywords": ["kw1"], "secondary_keywords": [], "long_tail_keywords": [], "seo_title": "Title", "meta_description": "Desc", "content_recommendations": [], "optimization_notes": [], "research_note": ""},
        "service_analysis": {"top_services": [{"service_name": "S1", "description": "D1", "target_industry": "Tech", "customer_benefit": "Speed", "recommendation_type": "existing"}], "research_note": "AI"},
        "audience_analysis": {"primary_audience": "Audience", "secondary_audience": "", "industries": [], "business_types": [], "customer_profiles": [], "geographic_markets": [], "customer_needs": [], "customer_challenges": [], "customer_interests": [], "marketing_segments": [], "evidence": [], "inferences": []}
    }

    with patch("app.main.run_complete_analysis", new_callable=AsyncMock) as mock_run:
        mock_run.return_value = mock_results
        response = client.post("/link-analysis", json={"url": "https://example.com"})
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["status"] == "success"
        assert "brand" in data
        assert "website" in data
        assert "analysis" in data
        # Check all 5 core sections inside unified analysis
        unified = data["analysis"]
        assert "competitor_analysis" in unified
        assert "target_search_queries" in unified
        assert "seo_improvements" in unified
        assert "top_services" in unified
        assert "target_audience" in unified

        # Check normalization
        assert unified["target_search_queries"][0]["platforms"] == ["Google"]
        assert unified["seo_improvements"]["primary_keyword"] == "kw1"
        assert unified["seo_improvements"]["recommended_title"] == "Title"
        assert unified["top_services"][0]["target_customer"] == "Tech"
        assert unified["top_services"][0]["main_benefit"] == "Speed"


def test_api_ai_not_configured():
    with patch("app.main.run_complete_analysis", new_callable=AsyncMock) as mock_run:
        mock_run.side_effect = RuntimeError("OpenAI API key is not configured")
        response = client.post("/link-analysis", json={"url": "https://example.com"})
        assert response.status_code == 503
        assert "AI service is not configured" in response.json()["detail"]


def test_api_website_timeout():
    with patch("app.main.extract_website", new_callable=AsyncMock) as mock_extract:
        mock_extract.side_effect = httpx.ReadTimeout("Timeout")
        response = client.post("/link-analysis", json={"url": "https://example.com"})
        assert response.status_code == 504
        assert "timed out" in response.json()["detail"]


def test_api_website_connection_error():
    with patch("app.main.extract_website", new_callable=AsyncMock) as mock_extract:
        mock_extract.side_effect = httpx.ConnectError("Connection refused")
        response = client.post("/link-analysis", json={"url": "https://example.com"})
        assert response.status_code == 502
        assert "Unable to connect" in response.json()["detail"]


def test_api_openai_timeout():
    with patch("app.main.run_complete_analysis", new_callable=AsyncMock) as mock_run:
        mock_request = MagicMock()
        mock_run.side_effect = APITimeoutError(request=mock_request)
        response = client.post("/link-analysis", json={"url": "https://example.com"})
        assert response.status_code == 504
        assert "timed out" in response.json()["detail"]
