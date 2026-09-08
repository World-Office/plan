#!/usr/bin/env python3
"""Verify 100% component coverage of spec.md against the generated inventory.

Coverage rule (spec.md §1): every UI component class present in the oracle
build's locale inventory MUST be named in spec.md. This script mechanically
enforces that: it walks inventory/_coverage.json, extracts every component
class, and fails listing any class that does not appear in spec.md.

Usage:  python3 check-coverage.py            # exit 0 = full coverage
"""
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).parent
SPEC = HERE / "spec.md"
COV = HERE / "inventory" / "_coverage.json"


def main() -> int:
    spec = SPEC.read_text(encoding="utf-8")
    coverage = json.loads(COV.read_text(encoding="utf-8"))
    missing = []
    checked = 0
    for app, meta in coverage["apps"].items():
        for comp in sorted(meta["components"]):
            checked += 1
            if f"`{comp}`" not in spec:
                missing.append(f"{app}: {comp}")
    print(f"checked {checked} components across {len(coverage['apps'])} apps")
    if missing:
        print(f"\nMISSING from spec.md ({len(missing)}):")
        for m in missing:
            print(f"  - {m}")
        return 1
    print("OK: 100% component coverage in spec.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
