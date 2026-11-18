"""Response validation utility using Pydantic models."""

from typing import Any, Dict
from pydantic import ValidationError
from app.schemas import (
    BusinessAnalysis,
    CompetitorAnalysis,
    SearchQueryAnalysis,
    SEOAnalysis,
    ServiceAnalysis,
    AudienceAnalysis,
    LinkAnalysisResponse
)


def validate_ai_response(section_name: str, data: Dict[str, Any]) -> Any:
    """Validate a specific AI response dictionary against its Pydantic model.
    
    Raises:
        ValidationError: If the data does not conform to the model schema.
    """
    model_map = {
        "analysis": BusinessAnalysis,
        "competitor_analysis": CompetitorAnalysis,
        "search_query_analysis": SearchQueryAnalysis,
        "seo_analysis": SEOAnalysis,
        "service_analysis": ServiceAnalysis,
        "audience_analysis": AudienceAnalysis,
        "full_response": LinkAnalysisResponse
    }

    model = model_map.get(section_name)
    if not model:
        raise ValueError(f"Unknown analysis section '{section_name}' for validation.")

    return model.model_validate(data)
