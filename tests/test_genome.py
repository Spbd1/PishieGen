from __future__ import annotations

import random

from pishiegen.genome import Genome, breed, random_genome


def test_random_genome_round_trip() -> None:
    genome = random_genome(random.Random(1), gene_count=4)

    parsed = Genome.parse(genome.compact_code())

    assert len(parsed.genes) == 4
    assert parsed.generation == genome.generation


def test_breed_increments_generation() -> None:
    rng = random.Random(2)
    parent_a = random_genome(rng, gene_count=4)
    parent_b = random_genome(rng, gene_count=4)

    child = breed(parent_a, parent_b, random.Random(3), mutation_rate=0.0)

    assert child.generation == 1
    assert len(child.genes) == 4
