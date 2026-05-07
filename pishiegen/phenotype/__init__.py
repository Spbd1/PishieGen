"""Phenotype expression from compact genomes."""

from pishiegen.phenotype.expression import express_genome
from pishiegen.phenotype.traits import PHENOTYPE_FIELDS, Phenotype, clamp

__all__ = ["PHENOTYPE_FIELDS", "Phenotype", "clamp", "express_genome"]
