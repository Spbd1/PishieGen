"""Genotype-to-phenotype expression rules."""

from __future__ import annotations

from dataclasses import dataclass
from math import tanh

from pishiegen.genome.core import Genome


@dataclass(frozen=True, slots=True)
class Phenotype:
    """Expressed trait values used by ecological and fitness modules."""

    traits: dict[str, float]

    def value(self, trait: str, default: float = 0.0) -> float:
        """Return a trait value if present."""

        return self.traits.get(trait, default)


def express_genome(genome: Genome) -> Phenotype:
    """Map a genome to bounded continuous phenotypic traits.

    Gene effects are weighted by dominance and passed through a smooth bounded
    transform. The bounded transform is a modeling convenience for stable early
    simulations.

    TODO: Compare this expression model with established artificial-life systems
    and quantitative genetics references before using it for scientific claims.
    """

    expressed: dict[str, float] = {}
    for trait, genes in genome.by_trait().items():
        additive_effect = sum(gene.effect * gene.dominance for gene in genes)
        expressed[trait] = tanh(additive_effect)
    return Phenotype(expressed)
