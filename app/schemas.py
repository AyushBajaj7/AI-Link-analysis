from pydantic import BaseModel, ConfigDict, Field, HttpUrl, model_validator


class LinkAnalysisRequest(BaseModel):
    url: HttpUrl
    model_config = ConfigDict(extra="forbid")


class BusinessAnalysis(BaseModel):
    business_overview: str
    business_category: str
    products_services: list[str]
    target_customers: list[str]
    strengths: list[str]
    weaknesses: list[str]
    inferences: list[str]


class Competitor(BaseModel):
    name: str
    website: str = ""
    verification_status: str
    reason: str = ""
    strengths: list[str] = Field(default_factory=list)
    weaknesses: list[str] = Field(default_factory=list)


class CompetitorAnalysis(BaseModel):
    competitors: list[Competitor] = Field(default_factory=list)
    competitive_advantages: list[str] = Field(default_factory=list)
    gaps: list[str] = Field(default_factory=list)
    opportunities: list[str] = Field(default_factory=list)
    evidence: list[str] = Field(default_factory=list)
    inferences: list[str] = Field(default_factory=list)


class SearchQuery(BaseModel):
    query: str
    platform: str
    search_intent: str
    relevance: str = ""
    target_audience: str = ""


class SearchQueryAnalysis(BaseModel):
    queries: list[SearchQuery] = Field(min_length=5, max_length=5)
    research_note: str = "These are AI-generated recommendations, not measured search-volume results."

    @model_validator(mode="before")
    @classmethod
    def handle_search_queries(cls, values):
        if isinstance(values, dict) and "search_queries" in values and "queries" not in values:
            values["queries"] = values["search_queries"]
        return values


class SEOAnalysis(BaseModel):
    primary_keywords: list[str] = Field(default_factory=list)
    secondary_keywords: list[str] = Field(default_factory=list)
    long_tail_keywords: list[str] = Field(default_factory=list)
    seo_title: str = ""
    meta_description: str = ""
    content_recommendations: list[str] = Field(default_factory=list)
    optimization_notes: list[str] = Field(default_factory=list)
    research_note: str = "These are AI-generated SEO recommendations, not measured ranking or search-volume data."


class ServiceItem(BaseModel):
    service_name: str
    description: str
    target_industry: str = ""
    customer_benefit: str = ""
    recommendation_type: str
    reason: str = ""


class ServiceAnalysis(BaseModel):
    services: list[ServiceItem] = Field(min_length=5, max_length=5)
    research_note: str = "Existing services are based on website evidence. Inferred services are AI-generated recommendations."

    @model_validator(mode="before")
    @classmethod
    def handle_top_services(cls, values):
        if isinstance(values, dict) and "top_services" in values and "services" not in values:
            values["services"] = values["top_services"]
        return values


class CustomerProfile(BaseModel):
    profile_name: str
    customer_type: str = ""
    needs: list[str] = Field(default_factory=list)
    challenges: list[str] = Field(default_factory=list)
    relevant_services: list[str] = Field(default_factory=list)


class AudienceAnalysis(BaseModel):
    primary_audience: str = ""
    secondary_audience: str = ""
    industries: list[str] = Field(default_factory=list)
    business_types: list[str] = Field(default_factory=list)
    customer_profiles: list[CustomerProfile] = Field(default_factory=list)
    geographic_markets: list[str] = Field(default_factory=list)
    customer_needs: list[str] = Field(default_factory=list)
    customer_challenges: list[str] = Field(default_factory=list)
    customer_interests: list[str] = Field(default_factory=list)
    marketing_segments: list[str] = Field(default_factory=list)
    evidence: list[str] = Field(default_factory=list)
    inferences: list[str] = Field(default_factory=list)


class LinkAnalysisResponse(BaseModel):
    message: str = "Website analysis completed successfully"
    status: str = "success"
    website_data: dict
    analysis: BusinessAnalysis
    competitor_analysis: CompetitorAnalysis
    search_query_analysis: SearchQueryAnalysis
    seo_analysis: SEOAnalysis
    service_analysis: ServiceAnalysis
    audience_analysis: AudienceAnalysis
