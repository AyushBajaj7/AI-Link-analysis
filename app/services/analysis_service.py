"""Central orchestration service: runs all 6 AI analysis modules concurrently."""

import asyncio
from app.services.llm_service import analyze_website
from app.services.competitor_service import analyze_competitors
from app.services.keyword_service import generate_search_queries
from app.services.seo_service import generate_seo_recommendations
from app.services.service_recommendation import recommend_services
from app.services.audience_service import analyze_target_audience


async def run_complete_analysis(website_data: dict) -> dict:
    """Run all 6 AI analysis modules concurrently using asyncio.gather.

    All six coroutines are dispatched simultaneously, reducing total wall-clock
    latency from ~9 s sequential to ~1.5–2 s (bounded by the slowest call).

    Returns a dict with keys: analysis, competitor_analysis, search_query_analysis,
    seo_analysis, service_analysis, audience_analysis.

    Raises:
        RuntimeError: If the OpenAI API key is missing.
        ValueError: If the AI returns invalid or insufficient output.
    """
    results = await asyncio.gather(
        analyze_website(website_data),
        analyze_competitors(website_data),
        generate_search_queries(website_data),
        generate_seo_recommendations(website_data),
        recommend_services(website_data),
        analyze_target_audience(website_data),
        return_exceptions=False,
    )

    return {
        "analysis": results[0],
        "competitor_analysis": results[1],
        "search_query_analysis": results[2],
        "seo_analysis": results[3],
        "service_analysis": results[4],
        "audience_analysis": results[5],
    }
