"""Run a minimal reproducible PishieGen simulation."""

from __future__ import annotations

import random

from pishiegen.experiments import create_seed_population, temperate_biome
from pishiegen.simulation import Simulation
from pishiegen.visualization import summarize_fitness


def main() -> None:
    biome = temperate_biome()
    population = create_seed_population(size=20, seed=42)
    result = Simulation(biome=biome, rng=random.Random(42)).run(population, generations=5)
    print(summarize_fitness(result))


if __name__ == "__main__":
    main()
