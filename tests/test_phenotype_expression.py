from __future__ import annotations

import pytest

from pishiegen.genome.encoding import Genome
from pishiegen.phenotype import PHENOTYPE_FIELDS, express_genome


NUMERIC_PHENOTYPE_FIELDS = (
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


def compact_genome(**fields: int) -> Genome:
    genome = Genome(0)
    for name, value in fields.items():
        genome = genome.set_field(name, value)
    return genome


def test_known_compact_genome_expresses_expected_structured_phenotype() -> None:
    genome = compact_genome(
        base_coat_color=8,
        hidden_coat_color=2,
        agouti_tabby_pattern=0b1010,
        pattern_intensity=12,
        fur_length_type=0b0011,
        ear_morphology=0b1101,
        tail_morphology=1,
        polydactyly=2,
        colorpoint_albino_locus=2,
        health_risk_loci=0,
        thermal_tolerance=0x69,
        camouflage_profile=0b0010_0111,
        agility_muscle=128,
        sensory_acuity=128,
        intelligence_cognition=204,
        circadian_tendency=2,
    )

    phenotype = express_genome(genome)

    assert phenotype.coat_color == "blue"
    assert phenotype.hidden_coat_color == "cinnamon"
    assert phenotype.pattern == "spotted tabby"
    assert phenotype.pattern_intensity == pytest.approx(0.8)
    assert phenotype.fur_length == 1.0
    assert phenotype.fur_type == "straight"
    assert phenotype.ear_type == "folded"
    assert phenotype.ear_size == 1.0
    assert phenotype.tail_type == "long"
    assert phenotype.polydactyly_status == "polydactyl"
    assert phenotype.colorpoint_status == "colorpoint"
    assert phenotype.health_risk_score == pytest.approx(0.2)
    assert phenotype.cold_tolerance == pytest.approx(0.75)
    assert phenotype.heat_tolerance == pytest.approx(0.35)
    assert phenotype.forest_camouflage == 1.0
    assert phenotype.desert_camouflage == pytest.approx(1 / 3)
    assert phenotype.snow_camouflage == pytest.approx(2 / 3)
    assert phenotype.wetland_mobility == pytest.approx(0.07)
    assert phenotype.agility == pytest.approx(128 / 255 + 0.08 + 0.035)
    assert phenotype.sensory_acuity == pytest.approx(128 / 255 + 0.10)
    assert phenotype.intelligence == pytest.approx(0.8)
    assert phenotype.circadian_type == "crepuscular"


def test_non_agouti_suppresses_visible_tabby_pattern() -> None:
    genome = compact_genome(agouti_tabby_pattern=0b0010, pattern_intensity=15)

    phenotype = express_genome(genome)

    assert phenotype.pattern == "solid"
    assert phenotype.pattern_intensity == 0.0


def test_polydactyly_improves_wetland_mobility_without_default_health_penalty() -> None:
    normal = express_genome(compact_genome(polydactyly=0))
    polydactyl = express_genome(compact_genome(polydactyly=2))

    assert polydactyl.wetland_mobility > normal.wetland_mobility
    assert polydactyl.health_risk_score == normal.health_risk_score


def test_phenotype_contains_required_fields() -> None:
    phenotype = express_genome(Genome(0))

    assert tuple(phenotype.traits) == PHENOTYPE_FIELDS


def test_all_normalized_phenotype_scores_are_clamped_to_zero_one() -> None:
    for raw in (0, 2**128 - 1):
        phenotype = express_genome(Genome(raw))
        for field in NUMERIC_PHENOTYPE_FIELDS:
            value = getattr(phenotype, field)
            assert 0.0 <= value <= 1.0, field
