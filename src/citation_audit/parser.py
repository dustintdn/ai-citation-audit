"""
parser.py — Response parsing: fuzzy mention detection, position, sentiment, citations.

For each LLM response, this module:
  1. Detects mentions of the target brand and any known competitors via fuzzy matching
  2. Assigns a MentionPosition (FIRST, TOP_3, PRESENT, ABSENT) based on ordering
     of first appearances relative to all tracked brands
  3. Infers sentiment (POSITIVE, NEUTRAL, NEGATIVE) from keyword heuristics in the
     surrounding sentence(s)
  4. Flags whether the response contains any citation URLs
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import Enum

from rapidfuzz import fuzz

# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------


class MentionPosition(str, Enum):
    FIRST = "FIRST"       # this brand's first mention precedes all others
    TOP_3 = "TOP_3"       # within the first 3 brands mentioned
    PRESENT = "PRESENT"   # mentioned but outside top 3
    ABSENT = "ABSENT"     # not detected in the response


class Sentiment(str, Enum):
    POSITIVE = "positive"
    NEUTRAL = "neutral"
    NEGATIVE = "negative"


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

#: Minimum fuzzy partial-ratio score to count as a mention (0–100)
FUZZY_THRESHOLD = 80

_POSITIVE_KEYWORDS: frozenset[str] = frozenset(
    [
        "best", "excellent", "recommend", "recommended", "leading", "top",
        "great", "popular", "powerful", "robust", "industry-leading",
        "widely used", "favorite", "preferred", "trusted", "number one",
        "#1", "outstanding", "superior", "ideal", "perfect", "strong",
        "innovative", "reliable", "comprehensive", "versatile",
    ]
)

_NEGATIVE_KEYWORDS: frozenset[str] = frozenset(
    [
        "worst", "poor", "expensive", "limited", "lacking", "difficult",
        "complex", "outdated", "inferior", "avoid", "disappointing",
        "overpriced", "buggy", "slow", "clunky", "bloated", "unreliable",
        "frustrating", "costly", "steep learning curve", "hard to use",
    ]
)

_URL_PATTERN = re.compile(r"https?://\S+")
_SENTENCE_SPLIT = re.compile(r"(?<=[.!?])\s+")


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------


@dataclass
class BrandMention:
    """Parsed mention record for a single brand within one LLM response."""

    brand: str
    position: MentionPosition
    sentiment: Sentiment
    first_sentence_index: int | None  # None when ABSENT


@dataclass
class ParsedResponse:
    """All parsed data extracted from one (model, prompt) response."""

    raw_text: str
    has_citation: bool
    mentions: list[BrandMention] = field(default_factory=list)

    def get(self, brand: str) -> BrandMention | None:
        """Return the BrandMention for *brand* (case-insensitive), or None."""
        brand_lower = brand.lower()
        for m in self.mentions:
            if m.brand.lower() == brand_lower:
                return m
        return None


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _split_sentences(text: str) -> list[str]:
    """Split *text* into sentences on punctuation boundaries."""
    return [s.strip() for s in _SENTENCE_SPLIT.split(text) if s.strip()]


def _find_first_sentence(brand: str, sentences: list[str]) -> int | None:
    """
    Return the index of the first sentence that fuzzy-matches *brand*,
    or None if not found above the threshold.
    """
    for i, sentence in enumerate(sentences):
        if fuzz.partial_ratio(brand.lower(), sentence.lower()) >= FUZZY_THRESHOLD:
            return i
    return None


def _infer_sentiment(brand: str, sentences: list[str], first_idx: int) -> Sentiment:
    """
    Infer sentiment from the sentence containing the mention and its neighbours.
    Uses simple keyword heuristics.
    """
    # Include the mention sentence plus one before and one after for context
    start = max(0, first_idx - 1)
    end = min(len(sentences), first_idx + 2)
    context = " ".join(sentences[start:end]).lower()

    pos_hits = sum(1 for kw in _POSITIVE_KEYWORDS if kw in context)
    neg_hits = sum(1 for kw in _NEGATIVE_KEYWORDS if kw in context)

    if pos_hits > neg_hits:
        return Sentiment.POSITIVE
    if neg_hits > pos_hits:
        return Sentiment.NEGATIVE
    return Sentiment.NEUTRAL


def _assign_positions(
    brand_sentence_map: dict[str, int | None],
) -> dict[str, MentionPosition]:
    """
    Given a mapping of brand → first_sentence_index (None = absent),
    return a mapping of brand → MentionPosition.

    Ranking is by ascending sentence index; ties share the same rank.
    """
    present = sorted(
        [(brand, idx) for brand, idx in brand_sentence_map.items() if idx is not None],
        key=lambda t: t[1],
    )

    positions: dict[str, MentionPosition] = {}

    for rank, (brand, _) in enumerate(present):
        if rank == 0:
            positions[brand] = MentionPosition.FIRST
        elif rank < 3:
            positions[brand] = MentionPosition.TOP_3
        else:
            positions[brand] = MentionPosition.PRESENT

    for brand, idx in brand_sentence_map.items():
        if idx is None:
            positions[brand] = MentionPosition.ABSENT

    return positions


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def parse_response(
    raw_text: str,
    brand: str,
    competitors: list[str],
) -> ParsedResponse:
    """
    Parse a single LLM response for brand/competitor mentions.

    Args:
        raw_text:    The full text response from the LLM.
        brand:       Target brand name.
        competitors: Known competitor names to also track.

    Returns:
        A :class:`ParsedResponse` with all detected mentions scored.
    """
    all_brands = [brand] + competitors
    sentences = _split_sentences(raw_text)
    has_citation = bool(_URL_PATTERN.search(raw_text))

    # Step 1: find first sentence index for each brand
    first_sentence_map: dict[str, int | None] = {
        b: _find_first_sentence(b, sentences) for b in all_brands
    }

    # Step 2: assign positions based on relative ordering
    position_map = _assign_positions(first_sentence_map)

    # Step 3: build BrandMention records
    mentions: list[BrandMention] = []
    for b in all_brands:
        first_idx = first_sentence_map[b]
        position = position_map[b]
        sentiment = (
            _infer_sentiment(b, sentences, first_idx)
            if first_idx is not None
            else Sentiment.NEUTRAL
        )
        mentions.append(
            BrandMention(
                brand=b,
                position=position,
                sentiment=sentiment,
                first_sentence_index=first_idx,
            )
        )

    return ParsedResponse(
        raw_text=raw_text,
        has_citation=has_citation,
        mentions=mentions,
    )
