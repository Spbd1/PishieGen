"""Plain-text summaries for reproducible command-line workflows."""

from __future__ import annotations

from pishiegen.simulation import SimulationResult


def summarize_fitness(result: SimulationResult) -> str:
    """Return a compact multi-line fitness summary."""

    lines = [f"biome={result.biome.name}", f"generations={result.generations}"]
    for index, mean in enumerate(result.mean_fitness_by_generation, start=1):
        lines.append(f"generation {index}: mean_fitness={mean:.6f}")
    lines.append(f"final_population={len(result.population)}")
    return "\n".join(lines)
