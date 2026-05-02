# AI Visibility Audit: HR & Recruiting Software (2025)

**Prepared using:** AI Citation Audit Tool  
**Target brand:** Indeed  
**Audit date:** May 2026  
**Models queried:** OpenAI GPT-5.4, Anthropic Claude Sonnet 4.6, Perplexity Sonar Pro  
**Methodology run:** 5 runs × 3 models × 14 prompts = 210 responses  

---

## Executive Summary

- **Indeed ranks last among all six tracked brands in AI-generated mention rate (32.9%)**, trailing Lever (82.9%) and Greenhouse (79.0%) by nearly 50 percentage points. The gap is structural: Indeed's low visibility is the most stable signal in the dataset (run-to-run stdev 0.026), meaning it is not noise or a bad sample — it is the consistent output of three major LLMs across five independent runs.

- **LLMs do not recommend Indeed.** Its recommendation-intent mention rate is 3.3% — Anthropic and Perplexity return 0.0% when asked to name one tool for a mid-sized company's hiring needs. When explicitly named in a comparison prompt, Indeed appears 80% of the time. Remove the explicit prompt and it almost disappears. Indeed achieves visibility only when users already know to ask about it.

- **Indeed is categorized as a job board, not a hiring platform.** 93.5% of responses that mention Indeed co-mention LinkedIn, ZipRecruiter, or Glassdoor. LLMs have filed Indeed in the candidate-sourcing bucket, not the ATS/applicant-management bucket. When users ask about switching away from their current tool, LLMs recommend Greenhouse (63%), Lever (43%), and BambooHR (37%) as destinations — not Indeed.

- **The tracked competitor set materially understates the competitive field.** BambooHR appears in 65.7% of all responses and Workable in 41.0% — neither was in the initial competitor list. iCIMS (28.1%), ADP (26.2%), and Ashby (23.3%) also appear frequently. Any share-of-voice benchmark built on the six tracked brands overstates Indeed's relative position.

- **Workday's 57-point cross-model gap and Perplexity's structural divergence are the key model-level findings.** Workday is nearly invisible on Perplexity (17.1%) despite ranking #3 on OpenAI and Anthropic. Perplexity consistently surfaces SMB-oriented tools (Gusto ranks #1 at 81.4%) — a distinct user population from the enterprise buyer the other models address.

---

## Methodology

Five independent audit runs were conducted between 06:27 and 08:47 UTC on 2 May 2026, spaced 30 minutes apart, using the AI Citation Audit Tool against OpenAI GPT-5.4, Anthropic Claude Sonnet 4.6, and Perplexity Sonar Pro. Each run fired a 14-prompt battery across 7 intent types — discovery, comparison, recommendation, problem-first, switching, persona, and feature-led — with 2 phrasings per intent, scoped to the use case of "evaluating and hiring full-time employees at a mid-sized company." Target brand was Indeed; tracked competitors were Greenhouse, Lever, Workday, Rippling, and Gusto. Responses were parsed using fuzzy string matching (RapidFuzz, 80% threshold) for brand mention detection, position ranking (FIRST / TOP_3 / PRESENT / ABSENT), and keyword-heuristic sentiment classification. All 210 raw responses are cached in `reports/run_*/raw/`. No run produced empty responses or triggered error states. Full run log is in `run_log.txt`.

---

## Share of Voice

| Brand | Mention Rate | Std Dev | Avg Position Score | Tier |
|---|---|---|---|---|
| Lever | 82.9% | 0.293 | 2.33 | TOP_3 |
| Greenhouse | 79.0% | 0.284 | 2.15 | TOP_3 |
| Gusto | 68.1% | 0.361 | 2.83 | PRESENT |
| Workday | 54.3% | 0.411 | 3.04 | PRESENT |
| Rippling | 47.1% | 0.391 | 3.24 | PRESENT |
| **Indeed** | **32.9%** | **0.345** | **3.09** | **PRESENT** |

*Position score: 1.0 = FIRST, 4.0 = ABSENT. Lower is better.*

Indeed is the least-mentioned tracked brand by a 14-point margin over the next lowest (Rippling). More telling than the rank is the position score: Indeed's 3.09 means it typically lands as a mid-list addition when it appears at all, not as a top-of-mind recommendation. Greenhouse holds the best position score (2.15) — it doesn't just appear frequently, it appears early. The effective competitive field extends well beyond the six tracked brands: BambooHR (65.7% of responses), Workable (41.0%), iCIMS (28.1%), and ADP (26.2%) all appear organically at rates exceeding Indeed's tracked mention rate. The audited share-of-voice gap is likely worse than these numbers show.

---

## Model Variance

| Brand | OpenAI (GPT-5.4) | Anthropic | Perplexity | Cross-Model Gap |
|---|---|---|---|---|
| Indeed | 38.6% ± 0.366 | 35.7% ± 0.311 | 24.3% ± 0.351 | 14.3pp |
| Greenhouse | 85.7% ± 0.229 | 87.1% ± 0.222 | 64.3% ± 0.334 | 22.9pp |
| Lever | 95.7% ± 0.142 | 88.6% ± 0.213 | 64.3% ± 0.375 | **31.4pp ⚑** |
| **Workday** | **71.4% ± 0.327** | **74.3% ± 0.371** | **17.1% ± 0.241** | **57.1pp ⚑** |
| Rippling | 51.4% ± 0.373 | 52.9% ± 0.363 | 37.1% ± 0.426 | 15.7pp |
| **Gusto** | 71.4% ± 0.349 | 51.4% ± 0.393 | **81.4% ± 0.273** | **30.0pp ⚑** |

**Brand rank order by model:**

| Rank | OpenAI | Anthropic | Perplexity |
|---|---|---|---|
| #1 | Lever | Lever | Gusto |
| #2 | Greenhouse | Greenhouse | Greenhouse ✓ |
| #3 | Workday | Workday | Lever |
| #4 | Gusto | Rippling | Rippling |
| #5 | Rippling | Gusto | Indeed |
| #6 | **Indeed** | **Indeed** | **Workday** |

Only Greenhouse holds a consistent rank across all three models (#2). Every other brand shifts. Three findings stand out:

**Workday's 57-point Perplexity gap** is the largest cross-model variance in the audit. Workday is a top-3 brand on OpenAI and Anthropic but nearly absent on Perplexity (17.1%). Perplexity's web-search grounding appears to surface more SMB-weight results, depressing enterprise-heavy brands and elevating Gusto (81.4%, ranked #1 on Perplexity). This is a meaningful segmentation signal: the model a buyer uses correlates with the market segment they operate in.

**Indeed is consistently low across all three models.** Unlike Workday, which has model-dependent variance, Indeed's range is 24–39% — low everywhere, with no model that rescues it. Perplexity is the weakest (24.3%), likely because its search-grounded outputs surface the job-board framing most directly.

**Perplexity is the most variable model overall** (stdev 0.409 across all brand/intent combinations), while OpenAI is the most consistent (stdev 0.362). For clients making recommendations about where to invest in AI visibility, OpenAI's higher consistency makes it the more reliable benchmark signal.

---

## Intent-Level Breakdown

| Brand | Discovery | Comparison | Rec. | Problem-First | Switching | Persona | Feature-Led | Swing |
|---|---|---|---|---|---|---|---|---|
| **Indeed** | **20.0%** | **80.0% ★** | **3.3% ▼** | **6.7%** | **50.0%** | **23.3%** | **46.7%** | **76.7%** |
| Greenhouse | 83.3% | 100.0% ★ | 76.7% | 93.3% | 63.3% | 43.3% ▼ | 93.3% | 56.7% |
| Lever | 80.0% | 93.3% | 56.7% ▼ | 80.0% | 80.0% | 93.3% | 96.7% ★ | 40.0% |
| Workday | 53.3% | 76.7% ★ | 66.7% | 63.3% | 33.3% | 23.3% ▼ | 63.3% | 53.3% |
| Rippling | 46.7% | 40.0% | 80.0% ★ | 33.3% | 6.7% ▼ | 46.7% | 76.7% | 73.3% |
| Gusto | 76.7% | 80.0% | 46.7% ▼ | 60.0% | 50.0% | 70.0% | 93.3% ★ | 46.7% |

*(★ = best intent, ▼ = worst)*

Indeed's 76.7-point intent swing is the second-largest in the audit and reveals a precise structural problem: **Indeed exists in LLM outputs primarily as a reference point, not a recommendation.** It surfaces when the prompt names it (comparison: 80%), when users ask about tools with specific features (feature-led: 46.7%, driven almost entirely by OpenAI), and in switching prompts where it is the tool being switched from — not the destination. When prompts simulate the actual buying decision ("what should I use?" / "our team is struggling with hiring"), Indeed nearly vanishes.

**Indeed's intent profile by model exposes an additional risk:** Anthropic and Perplexity return 0.0% on recommendation intent. OpenAI returns 10.0%. No model consistently surfaces Indeed as a proactive hiring-platform recommendation. Recommendation intent is where purchase decisions are influenced — and Indeed is absent from it across all three LLMs.

**Lever is the most intent-stable brand** (40.0% swing), appearing consistently across all seven intent types. Greenhouse dominates problem-first prompts (93.3%) — it is positioned by LLMs as the default solution for teams actively struggling with hiring, which is a high-conversion framing. Indeed does not hold that position on any intent type.

**Switching intent is particularly damaging for Indeed.** When asked what to use when moving away from a current tool, LLMs recommend Greenhouse (63% of switching responses), Lever (43%), and BambooHR (37%). Indeed does not appear as a recommended destination on switching prompts. The switching prompt is the highest-purchase-intent context in the battery — and Indeed is the implicit starting point, not the endpoint.

---

## Visibility Stability

| Brand | run_1 | run_2 | run_3 | run_4 | run_5 | Stdev | Volatility Rank |
|---|---|---|---|---|---|---|---|
| **Indeed** | 33.3% | 33.3% | 28.6% | 33.3% | 35.7% | **0.026** | **#1 — most stable** |
| Workday | 54.8% | 50.0% | 52.4% | 57.1% | 57.1% | 0.031 | #2 |
| Greenhouse | 83.3% | 78.6% | 81.0% | 78.6% | 73.8% | 0.035 | #3 |
| Lever | 83.3% | 85.7% | 88.1% | 81.0% | 76.2% | 0.046 | #4 |
| Gusto | 59.5% | 71.4% | 69.0% | 66.7% | 73.8% | 0.055 | #5 |
| Rippling | 47.6% | 47.6% | 47.6% | 38.1% | 54.8% | 0.059 | #6 — most volatile |

No brand crosses the 20-point flag threshold. The system is stable: findings reflect model training state, not sampling error.

Indeed's stdev of 0.026 is the lowest in the dataset. Its underperformance is not noise — it is the most reliable signal produced by this audit. This matters for client conversations: the problem cannot be dismissed as measurement variance or a bad day. It is consistent across 5 independent runs, 30 minutes apart, across 3 different LLMs.

Rippling's relative volatility (stdev 0.059, range 16.7pp) reflects thinner training signal — LLMs have less consistent information about it than about more established players. Gusto shows an upward trend across runs (59.5% → 73.8%), which may reflect recency-weighting in model outputs rather than a genuine change; a longer longitudinal series would be required to confirm.

---

## Sentiment Analysis

| Brand | Positive | Neutral | Negative | n | Net |
|---|---|---|---|---|---|
| Rippling | 87.9% | 10.1% | 2.0% | 99 | Positive |
| Greenhouse | 87.3% | 10.8% | 1.8% | 166 | Positive |
| **Indeed** | **87.0%** | **13.0%** | **0.0%** | **69** | Positive |
| Gusto | 86.0% | 11.2% | 2.8% | 143 | Positive |
| Lever | 81.6% | 15.5% | 2.9% | 174 | Positive |
| Workday | 78.9% | 16.7% | 4.4% | 114 | Positive |

No brand carries alarming negative framing. Workday's 4.4% negative rate is the highest and consistent with its enterprise positioning: LLMs occasionally surface cost and implementation complexity when comparing it. This is a known market dynamic, not a reputational issue.

**Indeed's 0.0% negative rate should not be read as a strength.** It reflects a sample of 69 mentions — the smallest of any brand — paired with generic, positive framing. LLMs cite Indeed briefly and favorably when they do mention it, but they have not built up the kind of detailed, nuanced knowledge base that produces comparative criticism. Lever's 2.9% negative rate, by contrast, comes from a sample of 174 mentions and reflects genuine comparative friction ("strong for mid-market but limited enterprise integrations") — the kind of substantive presence that indicates deep model familiarity. Zero negative framing at low mention volume is not authority; it is obscurity.

Indeed's sentiment is consistent across all three models: 87–89% positive, 0% negative. Perplexity shows slightly higher neutral framing (17.6%), consistent with its more hedged, citation-linked output style.

---

## Strategic Implications

**1. Fix the categorical miscategorization before optimizing frequency.**  
The 93.5% job-board conflation rate is the highest-priority finding. LLMs have a settled belief about what Indeed is: a candidate-sourcing tool, not a hiring platform. Publishing more content will not change this if the content reinforces the job-board identity. Indeed needs a sustained, structured content strategy that explicitly and repeatedly frames Indeed Hiring Platform as an ATS — authoritative comparison pages ("Indeed vs. Greenhouse"), feature documentation with ATS-specific terminology, and placement in analyst and review content that LLMs demonstrably index (G2, Capterra, HR tech media). The goal is not more mentions; it is mentions in the right semantic context.

**2. Target recommendation-intent content as the primary gap to close.**  
Indeed's 3.3% recommendation mention rate is the most actionable finding. Recommendation prompts simulate the highest-intent buying moment — "what should I use?" — and Indeed is functionally absent. Greenhouse answers that question 76.7% of the time. The content gap is not product awareness (comparison prompts show 80%) but recommendation authority. Case studies with quantified outcomes for mid-sized companies, independent analyst endorsements, and structured "best for" positioning ("best ATS for growing teams replacing spreadsheets") are the formats most likely to influence LLM recommendation responses.

**3. Invest in Perplexity-visible content surfaces to close the 14-point model gap.**  
Indeed's lowest mention rate is on Perplexity (24.3%), and Perplexity's web-search grounding means it reflects the current indexed web more directly than the other two models. Closing the gap here requires presence in the sources Perplexity cites: recent reviews on high-authority HR tech sites, structured data markup on product pages, and FAQ-format content that directly answers the question "what is the best ATS for mid-sized companies." This is also the fastest-acting lever — Perplexity's grounding can reflect content changes within days, not training cycles.

**4. Expand competitive intelligence to include BambooHR, Workable, and iCIMS.**  
The audit competitor set (Greenhouse, Lever, Workday, Rippling, Gusto) misses the three brands that LLMs organically surface most after Indeed's tracked competitors: BambooHR (65.7%), Workable (41.0%), and iCIMS (28.1%). Any share-of-voice benchmark or content strategy built on the current six-brand set is operating with an incomplete picture of the competitive field. A follow-up audit should include these three at minimum, and track switching-intent recommendations specifically — the prompt type where LLMs are actively directing users away from Indeed toward specific alternatives.

---

## Appendix

**Run log:** `run_log.txt`

**Raw data files:**

| Run | JSON | CSV | HTML |
|---|---|---|---|
| run_1 | `reports/run_1/citation_report.json` | `reports/run_1/citation_summary.csv` | `reports/run_1/report.html` |
| run_2 | `reports/run_2/citation_report.json` | `reports/run_2/citation_summary.csv` | `reports/run_2/report.html` |
| run_3 | `reports/run_3/citation_report.json` | `reports/run_3/citation_summary.csv` | `reports/run_3/report.html` |
| run_4 | `reports/run_4/citation_report.json` | `reports/run_4/citation_summary.csv` | `reports/run_4/report.html` |
| run_5 | `reports/run_5/citation_report.json` | `reports/run_5/citation_summary.csv` | `reports/run_5/report.html` |

**Audit parameters:**

```
--brand        "Indeed"
--industry     "HR and recruiting software"
--use-case     "evaluating and hiring full-time employees at a mid-sized company"
--competitors  "Greenhouse,Lever,Workday,Rippling,Gusto"
--models       openai,anthropic,perplexity
```

**Prompt battery (14 prompts, 7 intent types):**

| Intent | Phrasing |
|---|---|
| Discovery | "What are the best tools for HR and recruiting software?" |
| Discovery | "I'm looking for software to help me with evaluating and hiring full-time employees at a mid-sized company. What do you recommend?" |
| Comparison | "How does Indeed compare to its competitors in HR and recruiting software?" |
| Comparison | "What are the pros and cons of the top HR and recruiting software platforms?" |
| Recommendation | "If I had to pick one HR and recruiting software tool for a mid-sized company, what would you choose?" |
| Recommendation | "What do most HR and recruiting software professionals use for evaluating and hiring full-time employees at a mid-sized company?" |
| Problem-first | "Our team is struggling with evaluating and hiring full-time employees at a mid-sized company. What tools do people use to solve this?" |
| Problem-first | "We're having trouble managing evaluating and hiring full-time employees at a mid-sized company. What software would you recommend?" |
| Switching | "What are the best alternatives to Indeed for evaluating and hiring full-time employees at a mid-sized company?" |
| Switching | "We're looking to move away from our current HR and recruiting software tool. What should we consider?" |
| Persona | "I'm an operations manager evaluating HR and recruiting software tools for a growing startup. What are the top options?" |
| Persona | "As a team lead looking for evaluating and hiring full-time employees at a mid-sized company software, what would you suggest?" |
| Feature-led | "What HR and recruiting software platforms are known for the best reporting and analytics?" |
| Feature-led | "Which HR and recruiting software tools are easiest to onboard a new team onto?" |

**Tool version:** ai-citation-audit v0.1.0  
**Models:** OpenAI GPT-5.4, Anthropic Claude Sonnet 4.6, Perplexity Sonar Pro  
**Runs:** 5 × 30-minute intervals, 2 May 2026, 06:27–08:47 UTC
