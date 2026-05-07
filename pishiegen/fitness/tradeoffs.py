"""Trait trade-off assumptions for ecological fitness modeling.

The entries in this module are simulation assumptions inspired by broad
biological reasoning. They are not veterinary claims and should be calibrated
before being used for empirical inference.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

ConfidenceLevel = Literal["high", "moderate", "speculative"]


@dataclass(frozen=True, slots=True)
class TraitEffect:
    """Context-dependent benefits and costs associated with a trait.

    Effect weights use a small normalized modeling scale where positive values
    indicate advantages and negative values indicate costs in the named context.
    They are intended for transparent simulation configuration, not as measured
    veterinary or ecological effect sizes.
    """

    trait_name: str
    positive_effects: dict[str, float]
    negative_effects: dict[str, float]
    affected_contexts: list[str]
    biological_rationale: str
    confidence_level: ConfidenceLevel


TRAIT_TRADEOFFS: dict[str, TraitEffect] = {
    "thick_long_fur": TraitEffect(
        trait_name="Thick/long fur",
        positive_effects={
            "cold_tolerance": 0.35,
            "snow_biome_survival": 0.25,
        },
        negative_effects={
            "heat_stress_in_desert": -0.30,
            "hot_climate_stamina": -0.18,
        },
        affected_contexts=["cold", "snow", "desert", "hot_climate"],
        biological_rationale=(
            "Dense insulation can reduce heat loss in cold and snowy settings, "
            "but the same insulation can impede heat shedding during hot, open, "
            "or desert activity."
        ),
        confidence_level="high",
    ),
    "short_hairless_coat": TraitEffect(
        trait_name="Short/hairless coat",
        positive_effects={
            "heat_dissipation": 0.30,
            "heat_stress_reduction": 0.25,
        },
        negative_effects={
            "cold_vulnerability": -0.30,
            "snow_biome_survival": -0.25,
        },
        affected_contexts=["hot_climate", "desert", "cold", "snow"],
        biological_rationale=(
            "Sparse covering can make heat loss easier in warm climates, while "
            "providing less insulation against cold, wind, and snow exposure."
        ),
        confidence_level="high",
    ),
    "dark_coat": TraitEffect(
        trait_name="Dark coat",
        positive_effects={
            "night_camouflage": 0.24,
            "dense_forest_concealment": 0.20,
        },
        negative_effects={
            "heat_absorption_open_hot_biomes": -0.18,
            "snow_visibility": -0.26,
        },
        affected_contexts=["night", "dense_forest", "open_hot_biome", "snow"],
        biological_rationale=(
            "Dark coloration can conceal outlines in shadowed or nocturnal "
            "contexts, but may absorb more solar radiation and contrast strongly "
            "against snow."
        ),
        confidence_level="moderate",
    ),
    "light_white_coat": TraitEffect(
        trait_name="Light/white coat",
        positive_effects={
            "snow_camouflage": 0.32,
            "lower_heat_absorption_open_sun": 0.16,
        },
        negative_effects={
            "forest_camouflage": -0.22,
            "night_camouflage": -0.18,
        },
        affected_contexts=["snow", "open_sun", "forest", "night"],
        biological_rationale=(
            "Light coats can blend with snowy backgrounds and reflect more open "
            "sunlight, yet may be conspicuous in darker forest or night settings "
            "unless snow cover or bright moonlight changes the background."
        ),
        confidence_level="moderate",
    ),
    "tabby_disruptive_pattern": TraitEffect(
        trait_name="Tabby/disruptive pattern",
        positive_effects={
            "forest_grassland_camouflage": 0.26,
            "outline_disruption": 0.22,
        },
        negative_effects={
            "uniform_snow_camouflage": -0.16,
            "uniform_desert_camouflage": -0.14,
        },
        affected_contexts=["forest", "grassland", "snow", "desert"],
        biological_rationale=(
            "Striping and mottling can break up body outlines in textured "
            "vegetation, but may stand out on visually uniform snow or sand."
        ),
        confidence_level="moderate",
    ),
    "large_ears": TraitEffect(
        trait_name="Large ears",
        positive_effects={
            "heat_dissipation": 0.22,
            "prey_detection": 0.18,
        },
        negative_effects={
            "cold_exposure": -0.18,
            "dense_terrain_injury_exposure": -0.10,
        },
        affected_contexts=["hot_climate", "hunting", "cold", "dense_terrain"],
        biological_rationale=(
            "Larger external ears can increase surface area for heat exchange "
            "and sound collection, while exposing more tissue to cold or snags "
            "in dense terrain."
        ),
        confidence_level="moderate",
    ),
    "folded_ears": TraitEffect(
        trait_name="Folded ears",
        positive_effects={
            "aesthetic_or_negligible_ecological_effect": 0.01,
        },
        negative_effects={
            "health_risk": -0.25,
            "sensory_efficiency": -0.12,
        },
        affected_contexts=["health", "sensory", "human_preference"],
        biological_rationale=(
            "Folded ears are modeled as having no meaningful ecological benefit "
            "beyond possible human aesthetic preference, with penalties reserved "
            "for health-risk and altered sensory assumptions."
        ),
        confidence_level="high",
    ),
    "long_tail": TraitEffect(
        trait_name="Long tail",
        positive_effects={
            "balance": 0.22,
            "climbing": 0.16,
            "sharp_turns": 0.14,
        },
        negative_effects={
            "dense_terrain_injury_exposure": -0.08,
        },
        affected_contexts=["climbing", "pursuit", "escape", "dense_terrain"],
        biological_rationale=(
            "A long tail can aid balance and turning during climbing or rapid "
            "movement, but adds a small exposure cost where vegetation or tight "
            "spaces increase snagging or injury risk."
        ),
        confidence_level="moderate",
    ),
    "tailless_bobtail": TraitEffect(
        trait_name="Tailless/bobtail",
        positive_effects={
            "tail_injury_risk_reduction": 0.12,
        },
        negative_effects={
            "balance": -0.18,
            "agility": -0.14,
        },
        affected_contexts=["dense_terrain", "climbing", "pursuit", "escape"],
        biological_rationale=(
            "A reduced tail leaves less tail tissue exposed to injury, but is "
            "modeled as reducing balance and agility in contexts where tails aid "
            "body control."
        ),
        confidence_level="moderate",
    ),
    "polydactyly": TraitEffect(
        trait_name="Polydactyly",
        positive_effects={
            "grip": 0.14,
            "climbing": 0.12,
            "mud_wetland_stability": 0.12,
        },
        negative_effects={
            "locomotion_cost": -0.04,
        },
        affected_contexts=["climbing", "wetland", "mud", "general_locomotion"],
        biological_rationale=(
            "Extra toes are modeled as potentially improving contact and grip in "
            "some substrates, with only a small locomotion cost because the effect "
            "may be neutral in many settings."
        ),
        confidence_level="speculative",
    ),
    "high_intelligence": TraitEffect(
        trait_name="High intelligence",
        positive_effects={
            "flexible_behavior": 0.28,
            "biome_time_choice": 0.20,
            "failed_hunt_reduction": 0.18,
        },
        negative_effects={
            "metabolic_cost": -0.18,
            "slower_maturation_or_energy_demand": -0.14,
        },
        affected_contexts=["foraging", "hunting", "migration", "development"],
        biological_rationale=(
            "Flexible behavior can improve decisions across variable conditions, "
            "but larger or more active nervous-system demands are modeled as "
            "requiring more energy and development time."
        ),
        confidence_level="speculative",
    ),
    "high_agility": TraitEffect(
        trait_name="High agility",
        positive_effects={
            "hunting_success": 0.24,
            "escape_success": 0.24,
        },
        negative_effects={
            "energy_demand": -0.16,
            "endurance_without_stamina": -0.12,
        },
        affected_contexts=["hunting", "escape", "energy_budget", "endurance"],
        biological_rationale=(
            "Rapid acceleration and maneuvering can improve hunting and escape, "
            "but are modeled as energetically costly and less useful over long "
            "efforts without matching stamina."
        ),
        confidence_level="moderate",
    ),
}


def all_trait_effects() -> tuple[TraitEffect, ...]:
    """Return all configured trait trade-offs in stable registry order."""

    return tuple(TRAIT_TRADEOFFS.values())
