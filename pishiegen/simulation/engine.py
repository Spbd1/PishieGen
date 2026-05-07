"""Minimal agent-based simulation engine."""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from uuid import uuid4

from pishiegen.environment import Biome
from pishiegen.fitness import FitnessResult, score_fitness
from pishiegen.genome import Genome, breed
from pishiegen.phenotype import Phenotype, express_genome


@dataclass(frozen=True, slots=True)
class Organism:
    """Digital organism with heritable genome and expressed phenotype."""

    organism_id: str
    genome: Genome
    phenotype: Phenotype

    @classmethod
    def from_genome(cls, genome: Genome, organism_id: str | None = None) -> "Organism":
        """Construct an organism by expressing its genome."""

        return cls(organism_id or str(uuid4()), genome, express_genome(genome))


@dataclass(frozen=True, slots=True)
class SimulationResult:
    """Summary of a simulation run."""

    biome: Biome
    generations: int
    population: tuple[Organism, ...]
    mean_fitness_by_generation: tuple[float, ...]


@dataclass(slots=True)
class Simulation:
    """Small stochastic population simulation for reproducible experiments."""

    biome: Biome
    rng: random.Random = field(default_factory=random.Random)
    mutation_rate: float = 0.01

    def evaluate(self, organism: Organism) -> FitnessResult:
        """Evaluate a single organism in this simulation's biome."""

        return score_fitness(organism.phenotype, self.biome)

    def step(self, population: tuple[Organism, ...]) -> tuple[tuple[Organism, ...], float]:
        """Advance the population by one generation using fitness-weighted sampling."""

        if not population:
            return (), 0.0
        scored = [(organism, self.evaluate(organism).score) for organism in population]
        mean_fitness = sum(score for _, score in scored) / len(scored)
        weights = [max(score, 1e-9) for _, score in scored]
        target_size = min(len(population), self.biome.normalized().carrying_capacity)
        next_population: list[Organism] = []
        for _ in range(target_size):
            parent_a, parent_b = self.rng.choices(population, weights=weights, k=2)
            child_genome = breed(
                parent_a.genome,
                parent_b.genome,
                self.rng,
                mutation_rate=self.mutation_rate,
                offspring_parent_ids=(parent_a.organism_id, parent_b.organism_id),
            )
            next_population.append(Organism.from_genome(child_genome))
        return tuple(next_population), mean_fitness

    def run(self, population: tuple[Organism, ...], generations: int) -> SimulationResult:
        """Run a fixed-length simulation and return a compact summary."""

        mean_fitness: list[float] = []
        current = population
        for _ in range(max(0, generations)):
            current, generation_mean = self.step(current)
            mean_fitness.append(generation_mean)
        return SimulationResult(
            biome=self.biome,
            generations=max(0, generations),
            population=current,
            mean_fitness_by_generation=tuple(mean_fitness),
        )
