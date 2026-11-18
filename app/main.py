import httpx
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from openai import APIError, APIConnectionError, APITimeoutError
from app.schemas import LinkAnalysisRequest
from app.utils.url_validator import validate_url
from app.services.website_extractor import extract_website
from app.services.content_processor import process_website_data
from app.services.analysis_service import run_complete_analysis

app = FastAPI(
    title="AI Link Analysis API",
    description="Production-ready FastAPI service that analyzes websites using AI to generate competitor intelligence, search queries, SEO strategies, services, and audience segments.",
    version="1.0.0"
)

# Enable CORS for cross-origin frontend or evaluation clients (credentials disabled for wildcard origin)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def home():
    """Homepage status endpoint."""
    return {
        "message": "AI Link Analysis API is running",
        "status": "active"
    }


@app.get("/health")
async def health():
    """Application health probe."""
    return {
        "status": "healthy"
    }


@app.post("/link-analysis")
async def link_analysis(request: LinkAnalysisRequest):
    """Analyze a website link and generate comprehensive business intelligence across 5 major sections."""
    try:
        validate_url(str(request.url))
        website_data = await extract_website(str(request.url))
        processed_data = process_website_data(website_data)
        analysis_results = await run_complete_analysis(processed_data)

        # Extract brand summary
        raw_biz = analysis_results.get("analysis", {})
        title_str = processed_data.get("title", "")
        brand_name = (
            title_str.split("|")[0].split("-")[0].strip()
            if title_str
            else str(request.url).split("//")[-1].split("/")[0].replace("www.", "").capitalize()
        )
        brand = {
            "name": brand_name,
            "category": raw_biz.get("business_category", "Technology & Digital Services"),
            "summary": raw_biz.get("business_overview", "")
        }

        # Extract standardized modules
        comp_data = analysis_results.get("competitor_analysis", {})
        queries_data = analysis_results.get("search_query_analysis", {})
        seo_data = analysis_results.get("seo_analysis", {})
        services_data = analysis_results.get("service_analysis", {})
        audience_data = analysis_results.get("audience_analysis", {})

        queries_list = queries_data.get("queries") or queries_data.get("search_queries", [])
        services_list = services_data.get("top_services") or services_data.get("services", [])

        # Standardize search queries so both 'platform' & 'platforms' and 'intent' & 'search_intent' are present
        normalized_queries = []
        for q in queries_list:
            q_copy = dict(q)
            if "platforms" not in q_copy:
                p = q_copy.get("platform", "")
                q_copy["platforms"] = [p] if p else []
            if "platform" not in q_copy or not q_copy["platform"]:
                q_copy["platform"] = ", ".join(q_copy.get("platforms", []))
            intent_val = q_copy.get("intent") or q_copy.get("search_intent", "")
            q_copy["intent"] = intent_val
            q_copy["search_intent"] = intent_val
            rel_val = q_copy.get("business_relevance") or q_copy.get("relevance", "")
            q_copy["business_relevance"] = rel_val
            q_copy["relevance"] = rel_val
            normalized_queries.append(q_copy)

        # Standardize SEO improvements for both plural and singular key structures
        seo_copy = dict(seo_data)
        if "primary_keywords" in seo_copy and seo_copy["primary_keywords"] and "primary_keyword" not in seo_copy:
            seo_copy["primary_keyword"] = seo_copy["primary_keywords"][0]
        if "primary_keyword" in seo_copy and not seo_copy.get("primary_keywords"):
            seo_copy["primary_keywords"] = [seo_copy["primary_keyword"]]
        if "seo_title" in seo_copy and "recommended_title" not in seo_copy:
            seo_copy["recommended_title"] = seo_copy["seo_title"]
        if "recommended_title" in seo_copy and "seo_title" not in seo_copy:
            seo_copy["seo_title"] = seo_copy["recommended_title"]
        if "content_recommendations" in seo_copy and "supporting_content" not in seo_copy:
            seo_copy["supporting_content"] = seo_copy["content_recommendations"]
        if "supporting_content" in seo_copy and "content_recommendations" not in seo_copy:
            seo_copy["content_recommendations"] = seo_copy["supporting_content"]

        # Standardize top services
        normalized_services = []
        for s in services_list:
            s_copy = dict(s)
            if "target_customer" not in s_copy:
                s_copy["target_customer"] = s_copy.get("target_industry", "")
            if "main_benefit" not in s_copy:
                s_copy["main_benefit"] = s_copy.get("customer_benefit", "")
            if "customer_benefit" not in s_copy:
                s_copy["customer_benefit"] = s_copy.get("main_benefit", "")
            normalized_services.append(s_copy)

        # Standardize competitor analysis
        comp_copy = dict(comp_data)
        comp_copy.setdefault("brand_name", brand_name)
        comp_copy.setdefault("brand_overview", raw_biz.get("business_overview", ""))
        comp_copy.setdefault("brand_strengths", raw_biz.get("strengths", []))
        comp_copy.setdefault("brand_advantages", comp_copy.get("competitive_advantages", []))
        comp_copy.setdefault("market_opportunities", comp_copy.get("opportunities", []))

        # Unified analysis container conforming to the official specification
        unified_analysis = {
            "business_overview": raw_biz.get("business_overview", ""),
            "business_category": raw_biz.get("business_category", ""),
            "products_services": raw_biz.get("products_services", []),
            "target_customers": raw_biz.get("target_customers", []),
            "strengths": raw_biz.get("strengths", []),
            "weaknesses": raw_biz.get("weaknesses", []),
            "inferences": raw_biz.get("inferences", []),
            "competitor_analysis": comp_copy,
            "target_search_queries": normalized_queries,
            "seo_improvements": seo_copy,
            "top_services": normalized_services,
            "target_audience": audience_data,
        }

        return {
            "success": True,
            "status": "success",
            "message": "Website analysis completed successfully",
            "website": str(request.url),
            "brand": brand,
            "website_data": processed_data,
            "analysis": unified_analysis,
            "competitor_analysis": comp_data,
            "search_query_analysis": queries_data,
            "seo_analysis": seo_data,
            "service_analysis": services_data,
            "audience_analysis": audience_data,
        }
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except RuntimeError:
        raise HTTPException(
            status_code=503,
            detail="AI service is not configured correctly"
        )
    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=502,
            detail=f"Website returned HTTP status {e.response.status_code}"
        )
    except httpx.TimeoutException:
        raise HTTPException(
            status_code=504,
            detail="Request to website timed out"
        )
    except httpx.RequestError:
        raise HTTPException(
            status_code=502,
            detail="Unable to connect to the website"
        )
    except APITimeoutError:
        raise HTTPException(
            status_code=504,
            detail="AI provider request timed out"
        )
    except APIConnectionError:
        raise HTTPException(
            status_code=502,
            detail="Could not connect to AI provider"
        )
    except APIError:
        raise HTTPException(
            status_code=502,
            detail="AI provider request failed"
        )
