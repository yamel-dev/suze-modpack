# Network modpack (packwiz)

Requirements: packwiz, python 3, git.

## First build (once)
1. Edit the name/author at the top of build-pack.sh (Windows: build-pack.ps1).
2. Run ./build-pack.sh. Fix any slug listed in failed.txt (edit mods.txt, re-run).
3. python make_servers_dat.py "My Server" play.example.com
4. packwiz refresh, then commit everything to the `staging` branch.

## Everyday workflow (edit mods in a launcher)
1. Import the pack's .mrpack into Modrinth App or Prism (your "editing" instance).
2. Add, update or remove mods there with clicks. Test in singleplayer if you like.
3. Export a .mrpack from the launcher.
4. python import_mrpack.py MyPack.mrpack --dry-run   (preview)
   python import_mrpack.py MyPack.mrpack             (apply)
5. New mod? Add it to mods.txt with its side, then: python apply_sides.py
   Server-only mods (LuckPerms, Ledger...) never come from the launcher:
   add or update them with packwiz directly (packwiz update ledger).
6. Bump `version` in pack.toml, packwiz refresh, git diff, commit to `staging`.

mods.txt always decides client/server sides, whatever the launcher says.

## Pinned mods
A third column in mods.txt pins a mod (for example: axiom both 6.0.5).
Pinned mods are never changed by build-pack or import_mrpack.py.
Axiom is pinned to 6.0.5 because DBTools doesn't support newer Axiom versions.
To move a pin: packwiz unpin axiom, packwiz mr add https://modrinth.com/mod/axiom/version/<new>,
packwiz pin axiom, then update the version in mods.txt.

## Custom menus, HUD and loading screen (FancyMenu, Drippy, Spiffy HUD)
Design them in your editing instance, then copy config/fancymenu/ (and config/drippyloadingscreen/,
config/spiffyhud/ if they exist) into this folder's config/. In the copied config/fancymenu/options.txt
set modpack_mode to true so players get no editor, menu bar or hotkeys. Then packwiz refresh.

## Install URLs
Client:  java -jar packwiz-installer-bootstrap.jar <pack.toml URL>
Server:  java -jar packwiz-installer-bootstrap.jar -g -s server <pack.toml URL>
