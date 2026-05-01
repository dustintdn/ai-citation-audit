"""
scorer.py — Aggregates parsed responses into per-(brand × model × intent) scores.

Score dimensions:
  - mention_rate       float [0–1]: fraction of prompts where brand was not ABSENT
  - avg_position_score float [1–4]: mean numeric position (1=FIRST … 4=ABSENT)
  - sentiment_counts   breakdown of POSITIVE / NEUTRAL / NEGATIVE hits
  - dominant_sentiment the most common sentiment across prompts in this group
  - citation_rate      float [0–1]: fraction of responses that contained a URL
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field

from citation_audit.parser import (
    BrandMention,
    MentionPosition,
    ParsedResponse,
    Sentiment,
)
from citation_audit.prompts import Prompt, PromptIntent

# ---------------------------------------------------------------------------
# Position → numeric weight
# ---------------------------------------------------------------------------

_POSITION_SCORE: dict[MentionPosition, float] = {
    MentionPosition.FIRST: 1.0,
    MentionPosition.TOP_3: 2.0,
    MentionPosition.PRESENT: 3.0,
    MentionPosition.ABSENT: 4.0,
}


# ---------------------------------------------------------------------------
# Data models
# ---------------------------------------------------------------------------


@dataclass
class PromptResult:
    """Raw result for one (model, prompt) pair — input to the scorer."""

    model: str
    prompt: Prompt
    parsed: ParsedResponse


@dataclass
class BrandScore:
    """
    Aggregated scores for one (brand × model × intent) group.
    One row in the CSV summary.
    """

    brand: str
    model: str
    intent: PromptIntent
    mention_rate: float
    avg_position_score: float
    sentiment_counts: dict[Sentiment, int]
    dominant_sentiment: Sentiment
    citation_rate: float

    # Convenience: human-readable position label for the average score
    @property
    def avg_position_label(self) -> str:
        score = self.avg_position_score
        if score <= 1.0:
            return "FIRST"
        if score <= 2.0:
            return "TOP_3"
        if score <= 3.0:
            return "PRESENT"
        return "ABSENT"


@dataclass
class AuditResults:
    """Top-level container returned by :func:`score_results`."""

    brand: str
    industry: str
    competitors: list[str]
    scores: list[BrandScore]
    prompt_results: list[PromptResult]  # full raw data for the JSON report

    @property
    def all_tracked_brands(self) -> list[str]:
        return [self.brand] + self.competitors

    def scores_for(
        self,
        brand: str | None = None,
        model: str | None = None,
        intent: PromptIntent | None = None,
    ) -> list[BrandScore]:
        """Filter scores by any combination of brand / model / intent."""
        result = self.scores
        if brand is not None:
            result = [s for s in result if s.brand.lower() == brand.lower()]
        if model is not None:
            result = [s for s in result if s.model == model]
        if intent is not None:
            result = [s for s in result if s.intent == intent]
        return result


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _dominant(counts: dict[Sentiment, int]) -> Sentiment:
    """Return the sentiment with the highest count; NEUTRAL breaks ties."""
    if not counts:
        return Sentiment.NEUTRAL
    return max(counts, key=lambda s: (counts[s], s == Sentiment.NEUTRAL))


def _score_group(
    brand: str,
    model: str,
    intent: PromptIntent,
    mentions: list[tuple[BrandMention, bool]],  # (mention, has_citation)
) -> BrandScore:
    """Compute a :class:`BrandScore` from a list of (mention, has_citation) pairs."""
    n = len(mentions)
    present_count = sum(
        1 for m, _ in mentions if m.position != MentionPosition.ABSENT
    )
    position_sum = sum(_POSITION_SCORE[m.position] for m, _ in mentions)
    citation_count = sum(1 for _, has_cit in mentions if has_cit)

    sentiment_counts: dict[Sentiment, int] = defaultdict(int)
    for m, _ in mentions:
        if m.position != MentionPosition.ABSENT:
            sentiment_counts[m.sentiment] += 1

    return BrandScore(
        brand=brand,
        model=model,
        intent=intent,
        mention_rate=present_count / n if n else 0.0,
        avg_position_score=position_sum / n if n else 4.0,
        sentiment_counts=dict(sentiment_counts),
        dominant_sentiment=_dominant(dict(sentiment_counts)),
        citation_rate=citation_count / n if n else 0.0,
    )


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def score_results(
    prompt_results: list[PromptResult],
    brand: str,
    industry: str,
    competitors: list[str],
) -> AuditResults:
    """
    Aggregate a flat list of :class:`PromptResult` objects into brand scores.

    Groups by (brand × model × intent) and computes mention_rate,
    avg_position_score, sentiment breakdown, and citation_rate for each group.

    Args:
        prompt_results: One entry per (model, prompt) pair from the query phase.
        brand:          Target brand name.
        industry:       Industry context (stored on AuditResults for reporting).
        competitors:    Known competitor names.

    Returns:
        :class:`AuditResults` containing all scores and raw prompt results.
    """
    all_brands = [brand] + competitors

    # Group mentions: key = (brand, model, intent)
    groups: dict[
        tuple[str, str, PromptIntent],
        list[tuple[BrandMention, bool]],
    ] = defaultdict(list)

    for pr in prompt_results:
        for b in all_brands:
            mention = pr.parsed.get(b)
            if mention is None:
                continue
            key = (b, pr.model, pr.prompt.intent)
            groups[key].append((mention, pr.parsed.has_citation))

    scores = [
        _score_group(b, model, intent, mentions)
        for (b, model, intent), mentions in sorted(groups.items())
    ]

    return AuditResults(
        brand=brand,
        industry=industry,
        competitors=competitors,
        scores=scores,
        prompt_results=prompt_results,
    )
