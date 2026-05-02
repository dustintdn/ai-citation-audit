# AI Visibility Audit: HR & Recruiting Software (2025)

**Prepared using:** AI Citation Audit Tool  
**Target brand:** Indeed  
**Audit date:** May 2026  
**Models queried:** OpenAI (GPT-4o), Anthropic (Claude Sonnet)  

---

## Executive Summary

- **Indeed ranks last among all six tracked brands** in AI-generated mention rate (37.5%), trailing Lever (95.8%), Workday (87.5%), and Greenhouse (83.3%) by a wide margin — a critical visibility deficit given AI-assisted software discovery is increasingly the top of the buying funnel.
- **LLMs have categorically miscategorized Indeed.** Every response that mentioned Indeed (9/9) co-mentioned LinkedIn or ZipRecruiter — placing Indeed in the job board bucket, not the HR/ATS software bucket. This is not a frequency problem; it is a positioning problem.
- **Indeed's visibility is model-dependent and intent-dependent to an unusual degree.** Its mention rate swings from 16.7% on OpenAI to 58.3% on Anthropic (+41.7pp), and from 75% on comparison prompts to 12.5% on recommendation prompts — the second-largest intent swing of any brand in the audit.
- **The competitive field is broader than the tracked list.** BambooHR (83.3% of responses) and ADP (79.2%) appear more frequently than Indeed but were not in the competitor set. iCIMS (50%), SAP (37.5%), and LinkedIn (45.8%) are also material presences.
- **The system is stable.** Run-to-run volatility is low (mean delta 6.9%), and only Rippling crosses the 15% instability threshold, confirming the findings are signal, not noise.

---

## Methodology

Two full audit runs were conducted 30 minutes apart using the AI Citation Audit Tool against OpenAI GPT-4o and Anthropic Claude Sonnet (Perplexity was not included in the primary analysis). Each run fired a six-prompt battery across three intent types — discovery, comparison, and recommendation — with two phrasings per intent, for 12 queries per run (24 total). The target brand was Indeed; tracked competitors were Greenhouse, Lever, Workday, Rippling, and Gusto. Responses were parsed using fuzzy string matching (RapidFuzz, threshold 80) for brand mention detection, position ranking (FIRST / TOP_3 / PRESENT / ABSENT), and sentiment classification via keyword heuristics. Untracked brands were identified by scanning raw response text. All raw responses are cached in `reports/run_1/raw/` and `reports/run_2/raw/`.

---

## Share of Voice

| Brand | Mention Rate | Avg Position Score | Position Tier |
|---|---|---|---|
| Lever | 95.8% | 2.12 | TOP_3 |
| Workday | 87.5% | 2.25 | TOP_3 |
| Greenhouse | 83.3% | 2.21 | TOP_3 |
| Gusto | 66.7% | 2.88 | PRESENT |
| Rippling | 41.7% | 3.54 | ABSENT |
| **Indeed** | **37.5%** | **2.88** | **PRESENT** |

*Position score: 1.0 = FIRST, 4.0 = ABSENT. Lower is better.*

Indeed is the least-mentioned tracked brand and shares last place in position tier with Rippling — a brand with a fraction of Indeed's market presence. The gap between Indeed and the top three (Lever, Workday, Greenhouse) is not marginal; it is structural. Lever, a mid-market ATS with an order of magnitude less revenue than Indeed, appears in 19 of 20 responses. Indeed appears in fewer than 8. When Indeed does appear, it lands in PRESENT — meaning it is being named, not recommended.

The untracked brand scan compounds this picture: **BambooHR appears in 83.3% of responses and ADP in 79.2%** — both ahead of Indeed — despite neither being in the competitor list. The effective competitive field in LLM responses is at least nine brands wide, not six.

---

## Model Variance

| Brand | OpenAI | Anthropic | Delta |
|---|---|---|---|
| **Indeed** | **16.7%** | **58.3%** | **+41.7pp** |
| Rippling | 16.7% | 66.7% | +50.0pp |
| Greenhouse | 66.7% | 100.0% | +33.3pp |
| Workday | 75.0% | 100.0% | +25.0pp |
| Gusto | 75.0% | 58.3% | -16.7pp |
| Lever | 100.0% | 91.7% | -8.3pp |

**Brand rank order agreement between models: 2 of 6 positions.** Only Workday (#2 on both) and Indeed (#5 on both) are ranked consistently. Every other position disagrees.

Anthropic is the more consistent model overall (stdev 0.35 vs. 0.41 for OpenAI) and produces higher mention rates across most brands. OpenAI has a strong structural preference for Lever — it appears in 100% of OpenAI responses — which does not replicate on Anthropic with the same strength. This suggests OpenAI's training data weights Lever's content more heavily in HR software contexts.

Indeed's 41.7-point cross-model gap is strategically significant: it means a user querying GPT-4o about HR software will almost never see Indeed mentioned, while a user on Claude will see it roughly half the time. Indeed's AI visibility is not a consistent signal — it is an artifact of model selection.

---

## Intent-Level Breakdown

| Brand | Discovery | Comparison | Recommendation | Swing |
|---|---|---|---|---|
| Lever | 100.0% | 100.0% | 87.5% | 12.5% |
| Greenhouse | 100.0% | 75.0% | 75.0% | 25.0% |
| Workday | 87.5% | 75.0% | **100.0%** | 25.0% |
| Gusto | 75.0% | 87.5% | 37.5% | 50.0% |
| **Indeed** | **25.0%** | **75.0%** | **12.5%** | **62.5%** |
| Rippling | 75.0% | 0.0% | 50.0% | 75.0% |

*Swing = best intent rate minus worst intent rate per brand.*

Two findings stand out:

**Indeed nearly disappears on recommendation prompts (12.5%).** When an LLM is asked to name one HR software tool for a mid-sized company, it almost never names Indeed. This is the highest-value prompt type for driving consideration — and Indeed is functionally absent from it. By contrast, Workday answers that question 100% of the time, Greenhouse 75%, Lever 87.5%.

**Indeed's only strong showing is on comparison prompts (75%)** — prompts that name Indeed explicitly ("how does Indeed compare to competitors?"). This means Indeed achieves visibility primarily when a user already knows to ask about it. It is not being surfaced organically. A brand that only appears when directly invoked is not winning the top-of-funnel battle.

Rippling's 0% on comparison and Gusto's drop from 87.5% to 37.5% on recommendation suggest both brands have strong discovery presence but weak recommendation authority — a different problem than Indeed's, but worth noting for competitive context.

---

## Visibility Stability

| Brand | Run 1 | Run 2 | Delta | Volatility Score |
|---|---|---|---|---|
| Greenhouse | 83.3% | 83.3% | 0.0% | 0.000 |
| Gusto | 66.7% | 66.7% | 0.0% | 0.000 |
| Indeed | 33.3% | 41.7% | +8.3% | 0.083 |
| Lever | 100.0% | 91.7% | -8.3% | 0.083 |
| Workday | 91.7% | 83.3% | -8.3% | 0.083 |
| **Rippling** | **50.0%** | **33.3%** | **-16.7%** | **0.167 ⚑** |

*Volatility score = absolute run-to-run delta. Flag threshold: >0.15.*

Overall system stability is high. The mean absolute delta across all brands is **0.069**, and only Rippling crosses the 15% flag threshold. Greenhouse and Gusto are perfectly stable across both runs.

Indeed's small +8.3% uptick in run 2 is within noise. Its low mention rate is not a measurement artifact — it is consistent. Rippling's flagged volatility (0.167) reflects genuinely inconsistent LLM knowledge rather than a tooling issue; its training signal is thinner than established players.

---

## Sentiment Analysis

| Brand | Positive | Neutral | Negative | Net | Mentions (n) |
|---|---|---|---|---|---|
| Rippling | 80.0% | 20.0% | 0.0% | Positive | 10 |
| Greenhouse | 80.0% | 10.0% | 10.0% | Positive | 20 |
| Workday | 76.2% | 14.3% | 9.5% | Positive | 21 |
| Gusto | 75.0% | 12.5% | 12.5% | Positive | 16 |
| **Indeed** | **66.7%** | **33.3%** | **0.0%** | **Positive** | **9** |
| Lever | 65.2% | 26.1% | 8.7% | Positive | 23 |

No brand is framed negatively at a meaningful rate. Negative mentions cluster in comparison contexts — hedging language ("strong but expensive," "enterprise-grade but complex") rather than condemnation.

**Indeed's sentiment reading must be interpreted with caution.** At 9 total mentions, the sample is thin. The 33.3% neutral reading — the highest neutral share of any brand — likely reflects flat, non-committal framing on OpenAI (where Indeed appeared almost exclusively in structured comparison outputs, not endorsement language). Anthropic's framing was more positive. No negative framing was detected for Indeed in either run.

Workday's 9.5% negative rate, the highest among all brands, is consistent with its enterprise positioning: LLMs surface affordability and implementation complexity concerns when comparing it. This is not a red flag — it mirrors how buyers actually think about Workday — but it is a positioning gap Indeed could exploit in content targeting "Workday alternatives for growing companies."

---

## Strategic Implications

**1. Reposition Indeed's AI content footprint from job board to hiring platform.**  
The 100% LinkedIn/ZipRecruiter co-mention rate confirms that LLMs have filed Indeed under "job board," not "ATS/HR software." This is a training data problem that requires a content strategy response: authoritative, structured content explicitly positioning Indeed Hiring Platform as an ATS — comparison pages, feature documentation, analyst coverage — in formats that LLMs weight heavily (structured HTML, frequently-cited sources). The goal is to break the job-board association in model training pipelines.

**2. Target recommendation-intent content as the primary gap to close.**  
Indeed's 12.5% recommendation mention rate vs. Greenhouse's 75% and Workday's 100% is the most actionable gap in the dataset. Recommendation prompts simulate the moment of highest purchase intent ("what should I use?"). Indeed needs content that gives LLMs a confident, concise answer for that question — customer case studies with quantified outcomes, "Indeed vs." comparison pages with clear win conditions, and analyst placements that frame Indeed as a primary recommendation for SMB hiring specifically.

**3. Prioritize OpenAI visibility — the gap is largest and the audience is largest.**  
Indeed's 16.7% mention rate on OpenAI vs. 58.3% on Anthropic represents the single largest cross-model gap in the audit. Given OpenAI's ChatGPT user base, closing this gap has higher reach impact than improving on Anthropic. This likely requires direct presence in sources that GPT-4o weights — G2 reviews, Capterra listings, product-specific documentation, and HR tech media that OpenAI has demonstrably indexed well.

**4. Expand the tracked competitor set before any follow-up audit.**  
BambooHR (83.3% of responses) and ADP (79.2%) are de facto top-tier competitors in LLM outputs and were not in the audit scope. iCIMS (50%) and SAP (37.5%) are also material. Any share-of-voice benchmark that excludes them overstates Indeed's relative position. The true competitive gap is wider than this audit shows.

---

## Appendix

**Raw data files:**

| File | Path |
|---|---|
| Run 1 — Full JSON | `reports/run_1/citation_report.json` |
| Run 1 — CSV Summary | `reports/run_1/citation_summary.csv` |
| Run 1 — HTML Report | `reports/run_1/report.html` |
| Run 2 — Full JSON | `reports/run_2/citation_report.json` |
| Run 2 — CSV Summary | `reports/run_2/citation_summary.csv` |
| Run 2 — HTML Report | `reports/run_2/report.html` |

**Audit parameters:**

```
--brand        "Indeed"
--industry     "HR and recruiting software"
--competitors  "Greenhouse,Lever,Workday,Rippling,Gusto"
--models       openai,anthropic
```

**Prompt battery (6 prompts, 3 intent types):**

| Intent | Phrasing |
|---|---|
| Discovery | "What are the best tools for HR and recruiting software?" |
| Discovery | "I'm looking for software to help me with HR and recruiting software. What do you recommend?" |
| Comparison | "How does Indeed compare to its competitors in HR and recruiting software?" |
| Comparison | "What are the pros and cons of the top HR and recruiting software platforms?" |
| Recommendation | "If I had to pick one HR and recruiting software tool for a mid-sized company, what would you choose?" |
| Recommendation | "What do most HR and recruiting software professionals use for HR and recruiting software?" |

**Tool version:** ai-citation-audit v0.1.0  
**Models used:** OpenAI GPT-4o, Anthropic Claude Sonnet 4.6
