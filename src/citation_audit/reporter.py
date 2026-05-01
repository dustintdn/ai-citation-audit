"""
reporter.py — Writes the three output files from an AuditResults object.

Outputs:
  citation_report.json   Full raw data: prompts, responses, parsed mentions.
  citation_summary.csv   One row per (brand × model × intent).
  report.html            Standalone HTML client deliverable (Jinja2).
"""

from __future__ import annotations

import csv
import json
from collections import defaultdict
from datetime import datetime, timezone
from importlib import resources
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

from citation_audit.scorer import AuditResults, BrandScore


# ---------------------------------------------------------------------------
# JSON report
# ---------------------------------------------------------------------------


def _write_json(results: AuditResults, path: Path) -> None:
    raw_results = []
    for pr in results.prompt_results:
        raw_results.append(
            {
                "model": pr.model,
                "prompt": {
                    "intent": pr.prompt.intent.value,
                    "phrasing_index": pr.prompt.phrasing_index,
                    "text": pr.prompt.text,
                },
                "response": pr.parsed.raw_text,
                "has_citation": pr.parsed.has_citation,
                "mentions": [
                    {
                        "brand": m.brand,
                        "position": m.position.value,
                        "sentiment": m.sentiment.value,
                        "first_sentence_index": m.first_sentence_index,
                    }
                    for m in pr.parsed.mentions
                ],
            }
        )

    payload = {
        "brand": results.brand,
        "industry": results.industry,
        "competitors": results.competitors,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "results": raw_results,
    }
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


# ---------------------------------------------------------------------------
# CSV summary
# ---------------------------------------------------------------------------

_CSV_FIELDS = [
    "brand",
    "model",
    "intent",
    "mention_rate",
    "avg_position_score",
    "avg_position_label",
    "sentiment_positive",
    "sentiment_neutral",
    "sentiment_negative",
    "dominant_sentiment",
    "citation_rate",
]


def _score_to_row(score: BrandScore) -> dict[str, str | float | int]:
    return {
        "brand": score.brand,
        "model": score.model,
        "intent": score.intent.value,
        "mention_rate": round(score.mention_rate, 4),
        "avg_position_score": round(score.avg_position_score, 4),
        "avg_position_label": score.avg_position_label,
        "sentiment_positive": score.sentiment_counts.get("positive", 0),  # type: ignore[arg-type]
        "sentiment_neutral": score.sentiment_counts.get("neutral", 0),  # type: ignore[arg-type]
        "sentiment_negative": score.sentiment_counts.get("negative", 0),  # type: ignore[arg-type]
        "dominant_sentiment": score.dominant_sentiment.value,
        "citation_rate": round(score.citation_rate, 4),
    }


def _write_csv(results: AuditResults, path: Path) -> None:
    rows = [_score_to_row(s) for s in results.scores]
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=_CSV_FIELDS)
        writer.writeheader()
        writer.writerows(rows)


# ---------------------------------------------------------------------------
# HTML report
# ---------------------------------------------------------------------------


def _write_html(results: AuditResults, path: Path) -> None:
    template_dir = Path(__file__).parent / "templates"
    env = Environment(
        loader=FileSystemLoader(str(template_dir)),
        autoescape=True,
    )
    template = env.get_template("report.html.j2")

    # Group scores by model for the template
    models = sorted({s.model for s in results.scores})
    scores_by_model: dict[str, list[BrandScore]] = defaultdict(list)
    for score in results.scores:
        scores_by_model[score.model].append(score)

    html = template.render(
        brand=results.brand,
        industry=results.industry,
        competitors=results.competitors,
        models=models,
        scores_by_model=scores_by_model,
        generated_at=datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
    )
    path.write_text(html, encoding="utf-8")


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def write_reports(results: AuditResults, output_dir: Path) -> dict[str, Path]:
    """
    Write all three report files to *output_dir*.

    Args:
        results:    Scored audit results from :func:`~citation_audit.scorer.score_results`.
        output_dir: Directory to write output files into (created if absent).

    Returns:
        Dict mapping report name to its absolute :class:`Path`.
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    paths = {
        "json": output_dir / "citation_report.json",
        "csv": output_dir / "citation_summary.csv",
        "html": output_dir / "report.html",
    }

    _write_json(results, paths["json"])
    _write_csv(results, paths["csv"])
    _write_html(results, paths["html"])

    return paths
