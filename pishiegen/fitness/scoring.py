"""Biome-specific fitness functions."""

from __future__ import annotations

from dataclasses import dataclass

from pishiegen.environment import Biome
from pishiegen.phenotype import Phenotype


@dataclass(frozen=True, slots=True)
class FitnessResult:
    """Fitness score and interpretable components."""

    score: float
    components: dict[str, float]


def score_fitness(phenotype: Phenotype, biome: Biome) -> FitnessResult:
    """Score adaptation to a biome using conservative distance penalties.

    Trait matching is a simplified selection landscape: organisms closer to the
    biome's target traits receive higher scores. Stressors penalize inadequate
    corresponding traits.

    TODO: Calibrate scoring functions against explicit experimental hypotheses;
    this default is a transparent baseline, not an empirical model.
    """

    normalized_biome = biome.normalized()
    components: dict[str, float] = {}
    score = normalized_biome.resource_level

    for trait, target in normalized_biome.target_traits.items():
        distance = abs(phenotype.value(trait) - target)
        component = max(0.0, 1.0 - distance)
        components[f"match:{trait}"] = component
        score *= component

    for trait, intensity in normalized_biome.stressors.items():
        resistance = max(0.0, phenotype.value(trait))
        penalty = max(0.0, 1.0 - intensity * (1.0 - resistance))
        components[f"stress:{trait}"] = penalty
        score *= penalty

    return FitnessResult(score=max(0.0, score), components=components)
