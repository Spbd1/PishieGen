"""Genotype-to-phenotype expression rules for PishieGen."""

from __future__ import annotations

from math import tanh

from pishiegen.genome.core import Genome as AbstractGenome
from pishiegen.genome.decoder import decode_genome
from pishiegen.genome.encoding import Genome as CompactGenome
from pishiegen.phenotype.dominance import (
    decode_coat_allele,
    dominant_allele,
    expressed_coat_color,
)
from pishiegen.phenotype.traits import Phenotype, clamp


_PATTERN_BY_CODE = {
    0: "mackerel tabby",
    1: "classic tabby",
    2: "spotted tabby",
    3: "ticked tabby",
    4: "rosetted tabby",
    5: "broken tabby",
    6: "marbled tabby",
    7: "striped tabby",
}
_FUR_TYPES = ("straight", "wavy", "curly", "rex")
_EAR_TYPES = ("normal", "folded", "curled", "lynx-tufted")
_TAIL_TYPES = ("normal", "long", "bobtail", "tailless")
_POLYDACTYLY = ("none", "carrier", "polydactyl", "strong polydactyl")
_COLORPOINT = ("none", "carrier", "colorpoint", "albino")
_CIRCADIAN = ("nocturnal", "diurnal", "crepuscular")


def express_genome(genome: CompactGenome | AbstractGenome | int) -> Phenotype:
    """Convert a compact 128-bit genotype into a structured phenotype.

    The primary expression path accepts ``pishiegen.genome.encoding.Genome`` or a
    raw 128-bit integer. The older abstract gene ``Genome`` remains supported for
    existing simulations by expressing its arbitrary gene effects as
    ``extra_traits`` on an otherwise neutral phenotype.
    """

    if isinstance(genome, AbstractGenome):
        return _express_abstract_genome(genome)
    fields = decode_genome(genome)
    return _express_compact_fields(fields)


def _express_compact_fields(fields: dict[str, int]) -> Phenotype:
    base_allele = decode_coat_allele(fields["base_coat_color"])
    hidden_allele = decode_coat_allele(fields["hidden_coat_color"])
    visible_allele = dominant_allele(base_allele, hidden_allele)

    agouti_field = fields["agouti_tabby_pattern"]
    agouti = bool(agouti_field & 0b1000)
    pattern = _PATTERN_BY_CODE[agouti_field & 0b0111] if agouti else "solid"
    pattern_intensity = fields["pattern_intensity"] / 15.0 if agouti else 0.0

    fur_field = fields["fur_length_type"]
    fur_length = (fur_field & 0b0011) / 3.0
    fur_type = _FUR_TYPES[(fur_field >> 2) & 0b0011]

    ear_field = fields["ear_morphology"]
    ear_type = _EAR_TYPES[ear_field & 0b0011]
    ear_size = ((ear_field >> 2) & 0b0011) / 3.0

    tail_type = _TAIL_TYPES[fields["tail_morphology"] & 0b0011]
    polydactyly_status = _POLYDACTYLY[fields["polydactyly"]]
    colorpoint_status = _COLORPOINT[fields["colorpoint_albino_locus"]]

    thermal = fields["thermal_tolerance"]
    cold_tolerance = (thermal & 0x0F) / 15.0
    heat_tolerance = ((thermal >> 4) & 0x0F) / 15.0

    # Fur expression modifies thermal performance without inventing new colors.
    if fur_length >= 0.75:
        cold_tolerance += 0.15
        heat_tolerance -= 0.15
    elif fur_length <= 0.10:
        cold_tolerance -= 0.20
        heat_tolerance += 0.20
    elif fur_length <= 0.35:
        cold_tolerance -= 0.08
        heat_tolerance += 0.08

    if ear_size >= 0.75:
        heat_tolerance += 0.10
    elif ear_size <= 0.10:
        heat_tolerance -= 0.05

    camouflage = fields["camouflage_profile"]
    forest_camouflage = (camouflage & 0b11) / 3.0
    desert_camouflage = ((camouflage >> 2) & 0b11) / 3.0
    snow_camouflage = ((camouflage >> 4) & 0b11) / 3.0
    wetland_mobility = ((camouflage >> 6) & 0b11) / 3.0

    poly_bonus = {
        "none": 0.0,
        "carrier": 0.02,
        "polydactyl": 0.07,
        "strong polydactyl": 0.10,
    }[polydactyly_status]
    wetland_mobility += poly_bonus

    agility = fields["agility_muscle"] / 255.0
    if tail_type == "long":
        agility += 0.08
    elif tail_type == "normal":
        agility += 0.04
    elif tail_type == "bobtail":
        agility -= 0.08
    else:
        agility -= 0.15
    agility += poly_bonus / 2.0

    sensory_acuity = fields["sensory_acuity"] / 255.0
    if ear_size >= 0.75:
        sensory_acuity += 0.10
    if ear_type == "lynx-tufted":
        sensory_acuity += 0.04

    health_risk_score = fields["health_risk_loci"] / 255.0 * 0.60
    if ear_type == "folded":
        health_risk_score += 0.20
    if colorpoint_status == "albino":
        health_risk_score += 0.10

    return Phenotype(
        coat_color=expressed_coat_color(visible_allele),
        hidden_coat_color=expressed_coat_color(hidden_allele),
        pattern=pattern,
        pattern_intensity=pattern_intensity,
        fur_length=fur_length,
        fur_type=fur_type,
        ear_type=ear_type,
        ear_size=ear_size,
        tail_type=tail_type,
        polydactyly_status=polydactyly_status,
        colorpoint_status=colorpoint_status,
        health_risk_score=health_risk_score,
        cold_tolerance=cold_tolerance,
        heat_tolerance=heat_tolerance,
        forest_camouflage=forest_camouflage,
        desert_camouflage=desert_camouflage,
        snow_camouflage=snow_camouflage,
        wetland_mobility=wetland_mobility,
        agility=agility,
        sensory_acuity=sensory_acuity,
        intelligence=fields["intelligence_cognition"] / 255.0,
        circadian_type=_CIRCADIAN[fields["circadian_tendency"] % len(_CIRCADIAN)],
    )


def _express_abstract_genome(genome: AbstractGenome) -> Phenotype:
    extra_traits: dict[str, float] = {}
    for trait, genes in genome.by_trait().items():
        additive_effect = sum(gene.effect * gene.dominance for gene in genes)
        extra_traits[trait] = clamp((tanh(additive_effect) + 1.0) / 2.0)

    return Phenotype(
        coat_color="black",
        hidden_coat_color="black",
        pattern="solid",
        pattern_intensity=0.0,
        fur_length=0.5,
        fur_type="straight",
        ear_type="normal",
        ear_size=0.5,
        tail_type="normal",
        polydactyly_status="none",
        colorpoint_status="none",
        health_risk_score=0.0,
        cold_tolerance=0.5,
        heat_tolerance=0.5,
        forest_camouflage=0.5,
        desert_camouflage=0.5,
        snow_camouflage=0.5,
        wetland_mobility=0.5,
        agility=0.5,
        sensory_acuity=0.5,
        intelligence=0.5,
        circadian_type="crepuscular",
        extra_traits=extra_traits,
    )
