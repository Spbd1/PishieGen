"""Inheritance, mutation, and random genome generation."""

from __future__ import annotations

import random
from collections.abc import Sequence

from pishiegen.genome.core import Gene, Genome

DEFAULT_TRAITS: tuple[str, ...] = (
    "motility",
    "resource_efficiency",
    "thermal_tolerance",
    "stress_resistance",
)


def random_genome(
    rng: random.Random,
    gene_count: int = 8,
    traits: Sequence[str] = DEFAULT_TRAITS,
) -> Genome:
    """Create a compact random genome with bounded trait effects.

    TODO: Review whether uniform initialization is suitable for planned
    experiments; many biological and evolutionary simulations use domain-specific
    priors or benchmark landscapes.
    """

    genes = tuple(
        Gene(
            locus=f"L{index:03d}",
            trait=rng.choice(tuple(traits)),
            effect=rng.uniform(-1.0, 1.0),
            dominance=rng.uniform(0.0, 1.0),
        )
        for index in range(gene_count)
    )
    return Genome.from_genes(genes)


def mutate_gene(gene: Gene, rng: random.Random, step_size: float = 0.1) -> Gene:
    """Return a gene with a small Gaussian perturbation to its effect."""

    return Gene(
        locus=gene.locus,
        trait=gene.trait,
        effect=gene.effect + rng.gauss(0.0, step_size),
        dominance=gene.dominance,
    ).clamped()


def breed(
    parent_a: Genome,
    parent_b: Genome,
    rng: random.Random,
    mutation_rate: float = 0.01,
    offspring_parent_ids: tuple[str, str] = ("parent_a", "parent_b"),
) -> Genome:
    """Create an offspring genome via simple locus-wise recombination.

    This function models heritable variation through recombination-like sampling
    and mutation. It does not attempt to reproduce the mechanistic detail of any
    specific biological reproductive system.
    """

    if len(parent_a.genes) != len(parent_b.genes):
        raise ValueError("Parents must have the same number of genes.")
    offspring: list[Gene] = []
    for gene_a, gene_b in zip(parent_a.genes, parent_b.genes, strict=True):
        chosen = gene_a if rng.random() < 0.5 else gene_b
        if rng.random() < mutation_rate:
            chosen = mutate_gene(chosen, rng)
        offspring.append(chosen)
    return Genome.from_genes(
        offspring,
        generation=max(parent_a.generation, parent_b.generation) + 1,
        parent_ids=offspring_parent_ids,
    )
