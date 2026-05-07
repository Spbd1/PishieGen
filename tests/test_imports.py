from __future__ import annotations


def test_public_imports() -> None:
    import pishiegen

    assert pishiegen.Genome
    assert pishiegen.Phenotype
    assert pishiegen.Simulation
