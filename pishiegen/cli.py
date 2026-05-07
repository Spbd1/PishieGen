"""Command-line interface for PishieGen."""

from __future__ import annotations

import argparse
import json
import random

from pishiegen.environment import Biome
from pishiegen.experiments import create_seed_population, temperate_biome
from pishiegen.fitness import score_fitness
from pishiegen.genome import Genome, breed, random_genome
from pishiegen.phenotype import express_genome
from pishiegen.simulation import Organism, Simulation
from pishiegen.visualization import summarize_fitness


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="pishiegen", description="PishieGen artificial-life CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    generate = subparsers.add_parser("generate-organism", help="Generate a compact random genome")
    generate.add_argument("--seed", type=int, default=1)
    generate.add_argument("--genes", type=int, default=8)

    decode = subparsers.add_parser("decode-genome", help="Decode a genome code into phenotype traits")
    decode.add_argument("code")

    breed_parser = subparsers.add_parser("breed", help="Breed two compact genome codes")
    breed_parser.add_argument("parent_a")
    breed_parser.add_argument("parent_b")
    breed_parser.add_argument("--seed", type=int, default=1)
    breed_parser.add_argument("--mutation-rate", type=float, default=0.01)

    simulate = subparsers.add_parser("simulate-biome", help="Run a small biome simulation")
    simulate.add_argument("--seed", type=int, default=1)
    simulate.add_argument("--population", type=int, default=20)
    simulate.add_argument("--generations", type=int, default=5)
    simulate.add_argument("--biome", default="temperate_baseline")

    return parser


def _biome_from_name(name: str) -> Biome:
    if name == "temperate_baseline":
        return temperate_biome()
    raise ValueError(f"Unknown biome preset: {name}")


def main(argv: list[str] | None = None) -> int:
    """Run the command-line interface."""

    parser = _build_parser()
    args = parser.parse_args(argv)

    if args.command == "generate-organism":
        genome = random_genome(random.Random(args.seed), gene_count=args.genes)
        organism = Organism.from_genome(genome)
        fitness = score_fitness(organism.phenotype, temperate_biome())
        print(json.dumps({"genome": genome.compact_code(), "phenotype": organism.phenotype.traits, "baseline_fitness": fitness.score}, sort_keys=True))
        return 0

    if args.command == "decode-genome":
        phenotype = express_genome(Genome.parse(args.code))
        print(json.dumps(phenotype.traits, sort_keys=True))
        return 0

    if args.command == "breed":
        child = breed(
            Genome.parse(args.parent_a),
            Genome.parse(args.parent_b),
            random.Random(args.seed),
            mutation_rate=args.mutation_rate,
        )
        print(child.compact_code())
        return 0

    if args.command == "simulate-biome":
        biome = _biome_from_name(args.biome)
        population = create_seed_population(args.population, args.seed)
        result = Simulation(biome=biome, rng=random.Random(args.seed)).run(population, args.generations)
        print(summarize_fitness(result))
        return 0

    parser.error("Unhandled command")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
