"""Structured phenotype traits and bounded numeric helpers."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


def clamp(value: float, minimum: float = 0.0, maximum: float = 1.0) -> float:
    """Return ``value`` constrained to the inclusive ``minimum``/``maximum`` range."""

    return max(minimum, min(maximum, value))


@dataclass(frozen=True, slots=True)
class Phenotype:
    """Expressed Pishie traits derived from a compact computational genotype.

    Numeric ecological and fitness-facing values are normalized to the inclusive
    0-1 range. Categorical morphology fields remain human-readable strings.
    ``extra_traits`` preserves compatibility with older abstract gene genomes.
    """

    coat_color: str
    hidden_coat_color: str
    pattern: str
    pattern_intensity: float
    fur_length: float
    fur_type: str
    ear_type: str
    ear_size: float
    tail_type: str
    polydactyly_status: str
    colorpoint_status: str
    health_risk_score: float
    cold_tolerance: float
    heat_tolerance: float
    forest_camouflage: float
    desert_camouflage: float
    snow_camouflage: float
    wetland_mobility: float
    agility: float
    sensory_acuity: float
    intelligence: float
    circadian_type: str
    extra_traits: dict[str, float] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Clamp all normalized numeric values after dataclass construction."""

        for name in _NORMALIZED_FIELDS:
            object.__setattr__(self, name, clamp(float(getattr(self, name))))
        object.__setattr__(
            self,
            "extra_traits",
            {name: clamp(float(value)) for name, value in self.extra_traits.items()},
        )

    @property
    def traits(self) -> dict[str, Any]:
        """Return a serializable dictionary of all expressed phenotype fields."""

        values: dict[str, Any] = {
            "coat_color": self.coat_color,
            "hidden_coat_color": self.hidden_coat_color,
            "pattern": self.pattern,
            "pattern_intensity": self.pattern_intensity,
            "fur_length": self.fur_length,
            "fur_type": self.fur_type,
            "ear_type": self.ear_type,
            "ear_size": self.ear_size,
            "tail_type": self.tail_type,
            "polydactyly_status": self.polydactyly_status,
            "colorpoint_status": self.colorpoint_status,
            "health_risk_score": self.health_risk_score,
            "cold_tolerance": self.cold_tolerance,
            "heat_tolerance": self.heat_tolerance,
            "forest_camouflage": self.forest_camouflage,
            "desert_camouflage": self.desert_camouflage,
            "snow_camouflage": self.snow_camouflage,
            "wetland_mobility": self.wetland_mobility,
            "agility": self.agility,
            "sensory_acuity": self.sensory_acuity,
            "intelligence": self.intelligence,
            "circadian_type": self.circadian_type,
        }
        values.update(self.extra_traits)
        return values

    def value(self, trait: str, default: float = 0.0) -> float:
        """Return a numeric trait value for fitness scoring.

        Categorical traits intentionally return ``default`` because distance-based
        fitness scoring expects normalized continuous values.
        """

        if trait in self.extra_traits:
            return self.extra_traits[trait]
        value = getattr(self, trait, default)
        return value if isinstance(value, int | float) else default


_NORMALIZED_FIELDS = (
    "pattern_intensity",
    "fur_length",
    "ear_size",
    "health_risk_score",
    "cold_tolerance",
    "heat_tolerance",
    "forest_camouflage",
    "desert_camouflage",
    "snow_camouflage",
    "wetland_mobility",
    "agility",
    "sensory_acuity",
    "intelligence",
)


PHENOTYPE_FIELDS = (
    "coat_color",
    "hidden_coat_color",
    "pattern",
    "pattern_intensity",
    "fur_length",
    "fur_type",
    "ear_type",
    "ear_size",
    "tail_type",
    "polydactyly_status",
    "colorpoint_status",
    "health_risk_score",
    "cold_tolerance",
    "heat_tolerance",
    "forest_camouflage",
    "desert_camouflage",
    "snow_camouflage",
    "wetland_mobility",
    "agility",
    "sensory_acuity",
    "intelligence",
    "circadian_type",
)
