"""
Unit tests for citation_audit.scorer.

Covers: mention_rate, avg_position_score, sentiment aggregation,
        citation_rate, dominant_sentiment, and AuditResults.scores_for filtering.
"""

import pytest

from citation_audit.parser import BrandMention, MentionPosition, ParsedResponse, Sentiment
from citation_audit.prompts import Prompt, PromptIntent
from citation_audit.scorer import (
    AuditResults,
    BrandScore,
    PromptResult,
    score_results,
)

# ---------------------------------------------------------------------------
# Fixtures / factories
# ---------------------------------------------------------------------------

BRAND = "Acme CRM"
COMPETITORS = ["RivalSoft"]


def _mention(
    brand: str,
    position: MentionPosition,
    sentiment: Sentiment = Sentiment.NEUTRAL,
) -> BrandMention:
    return BrandMention(
        brand=brand,
        position=position,
        sentiment=sentiment,
        first_sentence_index=0 if position != MentionPosition.ABSENT else None,
    )


def _parsed(
    brand_position: MentionPosition,
    competitor_position: MentionPosition = MentionPosition.ABSENT,
    brand_sentiment: Sentiment = Sentiment.NEUTRAL,
    has_citation: bool = False,
) -> ParsedResponse:
    return ParsedResponse(
        raw_text="dummy",
        has_citation=has_citation,
        mentions=[
            _mention(BRAND, brand_position, brand_sentiment),
            _mention(COMPETITORS[0], competitor_position),
        ],
    )


def _prompt(intent: PromptIntent, phrasing_index: int = 0) -> Prompt:
    return Prompt(intent=intent, phrasing_index=phrasing_index, text="dummy prompt")


def _pr(
    model: str,
    intent: PromptIntent,
    brand_position: MentionPosition,
    brand_sentiment: Sentiment = Sentiment.NEUTRAL,
    has_citation: bool = False,
    phrasing_index: int = 0,
) -> PromptResult:
    return PromptResult(
        model=model,
        prompt=_prompt(intent, phrasing_index),
        parsed=_parsed(brand_position, brand_sentiment=brand_sentiment, has_citation=has_citation),
    )


def _score(prompt_results: list[PromptResult]) -> AuditResults:
    return score_results(
        prompt_results=prompt_results,
        brand=BRAND,
        industry="software",
        competitors=COMPETITORS,
    )


# ---------------------------------------------------------------------------
# mention_rate tests
# ---------------------------------------------------------------------------


class TestMentionRate:
    def test_all_present_gives_100_pct(self):
        prs = [
            _pr("openai", PromptIntent.DISCOVERY, MentionPosition.FIRST, phrasing_index=0),
            _pr("openai", PromptIntent.DISCOVERY, MentionPosition.TOP_3, phrasing_index=1),
        ]
        results = _score(prs)
        brand_scores = results.scores_for(brand=BRAND, model="openai", intent=PromptIntent.DISCOVERY)
        assert len(brand_scores) == 1
        assert brand_scores[0].mention_rate == 1.0

    def test_all_absent_gives_0_pct(self):
        prs = [
            _pr("openai", PromptIntent.DISCOVERY, MentionPosition.ABSENT, phrasing_index=0),
            _pr("openai", PromptIntent.DISCOVERY, MentionPosition.ABSENT, phrasing_index=1),
        ]
        results = _score(prs)
        brand_scores = results.scores_for(brand=BRAND, model="openai", intent=PromptIntent.DISCOVERY)
        assert brand_scores[0].mention_rate == 0.0

    def test_half_present_gives_50_pct(self):
        prs = [
            _pr("openai", PromptIntent.COMPARISON, MentionPosition.FIRST, phrasing_index=0),
            _pr("openai", PromptIntent.COMPARISON, MentionPosition.ABSENT, phrasing_index=1),
        ]
        results = _score(prs)
        brand_scores = results.scores_for(brand=BRAND, model="openai", intent=PromptIntent.COMPARISON)
        assert brand_scores[0].mention_rate == 0.5


# ---------------------------------------------------------------------------
# avg_position_score tests
# ---------------------------------------------------------------------------


class TestAvgPositionScore:
    def test_all_first_gives_score_1(self):
        prs = [
            _pr("openai", PromptIntent.RECOMMENDATION, MentionPosition.FIRST, phrasing_index=0),
            _pr("openai", PromptIntent.RECOMMENDATION, MentionPosition.FIRST, phrasing_index=1),
        ]
        results = _score(prs)
        s = results.scores_for(brand=BRAND, model="openai", intent=PromptIntent.RECOMMENDATION)[0]
        assert s.avg_position_score == 1.0
        assert s.avg_position_label == "FIRST"

    def test_first_and_absent_averages_to_present_label(self):
        # FIRST=1, ABSENT=4 → avg=2.5 → label PRESENT (> 2.0 threshold)
        prs = [
            _pr("openai", PromptIntent.DISCOVERY, MentionPosition.FIRST, phrasing_index=0),
            _pr("openai", PromptIntent.DISCOVERY, MentionPosition.ABSENT, phrasing_index=1),
        ]
        results = _score(prs)
        s = results.scores_for(brand=BRAND, model="openai", intent=PromptIntent.DISCOVERY)[0]
        assert s.avg_position_score == 2.5
        assert s.avg_position_label == "PRESENT"

    def test_all_absent_gives_score_4_and_absent_label(self):
        prs = [
            _pr("openai", PromptIntent.COMPARISON, MentionPosition.ABSENT, phrasing_index=0),
        ]
        results = _score(prs)
        s = results.scores_for(brand=BRAND, model="openai", intent=PromptIntent.COMPARISON)[0]
        assert s.avg_position_score == 4.0
        assert s.avg_position_label == "ABSENT"


# ---------------------------------------------------------------------------
# Sentiment aggregation tests
# ---------------------------------------------------------------------------


class TestSentimentAggregation:
    def test_all_positive_dominant_sentiment(self):
        prs = [
            _pr("openai", PromptIntent.DISCOVERY, MentionPosition.FIRST, Sentiment.POSITIVE, phrasing_index=0),
            _pr("openai", PromptIntent.DISCOVERY, MentionPosition.FIRST, Sentiment.POSITIVE, phrasing_index=1),
        ]
        results = _score(prs)
        s = results.scores_for(brand=BRAND, model="openai", intent=PromptIntent.DISCOVERY)[0]
        assert s.dominant_sentiment == Sentiment.POSITIVE
        assert s.sentiment_counts.get(Sentiment.POSITIVE, 0) == 2

    def test_mixed_sentiment_picks_majority(self):
        prs = [
            _pr("openai", PromptIntent.COMPARISON, MentionPosition.FIRST, Sentiment.NEGATIVE, phrasing_index=0),
            _pr("openai", PromptIntent.COMPARISON, MentionPosition.FIRST, Sentiment.NEGATIVE, phrasing_index=1),
            _pr("openai", PromptIntent.COMPARISON, MentionPosition.FIRST, Sentiment.POSITIVE, phrasing_index=0),
        ]
        results = _score(prs)
        s = results.scores_for(brand=BRAND, model="openai", intent=PromptIntent.COMPARISON)[0]
        assert s.dominant_sentiment == Sentiment.NEGATIVE

    def test_absent_mentions_excluded_from_sentiment_counts(self):
        prs = [
            _pr("openai", PromptIntent.RECOMMENDATION, MentionPosition.ABSENT, Sentiment.POSITIVE, phrasing_index=0),
        ]
        results = _score(prs)
        s = results.scores_for(brand=BRAND, model="openai", intent=PromptIntent.RECOMMENDATION)[0]
        # No present mentions → sentiment_counts should be empty
        assert s.sentiment_counts.get(Sentiment.POSITIVE, 0) == 0


# ---------------------------------------------------------------------------
# Citation rate tests
# ---------------------------------------------------------------------------


class TestCitationRate:
    def test_citation_rate_calculated_correctly(self):
        prs = [
            _pr("perplexity", PromptIntent.DISCOVERY, MentionPosition.FIRST, has_citation=True, phrasing_index=0),
            _pr("perplexity", PromptIntent.DISCOVERY, MentionPosition.FIRST, has_citation=False, phrasing_index=1),
        ]
        results = _score(prs)
        s = results.scores_for(brand=BRAND, model="perplexity", intent=PromptIntent.DISCOVERY)[0]
        assert s.citation_rate == 0.5


# ---------------------------------------------------------------------------
# AuditResults.scores_for filtering
# ---------------------------------------------------------------------------


class TestScoresFor:
    def _multi_model_results(self) -> AuditResults:
        prs = [
            _pr("openai", PromptIntent.DISCOVERY, MentionPosition.FIRST, phrasing_index=0),
            _pr("anthropic", PromptIntent.DISCOVERY, MentionPosition.TOP_3, phrasing_index=0),
            _pr("openai", PromptIntent.COMPARISON, MentionPosition.PRESENT, phrasing_index=0),
        ]
        return _score(prs)

    def test_filter_by_model(self):
        results = self._multi_model_results()
        openai_scores = results.scores_for(brand=BRAND, model="openai")
        assert all(s.model == "openai" for s in openai_scores)

    def test_filter_by_intent(self):
        results = self._multi_model_results()
        discovery = results.scores_for(brand=BRAND, intent=PromptIntent.DISCOVERY)
        assert all(s.intent == PromptIntent.DISCOVERY for s in discovery)

    def test_filter_by_brand_and_model(self):
        results = self._multi_model_results()
        scores = results.scores_for(brand=BRAND, model="anthropic")
        assert len(scores) == 1
        assert scores[0].model == "anthropic"
        assert scores[0].brand == BRAND
