"""Genome data structures and inheritance operators."""

from pishiegen.genome.core import Gene, Genome
from pishiegen.genome.operators import breed, random_genome

__all__ = ["Gene", "Genome", "breed", "random_genome"]
