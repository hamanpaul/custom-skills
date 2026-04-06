# WSL port plan

## Goal

Make the exported Obsidian sync service runnable on this host without orangepi-
specific paths or PicoClaw-specific vault assumptions.

## Porting decisions

- derive `HOME` dynamically instead of hardcoding `/home/haman`
- discover `ob` from the local runtime / NVM installs
- resolve `vaultPath` from `~/.config/obsidian-headless/sync/*/config.json`
- store incidents under `~/.local/state/obsidian-automation/incidents`
- keep Git backup optional and generic

## Target host

- home: `/home/paul_chen`
- vault path: `/home/paul_chen/notes`
- runtime: WSL2 + `systemd --user`
