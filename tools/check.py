#!/usr/bin/env python3
"""
The one check: rendering catalog.yml and parsing the result back must give the
same tree. If it does, no entry was dropped, reordered or mangled by the
alignment code. Run it after touching render.py.

    python3 tools/check.py
"""
import html
import re
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from render import ROOT, catalog_block, profile_block  # noqa: E402

STATUS = {"✅": "available", "🧪": "validating", "🚧": "ongoing", "🧭": "idea"}


def parse(lines):
    """Read a rendered tree back into nodes — the inverse of render_tree."""
    root, stack = [], []

    for raw in lines:
        m = re.match(r"^((?:[│ ] {3})*)(?:├── |└── )(.*)$", raw)
        if not m:
            continue

        depth, body = len(m.group(1)) // 4, m.group(2)
        full = re.match(r'^(.*?)\s+—\s+(.*?)\s*([✅🧪🚧🧭])\s*'
                        r'(?:<a href="([^"]+)">.*</a>)?\s*$', body)
        bare = re.match(r"^(.*?)\s*([✅🧪🚧🧭])\s*$", body)

        if full:
            node = {"name": html.unescape(full.group(1).strip()),
                    "blurb": html.unescape(full.group(2).strip()),
                    "status": STATUS[full.group(3)]}
            if full.group(4):
                node["url"] = full.group(4)
        elif bare:
            node = {"name": html.unescape(bare.group(1).strip()),
                    "status": STATUS[bare.group(2)]}
        else:
            node = {"name": html.unescape(body.strip()), "children": []}

        stack = stack[:depth]
        (stack[-1].setdefault("children", []) if stack else root).append(node)
        stack.append(node)

    return root


def strip(nodes, blurb_key="blurb"):
    """Only the fields a rendered tree can carry."""
    out = []
    for n in nodes:
        keep = {"name": n["name"]}
        blurb = n.get(blurb_key) or n.get("blurb")
        if blurb and not n.get("children"):
            keep["blurb"] = blurb
        if "status" in n:
            keep["status"] = n["status"]
        if "url" in n:
            keep["url"] = n["url"]
        if n.get("children"):
            keep["children"] = strip(n["children"], blurb_key)
        out.append(keep)
    return out


def highlights(tree):
    sections = []
    for top in tree:
        picks = []

        def collect(nodes):
            for n in nodes:
                if n.get("highlight"):
                    picks.append(n)
                collect(n.get("children", []))

        collect(top.get("children", []))
        if picks:
            sections.append({"name": top["name"], "children": picks})
    return sections


def compare(what, expected, actual):
    if expected == actual:
        print(f"  {what}: round-trips, {len(yaml.safe_dump(actual).splitlines())} lines")
        return True

    print(f"  {what}: MISMATCH")
    e = yaml.safe_dump(expected, allow_unicode=True, sort_keys=False).splitlines()
    a = yaml.safe_dump(actual, allow_unicode=True, sort_keys=False).splitlines()
    for i, (x, y) in enumerate(zip(e, a)):
        if x != y:
            print(f"    line {i}: expected {x!r}\n             got      {y!r}")
            break
    return False


def main():
    tree = yaml.safe_load((ROOT / "catalog.yml").read_text())["tree"]
    ok = True

    print("catalog.yml -> tree -> catalog.yml")
    ok &= compare("catalog", strip(tree), parse(catalog_block(tree)))
    ok &= compare("profile", strip(highlights(tree), "profile_blurb"),
                  parse(profile_block(tree)))

    # Every entry that names a repo should look like one, not a section title.
    entries = []

    def walk(nodes):
        for n in nodes:
            if "status" in n and "blurb" in n:
                entries.append(n)
            walk(n.get("children", []))

    walk(tree)
    counts = {}
    for n in entries:
        counts[n["status"]] = counts.get(n["status"], 0) + 1
    print(f"  {len(entries)} entries: " +
          ", ".join(f"{v} {k}" for k, v in sorted(counts.items())))

    dupes = {n["name"] for n in entries
             if sum(1 for m in entries if m["name"] == n["name"]) > 1}
    if dupes:
        print(f"  duplicate names: {sorted(dupes)}")
        ok = False

    print("ok" if ok else "FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
