"""Fitness scoring for biome-specific adaptation."""

from pishiegen.fitness.scoring import FitnessResult, score_fitness
from pishiegen.fitness.tradeoffs import TRAIT_TRADEOFFS, TraitEffect, all_trait_effects

__all__ = [
    "FitnessResult",
    "TRAIT_TRADEOFFS",
    "TraitEffect",
    "all_trait_effects",
    "score_fitness",
]
