"""Schema for PishieGen's compact 128-bit computational genome.

The 128-bit genome is a deterministic integer encoding, not a literal biological
sequence. Bit ranges are inclusive and use zero-based indexing from the least
significant bit. For example, ``base_coat_color`` occupies bits 0 through 7.
"""

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType


GENOME_BITS = 128
"""Total number of bits in the compact genome integer."""

GENOME_MIN = 0
"""Smallest valid raw genome value."""

GENOME_MAX = 2**GENOME_BITS - 1
"""Largest valid raw genome value."""


@dataclass(frozen=True, slots=True)
class FieldSpec:
    """Description of one named bit field in the 128-bit genome.

    Attributes:
        name: Stable field name used by encoders and decoders.
        start: Inclusive zero-based start bit, counted from the least significant
            bit of the raw integer.
        end: Inclusive zero-based end bit, counted from the least significant bit
            of the raw integer.
    """

    name: str
    start: int
    end: int

    @property
    def width(self) -> int:
        """Return the number of bits occupied by this field."""

        return self.end - self.start + 1

    @property
    def max_value(self) -> int:
        """Return the largest unsigned value that fits in this field."""

        return (1 << self.width) - 1

    @property
    def mask(self) -> int:
        """Return this field's mask at its encoded bit position."""

        return self.max_value << self.start


_FIELD_SPECS = (
    FieldSpec("base_coat_color", 0, 7),
    FieldSpec("hidden_coat_color", 8, 15),
    FieldSpec("agouti_tabby_pattern", 16, 19),
    FieldSpec("pattern_intensity", 20, 23),
    FieldSpec("fur_length_type", 24, 27),
    FieldSpec("ear_morphology", 28, 31),
    FieldSpec("tail_morphology", 32, 35),
    FieldSpec("polydactyly", 36, 37),
    FieldSpec("colorpoint_albino_locus", 38, 39),
    FieldSpec("health_risk_loci", 40, 47),
    FieldSpec("thermal_tolerance", 48, 55),
    FieldSpec("camouflage_profile", 56, 63),
    FieldSpec("agility_muscle", 64, 71),
    FieldSpec("sensory_acuity", 72, 79),
    FieldSpec("intelligence_cognition", 80, 87),
    FieldSpec("circadian_tendency", 88, 95),
    FieldSpec("mutation_markers", 96, 111),
    FieldSpec("lineage_markers", 112, 119),
    FieldSpec("reserved_experimental", 120, 127),
)
"""Ordered field specifications covering bits 0 through 127 exactly once."""

FIELD_SPECS = MappingProxyType({field.name: field for field in _FIELD_SPECS})
"""Immutable mapping from field names to their bit-range specifications."""

FIELD_ORDER = tuple(field.name for field in _FIELD_SPECS)
"""Stable field order used for deterministic dictionary output."""


def get_field_spec(name: str) -> FieldSpec:
    """Return the schema entry for ``name`` or raise ``KeyError``.

    Field names map to inclusive bit ranges in the 128-bit integer. For example,
    ``mutation_markers`` maps to bits 96 through 111.
    """

    try:
        return FIELD_SPECS[name]
    except KeyError as error:
        raise KeyError(f"Unknown genome field: {name!r}") from error
