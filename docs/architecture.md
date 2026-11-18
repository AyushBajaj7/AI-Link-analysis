# System Architecture

## Overview

The AI Link Analysis API uses a modular architecture.

The application separates request handling, website extraction,
content processing, AI analysis, and response validation.

## Processing Flow

1. Client submits a website URL.
2. FastAPI receives the request.
3. Pydantic validates the request.
4. URL security validation is performed.
5. HTTPX retrieves the website.
6. BeautifulSoup extracts readable HTML content.
7. Content processing cleans and prepares the extracted data.
8. The central analysis service coordinates the AI modules.
9. AI responses are parsed and validated.
10. The API returns structured JSON.

## Main Components

### main.py
Handles HTTP endpoints and request processing.

### website_extractor.py
Retrieves website HTML and extracts relevant information.

### content_processor.py
Cleans and prepares website content.

### analysis_service.py
Coordinates the individual AI analysis modules.

### llm_service.py
Generates business information.

### competitor_service.py
Identifies competitors and competitive opportunities.

### keyword_service.py
Generates search query recommendations.

### seo_service.py
Produces SEO recommendations.

### service_recommendation.py
Identifies existing and potential business services.

### audience_service.py
Generates target audience profiles.

### schemas.py
Defines request and response structures.

### url_validator.py
Validates URLs and blocks non-public destinations.

### response_validator.py
Validates AI-generated data against Pydantic models.

## AI Processing

The analysis modules currently run concurrently using
Python asyncio.

Each module receives the processed website information
and generates a different analysis result.

The central service combines the results into one response.

## Security Considerations

Production deployment requires outbound network restrictions
or validated DNS address pinning to prevent SSRF and
DNS-rebinding attacks.
