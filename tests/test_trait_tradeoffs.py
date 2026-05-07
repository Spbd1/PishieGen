from __future__ import annotations

from pishiegen.fitness import TRAIT_TRADEOFFS, TraitEffect, all_trait_effects


REQUIRED_TRADEOFF_KEYS = {
    "thick_long_fur",
    "short_hairless_coat",
    "dark_coat",
    "light_white_coat",
    "tabby_disruptive_pattern",
    "large_ears",
    "folded_ears",
    "long_tail",
    "tailless_bobtail",
    "polydactyly",
    "high_intelligence",
    "high_agility",
}


def test_required_trait_tradeoffs_are_registered() -> None:
    assert set(TRAIT_TRADEOFFS) == REQUIRED_TRADEOFF_KEYS
    assert all(isinstance(effect, TraitEffect) for effect in all_trait_effects())


def test_every_trait_has_at_least_one_benefit_and_cost() -> None:
    one_sided_traits = [
        effect.trait_name
        for effect in all_trait_effects()
        if not effect.positive_effects or not effect.negative_effects
    ]

    assert one_sided_traits == []


def test_tradeoff_effect_directions_are_explicit() -> None:
    for effect in all_trait_effects():
        assert all(value > 0.0 for value in effect.positive_effects.values())
        assert all(value < 0.0 for value in effect.negative_effects.values())


def test_tradeoffs_include_context_rationale_and_confidence() -> None:
    for effect in all_trait_effects():
        assert effect.affected_contexts
        assert effect.biological_rationale
        assert effect.confidence_level in {"high", "moderate", "speculative"}
