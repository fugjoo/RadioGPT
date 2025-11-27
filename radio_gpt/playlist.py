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
    platform: str = "INTERNAL"
    source_id: str | None = None


SONG_LIBRARY: List[Song] = [
    Song(
        "Midnight Drive",
        "Neon Routes",
        timedelta(minutes=3, seconds=20),
        0.72,
        ["synth", "pop"],
        "YOUTUBE",
        "YTv123midnight",
    ),
    Song(
        "Golden Hour",
        "Skyline Birds",
        timedelta(minutes=3, seconds=45),
        0.65,
        ["indie", "feelgood"],
        "SOUNDCLOUD",
        "sc-golden-hour-42",
    ),
    Song(
        "City Pulse",
        "Metrograph",
        timedelta(minutes=4, seconds=5),
        0.81,
        ["electro", "night"],
        "YOUTUBE",
        "YTv-city-pulse-88",
    ),
    Song(
        "Soft Landing",
        "Analog Dreams",
        timedelta(minutes=3, seconds=15),
        0.55,
        ["chill", "ambient"],
        "SOUNDCLOUD",
        "sc-soft-landing-77",
    ),
    Song(
        "Runaway Sun",
        "Vivid Lights",
        timedelta(minutes=3, seconds=50),
        0.79,
        ["pop", "roadtrip"],
        "YOUTUBE",
        "YTv-runaway-sun-03",
    ),
    Song(
        "Echoes",
        "The Lanterns",
        timedelta(minutes=4, seconds=10),
        0.68,
        ["indie", "melodic"],
        "SOUNDCLOUD",
        "sc-echoes-55",
    ),
    Song(
        "All In",
        "Starlit",
        timedelta(minutes=2, seconds=58),
        0.74,
        ["dance", "upbeat"],
        "YOUTUBE",
        "YTv-all-in-19",
    ),
    Song(
        "Satellite",
        "Aurora Lane",
        timedelta(minutes=3, seconds=34),
        0.62,
        ["pop", "warm"],
        "SOUNDCLOUD",
        "sc-satellite-21",
    ),
    Song(
        "Velvet",
        "Honey Circuit",
        timedelta(minutes=3, seconds=11),
        0.71,
        ["soul", "groove"],
        "YOUTUBE",
        "YTv-velvet-65",
    ),
    Song(
        "Slow Burn",
        "Paper Shore",
        timedelta(minutes=3, seconds=56),
        0.59,
        ["indie", "late-night"],
        "SOUNDCLOUD",
        "sc-slow-burn-16",
    ),
    Song(
        "Firefly",
        "Downtown Parade",
        timedelta(minutes=4, seconds=7),
        0.76,
        ["pop", "festival"],
        "YOUTUBE",
        "YTv-firefly-90",
    ),
    Song(
        "Northern Lines",
        "Arctic Forms",
        timedelta(minutes=3, seconds=42),
        0.64,
        ["indie", "guitar"],
        "SOUNDCLOUD",
        "sc-northern-lines-04",
    ),
    Song(
        "Parallel",
        "Nova Drive",
        timedelta(minutes=3, seconds=28),
        0.83,
        ["electro", "club"],
        "YOUTUBE",
        "YTv-parallel-12",
    ),
    Song(
        "Homebound",
        "Polaroid Trees",
        timedelta(minutes=3, seconds=17),
        0.58,
        ["folk", "acoustic"],
        "SOUNDCLOUD",
        "sc-homebound-81",
    ),
    Song(
        "Gravity",
        "Wide Awake",
        timedelta(minutes=3, seconds=47),
        0.77,
        ["pop", "anthem"],
        "YOUTUBE",
        "YTv-gravity-71",
    ),
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
