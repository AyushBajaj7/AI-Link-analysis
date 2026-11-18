# LLM Cost Analysis & Optimization

This report details token estimation and operating expenditure per website analysis.

## Token Usage Estimation

Per typical website analysis:
- **Average Cleaned HTML Input**: ~3,000 tokens (after script, style, and boilerplate stripping)
- **Aggregated JSON Output**: ~850 tokens (all 6 sections)

## Cost Breakdown per Single Analysis

### 1. Google Gemini 2.5 Flash (Recommended)
- **Input Cost**: $(3,000 / 1,000,000) \times \$0.075 = \$0.000225$
- **Output Cost**: $(850 / 1,000,000) \times \$0.300 = \$0.000255$
- **Total Cost per Analysis**: **$0.000480** (under $0.0005 per run)

### 2. OpenAI GPT-4o-mini
- **Input Cost**: $(3,000 / 1,000,000) \times \$0.150 = \$0.000450$
- **Output Cost**: $(850 / 1,000,000) \times \$0.600 = \$0.000510$
- **Total Cost per Analysis**: **$0.000960** (approx. 2x Gemini)

### 3. Anthropic Claude 3.5 Haiku
- **Input Cost**: $(3,000 / 1,000,000) \times \$1.000 = \$0.003000$
- **Output Cost**: $(850 / 1,000,000) \times \$5.000 = \$0.004250$
- **Total Cost per Analysis**: **$0.007250** (approx. 15x Gemini)

## Cost Optimization Strategies Implemented

1. **Semantic HTML Pre-filtering**: Stripping scripts, inline styles, navigation bars, and footers reduces raw HTML token count by **65% - 85%**.
2. **Text Capping**: Truncating main text to a maximum of 15,000 characters prevents outlier large pages from inflating billable tokens.
3. **Structured Single-Pass Prompting / Concurrent Calling**: Reduces roundtrip context duplication.
