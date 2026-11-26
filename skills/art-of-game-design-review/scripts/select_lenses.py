#!/usr/bin/env python3
"""Select targeted lenses from The Art of Game Design (3rd Edition, 116 lenses)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


DATA_PATH = Path(__file__).resolve().parent.parent / "references" / "lenses-full.json"

ID_ALIASES = {
    "67½": "67.5",
    "67.5": "67.5",
    "93½": "93.5",
    "93.5": "93.5",
    "95½": "95.5",
    "95.5": "95.5",
    "∞": "113",
    "inf": "113",
    "113": "113",
}


def load_data() -> dict:
    if not DATA_PATH.is_file():
        print(f"ERROR: Lens database not found: {DATA_PATH}", file=sys.stderr)
        sys.exit(2)
    return json.loads(DATA_PATH.read_text(encoding="utf-8"))


def parse_csv(raw: str | None) -> list[str]:
    if not raw:
        return []
    return [item.strip() for item in raw.split(",") if item.strip()]


def main() -> int:
    data = load_data()
    lenses = data["lenses"]
    valid_stages = set(data["stages"].keys())
    valid_symptoms = set(data["symptoms"].keys())
    valid_domains = {d["id"] for d in data["domains"]}
    valid_tags = set(data["tags"])
    valid_suits = sorted({s for lens in lenses for s in lens["suits"]})
    by_id = {lens["id"]: lens for lens in lenses}

    parser = argparse.ArgumentParser(
        description="Deterministic lens selector for The Art of Game Design (116 lenses)."
    )
    parser.add_argument("--stage", help="Filter by development stage")
    parser.add_argument("--symptom", help="Filter by diagnostic symptom")
    parser.add_argument("--tags", help="Comma-separated feature/genre tags (adds or narrows)")
    parser.add_argument("--domain", help="Filter by review domain ID")
    parser.add_argument("--suit", help="Filter by official card suit")
    parser.add_argument("--ids", help="Comma-separated lens IDs (supports 67.5/67½, 93.5/93½, 95.5/95½, 113/∞)")
    parser.add_argument("--search", help="Case-insensitive keyword search across EN/ZH title, intro, questions")
    parser.add_argument("--all", action="store_true", help="Select all 116 lenses")
    parser.add_argument("--limit", type=int, help="Cap maximum number of returned lenses")
    parser.add_argument(
        "--format",
        choices=["checklist", "markdown", "json"],
        default="checklist",
        help="Output format (default: checklist)",
    )
    parser.add_argument("--list-filters", action="store_true", help="List all valid filter values and exit")

    args = parser.parse_args()

    if args.list_filters:
        print("=== Stages (--stage) ===")
        for k, v in data["stages"].items():
            print(f"  {k:20s} {v}")
        print("\n=== Symptoms (--symptom) ===")
        for k, v in data["symptoms"].items():
            print(f"  {k:20s} {v}")
        print("\n=== Domains (--domain) ===")
        for d in data["domains"]:
            print(f"  {d['id']:28s} {d['name_zh']}")
        print(f"\n=== Tags (--tags) ===\n  {', '.join(sorted(valid_tags))}")
        print(f"\n=== Suits (--suit) ===\n  {', '.join(valid_suits)}")
        return 0

    if not any([args.all, args.stage, args.symptom, args.tags, args.domain, args.suit, args.ids, args.search]):
        parser.error("Provide at least one filter (--stage, --symptom, --tags, --domain, --suit, --ids, --search, --all, or --list-filters).")

    if args.stage and args.stage not in valid_stages:
        print(f"ERROR: Invalid --stage '{args.stage}'. Valid: {', '.join(sorted(valid_stages))}", file=sys.stderr)
        return 2
    if args.symptom and args.symptom not in valid_symptoms:
        print(f"ERROR: Invalid --symptom '{args.symptom}'. Valid: {', '.join(sorted(valid_symptoms))}", file=sys.stderr)
        return 2
    if args.domain and args.domain not in valid_domains:
        print(f"ERROR: Invalid --domain '{args.domain}'. Valid: {', '.join(sorted(valid_domains))}", file=sys.stderr)
        return 2
    if args.suit and args.suit not in valid_suits:
        print(f"ERROR: Invalid --suit '{args.suit}'. Valid: {', '.join(valid_suits)}", file=sys.stderr)
        return 2

    tags = parse_csv(args.tags)
    bad_tags = [t for t in tags if t not in valid_tags]
    if bad_tags:
        print(f"ERROR: Invalid --tags {bad_tags}. Valid: {', '.join(sorted(valid_tags))}", file=sys.stderr)
        return 2

    requested_ids: list[str] = []
    for raw_id in parse_csv(args.ids):
        norm = ID_ALIASES.get(raw_id, raw_id)
        if norm not in by_id:
            print(f"ERROR: Unknown lens ID '{raw_id}'.", file=sys.stderr)
            return 2
        if norm not in requested_ids:
            requested_ids.append(norm)

    if args.limit is not None and args.limit <= 0:
        print("ERROR: --limit must be a positive integer.", file=sys.stderr)
        return 2

    # Selection logic:
    # - Base set starts from all lenses if --all or no primary (stage/symptom/ids) is given;
    # - If --stage or --symptom is combined with --tags, tags expand/augment the slice with tag-matched lenses!
    # - Other filters (--domain, --suit, --search) narrow the candidate set.
    selected: list[dict]
    if requested_ids:
        selected = [by_id[i] for i in requested_ids]
    elif args.stage or args.symptom:
        matched_ids = set()
        for lens in lenses:
            stage_hit = bool(args.stage and args.stage in lens["stages"])
            symptom_hit = bool(args.symptom and args.symptom in lens["symptoms"])
            tag_hit = bool(tags and any(t in lens["tags"] for t in tags))
            if args.stage and args.symptom:
                base_hit = stage_hit and symptom_hit
            else:
                base_hit = stage_hit or symptom_hit
            if base_hit or tag_hit:
                matched_ids.add(lens["id"])
        selected = [lens for lens in lenses if lens["id"] in matched_ids]
    elif tags:
        selected = [lens for lens in lenses if any(t in lens["tags"] for t in tags)]
    else:
        selected = list(lenses)

    if args.domain:
        selected = [lens for lens in selected if lens["domain"] == args.domain]
    if args.suit:
        selected = [lens for lens in selected if args.suit in lens["suits"]]
    if args.search:
        kw = args.search.strip().lower()
        selected = [
            lens
            for lens in selected
            if kw in lens["title_en"].lower()
            or kw in lens["title_zh"].lower()
            or kw in lens["intro_en"].lower()
            or kw in lens["intro_zh"].lower()
            or any(kw in q.lower() for q in lens["questions_en"] + lens["questions_zh"])
        ]

    if args.limit is not None:
        selected = selected[: args.limit]

    if args.format == "json":
        print(json.dumps(selected, ensure_ascii=False, indent=2))
        return 0

    if not selected:
        print("No lenses matched the provided filters.")
        return 0

    print(f"# 命中透镜清单（共 {len(selected)} 张）\n")
    for lens in selected:
        print(f"## Lens #{lens['book_number']}：{lens['title_zh']}（{lens['title_en']}）")
        print(f"- 第 {lens['chapter']} 章《{lens['chapter_title_zh']}》｜分类：{', '.join(lens['suits'])}")
        if args.format == "markdown":
            print(f"- **意图**：{' '.join(lens['intro_zh'].splitlines())}")
        for qz, qe in zip(lens["questions_zh"], lens["questions_en"]):
            prefix = "- [ ]" if args.format == "checklist" else "-"
            print(f"{prefix} {qz} *(EN: {qe})*")
        print()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
