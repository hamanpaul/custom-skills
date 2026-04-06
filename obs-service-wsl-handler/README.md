# obs-service-wsl-handler

Host-adapted Obsidian headless sync service for this WSL/Linux machine.

This directory is derived from `custom-claw-tools/obs-service-handler`, but the
scripts here are updated so they can run on the current host without hardcoded
orangepi paths.

## What changed for this host

- No hardcoded `/home/haman`
- No hardcoded Node.js version in `PATH`
- `ob` is discovered from the local environment
- the sync guard pins `node` to the same bin directory as `ob`
- Vault path is resolved from `~/.config/obsidian-headless/sync/*/config.json`
- Incident logs default to `~/.local/state/obsidian-automation/incidents`
- Git backup no longer assumes `~/.picoclaw/workspace/notes`

## Validated host

- user: `paul_chen`
- home: `/home/paul_chen`
- host type: WSL2 with `systemd --user`
- `ob`: `/home/paul_chen/.nvm/versions/node/v22.20.0/bin/ob`
- vault path: `/home/paul_chen/notes`

## Requirements

- Linux with `systemd --user`
- `git`
- Node.js
- `obsidian-headless` (`ob`)
- `~/.config/obsidian-headless/auth_token`
- `~/.config/obsidian-headless/sync/<vault-id>/config.json`

Optional for Git backup:

- usable SSH key / remote access for the configured backup repo

## Install

Copy scripts:

```bash
install -m 755 bin/obsidian_sync_common.sh ~/.local/bin/
install -m 755 bin/obsidian_sync_guard.sh ~/.local/bin/
install -m 755 bin/obsidian_sync_healthcheck.sh ~/.local/bin/
install -m 755 bin/obsidian_git_backup.sh ~/.local/bin/
```

Copy user units:

```bash
install -m 644 systemd/obsidian-sync.service ~/.config/systemd/user/
install -m 644 systemd/obsidian-sync-healthcheck.service ~/.config/systemd/user/
install -m 644 systemd/obsidian-sync-healthcheck.timer ~/.config/systemd/user/
install -m 644 systemd/obsidian-git-backup.service ~/.config/systemd/user/
install -m 644 systemd/obsidian-git-backup.timer ~/.config/systemd/user/
systemctl --user daemon-reload
```

Enable startup execution:

```bash
systemctl --user enable --now obsidian-sync.service
systemctl --user enable --now obsidian-sync-healthcheck.timer
```

Optional:

```bash
systemctl --user enable --now obsidian-git-backup.timer
```

## Verification

```bash
systemctl --user status obsidian-sync.service
systemctl --user status obsidian-sync-healthcheck.timer
tail -f ~/.local/state/obsidian-automation/obsidian-sync-guard.log
tail -f ~/.local/state/obsidian-automation/obsidian-sync-healthcheck.log
systemctl --user start obsidian-sync-healthcheck.service
```

Expected healthy state:

- `obsidian-sync.service` stays active
- healthcheck logs `health ok`
- sync output reaches `Fully synced`

## Startup behavior

- `obsidian-sync.service` starts automatically in the user systemd session
- `obsidian-sync-healthcheck.timer` keeps checking and restarting on transient failures
- On WSL, services live as long as the distro / user systemd session is running
