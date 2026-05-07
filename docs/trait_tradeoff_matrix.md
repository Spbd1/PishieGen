# Trait trade-off matrix

This matrix documents PishieGen's formal trait trade-off assumptions. These are **simulation assumptions inspired by biology**, not direct veterinary claims, diagnostic guidance, or measured ecological effect sizes. The weights in `pishiegen.fitness.tradeoffs` are intentionally small, transparent modeling defaults that should be calibrated before publication-quality biological interpretation.

## Modeling rules

- No major trait is treated as universally good: every listed trait has at least one modeled benefit and at least one modeled cost.
- Effects are context-dependent. A trait that helps in snow, forest, heat, hunting, or climbing can be costly in another biome or life-history context.
- Fantasy explanations are intentionally excluded. Rationales use conservative heat exchange, camouflage, movement, sensory, health-risk, or energy-budget assumptions.
- `confidence_level` separates evidence-grounded assumptions from more speculative simulation choices:
  - `high`: broad biological or health-risk reasoning is relatively direct.
  - `moderate`: plausible ecological trade-off, but exact magnitude is model-specific.
  - `speculative`: useful for simulation diversity, but especially in need of calibration.

## Matrix

| Trait | Potential advantages | Potential disadvantages | Main contexts | Confidence | Rationale summary |
| --- | --- | --- | --- | --- | --- |
| Thick/long fur | Cold tolerance; snow biome survival | Heat stress in desert; stamina penalty in hot climates | Cold, snow, desert, hot climate | High | Insulation helps retain heat in cold settings but impedes heat shedding in hot open environments. |
| Short/hairless coat | Heat dissipation; lower heat stress | Cold vulnerability; lower snow survival | Hot climate, desert, cold, snow | High | Sparse covering supports heat loss but provides less insulation against cold exposure. |
| Dark coat | Night camouflage; dense forest concealment | Heat absorption in open hot biomes; visibility on snow | Night, dense forest, open hot biomes, snow | Moderate | Dark coloration can blend with shadowed backgrounds but may absorb more solar radiation and contrast with snow. |
| Light/white coat | Snow camouflage; lower heat absorption in open sun | Poor forest/night camouflage unless snow or moonlight context applies | Snow, open sun, forest, night | Moderate | Light coloration can match snow and reflect sunlight, while standing out in darker habitats. |
| Tabby/disruptive pattern | Forest/grassland camouflage; outline disruption | Less effective in uniform snow/desert backgrounds | Forest, grassland, snow, desert | Moderate | Patterning can break outlines in textured vegetation but may be conspicuous on uniform backgrounds. |
| Large ears | Heat dissipation; prey detection | Cold exposure penalty; potential injury exposure in dense terrain | Hot climate, hunting, cold, dense terrain | Moderate | Larger ears increase heat-exchange and sound-collection surface area, but expose more tissue. |
| Folded ears | Aesthetic only or negligible ecological advantage | Health-risk penalty; reduced sensory efficiency | Health, sensory, human preference | High | Folded ears are modeled as ecologically negligible except for possible human preference, with health and sensory costs. |
| Long tail | Balance; climbing; sharp turns | Minor injury/exposure risk in dense terrain | Climbing, pursuit, escape, dense terrain | Moderate | Tail length can help body control but creates a small snagging or injury exposure cost. |
| Tailless/bobtail | Lower tail injury risk | Balance/agility penalty | Dense terrain, climbing, pursuit, escape | Moderate | Less tail tissue can reduce injury exposure, while reduced tail leverage can affect balance. |
| Polydactyly | Grip; climbing; mud/wetland stability | Small locomotion cost or neutral effect | Climbing, wetland, mud, general locomotion | Speculative | Extra toes may improve contact with some substrates, but the net effect may be neutral or slightly costly. |
| High intelligence | Flexible behavior; better biome/time choice; reduced failed hunts | Metabolic cost; slower maturation or higher energy demand | Foraging, hunting, migration, development | Speculative | Behavioral flexibility helps in variable environments but is modeled as energetically and developmentally costly. |
| High agility | Hunting success; escape success | Energy demand; lower endurance if not paired with stamina | Hunting, escape, energy budget, endurance | Moderate | Maneuverability improves short-term pursuits and escapes, but costs energy and may not imply endurance. |

## Implementation link

The canonical machine-readable matrix lives in `pishiegen/fitness/tradeoffs.py`. Tests in `tests/test_trait_tradeoffs.py` audit the registry so that future additions fail if they are one-sided.
