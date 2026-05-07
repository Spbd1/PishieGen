"""Bit-level utilities and dataclass for the 128-bit PishieGen genome.

The compact genome stores named unsigned integer fields inside a single Python
integer constrained to ``0 <= raw < 2**128``. Bit positions are zero-based from
the least significant bit; each named field's inclusive range is defined in
``pishiegen.genome.schema``. This is a computational genotype inspired by
inheritance concepts, not a literal biological genome.
"""

from __future__ import annotations

from dataclasses import dataclass

from pishiegen.genome.schema import (
    FIELD_ORDER,
    GENOME_BITS,
    GENOME_MAX,
    GENOME_MIN,
    get_field_spec,
)


def validate_raw_genome(raw: int) -> None:
    """Validate that ``raw`` is an integer in the inclusive 128-bit range.

    Valid genomes occupy bits 0 through 127, so the accepted range is
    ``0 <= raw <= 2**128 - 1``.
    """

    if not isinstance(raw, int):
        raise TypeError("Genome raw value must be an int.")
    if raw < GENOME_MIN or raw > GENOME_MAX:
        raise ValueError(f"Genome raw value must satisfy 0 <= raw < 2**{GENOME_BITS}.")


def _validate_bit_window(start: int, width: int) -> None:
    """Validate a bit window within the 0-through-127 genome range."""

    if not isinstance(start, int) or not isinstance(width, int):
        raise TypeError("Bit start and width must be integers.")
    if width <= 0:
        raise ValueError("Bit width must be positive.")
    if start < 0 or start + width > GENOME_BITS:
        raise ValueError(f"Bit window must fit within bits 0 through {GENOME_BITS - 1}.")


def extract_bits(raw: int, start: int, width: int) -> int:
    """Extract an unsigned value from ``raw`` over ``width`` bits at ``start``.

    ``start`` is the least significant bit of the field. For example, extracting
    ``start=8`` and ``width=8`` reads bits 8 through 15.
    """

    validate_raw_genome(raw)
    _validate_bit_window(start, width)
    return (raw >> start) & ((1 << width) - 1)


def set_bits(raw: int, start: int, width: int, value: int) -> int:
    """Set a bit field and return the updated 128-bit genome integer.

    The field spans bits ``start`` through ``start + width - 1`` inclusively.
    Bits outside that range are preserved exactly.
    """

    validate_raw_genome(raw)
    _validate_bit_window(start, width)
    if not isinstance(value, int):
        raise TypeError("Bit field value must be an int.")
    max_value = (1 << width) - 1
    if value < 0 or value > max_value:
        raise ValueError(f"Value {value!r} does not fit in {width} bits.")
    mask = max_value << start
    updated = (raw & ~mask) | (value << start)
    validate_raw_genome(updated)
    return updated


@dataclass(frozen=True, slots=True)
class Genome:
    """Compact 128-bit computational genotype.

    ``raw`` must satisfy ``0 <= raw < 2**128``. Named fields cover fixed bit
    ranges from ``base_coat_color`` in bits 0 through 7 to
    ``reserved_experimental`` in bits 120 through 127.
    """

    raw: int

    def __post_init__(self) -> None:
        """Validate the raw integer immediately after construction."""

        self.validate()

    def validate(self) -> None:
        """Validate that this genome's raw integer fits bits 0 through 127."""

        validate_raw_genome(self.raw)

    def get_field(self, name: str) -> int:
        """Return the unsigned value for a named field's configured bit range."""

        spec = get_field_spec(name)
        return extract_bits(self.raw, spec.start, spec.width)

    def set_field(self, name: str, value: int) -> "Genome":
        """Return a new genome with one named field changed.

        Only the named field's inclusive bit range is modified; all other field
        ranges remain unchanged.
        """

        spec = get_field_spec(name)
        return Genome(set_bits(self.raw, spec.start, spec.width, value))

    def to_dict(self) -> dict[str, int]:
        """Decode every named bit range into a deterministic dictionary."""

        return {name: self.get_field(name) for name in FIELD_ORDER}
