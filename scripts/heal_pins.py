#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Move every release pin of this starter together, or refuse.

release-heal used to bump one byte: the reusable workflow's engine
``default:``. The engine example in ``nika.yml`` and both first-party
``nika-action`` pins were never healed, so a new clone started on an
engine example and an action release several waves behind.

The carriers, each matched exactly once:

* ``.github/workflows/nika-check.yml`` · ``default: '<engine>'``
* ``.github/workflows/nika.yml`` · ``engine-version: '<engine>'``
* both files · ``uses: supernovae-st/nika-action@<action tag>``

A missing or duplicated carrier refuses with nothing written, so a layout
change turns the heal red instead of silently skipping a pin.

    python3 scripts/heal_pins.py --engine 0.120.3 --action v1.0.25
    python3 scripts/heal_pins.py --check      # every carrier agrees
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REUSABLE = Path(".github/workflows/nika-check.yml")
SELF_CHECK = Path(".github/workflows/nika.yml")

ENGINE = re.compile(r"\d+\.\d+\.\d+")
ACTION = re.compile(r"v1\.\d+\.\d+")
CARRIERS = (
    (REUSABLE, "engine", re.compile(r"(default: ')(\d+\.\d+\.\d+)(')")),
    (SELF_CHECK, "engine", re.compile(r"(engine-version: ')(\d+\.\d+\.\d+)(')")),
    (REUSABLE, "action", re.compile(r"(uses: supernovae-st/nika-action@)(v\d+\.\d+\.\d+)(\s)")),
    (SELF_CHECK, "action", re.compile(r"(uses: supernovae-st/nika-action@)(v\d+\.\d+\.\d+)(\s)")),
)


class PinError(ValueError):
    """A carrier is missing, duplicated or a target is malformed."""


def read(texts: dict[Path, str]) -> dict[str, set[str]]:
    """The value each kind of carrier holds, every carrier matched exactly once."""
    values: dict[str, set[str]] = {"engine": set(), "action": set()}
    for path, kind, pattern in CARRIERS:
        found = pattern.findall(texts[path])
        if len(found) != 1:
            raise PinError(f"{path} {kind} pin: expected exactly one, found {len(found)}")
        values[kind].add(found[0][1])
    return values


def rewrite(texts: dict[Path, str], engine: str, action: str) -> dict[Path, str]:
    """Return the carriers moved to ``engine`` and ``action``."""
    if not ENGINE.fullmatch(engine):
        raise PinError(f"not a stable engine version: {engine!r}")
    if not ACTION.fullmatch(action):
        raise PinError(f"not a nika-action v1 release tag: {action!r}")
    read(texts)
    target = {"engine": engine, "action": action}
    updated = dict(texts)
    for path, kind, pattern in CARRIERS:
        updated[path] = pattern.sub(lambda m: f"{m.group(1)}{target[kind]}{m.group(3)}", updated[path])
    return updated


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--engine", help="the published nika release, e.g. 0.120.3")
    parser.add_argument("--action", help="the published nika-action release tag, e.g. v1.0.25")
    parser.add_argument("--check", action="store_true", help="refuse carriers that disagree")
    parser.add_argument("--root", type=Path, default=ROOT, help=argparse.SUPPRESS)
    args = parser.parse_args(argv)
    paths = {REUSABLE, SELF_CHECK}
    texts = {path: (args.root / path).read_text() for path in paths}
    try:
        if args.check:
            values = read(texts)
            split = {kind: sorted(v) for kind, v in values.items() if len(v) != 1}
            if split:
                print(f"heal_pins: carriers disagree {split}", file=sys.stderr)
                return 1
            print(f"heal_pins: ok — engine {values['engine'].pop()} · nika-action {values['action'].pop()}")
            return 0
        if not (args.engine and args.action):
            parser.error("--engine and --action are required unless --check")
        updated = rewrite(texts, args.engine, args.action)
    except PinError as error:
        print(f"heal_pins: {error} · nothing written", file=sys.stderr)
        return 1
    for path in paths:
        if updated[path] != texts[path]:
            (args.root / path).write_text(updated[path])
    moved = sorted(str(p) for p in paths if updated[p] != texts[p])
    print(f"heal_pins: engine {args.engine} · nika-action {args.action} · moved {moved or 'nothing'}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
