#!/usr/bin/env python3
"""Syncs this packwiz pack with a .mrpack exported from the Modrinth App or Prism.

  python import_mrpack.py MyPack.mrpack            # apply
  python import_mrpack.py MyPack.mrpack --dry-run  # only show what would change

Every mod is pinned to the exact version chosen in the launcher. Mods removed in
the launcher are removed from the pack, except server-only mods (launchers never
install those, so they are kept and updated with `packwiz update <name>`). Pinned mods (pin = true) are never changed. Sides are then enforced from mods.txt.
Config files inside the .mrpack are ignored: configs live in the config repo."""
import json, pathlib, re, subprocess, sys, zipfile

if len(sys.argv) < 2:
    print(__doc__); sys.exit(1)
mrpack, dry = sys.argv[1], "--dry-run" in sys.argv
URL_RE = re.compile(r"cdn\.modrinth\.com/data/([A-Za-z0-9]+)/versions/([A-Za-z0-9]+)/")

def run(cmd):
    print("  $", " ".join(cmd))
    if not dry:
        subprocess.run(cmd, check=False)

with zipfile.ZipFile(mrpack) as z:
    index = json.loads(z.read("modrinth.index.json"))

wanted, skipped = {}, []
for f in index.get("files", []):
    m = next((URL_RE.search(u) for u in f.get("downloads", []) if URL_RE.search(u)), None)
    if m:
        wanted[m.group(1)] = (m.group(2), f["path"])
    else:
        skipped.append(f["path"])

current = {}
for folder in ("mods", "resourcepacks", "shaderpacks"):
    d = pathlib.Path(folder)
    for t in d.glob("*.pw.toml") if d.exists() else []:
        text = t.read_text()
        mid = re.search(r'(?m)^mod-id = "([^"]+)"', text)
        ver = re.search(r'(?m)^version = "([^"]+)"', text)
        pinned = re.search(r'(?m)^pin = true', text) is not None
        if mid:
            current[mid.group(1)] = (ver.group(1) if ver else None, t, pinned)

print(f"Launcher pack: {len(wanted)} Modrinth files. Packwiz pack: {len(current)}.")
for pid, (vid, path) in sorted(wanted.items(), key=lambda x: x[1][1]):
    if pid in current and current[pid][0] == vid:
        continue
    if pid in current and current[pid][2]:
        name = current[pid][1].name[:-len(".pw.toml")]
        print(f"[pinned] {name}: launcher has a different version, keeping the pinned one")
        continue
    action = "update" if pid in current else "add"
    print(f"[{action}] {path}")
    run(["packwiz", "-y", "modrinth", "add", "--project-id", pid, "--version-id", vid])

# Launchers don't install server-only mods, so they never appear in the export.
# Never remove anything mods.txt marks as "server".
server_only = set()
mods_txt = pathlib.Path("mods.txt")
if mods_txt.exists():
    for line in mods_txt.read_text().splitlines():
        line = line.split("#", 1)[0].split()
        if len(line) >= 2 and line[1] == "server":
            server_only.add(line[0].lower())

for pid, (vid, t, pinned) in current.items():
    if pid not in wanted:
        name = t.name[:-len(".pw.toml")]
        if pinned:
            print(f"[keep]   {name} (pinned; unpin with: packwiz unpin {name})")
            continue
        if name.lower() in server_only:
            print(f"[keep]   {name} (server-only, update it with: packwiz update {name})")
            continue
        print(f"[remove] {name}")
        run(["packwiz", "remove", name])

if skipped:
    print("\nNot from Modrinth, add these by hand:")
    for p in skipped: print("  -", p)

if not dry:
    subprocess.run([sys.executable, "apply_sides.py"])
    subprocess.run(["packwiz", "refresh"])
print("\nDone. Review with `git diff`, then commit to the staging branch.")
