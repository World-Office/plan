#!/usr/bin/env python3
"""Generate the OnlyOffice UI feature inventory from the running oracle.

Source of truth: the ONLYOFFICE DocumentServer build deployed in
~/workspace/nextcloud (container nc-ooh-onlyoffice-1, DS 9.4 build 129).
Every user-visible control, menu entry, dialog and setting in web-apps is
named by a key in the app's English locale file. The full key set is
therefore the complete, build-exact UI feature surface.

Outputs (in inventory/):
  <app>.md          every component with every key = value
  _coverage.json    component -> key count, plus totals
  enums.md          aggregated enumeration data (chart types, transitions,
                    animation effects, form field types, roles)

Usage:  python3 generate-inventory.py [--container nc-ooh-onlyoffice-1]
Requires: docker CLI with access to the oracle container.
"""
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path

APPS = {
    "documenteditor": "DE",
    "spreadsheeteditor": "SSE",
    "presentationeditor": "PE",
    "pdfeditor": "PDFE",
    "visioeditor": "VE",
}
# UI variants deployed per editor. `main` = desktop editor; the others only
# exist where the build ships them (mobile/embed/forms).
VARIANTS = ("main", "mobile", "embed", "forms")
HERE = Path(__file__).parent
INV = HERE / "inventory"


def flatten(d, prefix=""):
    """Nested variant locales (mobile/embed/forms) -> flat dot-key dict."""
    out = {}
    for k, v in d.items():
        key = f"{prefix}.{k}" if prefix else k
        if isinstance(v, dict):
            out.update(flatten(v, key))
        else:
            out[key] = v
    return out


def fetch(container: str, app: str, variant: str):
    remote = (
        f"/var/www/onlyoffice/documentserver/web-apps/apps/{app}/{variant}/locale/en.json"
    )
    probe = subprocess.run(
        ["docker", "exec", container, "test", "-f", remote]
    )
    if probe.returncode != 0:
        return None  # variant not shipped for this editor
    raw = subprocess.run(
        ["docker", "exec", container, "cat", remote],
        capture_output=True,
        text=True,
        check=True,
    ).stdout
    parsed = json.loads(raw)
    nested = any(isinstance(v, dict) for v in parsed.values())
    return flatten(parsed), nested


def component_of(key: str, nested: bool) -> str:
    """Main locales are FLAT with dot-namespaced class paths (group = first 3
    dot-segments, e.g. `DE.Views.Toolbar`). Variant locales (mobile/embed/
    forms) NEST section dicts (group = first 2 dot-segments for sectioned
    keys, else the first segment)."""
    parts = key.split(".")
    if nested:
        if len(parts) >= 3:
            return ".".join(parts[:2])
        return parts[0]
    if len(parts) >= 3:
        return ".".join(parts[:3])
    return parts[0]


def write_inventory(label: str, data: dict, nested: bool) -> dict:
    by_comp: dict[str, list[tuple[str, str]]] = {}
    for k in sorted(data):
        by_comp.setdefault(component_of(k, nested), []).append((k, str(data[k])))
    lines = [f"# {label} — {len(data)} keys in {len(by_comp)} components", ""]
    for comp in sorted(by_comp):
        lines.append(f"## {comp} ({len(by_comp[comp])})")
        lines.append("")
        for k, v in by_comp[comp]:
            lines.append(f"- `{k}` = {v}")
        lines.append("")
    (INV / f"{label.replace('/', '-')}.md").write_text("\n".join(lines), encoding="utf-8")
    return {c: len(v) for c, v in by_comp.items()}


def write_enums(all_data: dict[str, dict]) -> None:
    de, sse, pe, pde = (
        all_data["documenteditor/main"],
        all_data["spreadsheeteditor/main"],
        all_data["presentationeditor/main"],
        all_data["pdfeditor/main"],
    )
    out = ["# Enumerated option sets (aggregated from locale keys)", ""]

    def sect(title, items):
        out.append(f"## {title}")
        out.append("")
        for i in sorted(items):
            out.append(f"- {i}")
        out.append("")

    sect(
        "Chart types (Common.define.chartData)",
        {str(v) for k, v in de.items() if k.startswith("Common.define.chartData")},
    )
    sect(
        "Slide transitions (PE.Views.Transitions)",
        {
            str(v)
            for k, v in pe.items()
            if k.startswith("PE.Views.Transitions") and isinstance(v, str) and len(v) < 40
        },
    )
    sect(
        "Animation effect families (Common.define.effectData, PE)",
        {str(v) for k, v in pe.items() if k.startswith("Common.define.effectData")},
    )
    sect(
        "PDF form field types (PDFE.Views.FormsTab)",
        {
            str(v)
            for k, v in pde.items()
            if k.startswith("PDFE.Views.FormsTab")
            and isinstance(v, str)
            and 2 < len(v) < 30
        },
    )
    sect(
        "Form recipient roles (DE.Views.Role*/FormsTab)",
        {
            str(v)[:80]
            for k, v in de.items()
            if "Role" in component_of(k, False) and isinstance(v, str)
        },
    )
    sect(
        "AutoCorrect options (Common.Views.AutoCorrectDialog)",
        {str(v) for k, v in de.items() if k.startswith("Common.Views.AutoCorrectDialog")},
    )
    (INV / "enums.md").write_text("\n".join(out), encoding="utf-8")


def main() -> int:
    container = "nc-ooh-onlyoffice-1"
    if "--container" in sys.argv:
        container = sys.argv[sys.argv.index("--container") + 1]
    INV.mkdir(exist_ok=True)
    all_data: dict[str, dict] = {}
    coverage: dict = {"source_container": container, "apps": {}}
    total_keys, total_comps = 0, 0
    for app in APPS:
        for variant in VARIANTS:
            fetched = fetch(container, app, variant)
            if fetched is None:
                continue
            data, nested = fetched
            label = f"{app}/{variant}"
            all_data[label] = data
            comps = write_inventory(label, data, nested)
            coverage["apps"][label] = {
                "keys": len(data),
                "components": comps,
            }
            total_keys += len(data)
            total_comps += len(comps)
            print(f"{label}: {len(data)} keys / {len(comps)} components")
    write_enums(all_data)
    coverage["totals"] = {"keys": total_keys, "components": total_comps}
    (INV / "_coverage.json").write_text(json.dumps(coverage, indent=2))
    print(f"TOTAL: {total_keys} keys / {total_comps} components -> {INV}/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
