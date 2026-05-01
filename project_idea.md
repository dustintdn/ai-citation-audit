You are a senior Python engineer helping me build a production-quality CLI tool 
called the AI Citation Audit Tool. We will develop this spec-first — read the 
full spec before writing any code, ask clarifying questions if anything is 
ambiguous, then proceed file by file.

---

## GOAL

Build a Python CLI tool that audits how a target brand is mentioned across 
multiple LLM APIs (OpenAI, Anthropic, Perplexity). The tool fires a structured 
prompt battery at each LLM, parses responses for brand and competitor mentions, 
scores citation quality, and outputs a structured audit report.

---

## FUNCTIONAL SPEC

### Inputs (CLI flags)
- `--brand`         Target brand name (e.g. "Salesforce")
- `--industry`      Industry/category context (e.g. "CRM software")
- `--competitors`   Optional comma-separated list of known competitors to track
- `--models`        Which LLMs to query: openai, anthropic, perplexity (default: all)
- `--output-dir`    Directory to write report files (default: ./reports)

### Prompt Battery
Generate prompts across 3 intent types, 2 phrasings each = 6 prompts per model minimum:

  DISCOVERY:
    - "What are the best tools for [industry]?"
    - "I'm looking for software to help me with [industry use case]. What do you recommend?"

  COMPARISON:
    - "How does [brand] compare to its competitors in [industry]?"
    - "What are the pros and cons of the top [industry] platforms?"

  RECOMMENDATION:
    - "If I had to pick one [industry] tool for a mid-sized company, what would you choose?"
    - "What do most [industry] professionals use for [use case]?"

### Parsing & Scoring
For each LLM response:
  - Extract all brand/product mentions using fuzzy matching (not just exact string match)
  - Record mention position: FIRST, TOP_3, PRESENT, ABSENT
  - Record sentiment context: positive, neutral, negative (use simple keyword heuristics)
  - Record whether a citation/source URL was included (relevant for Perplexity)

### Output Files
1. `citation_report.json`   — full raw data: prompt, model, response, parsed mentions
2. `citation_summary.csv`   — one row per (brand x model x prompt_type): mention_rate, avg_position, sentiment
3. `report.html`            — a clean, standalone HTML summary with a table and basic styling.
                              Should be readable as a client deliverable without opening Python.

### Architecture Requirements
- `src/` layout with modules: `prompts.py`, `llm_clients.py`, `parser.py`, `scorer.py`, `reporter.py`, `cli.py`
- Config via `.env` for API keys (OPENAI_API_KEY, ANTHROPIC_API_KEY, PERPLEXITY_API_KEY)
- Each LLM client should implement a common abstract interface so new models can be added easily
- Async where it makes the querying faster; models should be queried concurrently
- All LLM responses stored raw before parsing so the tool is re-runnable without re-querying

### Non-Goals (out of scope for v1)
- No database, no auth, no frontend
- No fine-tuning or model training
- No scheduled runs (that's v2)

---

## ENGINEERING STANDARDS
- Python 3.11+
- Use `typer` for the CLI
- Use `httpx` or `openai`/`anthropic` SDKs for API calls
- Use `rapidfuzz` for fuzzy brand mention matching
- Use `jinja2` for the HTML report template
- Use `pytest` with at least 3 meaningful unit tests (parser and scorer logic)
- `pyproject.toml` for dependency management
- Type hints throughout
- A complete `README.md` with setup instructions, example CLI invocation, and a 
  sample output screenshot placeholder

---

## PROCESS INSTRUCTIONS FOR THE AGENT
1. Confirm you have read and understood the full spec
2. Propose the complete file tree before writing any code
3. Implement one module at a time, starting with: prompts.py → llm_clients.py → 
   parser.py → scorer.py → reporter.py → cli.py → tests
4. After each module, briefly summarize what was built and flag any decisions made
5. Do not proceed to the next module until I confirm
6. At the end, generate the README.md and pyproject.toml

Begin by confirming the spec and proposing the file tree.