"""Compact genome representation for digital organisms.

Genes are intentionally abstract: each gene stores a signed regulatory weight for
one named trait. This is a conservative computational analogue of heritable
variation and regulation, not a claim about real molecular genetics.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True, slots=True)
class Gene:
    """A minimal heritable unit that contributes to one phenotypic trait."""

    locus: str
    trait: str
    effect: float
    dominance: float = 0.5

    def clamped(self, minimum: float = -1.0, maximum: float = 1.0) -> "Gene":
        """Return a copy with bounded numeric values for stable simulations."""

        return Gene(
            locus=self.locus,
            trait=self.trait,
            effect=max(minimum, min(maximum, self.effect)),
            dominance=max(0.0, min(1.0, self.dominance)),
        )


@dataclass(frozen=True, slots=True)
class Genome:
    """A compact collection of genes with a reproducibility seed.

    TODO: Validate default locus counts and trait effect distributions against
    published artificial-life benchmark systems before treating them as more
    than modeling assumptions.
    """

    genes: tuple[Gene, ...]
    generation: int = 0
    parent_ids: tuple[str, ...] = ()

    @classmethod
    def from_genes(
        cls,
        genes: Iterable[Gene],
        generation: int = 0,
        parent_ids: tuple[str, ...] = (),
    ) -> "Genome":
        """Construct a genome while normalizing gene numeric ranges."""

        return cls(tuple(gene.clamped() for gene in genes), generation, parent_ids)

    def by_trait(self) -> dict[str, list[Gene]]:
        """Group genes by expressed trait name."""

        grouped: dict[str, list[Gene]] = {}
        for gene in self.genes:
            grouped.setdefault(gene.trait, []).append(gene)
        return grouped

    def compact_code(self) -> str:
        """Serialize to a simple text code for CLI exchange and tests."""

        fields = [f"generation={self.generation}"]
        fields.extend(
            f"{gene.locus}:{gene.trait}:{gene.effect:.6f}:{gene.dominance:.6f}"
            for gene in self.genes
        )
        return "|".join(fields)

    @classmethod
    def parse(cls, code: str) -> "Genome":
        """Parse a compact code produced by :meth:`compact_code`."""

        if not code:
            raise ValueError("Genome code must not be empty.")
        parts = code.split("|")
        generation = 0
        genes: list[Gene] = []
        for index, part in enumerate(parts):
            if index == 0 and part.startswith("generation="):
                generation = int(part.split("=", 1)[1])
                continue
            locus, trait, effect, dominance = part.split(":")
            genes.append(Gene(locus, trait, float(effect), float(dominance)))
        return cls.from_genes(genes, generation=generation)
