#!/usr/bin/env python3
"""Build a part script into STEP, STL and 3MF, then render and check it.

A part script is a Python file in models/ that defines either:
  - build(**params) -> build123d Part/Compound, with keyword defaults, or
  - a module-level variable named `part`.

Usage:
  python tools/build.py models/bracket.py [--set key=value ...] [--no-render] [--no-check]

Outputs go to out/<name>/.
"""
from __future__ import annotations

import argparse
import ast
import importlib.util
import inspect
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))


def load_module(path: Path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def parse_value(raw: str):
    """Python literal (1.5, 'x', (1, 2), None); true/false in any case; else a plain string."""
    if raw.strip().lower() in ("true", "false"):
        return raw.strip().lower() == "true"
    try:
        return ast.literal_eval(raw)
    except (ValueError, SyntaxError):
        return raw


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("script", type=Path)
    ap.add_argument("--set", action="append", default=[], metavar="KEY=VALUE",
                    help="override a build() parameter")
    ap.add_argument("--name", help="output name (default: script stem)")
    ap.add_argument("--no-render", action="store_true")
    ap.add_argument("--no-check", action="store_true")
    args = ap.parse_args()

    from build123d import export_step, export_stl, Mesher

    mod = load_module(args.script.resolve())
    params = {}
    if hasattr(mod, "build"):
        sig = inspect.signature(mod.build)
        params = {k: v.default for k, v in sig.parameters.items()
                  if v.default is not inspect.Parameter.empty}
        for item in args.set:
            k, _, v = item.partition("=")
            if k not in sig.parameters:
                print(f"error: build() has no parameter {k!r}", file=sys.stderr)
                return 2
            params[k] = parse_value(v)
        part = mod.build(**params)
    elif hasattr(mod, "part"):
        if args.set:
            print("error: --set needs a build() function; this script has no build()", file=sys.stderr)
            return 2
        part = mod.part
    else:
        print("error: script must define build() or `part`", file=sys.stderr)
        return 2

    name = args.name or args.script.stem
    out = ROOT / "out" / name
    out.mkdir(parents=True, exist_ok=True)

    step, stl, mf = out / f"{name}.step", out / f"{name}.stl", out / f"{name}.3mf"
    export_step(part, str(step))
    export_stl(part, str(stl), tolerance=0.01, angular_tolerance=0.1)
    # One 3MF object per solid, so multi-piece designs arrive in PrusaSlicer
    # as separate objects.
    mesher = Mesher()
    for solid in part.solids():
        mesher.add_shape(solid, linear_deflection=0.01, angular_deflection=0.1)
    mesher.write(str(mf))

    bb = part.bounding_box()
    summary = {
        "name": name,
        "params": params,
        "files": {"step": str(step), "stl": str(stl), "3mf": str(mf)},
        "bbox_mm": [round(bb.size.X, 3), round(bb.size.Y, 3), round(bb.size.Z, 3)],
        "volume_mm3": round(sum(s.volume for s in part.solids()), 2),
        "solids": len(part.solids()),
        "is_valid": bool(part.is_valid() if callable(part.is_valid) else part.is_valid),
    }

    if not args.no_render:
        from render import render
        summary["renders"] = [str(p) for p in render(stl, out)]
    if not args.no_check:
        from check import check
        summary["check"] = check(stl)

    (out / "summary.json").write_text(json.dumps(summary, indent=2))
    print(json.dumps(summary, indent=2))
    ok = summary["is_valid"] and summary.get("check", {}).get("ok", True)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
