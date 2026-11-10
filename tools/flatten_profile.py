#!/usr/bin/env python3
"""Flatten PrusaSlicer vendor presets (with `inherits`) into one .ini for the CLI.

Usage:
  python tools/flatten_profile.py /usr/share/PrusaSlicer/profiles/PrusaResearch.ini \
      --printer "Original Prusa i3 MK3S & MK3S+" \
      --print "0.20mm QUALITY @MK3" \
      --filament "Prusament PLA" \
      -o profiles/mk3s_pla_0.20mm.ini
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path


def parse(path: Path) -> dict[tuple[str, str], dict[str, str]]:
    sections, cur = {}, None
    for line in path.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^\[(\w+):(.+)\]\s*$", line)
        if m:
            cur = sections.setdefault((m.group(1), m.group(2)), {})
            continue
        if cur is None or not line.strip() or line.lstrip().startswith("#"):
            continue
        k, sep, v = line.partition("=")
        if sep:
            cur[k.strip()] = v.strip()
    return sections


def resolve(sections, kind: str, name: str, seen=()) -> dict[str, str]:
    if (kind, name) not in sections:
        raise SystemExit(f"preset not found: [{kind}:{name}]")
    if name in seen:
        raise SystemExit(f"inheritance cycle at {name}")
    own = sections[(kind, name)]
    merged: dict[str, str] = {}
    for parent in filter(None, (p.strip() for p in own.get("inherits", "").split(";"))):
        merged.update(resolve(sections, kind, parent, seen + (name,)))
    merged.update(own)
    merged.pop("inherits", None)
    return merged


# Keys that describe the preset itself rather than slicing settings.
META = {"renamed_from", "compatible_printers", "compatible_printers_condition",
        "compatible_prints", "compatible_prints_condition", "alias",
        "printer_vendor", "thumbnails", "thumbnails_format"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("bundle", type=Path)
    ap.add_argument("--printer", required=True)
    ap.add_argument("--print", dest="print_", required=True)
    ap.add_argument("--filament", required=True)
    ap.add_argument("-o", "--output", type=Path, required=True)
    a = ap.parse_args()

    s = parse(a.bundle)
    cfg: dict[str, str] = {}
    for kind, name in (("printer", a.printer), ("print", a.print_), ("filament", a.filament)):
        cfg.update({k: v for k, v in resolve(s, kind, name).items() if k not in META})
    cfg["printer_settings_id"] = a.printer
    cfg["print_settings_id"] = a.print_
    cfg["filament_settings_id"] = a.filament

    header = (f"# Flattened from {a.bundle.name}\n# printer: {a.printer}\n"
              f"# print: {a.print_}\n# filament: {a.filament}\n")
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_text(header + "".join(f"{k} = {v}\n" for k, v in sorted(cfg.items())))
    print(f"wrote {a.output} ({len(cfg)} keys)")


if __name__ == "__main__":
    main()
