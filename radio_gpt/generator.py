from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
import re
from typing import List, Optional

from .jingles import Jingle, JingleVault
from .news import NewsItem, Newsroom
from .playlist import PlaylistPlanner, Song
from .scriptwriter import ScriptWriter


@dataclass
class ShowSegment:
    """Represents a scheduled element in the show timeline."""

    kind: str
    title: str
    description: str
    start: datetime
    duration: timedelta
    payload: Optional[dict] = None

    def as_dict(self) -> dict:
        return {
            "kind": self.kind,
            "title": self.title,
            "description": self.description,
            "start": self.start.isoformat(),
            "duration_seconds": int(self.duration.total_seconds()),
            "payload": self.payload or {},
        }


@dataclass
class RadioShow:
    """Container for a generated show."""

    station: str
    host: str
    start: datetime
    segments: List[ShowSegment]

    @property
    def duration(self) -> timedelta:
        if not self.segments:
            return timedelta()
        last = self.segments[-1]
        return (last.start + last.duration) - self.start

    def as_dict(self) -> dict:
        return {
            "station": self.station,
            "host": self.host,
            "start": self.start.isoformat(),
            "duration_seconds": int(self.duration.total_seconds()),
            "segments": [segment.as_dict() for segment in self.segments],
        }

    def as_timeline(self) -> dict:
        return {
            "station": self.station,
            "host": self.host,
            "server_time": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
            "items": [
                {
                    "start_utc": segment.start.isoformat(),
                    "type": segment.kind.upper(),
                    "payload": segment.payload or {},
                    "duration_seconds": int(segment.duration.total_seconds()),
                }
                for segment in self.segments
            ],
        }

    def render_text(self) -> str:
        lines = [
            f"{self.station} mit {self.host} — Sendestart: {self.start:%Y-%m-%d %H:%M}",
            f"Gesamtlänge: {int(self.duration.total_seconds()//60)} Minuten",
            "",
        ]
        for segment in self.segments:
            timestamp = segment.start.strftime("%H:%M:%S")
            minutes = int(segment.duration.total_seconds() // 60)
            seconds = int(segment.duration.total_seconds() % 60)
            lines.append(
                f"[{timestamp}] ({minutes:02d}:{seconds:02d}) {segment.kind.upper()}: {segment.title} — {segment.description}"
            )
        return "\n".join(lines)


class ShowGenerator:
    """High-level orchestrator that assembles a complete radio show."""

    def __init__(
        self,
        *,
        station: str = "RadioGPT",
        host: str = "Alex",
        seed: Optional[int] = None,
    ) -> None:
        self.station = station
        self.host = host
        self.seed = seed
        self._playlist = PlaylistPlanner(seed=seed)
        self._jingles = JingleVault(seed=seed)
        self._newsroom = Newsroom()
        self._writer = ScriptWriter(station=station, host=host, seed=seed)
        self._cdn_base = "https://cdn.radio.gpt"

    def build_show(
        self,
        *,
        duration_minutes: int = 60,
        start: Optional[datetime] = None,
        include_weather: bool = True,
        include_local: bool = True,
    ) -> RadioShow:
        if duration_minutes <= 0:
            raise ValueError("duration_minutes must be positive")

        show_start = start or datetime.now(timezone.utc).replace(microsecond=0)
        segments: List[ShowSegment] = []

        current_time = show_start
        target_duration = timedelta(minutes=duration_minutes)

        # 1. Intro
        intro_text = self._writer.build_intro()
        intro_duration = timedelta(seconds=50)
        segments.append(
            ShowSegment(
                kind="tts_break",
                title="Show-Opener",
                description=intro_text,
                start=current_time,
                duration=intro_duration,
                payload=self._tts_payload("show-opener", intro_duration),
            )
        )
        current_time += intro_duration

        # 2. First song
        first_song = self._playlist.pick_energy_song(min_energy=0.7)
        segments.append(self._song_segment(first_song, current_time))
        current_time += first_song.duration

        # 3. First jingle
        first_jingle = self._jingles.next_jingle()
        segments.append(self._jingle_segment(first_jingle, current_time))
        current_time += first_jingle.duration

        # 4. News bulletin early on
        news_items = self._newsroom.compose_news(include_weather=include_weather, include_local=include_local)
        news_text = self._writer.build_news_bulletin(news_items)
        news_duration = timedelta(seconds=180)
        segments.append(
            ShowSegment(
                kind="tts_break",
                title="Nachrichten",
                description=news_text,
                start=current_time,
                duration=news_duration,
                payload=self._tts_payload("news-bulletin", news_duration),
            )
        )
        current_time += news_duration

        # 5. Core rotation of music + moderation + jingles
        while current_time - show_start < target_duration - timedelta(minutes=5):
            song = self._playlist.next_song()
            segments.append(self._song_segment(song, current_time))
            current_time += song.duration

            if current_time - show_start >= target_duration:
                break

            talk = self._writer.build_music_intro(song)
            talk_duration = timedelta(seconds=65)
            segments.append(
                ShowSegment(
                    kind="tts_break",
                    title=f"Moderation zu {song.title}",
                    description=talk,
                    start=current_time,
                    duration=talk_duration,
                    payload=self._tts_payload(f"moderation-{self._slug(song.title)}", talk_duration),
                )
            )
            current_time += talk_duration

            if current_time - show_start >= target_duration:
                break

            jingle = self._jingles.next_jingle()
            segments.append(self._jingle_segment(jingle, current_time))
            current_time += jingle.duration

        # 6. Closing talk and outro music
        outro_text = self._writer.build_outro()
        outro_duration = timedelta(seconds=70)
        segments.append(
            ShowSegment(
                kind="tts_break",
                title="Abmoderation",
                description=outro_text,
                start=current_time,
                duration=outro_duration,
                payload=self._tts_payload("outro", outro_duration),
            )
        )
        current_time += outro_duration

        closing_song = self._playlist.pick_energy_song(min_energy=0.5)
        segments.append(self._song_segment(closing_song, current_time))

        return RadioShow(
            station=self.station,
            host=self.host,
            start=show_start,
            segments=segments,
        )

    def _song_segment(self, song: Song, start: datetime) -> ShowSegment:
        event_type = self._event_type_for_song(song)
        return ShowSegment(
            kind=event_type.lower(),
            title=f"{song.artist} – {song.title}",
            description=self._writer.build_song_backannounce(song),
            start=start,
            duration=song.duration,
            payload={
                "type": event_type,
                "platform": song.platform,
                "source_id": song.source_id,
                "url": song.playback_url,
                "expected_duration": int(song.duration.total_seconds()),
            },
        )

    def _jingle_segment(self, jingle: Jingle, start: datetime) -> ShowSegment:
        return ShowSegment(
            kind="jingle",
            title=jingle.name,
            description=jingle.slogan,
            start=start,
            duration=jingle.duration,
            payload={
                "type": "JINGLE",
                "asset_url": f"{self._cdn_base}/jingles/{self._slug(jingle.name)}.ogg",
                "expected_duration": int(jingle.duration.total_seconds()),
            },
        )

    def _event_type_for_song(self, song: Song) -> str:
        if song.platform.upper() == "YOUTUBE":
            return "YT_TRACK"
        if song.platform.upper() == "SOUNDCLOUD":
            return "SC_TRACK"
        return "AUDIO_TRACK"

    def _tts_payload(self, name: str, duration: timedelta) -> dict:
        return {
            "type": "TTS_BREAK",
            "url": f"{self._cdn_base}/tts/{self._slug(name)}.ogg",
            "duration": int(duration.total_seconds()),
        }

    def _slug(self, value: str) -> str:
        value = value.lower()
        value = re.sub(r"[^a-z0-9]+", "-", value)
        return value.strip("-")
