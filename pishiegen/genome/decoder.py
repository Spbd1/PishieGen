"""Deterministic decoder for the compact 128-bit PishieGen genome.

Decoding is intentionally mechanical: each named output is the unsigned integer
stored in its documented bit range. No randomness or biological inference is
performed.
"""

from __future__ import annotations

from pishiegen.genome.encoding import Genome


def decode_genome(genome: Genome | int) -> dict[str, int]:
    """Decode a 128-bit genome into deterministic field values.

    Args:
        genome: Either a ``Genome`` instance or a raw integer constrained to bits
            0 through 127.

    Returns:
        A dictionary in schema order, from ``base_coat_color`` (bits 0-7) through
        ``reserved_experimental`` (bits 120-127).
    """

    if isinstance(genome, Genome):
        compact = genome
    else:
        compact = Genome(genome)
    return compact.to_dict()
