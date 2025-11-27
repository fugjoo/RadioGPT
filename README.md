# RadioGPT

RadioGPT erzeugt vollautomatisch eine einstündige Radiosendung mit Musikrotation, Jingles, Moderationstexten und einem Newsblock. Alles läuft lokal und deterministisch, optional sogar reproduzierbar über einen Seed.

## Features
- Vorgenerierte Musikbibliothek mit Energieleveln und Tags zur Sendungsplanung
- Dynamische Jingle-Auswahl für ein produziertes Klangbild
- Nachrichtenblock mit globalen, lokalen Themen und Wetter-Snippets
- Moderationsbausteine für Intro, Musiküberleitungen und Abmoderation
- Ausgabe als menschenlesbarer Sendeplan oder strukturiertes JSON

## Verwendung
```bash
# Textbasierte Ausgabe für 45 Minuten, Host "Mia"
python -m radio_gpt --duration 45 --host "Mia"

# JSON-Ausgabe für 60 Minuten mit festem Seed
python -m radio_gpt --json --seed 7
```

Die Zeitleiste enthält Startzeitpunkte, Laufzeiten und Beschreibungen für jeden Show-Bestandteil.
