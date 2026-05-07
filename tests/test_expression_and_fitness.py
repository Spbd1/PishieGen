from __future__ import annotations

from pishiegen.environment import Biome
from pishiegen.fitness import score_fitness
from pishiegen.genome import Gene, Genome
from pishiegen.phenotype import express_genome


def test_expression_produces_bounded_traits() -> None:
    genome = Genome.from_genes([Gene("L001", "motility", 1.0, 1.0)])

    phenotype = express_genome(genome)

    assert 0.0 < phenotype.value("motility") < 1.0


def test_fitness_score_is_non_negative() -> None:
    genome = Genome.from_genes([Gene("L001", "motility", 0.5, 1.0)])
    biome = Biome(name="test", target_traits={"motility": 0.2})

    result = score_fitness(express_genome(genome), biome)

    assert result.score >= 0.0
    assert "match:motility" in result.components
