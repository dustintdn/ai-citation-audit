"""
cli.py — Typer CLI entry point for the AI Citation Audit Tool.

Usage example:
    citation-audit \\
        --brand Salesforce \\
        --industry "CRM software" \\
        --competitors "HubSpot,Zoho,Pipedrive" \\
        --models openai,anthropic \\
        --output-dir ./reports
"""

from __future__ import annotations

import asyncio
from pathlib import Path
from typing import Annotated

import typer
from dotenv import load_dotenv

from citation_audit.llm_clients import AVAILABLE_MODELS, build_clients
from citation_audit.parser import parse_response
from citation_audit.prompts import build_prompt_battery
from citation_audit.reporter import write_reports
from citation_audit.scorer import PromptResult, score_results

load_dotenv()

app = typer.Typer(
    name="citation-audit",
    help="Audit how your brand is mentioned across LLM APIs.",
    add_completion=False,
)


# ---------------------------------------------------------------------------
# Async core
# ---------------------------------------------------------------------------


async def _run_audit(
    brand: str,
    industry: str,
    use_case: str | None,
    competitors: list[str],
    models: list[str],
    output_dir: Path,
) -> dict[str, Path]:
    raw_dir = output_dir / "raw"
    prompts = build_prompt_battery(brand=brand, industry=industry, use_case=use_case)
    clients = build_clients(models=models, raw_dir=raw_dir)

    typer.echo(
        f"Querying {len(clients)} model(s) × {len(prompts)} prompts "
        f"= {len(clients) * len(prompts)} requests (cached responses skipped)…"
    )

    # Build all (client, prompt_index, prompt) tasks and fire concurrently
    async def _fetch(client, idx: int, prompt):
        response_text = await client.query(prompt, idx)
        return client.name, prompt, response_text

    tasks = [
        _fetch(client, idx, prompt)
        for client in clients
        for idx, prompt in enumerate(prompts)
    ]
    raw_results = await asyncio.gather(*tasks)

    # Parse every response
    typer.echo("Parsing responses…")
    prompt_results: list[PromptResult] = []
    for model_name, prompt, response_text in raw_results:
        parsed = parse_response(
            raw_text=response_text,
            brand=brand,
            competitors=competitors,
        )
        prompt_results.append(
            PromptResult(model=model_name, prompt=prompt, parsed=parsed)
        )

    # Score and report
    typer.echo("Scoring and writing reports…")
    audit_results = score_results(
        prompt_results=prompt_results,
        brand=brand,
        industry=industry,
        competitors=competitors,
    )
    return write_reports(results=audit_results, output_dir=output_dir)


# ---------------------------------------------------------------------------
# CLI command
# ---------------------------------------------------------------------------


@app.command()
def audit(
    brand: Annotated[
        str,
        typer.Option("--brand", help="Target brand name (e.g. 'Salesforce')."),
    ],
    industry: Annotated[
        str,
        typer.Option("--industry", help="Industry/category context (e.g. 'CRM software')."),
    ],
    competitors: Annotated[
        str | None,
        typer.Option(
            "--competitors",
            help="Comma-separated list of competitor names to track.",
        ),
    ] = None,
    models: Annotated[
        str | None,
        typer.Option(
            "--models",
            help=f"Comma-separated models to query. Available: {', '.join(AVAILABLE_MODELS)}. Default: all.",
        ),
    ] = None,
    output_dir: Annotated[
        Path,
        typer.Option("--output-dir", help="Directory to write report files into."),
    ] = Path("./reports"),
    use_case: Annotated[
        str | None,
        typer.Option(
            "--use-case",
            help="Specific use-case for prompt interpolation. Defaults to --industry if omitted.",
        ),
    ] = None,
) -> None:
    """Run a full citation audit for BRAND across one or more LLM APIs."""

    # Parse comma-separated inputs
    competitor_list: list[str] = (
        [c.strip() for c in competitors.split(",") if c.strip()]
        if competitors
        else []
    )
    model_list: list[str] = (
        [m.strip() for m in models.split(",") if m.strip()]
        if models
        else AVAILABLE_MODELS
    )

    # Validate model names early so we fail fast before any API calls
    unknown = [m for m in model_list if m not in AVAILABLE_MODELS]
    if unknown:
        typer.echo(
            f"[error] Unknown model(s): {unknown}. "
            f"Available: {AVAILABLE_MODELS}",
            err=True,
        )
        raise typer.Exit(code=1)

    typer.echo(f"\nAI Citation Audit — {brand} / {industry}")
    typer.echo(f"Models:      {', '.join(model_list)}")
    typer.echo(f"Competitors: {', '.join(competitor_list) or '(none)'}")
    typer.echo(f"Output dir:  {output_dir.resolve()}\n")

    try:
        paths = asyncio.run(
            _run_audit(
                brand=brand,
                industry=industry,
                use_case=use_case,
                competitors=competitor_list,
                models=model_list,
                output_dir=output_dir,
            )
        )
    except KeyboardInterrupt:
        typer.echo("\nAborted.", err=True)
        raise typer.Exit(code=130)

    typer.echo("\nDone. Reports written:")
    for label, path in paths.items():
        typer.echo(f"  [{label.upper():4s}] {path.resolve()}")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def main() -> None:
    app()
