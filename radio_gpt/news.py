from __future__ import annotations

import random
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional


@dataclass
class NewsItem:
    headline: str
    summary: str
    category: str
    relevance: float


GLOBAL_NEWS: List[NewsItem] = [
    NewsItem(
        headline="Innovativer Speicher für erneuerbare Energien erreicht Marktreife",
        summary="Ein europäisches Konsortium stellt einen modularen Salzbatteriepark vor, der Solar- und Windparks unabhängiger macht.",
        category="wirtschaft",
        relevance=0.9,
    ),
    NewsItem(
        headline="Neues Bahnkonzept verspricht pünktlichere Pendlerzüge",
        summary="Digitale Stellwerke werden in drei Metropolregionen in Betrieb genommen, um Verspätungen zu halbieren.",
        category="verkehr",
        relevance=0.8,
    ),
    NewsItem(
        headline="KI-gestützte Medizin erkennt Herzrhythmusstörungen früher",
        summary="Eine Studie zeigt, dass ein neues Screening-Tool in Hausarztpraxen Risikopatienten deutlich schneller identifiziert.",
        category="gesundheit",
        relevance=0.85,
    ),
    NewsItem(
        headline="Bundesliga startet mit torreichem Freitagsspiel",
        summary="Der Aufsteiger zeigt keine Scheu und ringt dem Favoriten ein 3:3 ab — Fans feiern den offenen Schlagabtausch.",
        category="sport",
        relevance=0.7,
    ),
    NewsItem(
        headline="Start-up eröffnet Europas größtes vertikales Gewächshaus",
        summary="Mit LED-gestützter Landwirtschaft sollen regionale Märkte ganzjährig mit frischem Gemüse versorgt werden.",
        category="umwelt",
        relevance=0.77,
    ),
]

LOCAL_NEWS: List[NewsItem] = [
    NewsItem(
        headline="Neuer Radweg verbindet Innenstadt mit dem See",
        summary="Die 6 Kilometer lange Route erhält breite Schutzstreifen und smarte Ampeln für schnelleren Radverkehr.",
        category="lokal",
        relevance=0.65,
    ),
    NewsItem(
        headline="Open-Air-Kino verlängert Saison bis Oktober",
        summary="Beliebte Klassiker laufen auf der Hafenbühne, zusätzlich gibt es Podcast-Abende mit Live-Publikum.",
        category="kultur",
        relevance=0.58,
    ),
]

WEATHER_TEMPLATES: List[str] = [
    "Heute viel Sonne, am Nachmittag lockere Wolken, Höchstwerte um 22 Grad.",
    "Leichter Regen in den frühen Morgenstunden, später trocken bei 18 Grad und frischem Wind.",
    "Wolkig mit Auflockerungen, zum Abend klart es weiter auf, Höchsttemperaturen bei 20 Grad.",
]


class Newsroom:
    """Provides curated news and weather suggestions."""

    def __init__(self, *, seed: Optional[int] = None) -> None:
        self.random = random.Random(seed)

    def compose_news(
        self, *, include_weather: bool = True, include_local: bool = True, limit: int = 5
    ) -> List[NewsItem]:
        pool = GLOBAL_NEWS.copy()
        if include_local:
            pool.extend(LOCAL_NEWS)
        selection = sorted(pool, key=lambda item: item.relevance, reverse=True)[: limit - 1]

        if include_weather:
            weather = self._weather_item()
            selection.append(weather)

        self.random.shuffle(selection)
        return selection

    def _weather_item(self) -> NewsItem:
        template = self.random.choice(WEATHER_TEMPLATES)
        return NewsItem(
            headline="Wetter",
            summary=template,
            category="wetter",
            relevance=0.5,
        )
