import pytest
from pydantic import ValidationError
from app.schemas import (
    LinkAnalysisRequest,
    SearchQueryAnalysis,
    ServiceAnalysis
)


def test_valid_request():
    request = LinkAnalysisRequest(
        url="https://example.com"
    )
    assert str(request.url) == "https://example.com/"


def test_invalid_request():
    with pytest.raises(ValidationError):
        LinkAnalysisRequest(
            url="not-a-valid-url"
        )


def test_request_rejects_extra_fields():
    with pytest.raises(ValidationError):
        LinkAnalysisRequest(
            url="https://example.com",
            name="Example"
        )


def test_search_query_count_validation():
    with pytest.raises(ValidationError):
        SearchQueryAnalysis(
            queries=[
                {
                    "query": "test query",
                    "platform": "Google",
                    "search_intent": "Commercial"
                }
            ]
        )


def test_service_count_validation():
    with pytest.raises(ValidationError):
        ServiceAnalysis(
            services=[
                {
                    "service_name": "Test Service",
                    "description": "Test Description",
                    "recommendation_type": "existing"
                }
            ]
        )
