"""Simple dominance helpers for coat-color allele expression."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CoatAllele:
    """Decoded coat allele plus modifier information."""

    name: str
    dilute: bool = False


_COAT_ALLELES = (
    "black",
    "chocolate",
    "cinnamon",
    "orange",
    "cream",
    "silver",
    "white",
    "red",
)

_DOMINANCE_RANK = {
    "white": 8,
    "black": 7,
    "red": 6,
    "orange": 5,
    "chocolate": 4,
    "cinnamon": 3,
    "silver": 2,
    "cream": 1,
}

_DILUTIONS = {
    "black": "blue",
    "chocolate": "lilac",
    "cinnamon": "fawn",
    "orange": "cream",
    "red": "cream",
    "silver": "pale silver",
    "cream": "cream",
    "white": "white",
}


def decode_coat_allele(raw_value: int) -> CoatAllele:
    """Decode an 8-bit coat field into a base allele and dilution modifier."""

    return CoatAllele(
        name=_COAT_ALLELES[raw_value % len(_COAT_ALLELES)],
        dilute=bool(raw_value & 0b1000),
    )


def dominant_allele(first: CoatAllele, second: CoatAllele) -> CoatAllele:
    """Return the allele that wins the simple dominance hierarchy."""

    first_rank = _DOMINANCE_RANK[first.name]
    second_rank = _DOMINANCE_RANK[second.name]
    return first if first_rank >= second_rank else second


def expressed_coat_color(allele: CoatAllele) -> str:
    """Return the visible color, applying dilution only as a modifier."""

    if not allele.dilute:
        return allele.name
    return _DILUTIONS[allele.name]
