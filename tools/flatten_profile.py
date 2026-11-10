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
import sys
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


class _Num(float):
    """A scalar config number that also indexes like a 1-element vector (nozzle_diameter[0])."""
    def __getitem__(self, i):
        if i != 0:
            raise IndexError(i)
        return float(self)


def _value(v: str):
    """Config value as Python: comma-separated numbers become a list, a number an
    indexable float, anything else a string."""
    parts = [p.strip() for p in v.split(",")]
    try:
        nums = [float(p) for p in parts]
    except ValueError:
        return v.strip().strip('"')
    return nums if len(nums) > 1 else _Num(nums[0])


def eval_condition(cond: str, printer: dict):
    """Evaluate a PrusaSlicer compatible_printers_condition against a resolved printer
    preset. Supports =~ /re/, !~ /re/, ==, !=, <, >, <=, >=, and/or/not, parentheses,
    [i] indexing. Returns True/False, or None if it uses something unsupported."""
    regexes = []

    def sub(m):
        regexes.append(m.group(3))
        neg = "not " if m.group(2) == "!~" else ""
        return f"{neg}_re({len(regexes) - 1}, {m.group(1)})"

    # x=~/re/ -> _re(i, x); then PrusaSlicer's "!" (not) -> Python "not".
    expr = re.sub(r"([A-Za-z_]\w*(?:\[\d+\])?)\s*(=~|!~)\s*/(.*?)/", sub, cond)
    expr = expr.replace("&&", " and ").replace("||", " or ")
    expr = re.sub(r"!(?!=)", " not ", expr)
    expr = re.sub(r"\btrue\b", "True", re.sub(r"\bfalse\b", "False", expr))
    env = {k: _value(v) for k, v in printer.items()}
    nd = env.get("nozzle_diameter")
    env.setdefault("num_extruders", len(nd) if isinstance(nd, list) else 1)
    env["_re"] = lambda i, x: re.search(regexes[i], str(x)) is not None
    try:
        return bool(eval(expr, {"__builtins__": {}}, env))
    except Exception:
        return None


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
    printer = resolve(s, "printer", a.printer)
    notes = printer.get("printer_notes", "")
    for kind, name in (("printer", a.printer), ("print", a.print_), ("filament", a.filament)):
        preset = resolve(s, kind, name)
        cond = preset.get("compatible_printers_condition", "")
        if kind != "printer" and cond:
            ok = eval_condition(cond, printer)
            if ok is None:
                print(f"warning: couldn't evaluate {kind} preset {name!r} compatibility "
                      f"(condition: {cond}); check it in PrusaSlicer", file=sys.stderr)
            elif not ok:
                print(f"warning: {kind} preset {name!r} is not for this printer "
                      f"(condition: {cond})", file=sys.stderr)
        cfg.update({k: v for k, v in preset.items() if k not in META})
    cfg["printer_settings_id"] = a.printer
    cfg["print_settings_id"] = a.print_
    cfg["filament_settings_id"] = a.filament

    header = (f"# Flattened from {a.bundle.name}\n# printer: {a.printer}\n"
              f"# print: {a.print_}\n# filament: {a.filament}\n")
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_text(header + "".join(f"{k} = {v}\n" for k, v in sorted(cfg.items())), encoding="utf-8")
    print(f"wrote {a.output} ({len(cfg)} keys)")


if __name__ == "__main__":
    main()
