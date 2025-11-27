from __future__ import annotations

import itertools
import random
from dataclasses import dataclass
from datetime import timedelta
from typing import Iterable, List, Optional


@dataclass
class Song:
    title: str
    artist: str
    duration: timedelta
    energy: float
    tags: List[str]


SONG_LIBRARY: List[Song] = [
    Song("Midnight Drive", "Neon Routes", timedelta(minutes=3, seconds=20), 0.72, ["synth", "pop"]),
    Song("Golden Hour", "Skyline Birds", timedelta(minutes=3, seconds=45), 0.65, ["indie", "feelgood"]),
    Song("City Pulse", "Metrograph", timedelta(minutes=4, seconds=5), 0.81, ["electro", "night"]),
    Song("Soft Landing", "Analog Dreams", timedelta(minutes=3, seconds=15), 0.55, ["chill", "ambient"]),
    Song("Runaway Sun", "Vivid Lights", timedelta(minutes=3, seconds=50), 0.79, ["pop", "roadtrip"]),
    Song("Echoes", "The Lanterns", timedelta(minutes=4, seconds=10), 0.68, ["indie", "melodic"]),
    Song("All In", "Starlit", timedelta(minutes=2, seconds=58), 0.74, ["dance", "upbeat"]),
    Song("Satellite", "Aurora Lane", timedelta(minutes=3, seconds=34), 0.62, ["pop", "warm"]),
    Song("Velvet", "Honey Circuit", timedelta(minutes=3, seconds=11), 0.71, ["soul", "groove"]),
    Song("Slow Burn", "Paper Shore", timedelta(minutes=3, seconds=56), 0.59, ["indie", "late-night"]),
    Song("Firefly", "Downtown Parade", timedelta(minutes=4, seconds=7), 0.76, ["pop", "festival"]),
    Song("Northern Lines", "Arctic Forms", timedelta(minutes=3, seconds=42), 0.64, ["indie", "guitar"]),
    Song("Parallel", "Nova Drive", timedelta(minutes=3, seconds=28), 0.83, ["electro", "club"]),
    Song("Homebound", "Polaroid Trees", timedelta(minutes=3, seconds=17), 0.58, ["folk", "acoustic"]),
    Song("Gravity", "Wide Awake", timedelta(minutes=3, seconds=47), 0.77, ["pop", "anthem"]),
]


class PlaylistPlanner:
    """Plans songs for the show and keeps a rotation going."""

    def __init__(self, *, seed: Optional[int] = None) -> None:
        self.random = random.Random(seed)
        self._rotation = itertools.cycle(self._shuffled_library())

    def _shuffled_library(self) -> List[Song]:
        songs = SONG_LIBRARY.copy()
        self.random.shuffle(songs)
        return songs

    def next_song(self) -> Song:
        return next(self._rotation)

    def pick_energy_song(self, *, min_energy: float) -> Song:
        candidates = [song for song in SONG_LIBRARY if song.energy >= min_energy]
        if not candidates:
            return self.next_song()
        return self.random.choice(candidates)

    def search(self, tag: str) -> Iterable[Song]:
        lowered = tag.lower()
        return [song for song in SONG_LIBRARY if lowered in (t.lower() for t in song.tags)]
