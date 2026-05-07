from __future__ import annotations

import random

from pishiegen.cli import main
from pishiegen.experiments import create_seed_population, temperate_biome
from pishiegen.simulation import Simulation


def test_simulation_runs_for_requested_generations() -> None:
    population = create_seed_population(size=5, seed=4, gene_count=4)

    result = Simulation(temperate_biome(), rng=random.Random(4)).run(population, generations=3)

    assert result.generations == 3
    assert len(result.mean_fitness_by_generation) == 3
    assert len(result.population) == 5


def test_cli_generate_organism(capsys) -> None:  # type: ignore[no-untyped-def]
    exit_code = main(["generate-organism", "--seed", "5", "--genes", "4"])

    captured = capsys.readouterr()

    assert exit_code == 0
    assert "genome" in captured.out
