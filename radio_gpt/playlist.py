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

    @property
    def playback_url(self) -> Optional[str]:
        if not self.source_id:
            return None
        if self.platform.upper() == "YOUTUBE":
            return f"https://www.youtube.com/watch?v={self.source_id}"
        if self.platform.upper() == "SOUNDCLOUD":
            return f"https://soundcloud.com/{self.source_id}"
        return None


SONG_LIBRARY: List[Song] = [
    Song(
        "Candyland",
        "Tobu",
        timedelta(minutes=3, seconds=16),
        0.82,
        ["electro", "feelgood", "ncs"],
        "YOUTUBE",
        "IIrCDAV3EgI",
    ),
    Song(
        "Sky High",
        "Elektronomia",
        timedelta(minutes=3, seconds=56),
        0.8,
        ["dance", "anthem", "ncs"],
        "YOUTUBE",
        "TW9d8vYrVFQ",
    ),
    Song(
        "Blank",
        "Disfigure",
        timedelta(minutes=3, seconds=28),
        0.78,
        ["bass", "gaming", "ncs"],
        "YOUTUBE",
        "p7ZsBPK656s",
    ),
    Song(
        "Firefly",
        "Jim Yosef",
        timedelta(minutes=3, seconds=18),
        0.77,
        ["melodic", "electronic", "uplifting"],
        "YOUTUBE",
        "x_OwcYTNbHs",
    ),
    Song(
        "Chill Day",
        "LAKEY INSPIRED",
        timedelta(minutes=3, seconds=21),
        0.6,
        ["chillhop", "lofi", "afternoon"],
        "YOUTUBE",
        "3HjG1Y4QpVA",
    ),
    Song(
        "Sunny",
        "Ikson",
        timedelta(minutes=2, seconds=20),
        0.58,
        ["acoustic", "feelgood", "soundcloud"],
        "SOUNDCLOUD",
        "ikson/sunny-free-download",
    ),
    Song(
        "Dreams",
        "Joakim Karud",
        timedelta(minutes=2, seconds=30),
        0.63,
        ["jazzhop", "instrumental", "soundcloud"],
        "SOUNDCLOUD",
        "joakimkarud/dreams-1",
    ),
    Song(
        "Be With You",
        "Dyalla",
        timedelta(minutes=3, seconds=20),
        0.67,
        ["chill", "electronic", "vocals"],
        "SOUNDCLOUD",
        "dyalla/be-with-you",
    ),
    Song(
        "Desire",
        "Markvard",
        timedelta(minutes=3, seconds=14),
        0.7,
        ["tropical", "guitar", "summer"],
        "YOUTUBE",
        "A2AydJcUKR0",
    ),
    Song(
        "Feel Good",
        "Syn Cole",
        timedelta(minutes=3, seconds=31),
        0.85,
        ["festival", "house", "ncs"],
        "YOUTUBE",
        "q1ULJ92aldE",
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
