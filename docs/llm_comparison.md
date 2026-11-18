# LLM Platform & Model Comparison

This document provides a comparative evaluation of Large Language Model (LLM) providers and models for website link analysis, as required by Section 6 of the assignment specification.

> **Operational Status**: The active operational engine implemented in the codebase is **OpenAI `gpt-4o-mini`**. The comparison below benchmarks the active model against alternative market offerings (**Google Gemini 2.5 Flash** and **Anthropic Claude 3.5 Haiku**) across official pricing, architectural constraints, and estimated operational costs.

---

## 1. Official Provider Specifications & Pricing

| Criteria | OpenAI GPT-4o-mini (Active) | Google Gemini 2.5 Flash (Evaluated) | Anthropic Claude 3.5 Haiku (Evaluated) |
|---|---|---|---|
| **Provider** | OpenAI | Google DeepMind | Anthropic |
| **Model Identifier** | `gpt-4o-mini` | `gemini-2.5-flash` | `claude-3-5-haiku-20241022` |
| **Official Input Price / 1M Tokens** | **$0.150** | $0.075 | $1.000 |
| **Official Output Price / 1M Tokens**| **$0.600** | $0.300 | $5.000 |
| **Context Window** | 128,000 tokens | 1,000,000 tokens | 200,000 tokens |
| **Structured JSON Mode** | Native (`json_object` / Schema) | Native (`application/json`) | Tool Calling Mode |
| **Implementation Status** | **Active Implementation** | Evaluated Research Alternative | Evaluated Research Alternative |

---

## 2. Estimated Operational Cost per Analysis

Estimates are calculated based on typical cleaned website content:
- **Estimated Input**: ~3,000 tokens (HTML boilerplate, navigation, and noise tags stripped)
- **Estimated Output**: ~850 tokens (across 6 analysis modules)

### OpenAI GPT-4o-mini (Active Engine)
- Input: $\frac{3,000}{1,000,000} \times \$0.150 = \$0.000450$
- Output: $\frac{850}{1,000,000} \times \$0.600 = \$0.000510$
- **Total Estimated Cost per Run**: **$0.000960** (~1,041 complete analyses per $1.00 USD)

### Google Gemini 2.5 Flash (Evaluated Alternative)
- Input: $\frac{3,000}{1,000,000} \times \$0.075 = \$0.000225$
- Output: $\frac{850}{1,000,000} \times \$0.300 = \$0.000255$
- **Total Estimated Cost per Run**: **$0.000480** (~2,083 complete analyses per $1.00 USD)

### Anthropic Claude 3.5 Haiku (Evaluated Alternative)
- Input: $\frac{3,000}{1,000,000} \times \$1.000 = \$0.003000$
- Output: $\frac{850}{1,000,000} \times \$5.000 = \$0.004250$
- **Total Estimated Cost per Run**: **$0.007250** (~138 complete analyses per $1.00 USD)

---

## 3. Qualitative Model Comparison

| Evaluation Dimension | OpenAI GPT-4o-mini | Google Gemini 2.5 Flash | Anthropic Claude 3.5 Haiku |
|---|---|---|---|
| **JSON Schema Enforcement** | Reliable schema adherence via `response_format={"type": "json_object"}`. | Strong native JSON mode support via SDK. | Requires structured tool calling definition. |
| **Search Query & SEO Understanding** | High comprehension of marketing intent, platform nuances (LinkedIn vs IG vs Google). | Strong general knowledge and entity identification. | Strong nuances in tone and B2B positioning. |
| **Large Website Handling** | 128k context is sufficient for all single-page text extracts (15k char limit). | 1M context is ideal for future deep full-domain crawlers. | 200k context handles extensive corporate documentation. |
| **Availability & Ecosystem** | Broad regional availability and stable developer ecosystem. | Rapidly expanding global availability. | High demand; regional rate-limiting variations. |

---

## 4. Benchmark Runner Execution

The repository includes a benchmark simulation utility (`tests/model_comparison.py`) to verify relative throughput behavior:

```bash
python tests/model_comparison.py
```

Output:
- `gpt-4o-mini`: ~1.20s simulated latency baseline
- `gemini-2.5-flash`: ~1.20s simulated latency baseline
- `claude-3-5-haiku`: ~2.80s simulated latency baseline

---

## 5. Selection Rationale

1. **Production Reliability**: `gpt-4o-mini` is implemented as the active engine because it provides high determinism in structured JSON generation, fast parallel completions via `AsyncOpenAI`, and cost efficiency ($0.00096 per full run).
2. **Future Extensibility**: The modular service architecture allows adding Gemini 2.5 Flash as an alternate provider in the future by introducing a provider abstraction layer without modifying existing business logic.
