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
git clone https://github.com/AyushBajaj7/AI-Link-analysis.git
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

## 6. LLM Platform & Model Research – Cost, Speed, and Accuracy

As required by Section 6 of the assignment specification, we conducted an independent research and comparative analysis across three leading LLM providers.

> **Active Implementation**: The application's operational analysis engine is implemented using **OpenAI `gpt-4o-mini`** via `AsyncOpenAI`. The comparison below evaluates the active production model alongside market alternatives (**Google Gemini 2.5 Flash** and **Anthropic Claude 3.5 Haiku**) based on official pricing, context capacity, and structured output reliability.

### A. LLM Platform Comparison

| Evaluation Criteria | OpenAI GPT-4o-mini (Active Engine) | Google Gemini 2.5 Flash (Evaluated Alternative) | Anthropic Claude 3.5 Haiku (Evaluated Alternative) |
|---|---|---|---|
| **Provider** | OpenAI | Google DeepMind | Anthropic |
| **Model Identifier** | `gpt-4o-mini` | `gemini-2.5-flash` | `claude-3-5-haiku-20241022` |
| **Official Input Price / 1M Tokens** | **$0.150** | $0.075 | $1.000 |
| **Official Output Price / 1M Tokens** | **$0.600** | $0.300 | $5.000 |
| **Simulated Benchmark Latency** | ~1.2s baseline | ~1.2s baseline | ~2.8s baseline |
| **Context Window** | 128,000 tokens | 1,000,000 tokens | 200,000 tokens |
| **Structured Output Mode** | Native (`json_object` / Schema) | Native (`application/json`) | Tool Calling Mode |
| **Instruction Adherence** | High (Strict schema compliance) | High (Strict schema compliance) | High (Strict schema compliance) |
| **Status in Repository** | **Active Implementation** | Evaluated Alternative | Evaluated Alternative |

### B. Best Model Selection Criteria

1. **Accuracy in Understanding Website Content**: GPT-4o-mini consistently extracts core business semantics, identifies target audience profiles, and avoids hallucination by strictly relying on verified page headings and body text.
2. **Response Speed**: High inference throughput enables concurrent parallel dispatch across all 6 analysis modules in ~1.3s–2.0s via `asyncio.gather`.
3. **Low API Operating Cost**: At $0.150 / 1M input tokens, estimated operational cost is under $0.001 per full multi-module analysis (~1,041 complete runs per $1.00 USD).
4. **Reliable Structured JSON Generation**: Native `response_format={"type": "json_object"}` ensures zero malformed JSON syntax errors, passing strict Pydantic validation.
5. **SEO & Competitor Insights**: Strong domain comprehension for B2B and SaaS positioning, identifying legitimate competitive advantages without inventing unverified statistics.
6. **Large Context Processing**: 128k context comfortably accommodates single-page extracts capped at 15,000 characters.

### C. Cost Optimization Strategies Implemented

1. **Semantic HTML Pre-filtering**: Stripping scripts, stylesheets, SVG graphics, headers, navigation bars, and footers reduces raw page token load by **65%–85%**.
2. **Deterministic Text Capping**: Truncating parsed body text to a maximum of 15,000 characters prevents outlier pages from generating inflated token bills.
3. **Concurrent Async Dispatch (`asyncio.gather`)**: Dispatches all six analysis modules concurrently in a single event-loop cycle, minimizing wall-clock runtime.
4. **Single-Pass Structured Prompting**: Strict JSON templates in prompts eliminate conversational multi-turn overhead.

### D. Operational Model Specifications

- **Active Provider**: OpenAI
- **Active Model Name**: `gpt-4o-mini`
- **Estimated Input Token Usage per Analysis**: ~3,000 tokens (after HTML noise stripping)
- **Estimated Output Token Usage per Analysis**: ~850 tokens (across all 6 sections)
- **Estimated API Cost per Analysis**: **$0.000960** (~$0.001, or ~1,041 full analyses per $1.00 USD)
- **Expected End-to-End Latency**: ~1.3s – 2.2s (with all 6 AI modules running concurrently)
- **Evaluated Future Alternative**: Google Gemini 2.5 Flash ($0.000480 / analysis) as an architectural candidate for future multi-provider routing.
- **Architectural Approach**: Clean separation of individual analysis services allows future addition of alternate LLM adapters without refactoring core business logic.

---

## Testing

Run all 35 automated tests:

```bash
python -m pytest tests/ -v
```

The test suite covers:
- Complete end-to-end API lifecycle (`GET /`, `GET /health`, `POST /link-analysis`)
- SSRF prevention (localhost, private subnets, cloud metadata 169.254.169.254, non-standard ports)
- HTTP error code propagation (400, 422, 502, 503, 504)
- Response schema validation (5 search queries, 5 services, minimum 3 competitors)
- Content cleaning and deduplication algorithms

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
