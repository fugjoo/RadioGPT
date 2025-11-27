from __future__ import annotations

import argparse
import json
from datetime import datetime
from typing import Optional

from .generator import ShowGenerator


def parse_args(argv: Optional[list[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generiert eine komplette RadioGPT-Stunde.")
    parser.add_argument("--duration", type=int, default=60, help="Länge der Sendung in Minuten (Standard: 60)")
    parser.add_argument("--host", type=str, default="Alex", help="Name des Hosts")
    parser.add_argument("--station", type=str, default="RadioGPT", help="Stationsname")
    parser.add_argument("--seed", type=int, default=None, help="Optionaler Seed für reproduzierbare Abläufe")
    parser.add_argument("--json", action="store_true", help="Ergebnis als JSON statt als Text ausgeben")
    parser.add_argument(
        "--timeline",
        action="store_true",
        help="Synchronisierte Timeline für Webplayer ausgeben",
    )
    return parser.parse_args(argv)


def main(argv: Optional[list[str]] = None) -> int:
    args = parse_args(argv)
    generator = ShowGenerator(station=args.station, host=args.host, seed=args.seed)
    show = generator.build_show(duration_minutes=args.duration)

    if args.timeline:
        print(json.dumps(show.as_timeline(), ensure_ascii=False, indent=2))
    elif args.json:
        print(json.dumps(show.as_dict(), ensure_ascii=False, indent=2))
    else:
        print(show.render_text())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
