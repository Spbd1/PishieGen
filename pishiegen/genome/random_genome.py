"""Random generator for compact 128-bit PishieGen genomes.

The generator creates a single Python integer spanning bits 0 through 127. It is
seedable for reproducible simulations and tests. The resulting values are a
computational genotype, not a literal biological sequence.
"""

from __future__ import annotations

import random
import sys
from types import ModuleType
from typing import Any

from pishiegen.genome.encoding import Genome
from pishiegen.genome.operators import random_genome as _legacy_random_genome
from pishiegen.genome.schema import GENOME_BITS


def random_genome(seed: int | str | bytes | bytearray | None = None) -> Genome:
    """Return a random 128-bit ``Genome`` with optional deterministic seeding.

    Passing the same ``seed`` produces the same raw integer. Omitting ``seed``
    uses Python's default entropy source for non-deterministic initialization.
    The returned genome's raw value covers bits 0 through 127.
    """

    rng = random.Random(seed)
    return Genome(rng.getrandbits(GENOME_BITS))


class _CallableRandomGenomeModule(ModuleType):
    """Keep ``from pishiegen.genome import random_genome`` callable.

    Python binds imported submodules onto their parent package. Because this
    module intentionally has the same name as the legacy package-level helper,
    making the module callable preserves older call sites that generate the
    existing gene-list genome representation.
    """

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        if args and isinstance(args[0], random.Random):
            return _legacy_random_genome(*args, **kwargs)
        if "gene_count" in kwargs or (len(args) >= 2 and isinstance(args[1], int)):
            return _legacy_random_genome(*args, **kwargs)
        return random_genome(*args, **kwargs)


sys.modules[__name__].__class__ = _CallableRandomGenomeModule
