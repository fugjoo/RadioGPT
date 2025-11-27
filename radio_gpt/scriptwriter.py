from __future__ import annotations

import random
from typing import Iterable, List, Optional

from .news import NewsItem
from .playlist import Song


class ScriptWriter:
    """Creates natural-sounding moderation lines and text blocks."""

    def __init__(self, *, station: str, host: str, seed: Optional[int] = None) -> None:
        self.station = station
        self.host = host
        self.random = random.Random(seed)

    def build_intro(self) -> str:
        greetings = [
            "Guten Abend und willkommen zu einer neuen Ausgabe RadioGPT!",
            "Schön, dass ihr eingeschaltet habt — hier ist RadioGPT!",
            "Hallo zusammen, hier ist RadioGPT mit frischen Vibes für euren Tag!",
        ]
        promise = self.random.choice(
            [
                "Wir liefern euch die besten neuen Tracks, dazu schnelle News und lokale Tipps.",
                "Euch erwartet eine Stunde voller Energie, entspannter Stimmen und smarter Stories.",
                "Wir bringen euch durch die Stunde mit neuen Releases, Updates und guten Geschichten.",
            ]
        )
        return f"{self.random.choice(greetings)} Ich bin {self.host}. {promise}"

    def build_music_intro(self, song: Song) -> str:
        hooks = [
            f"Gleich hört ihr {song.artist} mit '{song.title}', perfekt für euren Moment gerade.",
            f"{song.title} von {song.artist} passt großartig in die Stimmung — viel Spaß!",
            f"Noch ein Highlight in unserer Rotation: {song.artist} und '{song.title}'.",
        ]
        vibe = self._describe_vibe(song)
        platform = self._platform_hint(song)
        fact = self.random.choice(
            [
                "Der Track trendet gerade auf mehreren Indie-Playlists.",
                "Das Stück wurde komplett analog produziert.",
                "Viele von euch feiern den Sound bereits im Netz.",
            ]
        )
        return " ".join(filter(None, [self.random.choice(hooks), vibe, fact, platform]))

    def build_song_backannounce(self, song: Song) -> str:
        closer = self.random.choice(
            [
                "Ihr habt es bei uns zuerst gehört.",
                "Perfekt, um weiter in den Abend zu starten.",
                "So klingt der Soundtrack zu eurem Wochenende.",
            ]
        )
        platform = self._platform_hint(song)
        return " ".join(filter(None, [f"{song.artist} mit '{song.title}'.", closer, platform]))

    def build_news_bulletin(self, news: Iterable[NewsItem]) -> str:
        lines: List[str] = ["Kurz und knackig — hier sind die aktuellen Themen:"]
        for item in news:
            lines.append(f"• {item.headline}: {item.summary}")
        lines.append("Mehr Updates jederzeit auf radiogpt.fm.")
        return " ".join(lines)

    def build_outro(self) -> str:
        thanks = self.random.choice(
            [
                "Danke fürs Einschalten!",
                "Das war's für diese Stunde — schön, dass ihr dabei wart.",
                "Wir hören uns in der nächsten Stunde wieder.",
            ]
        )
        cta = self.random.choice(
            [
                "Checkt die Playlist in der App, falls ihr etwas verpasst habt.",
                "Folgt uns auf Social für Bonusinhalte hinter den Kulissen.",
                "Schickt uns eure Musikwünsche per Sprachmessage — wir hören rein.",
            ]
        )
        return f"{thanks} {cta}"

    def _describe_vibe(self, song: Song) -> str:
        if not song.tags:
            return ""
        samples = self.random.sample(song.tags, k=min(2, len(song.tags)))
        if len(samples) == 1:
            return f"Klingt nach {samples[0]}-Vibes."
        return f"Mix aus {samples[0]} und {samples[1]} — passt perfekt."

    def _platform_hint(self, song: Song) -> str:
        if not song.source_id:
            return ""
        if song.platform.upper() == "YOUTUBE":
            return f"Falls ihr den Clip sehen wollt: {song.playback_url}."
        if song.platform.upper() == "SOUNDCLOUD":
            return f"Gibt's auch bei SoundCloud: {song.playback_url}."
        return ""
