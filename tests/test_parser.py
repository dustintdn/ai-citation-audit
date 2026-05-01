"""
Unit tests for citation_audit.parser.

Covers: fuzzy mention detection, position ranking, sentiment inference,
        citation (URL) detection, and ABSENT handling.
"""

import pytest

from citation_audit.parser import (
    MentionPosition,
    ParsedResponse,
    Sentiment,
    parse_response,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

BRAND = "Acme CRM"
COMPETITORS = ["RivalSoft", "OtherTool"]


def _parse(text: str, brand: str = BRAND, competitors: list[str] | None = None) -> ParsedResponse:
    return parse_response(text, brand=brand, competitors=competitors or COMPETITORS)


# ---------------------------------------------------------------------------
# Position tests
# ---------------------------------------------------------------------------


class TestMentionPosition:
    def test_brand_mentioned_first_gets_first(self):
        text = (
            "Acme CRM is the best tool on the market. "
            "RivalSoft is a decent alternative. "
            "OtherTool is also worth considering."
        )
        result = _parse(text)
        assert result.get(BRAND).position == MentionPosition.FIRST

    def test_brand_mentioned_second_gets_top3(self):
        text = (
            "RivalSoft leads the industry. "
            "Acme CRM is also an excellent choice. "
            "OtherTool rounds out the options."
        )
        result = _parse(text)
        assert result.get(BRAND).position == MentionPosition.TOP_3

    def test_brand_absent_when_not_mentioned(self):
        text = "RivalSoft and OtherTool dominate this space. Neither has serious competition."
        result = _parse(text)
        assert result.get(BRAND).position == MentionPosition.ABSENT

    def test_competitor_ranked_correctly(self):
        # 4 brands mentioned in order: Acme CRM → FIRST, RivalSoft → TOP_3,
        # OtherTool → TOP_3, LastPlace → PRESENT (rank 3, zero-indexed)
        text = (
            "Acme CRM is the market leader. "
            "RivalSoft is popular among startups. "
            "OtherTool is also worth considering. "
            "LastPlace is rarely recommended by anyone."
        )
        result = _parse(text, competitors=["RivalSoft", "OtherTool", "LastPlace"])
        assert result.get("RivalSoft").position == MentionPosition.TOP_3
        assert result.get("OtherTool").position == MentionPosition.TOP_3
        assert result.get("LastPlace").position == MentionPosition.PRESENT

    def test_fuzzy_match_catches_slight_variation(self):
        # Hyphenated variant "Acme-CRM" should fuzzy-match "Acme CRM" above threshold
        text = "Many companies prefer Acme-CRM for their sales pipeline management."
        result = _parse(text)
        assert result.get(BRAND).position != MentionPosition.ABSENT

    def test_all_brands_absent(self):
        text = "There are many great tools available for businesses today."
        result = _parse(text)
        for b in [BRAND] + COMPETITORS:
            assert result.get(b).position == MentionPosition.ABSENT


# ---------------------------------------------------------------------------
# Sentiment tests
# ---------------------------------------------------------------------------


class TestSentiment:
    def test_positive_keywords_yield_positive_sentiment(self):
        text = "Acme CRM is the best and most trusted platform. Highly recommended."
        result = _parse(text)
        assert result.get(BRAND).sentiment == Sentiment.POSITIVE

    def test_negative_keywords_yield_negative_sentiment(self):
        text = "Acme CRM is overpriced and has a steep learning curve. Most users find it frustrating."
        result = _parse(text)
        assert result.get(BRAND).sentiment == Sentiment.NEGATIVE

    def test_no_sentiment_keywords_yields_neutral(self):
        text = "Acme CRM is a software product used by companies in the sales industry."
        result = _parse(text)
        assert result.get(BRAND).sentiment == Sentiment.NEUTRAL

    def test_absent_brand_sentiment_is_neutral(self):
        text = "RivalSoft is the top choice. OtherTool is also popular."
        result = _parse(text)
        # Absent brands default to NEUTRAL — no sentiment to infer
        assert result.get(BRAND).sentiment == Sentiment.NEUTRAL


# ---------------------------------------------------------------------------
# Citation detection tests
# ---------------------------------------------------------------------------


class TestCitationDetection:
    def test_url_in_response_sets_has_citation_true(self):
        text = "Acme CRM is excellent. See https://acmecrm.com/features for details."
        result = _parse(text)
        assert result.has_citation is True

    def test_no_url_sets_has_citation_false(self):
        text = "Acme CRM is a popular tool in the industry."
        result = _parse(text)
        assert result.has_citation is False

    def test_http_url_also_detected(self):
        text = "More info at http://example.com/page — Acme CRM leads the market."
        result = _parse(text)
        assert result.has_citation is True


# ---------------------------------------------------------------------------
# ParsedResponse.get() helper
# ---------------------------------------------------------------------------


class TestParsedResponseGet:
    def test_get_returns_mention_for_known_brand(self):
        text = "Acme CRM is the best tool available."
        result = _parse(text)
        mention = result.get(BRAND)
        assert mention is not None
        assert mention.brand == BRAND

    def test_get_is_case_insensitive(self):
        text = "Acme CRM is the best tool available."
        result = _parse(text)
        assert result.get("acme crm") is not None
        assert result.get("ACME CRM") is not None

    def test_get_returns_none_for_unknown_brand(self):
        text = "Acme CRM is the best tool available."
        result = _parse(text)
        assert result.get("UnknownBrand XYZ") is None
