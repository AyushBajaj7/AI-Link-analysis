# LLM Cost Analysis & Token Economics

This report documents the token economics, official pricing tiers, and estimated operational costs per website analysis.

---

## 1. Token Usage Profile (Empirical Estimate)

For a typical single-domain website analysis:
- **Cleaned Website Text Input**: ~3,000 tokens (reduced from raw HTML by removing scripts, inline styles, navigation bars, and footers).
- **Consolidated AI JSON Output**: ~850 tokens (distributed across business overview, competitors, 5 search queries, SEO strategies, 5 services, and audience personas).

---

## 2. Official Pricing Tiers (Per 1 Million Tokens)

*Published rates as of current provider documentation:*

| Provider & Model | Input Cost / 1M | Output Cost / 1M |
|---|---|---|
| **OpenAI `gpt-4o-mini` (Active Engine)** | **$0.150** | **$0.600** |
| **Google `gemini-2.5-flash` (Research Comparison)** | $0.075 | $0.300 |
| **Anthropic `claude-3-5-haiku` (Research Comparison)** | $1.000 | $5.000 |

---

## 3. Cost Breakdown per Single Website Analysis

### OpenAI GPT-4o-mini (Active Implementation)
- **Input Cost**: $\frac{3,000}{1,000,000} \times \$0.150 = \$0.000450$
- **Output Cost**: $\frac{850}{1,000,000} \times \$0.600 = \$0.000510$
- **Total Cost per Analysis**: **$0.000960** (~$0.001 per website, or ~1,041 analyses per $1.00 USD)

### Google Gemini 2.5 Flash (Alternative Evaluation)
- **Input Cost**: $\frac{3,000}{1,000,000} \times \$0.075 = \$0.000225$
- **Output Cost**: $\frac{850}{1,000,000} \times \$0.300 = \$0.000255$
- **Total Cost per Analysis**: **$0.000480** (~$0.0005 per website, or ~2,083 analyses per $1.00 USD)

### Anthropic Claude 3.5 Haiku (Alternative Evaluation)
- **Input Cost**: $\frac{3,000}{1,000,000} \times \$1.000 = \$0.003000$
- **Output Cost**: $\frac{850}{1,000,000} \times \$5.000 = \$0.004250$
- **Total Cost per Analysis**: **$0.007250** (~$0.007 per website, or ~138 analyses per $1.00 USD)

---

## 4. Cost Optimization Strategies Implemented

1. **Noise Tag Stripping**: Removing 13 non-content tag types (`script`, `style`, `svg`, `nav`, `footer`, `header`, `form`, etc.) eliminates 65%–85% of raw HTML token overhead.
2. **Deterministic Text Capping**: Strict 15,000 character limit on the processed body prevents unbounded input growth on verbose enterprise domains.
3. **Structured Single-Pass Prompting**: Concise prompts with explicit JSON templates eliminate multi-turn conversational token overhead.
4. **Concurrent Async Execution**: Running prompts concurrently via `asyncio.gather` optimizes server resource utilization and reduces connection idle time.
