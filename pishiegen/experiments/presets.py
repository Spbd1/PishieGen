"""Small reproducible experiment presets."""

from __future__ import annotations

import random

from pishiegen.environment import Biome
from pishiegen.genome import random_genome
from pishiegen.simulation import Organism


def temperate_biome() -> Biome:
    """Return a transparent default biome for smoke tests and examples."""

    return Biome(
        name="temperate_baseline",
        carrying_capacity=100,
        resource_level=0.8,
        target_traits={"resource_efficiency": 0.4, "motility": 0.1},
        stressors={"stress_resistance": 0.2},
    )


def create_seed_population(size: int, seed: int, gene_count: int = 8) -> tuple[Organism, ...]:
    """Create a reproducible starting population."""

    rng = random.Random(seed)
    return tuple(Organism.from_genome(random_genome(rng, gene_count)) for _ in range(size))
