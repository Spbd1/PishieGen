"""Biome model for selective pressures and resources."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class Biome:
    """A minimal ecological context for evaluating digital organisms."""

    name: str
    carrying_capacity: int = 100
    resource_level: float = 1.0
    target_traits: dict[str, float] = field(default_factory=dict)
    stressors: dict[str, float] = field(default_factory=dict)

    def normalized(self) -> "Biome":
        """Return a biome with stable numeric bounds."""

        return Biome(
            name=self.name,
            carrying_capacity=max(1, self.carrying_capacity),
            resource_level=max(0.0, min(1.0, self.resource_level)),
            target_traits={key: max(-1.0, min(1.0, value)) for key, value in self.target_traits.items()},
            stressors={key: max(0.0, value) for key, value in self.stressors.items()},
        )
