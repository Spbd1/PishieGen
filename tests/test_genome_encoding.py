from __future__ import annotations

import pytest

from pishiegen.genome.decoder import decode_genome
from pishiegen.genome.encoding import Genome, extract_bits, set_bits
from pishiegen.genome.random_genome import random_genome
from pishiegen.genome.schema import FIELD_ORDER, GENOME_MAX, get_field_spec


def test_valid_128_bit_range() -> None:
    assert Genome(0).raw == 0
    assert Genome(GENOME_MAX).raw == GENOME_MAX

    with pytest.raises(ValueError):
        Genome(-1)
    with pytest.raises(ValueError):
        Genome(2**128)


def test_field_extraction_correctness() -> None:
    raw = 0
    expected: dict[str, int] = {}
    for index, name in enumerate(FIELD_ORDER):
        spec = get_field_spec(name)
        value = min(index + 1, spec.max_value)
        raw = set_bits(raw, spec.start, spec.width, value)
        expected[name] = value

    genome = Genome(raw)

    assert genome.to_dict() == expected
    assert decode_genome(genome) == expected
    assert extract_bits(raw, 96, 16) == expected["mutation_markers"]


def test_setting_a_field_does_not_corrupt_other_fields() -> None:
    original = Genome(GENOME_MAX)
    updated = original.set_field("polydactyly", 0)

    assert updated.get_field("polydactyly") == 0
    for name in FIELD_ORDER:
        if name != "polydactyly":
            assert updated.get_field(name) == original.get_field(name)


def test_random_genome_reproducibility_with_seed() -> None:
    genome_a = random_genome(seed=42)
    genome_b = random_genome(seed=42)
    genome_c = random_genome(seed=43)

    assert 0 <= genome_a.raw < 2**128
    assert genome_a == genome_b
    assert genome_a != genome_c
