from __future__ import annotations

import itertools
import random
from dataclasses import dataclass
from datetime import timedelta
from typing import List, Optional


@dataclass
class Jingle:
    name: str
    slogan: str
    duration: timedelta


JINGLE_LIBRARY: List[Jingle] = [
    Jingle("RadioGPT Sonic Pulse", "Immer einen Beat voraus.", timedelta(seconds=12)),
    Jingle("News Flash", "Die wichtigsten Stories in 180 Sekunden.", timedelta(seconds=9)),
    Jingle("Community Corner", "Deine Stadt. Deine Story. Auf RadioGPT.", timedelta(seconds=14)),
    Jingle("Top Of The Hour", "RadioGPT — Ideen auf Empfang.", timedelta(seconds=10)),
    Jingle("Night Flow", "Mehr Atmosphäre, mehr Musik, mehr du.", timedelta(seconds=13)),
]


class JingleVault:
    """Cycles through jingles so the show sounds produced."""

    def __init__(self, *, seed: Optional[int] = None) -> None:
        self.random = random.Random(seed)
        self._cycle = itertools.cycle(self._shuffled())

    def _shuffled(self) -> List[Jingle]:
        jingles = JINGLE_LIBRARY.copy()
        self.random.shuffle(jingles)
        return jingles

    def next_jingle(self) -> Jingle:
        return next(self._cycle)
