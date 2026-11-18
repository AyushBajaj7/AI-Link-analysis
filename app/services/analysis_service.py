import asyncio
from app.services.llm_service import analyze_website
from app.services.competitor_service import analyze_competitors
from app.services.keyword_service import generate_search_queries
from app.services.seo_service import generate_seo_recommendations
from app.services.service_recommendation import recommend_services
from app.services.audience_service import analyze_target_audience


async def run_complete_analysis(website_data):
    results = await asyncio.gather(
        analyze_website(website_data),
        analyze_competitors(website_data),
        generate_search_queries(website_data),
        generate_seo_recommendations(website_data),
        recommend_services(website_data),
        analyze_target_audience(website_data)
    )

    return {
        "analysis": results[0],
        "competitor_analysis": results[1],
        "search_query_analysis": results[2],
        "seo_analysis": results[3],
        "service_analysis": results[4],
        "audience_analysis": results[5]
    }
