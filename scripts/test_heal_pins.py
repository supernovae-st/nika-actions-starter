#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""The release heal moves every starter pin together, or refuses."""
from __future__ import annotations

import contextlib
import io
import pathlib
import sys
import tempfile
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import heal_pins

ROOT = heal_pins.ROOT
PATHS = (heal_pins.REUSABLE, heal_pins.SELF_CHECK)


def live() -> dict[pathlib.Path, str]:
    return {path: (ROOT / path).read_text() for path in PATHS}


class HealPins(unittest.TestCase):
    def test_every_carrier_of_the_live_workflows_moves(self):
        before = live()
        after = heal_pins.rewrite(before, "9.9.9", "v1.9.9")
        self.assertEqual(heal_pins.read(after), {"engine": {"9.9.9"}, "action": {"v1.9.9"}})
        changed = [(a, b) for path in PATHS
                   for a, b in zip(before[path].splitlines(), after[path].splitlines()) if a != b]
        self.assertEqual(len(changed), 4, changed)
        for old, new in changed:
            self.assertEqual(old.split("#")[1:], new.split("#")[1:], "a pin comment changed")

    def test_a_second_run_is_a_no_op(self):
        once = heal_pins.rewrite(live(), "9.9.9", "v1.9.9")
        self.assertEqual(heal_pins.rewrite(once, "9.9.9", "v1.9.9"), once)

    def test_a_missing_or_duplicated_carrier_refuses(self):
        texts = live()
        line = next(l for l in texts[heal_pins.SELF_CHECK].splitlines() if "engine-version: '" in l)
        for broken in (texts[heal_pins.SELF_CHECK].replace(line + "\n", ""),
                       texts[heal_pins.SELF_CHECK].replace(line, line + "\n" + line)):
            with self.assertRaisesRegex(heal_pins.PinError, "nika.yml engine pin"):
                heal_pins.rewrite({**texts, heal_pins.SELF_CHECK: broken}, "9.9.9", "v1.9.9")

    def test_only_stable_engines_and_v1_action_tags_are_accepted(self):
        for engine, action in (("v0.120.3", "v1.0.25"), ("0.121.0-rc.1", "v1.0.25"),
                               ("0.120.3", "1.0.25"), ("0.120.3", "v2.0.0"), ("0.120.3", "v1")):
            with self.assertRaises(heal_pins.PinError):
                heal_pins.rewrite(live(), engine, action)

    def test_check_names_disagreeing_carriers(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            texts = heal_pins.rewrite(live(), "9.9.9", "v1.9.9")
            texts[heal_pins.SELF_CHECK] = texts[heal_pins.SELF_CHECK].replace(
                "engine-version: '9.9.9'", "engine-version: '9.9.8'")
            for path, text in texts.items():
                (root / path).parent.mkdir(parents=True, exist_ok=True)
                (root / path).write_text(text)
            err = io.StringIO()
            with contextlib.redirect_stderr(err):
                self.assertEqual(heal_pins.main(["--check", "--root", tmp]), 1)
            self.assertIn("9.9.8", err.getvalue())
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(heal_pins.main(["--engine", "9.9.9", "--action", "v1.9.9",
                                                 "--root", tmp]), 0)
                self.assertEqual(heal_pins.main(["--check", "--root", tmp]), 0)

    def test_the_live_carriers_agree(self):
        values = heal_pins.read(live())
        self.assertEqual(len(values["engine"]), 1, values)
        self.assertEqual(len(values["action"]), 1, values)

    def test_release_heal_moves_the_pins_through_this_script(self):
        heal = (ROOT / ".github/workflows/release-heal.yml").read_text()
        self.assertIn('python3 scripts/heal_pins.py --engine "${ver}" --action "${action}"', heal)
        self.assertNotIn("perl -pi", heal)


if __name__ == "__main__":
    unittest.main()
