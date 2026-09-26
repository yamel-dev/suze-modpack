#!/usr/bin/env python3
"""Forces the client/server side of every mod listed in mods.txt, and reports
mods in the pack that mods.txt doesn't mention (they keep Modrinth's default side)."""
import pathlib, re, sys

root = pathlib.Path(".")
sides = {}
for line in (root / "mods.txt").read_text().splitlines():
    line = line.split("#", 1)[0].strip()
    if line:
        slug, side = line.split()[:2]
        sides[slug.lower()] = side

files = {}
for folder in ("mods", "resourcepacks", "shaderpacks"):
    for f in (root / folder).glob("*.pw.toml") if (root / folder).exists() else []:
        files[f.name[:-len(".pw.toml")].lower()] = f

missing_in_pack, unknown = [], []
for slug, side in sides.items():
    f = files.get(slug)
    if not f:
        missing_in_pack.append(slug); continue
    text = f.read_text()
    new = re.sub(r'(?m)^side = ".*"$', f'side = "{side}"', text)
    if 'side = ' not in text:
        new = new.replace("\n[download]", f'\nside = "{side}"\n\n[download]', 1)
    f.write_text(new)

for slug in files:
    if slug not in sides:
        unknown.append(slug)

if missing_in_pack:
    print("In mods.txt but not in the pack (wrong slug, or not added yet):")
    for s in missing_in_pack: print("  -", s)
if unknown:
    print("In the pack but not in mods.txt (add them with a side, then re-run):")
    for s in unknown: print("  -", s)
if not missing_in_pack and not unknown:
    print("Sides applied. mods.txt and the pack match.")
sys.exit(0)
