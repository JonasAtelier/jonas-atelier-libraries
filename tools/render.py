#!/usr/bin/env python3
"""
Render catalog.yml into the two README trees, and optionally the ledger.

    python3 tools/render.py            # both READMEs
    python3 tools/render.py --stats    # ...and refresh the profile ledger

tools/check.py proves a render round-trips back to the same YAML.

catalog.yml is the only place entries are edited. Everything between the
<!-- tree:start --> and <!-- tree:end --> markers in either README is
generated, so do not hand-edit inside them.
"""
import argparse
import html
import json
import os
import re
import subprocess
import sys
import unicodedata
from datetime import date
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
PROFILE = Path(os.environ.get("ATELIER_PROFILE", ROOT.parent / "JonasAtelier"))
OWNER = "JonasAtelier"

ICON = {"available": "✅", "validating": "🧪", "ongoing": "🚧", "idea": "🧭"}
START, END = "<!-- tree:start -->", "<!-- tree:end -->"


# --------------------------------------------------------------- tree render

def width(text):
    """Columns a string occupies in GitHub's monospace <pre>.

    len() is wrong twice over here: an emoji takes two columns, and a
    variation selector or zero-width joiner takes none. Pad on this, not on
    the escaped string - "&amp;" is five characters wide and one column.
    """
    total = 0
    for ch in text:
        code = ord(ch)
        if code in (0xFE0F, 0xFE0E, 0x200D) or unicodedata.combining(ch):
            continue
        if (unicodedata.east_asian_width(ch) in ("W", "F")
                or 0x1F300 <= code <= 0x1FAFF or 0x2600 <= code <= 0x27BF):
            total += 2
        else:
            total += 1
    return total


def pad(text, columns):
    return html.escape(text, quote=False) + " " * max(0, columns - width(text))


def _leaf(node, name_w, blurb_w, blurb_key, link_text):
    """One entry line: name, blurb, status icon, and a link if it has one."""
    blurb = node.get(blurb_key) or node.get("blurb", "")
    if not blurb:
        return f"{html.escape(node['name'], quote=False)} {ICON[node['status']]}"

    line = f"{pad(node['name'], name_w)}— {pad(blurb, blurb_w)}{ICON[node['status']]}"
    if node.get("url"):
        line += f'  <a href="{node["url"]}">{link_text}</a>'
    return line


def _widths(siblings, blurb_key):
    """Align the em-dash and status columns across a run of siblings."""
    leaves = [n for n in siblings if not n.get("children") and n.get("blurb")]
    if not leaves:
        return 0, 0
    name_w = max(width(n["name"]) for n in leaves) + 1
    blurb_w = max(width(n.get(blurb_key) or n["blurb"]) for n in leaves) + 1
    return name_w, blurb_w


def render_tree(nodes, prefix="", blurb_key="blurb", link_text="🔗 GitHub"):
    """Recursive tree render. A blank spacer separates sibling *sections*."""
    out = []
    name_w, blurb_w = _widths(nodes, blurb_key)

    for i, node in enumerate(nodes):
        last = i == len(nodes) - 1
        connector = "└── " if last else "├── "
        child_prefix = prefix + ("    " if last else "│   ")

        if node.get("children"):
            out.append(prefix + connector + html.escape(node["name"], quote=False))
            out += render_tree(node["children"], child_prefix, blurb_key, link_text)
            if node.get("note"):
                out.append(child_prefix.rstrip() or "│")
                out.append(child_prefix + html.escape(node["note"], quote=False))
        else:
            out.append(prefix + connector
                       + _leaf(node, name_w, blurb_w, blurb_key, link_text))

        # Sections get air between them; plain entries do not.
        if not last and (node.get("children") or nodes[i + 1].get("children")):
            out.append((prefix + "│").rstrip("\n"))

    return out


def catalog_block(tree):
    return ["<pre>", "Jonas Atelier"] + render_tree(tree) + ["</pre>"]


def profile_block(tree):
    """The profile shows only highlighted entries, flat under each section."""
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

    return ["<pre>"] + render_tree(sections, blurb_key="profile_blurb",
                                   link_text="🔗") + ["</pre>"]


# ------------------------------------------------------------------- ledger

def all_repos():
    out = subprocess.run(
        ["gh", "repo", "list", OWNER, "--limit", "200", "--no-archived",
         "--json", "name,primaryLanguage,createdAt"],
        capture_output=True, text=True, check=True).stdout
    return json.loads(out)


def commit_count(repo):
    """Ask for one commit and read the last page number out of the Link header
    - far cheaper than walking every commit."""
    r = subprocess.run(
        ["gh", "api", "-i", f"repos/{OWNER}/{repo}/commits?per_page=1"],
        capture_output=True, text=True)
    m = re.search(r'[?&]page=(\d+)>; rel="last"', r.stdout)
    if m:
        return int(m.group(1))
    return 1 if '"sha"' in r.stdout else 0


def render_ledger(path):
    repos = all_repos()
    langs, total = {}, 0
    for r in repos:
        lang = (r.get("primaryLanguage") or {}).get("name") or "other"
        langs[lang] = langs.get(lang, 0) + 1
        total += commit_count(r["name"])
        print(f"    {r['name']}", end="\r", file=sys.stderr)

    svg = path.read_text()

    # "since" is when the work started, not when the oldest repo was pushed to
    # GitHub. Only a human knows that, so keep whatever the SVG already says.
    since = re.search(r'<text class="num"[^>]*>(\d{4})</text>\s*'
                      r'<text class="cap"[^>]*>since<', svg).group(1)

    # One "other" bucket, not two: unlabelled repos join the tail.
    unlabelled = langs.pop("other", 0)
    ranked = sorted(langs.items(), key=lambda kv: -kv[1])
    top, rest = ranked[:5], ranked[5:]
    tail = unlabelled + sum(v for _, v in rest)
    if tail:
        top.append(("other", tail))

    stats = [(len(repos), "repositories"), (langs.get("C", 0), "written in C"),
             (total, "commits")]
    for value, caption in stats:
        svg = re.sub(rf'(<text class="num"[^>]*>)\d+(</text>\s*'
                     rf'<text class="cap"[^>]*>{re.escape(caption)}<)',
                     rf'\g<1>{value}\g<2>', svg)

    svg = re.sub(r'(<desc id="sd">)[^<]*(</desc>)',
                 rf'\g<1>{len(repos)} repositories, {langs.get("C", 0)} written in C, '
                 rf'{total} commits, active since {since}, with a language bar by '
                 rf'repository.\g<2>', svg)
    svg = re.sub(r'(SNAPSHOT )\d{4}-\d{2}-\d{2}', rf'\g<1>{date.today()}', svg)

    # Bar segments and legend, in the same order, scaled to 1080 px.
    x, bar = 60.0, []
    palette = ["#70e1b2", "#f2bd68", "#51c99c", "#9edbc4", "#5fbf9a", "#2f6a63"]
    for i, ((_, n), colour) in enumerate(zip(top, palette)):
        w = 1080.0 * n / len(repos)
        bar.append(f'    <rect x="{x:.1f}" y="150" width="{w:.1f}" height="14" '
                   f'fill="{colour}" style="animation-delay:{0.50 + i * 0.09:.2f}s" '
                   f'class="seg"/>')
        x += w
    bar.append('    <rect class="shine" x="0" y="150" width="260" height="14" '
               'fill="url(#sweep)"/>')
    svg = re.sub(r'( *<rect x="60\.0".*?url\(#sweep\)"/>)', "\n".join(bar), svg,
                 flags=re.S)

    legend, cx = [], 60
    for (name, n), colour in zip(top, palette):
        legend.append(f'  <circle cx="{cx}" cy="187" r="4.5" fill="{colour}"/>'
                      f'<text class="leg" x="{cx + 11}" y="191">{name} {n}</text>')
        cx += 11 + len(f"{name} {n}") * 7.3 + 24
        cx = int(cx)
    # Greedy to the foot line: the legend is several rows and a lazy match
    # would replace only the first, leaving the old ones behind.
    svg = re.sub(r'  <circle cx="60" cy="187".*(?=\n\n  <text class="foot")',
                 "\n".join(legend), svg, flags=re.S)

    path.write_text(svg)
    return len(repos), langs.get("C", 0), total, since


# --------------------------------------------------------------------- main

def splice(path, block):
    text = path.read_text()
    if START not in text or END not in text:
        sys.exit(f"{path} has no {START} / {END} markers")
    head, rest = text.split(START, 1)
    _, tail = rest.split(END, 1)
    path.write_text(f"{head}{START}\n" + "\n".join(block) + f"\n{END}{tail}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stats", action="store_true",
                    help="also refresh the profile ledger from GitHub")
    args = ap.parse_args()

    tree = yaml.safe_load((ROOT / "catalog.yml").read_text())["tree"]

    splice(ROOT / "README.md", catalog_block(tree))
    print(f"catalog:  {ROOT / 'README.md'}")

    if PROFILE.exists():
        splice(PROFILE / "README.md", profile_block(tree))
        print(f"profile:  {PROFILE / 'README.md'}")
        if args.stats:
            n, c, commits, since = render_ledger(PROFILE / "assets" / "ledger.svg")
            print(f"ledger:   {n} repos, {c} in C, {commits} commits, since {since}")
    else:
        print(f"profile:  skipped, {PROFILE} not found")


if __name__ == "__main__":
    main()
