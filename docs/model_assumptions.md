# Model assumptions and validation TODOs

PishieGen begins with transparent, intentionally simple assumptions so that each component can be tested independently.

## Genome

Genes are abstract heritable records with a locus, trait label, effect size, and dominance-like weight. This is a computational representation of heritable variation, not a molecular model.

TODO: Review artificial-life and quantitative-genetics literature before selecting default effect-size distributions for publication-quality experiments.

## Phenotype expression

The first expression model uses additive weighted gene effects and a bounded nonlinear transform. The transform prevents unstable trait magnitudes in small simulations.

TODO: Compare additive expression with alternative regulatory-network models and document tradeoffs.

## Fitness

The first fitness model scores trait-environment distance and stressor response. This is a selection-landscape abstraction.

TODO: Define validation datasets or benchmark landscapes for each planned biome.

## Simulation

The first simulation uses fitness-weighted sampling with fixed population size bounded by carrying capacity.

TODO: Evaluate demographic stochasticity, density dependence, and multi-species interactions before interpreting dynamics as ecological claims.
