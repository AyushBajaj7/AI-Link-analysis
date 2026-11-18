# AI Link Analysis API

An AI-powered website analysis system built with Python and FastAPI.

The application accepts a website URL, extracts its publicly accessible content, and uses Large Language Models (LLMs) to generate business intelligence, competitor research, SEO recommendations, service suggestions, and target audience insights.

## Features

### 1. Business Analysis
- Business overview
- Business category
- Products and services
- Target customers
- Business strengths and weaknesses
- Potential opportunities and inferences

### 2. Competitor Analysis
- Competitor identification
- Competitor website references
- Competitive strengths and weaknesses
- Competitive advantages
- Market gaps and opportunities
- Evidence and inferred findings

### 3. Search Query Recommendations
- Five relevant search query suggestions
- Platform identification
- Search intent
- Query relevance
- Target audience

### 4. SEO Recommendations
- Primary keywords
- Secondary keywords
- Long-tail keywords
- SEO title
- Meta description
- Content improvement recommendations

### 5. Service Recommendations
- Five relevant service recommendations
- Service descriptions
- Target industries
- Customer benefits
- Existing versus inferred service classification

### 6. Target Audience Analysis
- Primary and secondary audiences
- Relevant industries
- Business types
- Customer profiles
- Geographic markets
- Customer needs and challenges
- Customer interests
- Marketing segments

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| FastAPI | REST API framework |
| Uvicorn | ASGI server |
| Pydantic | Data validation |
| HTTPX | Asynchronous website requests |
| BeautifulSoup | HTML parsing |
| OpenAI API | AI-powered analysis |
| Pytest | Automated testing |

## Project Structure

```text
ai-link-analysis/
├── app/
│   ├── main.py
│   ├── config.py
│   ├── schemas.py
│   ├── services/
│   │   ├── website_extractor.py
│   │   ├── content_processor.py
│   │   ├── analysis_service.py
│   │   ├── llm_service.py
│   │   ├── competitor_service.py
│   │   ├── keyword_service.py
│   │   ├── seo_service.py
│   │   ├── service_recommendation.py
│   │   └── audience_service.py
│   └── utils/
│       ├── url_validator.py
│       ├── response_validator.py
│       └── logger.py
├── tests/
├── docs/
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Installation

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd ai-link-analysis
```

### 2. Create a virtual environment

Windows:

```powershell
python -m venv venv
venv\Scripts\activate
```

Linux and macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root.

```env
OPENAI_API_KEY=your_openai_api_key
LLM_MODEL=gpt-4o-mini
REQUEST_TIMEOUT=30
MAX_RETRIES=2
MAX_WEBSITE_SIZE=2097152
MAX_REDIRECTS=5
```

Never commit your actual API key.

### 5. Start the application

```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 4000
```

The API will be available at:

http://127.0.0.1:4000

## API Documentation

FastAPI automatically generates interactive Swagger documentation.

http://127.0.0.1:4000/docs

## API Endpoint

### POST /link-analysis

Accepts a website URL and generates a complete analysis.

#### Request

```json
{
  "url": "https://example.com"
}
```

#### Successful Response

The response contains:

- message
- status
- website_data
- analysis
- competitor_analysis
- search_query_analysis
- seo_analysis
- service_analysis
- audience_analysis

See `docs/sample_response.json` for a complete example generated from an actual successful API run.

## Testing

Run all automated tests:

```bash
python -m pytest tests/ -v
```

## LLM Evaluation

The project evaluates LLM providers using:

- API pricing
- Response speed
- Analysis quality
- Context window
- Structured JSON support
- Reliability

See:

- `docs/llm_comparison.md`
- `docs/cost_analysis.md`
- `docs/performance_results.md`

## Security

The application includes URL validation, public-address checks, redirect limits, content-size limits, and request timeouts.

Production deployments must also enforce DNS-pinning or equivalent network-level outbound protections to prevent SSRF and DNS-rebinding attacks.

API keys are managed through environment variables.

## Limitations

- Analysis quality depends on the available website content.
- Competitor suggestions may require independent verification.
- Search query recommendations are AI-generated suggestions, not measured search-volume data.
- Inferred services and audience profiles should not be treated as verified company facts.
- Website extraction may fail when a website blocks automated requests.
- AI-generated results should be reviewed before business decisions.

## Future Improvements

- Support for multiple LLM providers
- Result caching
- Consolidated AI requests
- Advanced competitor verification
- Search-volume integrations
- Background processing for large websites
- Dashboard for viewing analysis results

## Author

Ayush Bajaj
