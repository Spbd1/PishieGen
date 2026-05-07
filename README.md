# PishieGen

PishieGen is a research-oriented Python package for biomimetic artificial-life experiments. It models digital organisms with compact genomes, genotype-to-phenotype expression, inheritance with mutation, biome-specific fitness scoring, and small agent-based ecological simulations.

The project is intentionally minimal. It is designed as computational biology / artificial-life software rather than entertainment software, and it avoids claims that the default models are empirically validated. Default equations are transparent baselines for reproducible experiments.

## Core concepts

### Biomimetic artificial-life simulator

PishieGen represents each organism as an agent with a heritable genome and an expressed phenotype. A simulation evaluates organisms in a biome and samples future generations using fitness-weighted reproduction. This follows broad artificial-life and evolutionary-computation principles while remaining conservative about biological interpretation.

TODO: Add literature review notes that connect each default model component to established artificial-life and agent-based modeling references.

### Genotype-phenotype mapping

A `Genome` is a compact tuple of `Gene` records. Each gene has a locus, trait name, bounded effect, and dominance-like weight. Expression groups genes by trait, sums weighted effects, and bounds each trait with a smooth transform for numerical stability.

TODO: Validate the expression rule against explicit benchmark tasks before using it as a scientific model of trait development.

### Inheritance and mutation

The `breed` operator performs simple locus-wise recombination between two parent genomes and applies small Gaussian mutations to gene effects. This is a deliberately abstract model of heritable variation, not a mechanistic representation of any specific biological reproductive system.

TODO: Add configurable mutation distributions and document when each distribution is appropriate for a given experiment.

### Biome-specific adaptation

A `Biome` defines resource level, carrying capacity, target trait values, and stressors. Fitness scoring rewards phenotype values near biome targets and penalizes insufficient stress resistance. These functions are transparent defaults intended for controlled computational experiments.

TODO: Calibrate biome fitness functions against preregistered hypotheses or domain-specific validation data.

### Reproducible simulation experiments

Experiments can use explicit random seeds for genome generation and simulation sampling. The `experiments` package includes a small temperate baseline biome and a reproducible seed-population helper.

## Installation

```bash
python -m pip install -e .
```

For development tests:

```bash
python -m pip install -e '.[dev]'
pytest
```

## CLI

PishieGen installs a `pishiegen` command with four minimal subcommands:

```bash
pishiegen generate-organism --seed 7 --genes 8
pishiegen decode-genome '<compact-genome-code>'
pishiegen breed '<parent-a-code>' '<parent-b-code>' --seed 11 --mutation-rate 0.02
pishiegen simulate-biome --seed 3 --population 20 --generations 5
```

The same CLI can be invoked without installation:

```bash
python -m pishiegen.cli simulate-biome --seed 3 --population 20 --generations 5
```

## Package layout

```text
pishiegen/
  genome/         Genome representation, random generation, inheritance, mutation
  phenotype/      Genotype-to-phenotype expression
  environment/    Biome definitions
  fitness/        Biome-specific fitness scoring
  simulation/     Agent-based population simulation
  experiments/    Reproducible presets and helpers
  visualization/  Early text summaries, no UI
examples/         Runnable minimal examples
docs/             Scientific assumptions and validation notes
tests/            Unit tests and placeholders
```

## Current scope

Implemented:

- Dataclass-based genome, phenotype, biome, fitness, organism, and simulation records.
- Reproducible random genome generation and seed-population helpers.
- Minimal CLI for organism generation, genome decoding, breeding, and biome simulation.
- Unit test smoke coverage for imports, CLI commands, inheritance, expression, and simulation.

Remaining work:

- Add empirical validation notes and literature citations for every model assumption.
- Add experiment configuration files and reproducibility metadata exports.
- Add richer ecological interactions only when tied to testable hypotheses.
- Add visual analysis utilities after core scientific APIs stabilize.
- Keep storage and user-interface concerns out of the first research core.
