"""
prompts.py — Prompt battery generator.

Generates 14 prompts across 7 intent types (DISCOVERY, COMPARISON, RECOMMENDATION,
PROBLEM_FIRST, SWITCHING, PERSONA, FEATURE_LED), 2 phrasings each, interpolated
with brand, industry, and use_case context.
"""

from dataclasses import dataclass
from enum import Enum


class PromptIntent(str, Enum):
    DISCOVERY = "discovery"
    COMPARISON = "comparison"
    RECOMMENDATION = "recommendation"
    PROBLEM_FIRST = "problem_first"
    SWITCHING = "switching"
    PERSONA = "persona"
    FEATURE_LED = "feature_led"


@dataclass(frozen=True)
class Prompt:
    intent: PromptIntent
    phrasing_index: int  # 0 or 1
    text: str


_TEMPLATES: list[tuple[PromptIntent, str]] = [
    # DISCOVERY
    (
        PromptIntent.DISCOVERY,
        "What are the best tools for {industry}?",
    ),
    (
        PromptIntent.DISCOVERY,
        "I'm looking for software to help me with {use_case}. What do you recommend?",
    ),
    # COMPARISON
    (
        PromptIntent.COMPARISON,
        "How does {brand} compare to its competitors in {industry}?",
    ),
    (
        PromptIntent.COMPARISON,
        "What are the pros and cons of the top {industry} platforms?",
    ),
    # RECOMMENDATION
    (
        PromptIntent.RECOMMENDATION,
        "If I had to pick one {industry} tool for a mid-sized company, what would you choose?",
    ),
    (
        PromptIntent.RECOMMENDATION,
        "What do most {industry} professionals use for {use_case}?",
    ),
    # PROBLEM_FIRST
    (
        PromptIntent.PROBLEM_FIRST,
        "Our team is struggling with {use_case}. What tools do people use to solve this?",
    ),
    (
        PromptIntent.PROBLEM_FIRST,
        "We're having trouble managing {use_case}. What software would you recommend?",
    ),
    # SWITCHING
    (
        PromptIntent.SWITCHING,
        "What are the best alternatives to {brand} for {use_case}?",
    ),
    (
        PromptIntent.SWITCHING,
        "We're looking to move away from our current {industry} tool. What should we consider?",
    ),
    # PERSONA
    (
        PromptIntent.PERSONA,
        "I'm an operations manager evaluating {industry} tools for a growing startup. What are the top options?",
    ),
    (
        PromptIntent.PERSONA,
        "As a team lead looking for {use_case} software, what would you suggest?",
    ),
    # FEATURE_LED
    (
        PromptIntent.FEATURE_LED,
        "What {industry} platforms are known for the best reporting and analytics?",
    ),
    (
        PromptIntent.FEATURE_LED,
        "Which {industry} tools are easiest to onboard a new team onto?",
    ),
]


def build_prompt_battery(
    brand: str,
    industry: str,
    use_case: str | None = None,
) -> list[Prompt]:
    """
    Return the 6-prompt battery interpolated with the given context.

    Args:
        brand:     Target brand name (e.g. "Salesforce").
        industry:  Industry/category context (e.g. "CRM software").
        use_case:  Optional specific use case; defaults to ``industry`` if omitted.

    Returns:
        List of :class:`Prompt` objects in template order.
    """
    resolved_use_case = use_case if use_case else industry

    intent_counters: dict[PromptIntent, int] = {}
    prompts: list[Prompt] = []

    for intent, template in _TEMPLATES:
        idx = intent_counters.get(intent, 0)
        text = template.format(
            brand=brand,
            industry=industry,
            use_case=resolved_use_case,
        )
        prompts.append(Prompt(intent=intent, phrasing_index=idx, text=text))
        intent_counters[intent] = idx + 1

    return prompts
