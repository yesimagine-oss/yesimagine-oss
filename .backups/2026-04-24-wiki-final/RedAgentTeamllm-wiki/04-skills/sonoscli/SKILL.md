---
name: sonoscli
description: Control Sonos speakers (discover/status/play/volume/group).
homepage: https://sonoscli.sh
metadata: {"clawdbot":{"emoji":"🔊","requires":{"bins":["sonos"]},"install":[{"id":"go","kind":"go","module":"github.com/steipete/sonoscli/cmd/sonos@latest","bins":["sonos"],"label":"Install sonoscli (go)"}]}}

# Provenance
provenance:
  source_url: "internal"
  captured_at: "2026-04-20"
  verified_by: "Red Agent Team"
  verification_method: "auto"
  trust_score: 0.95

# Trust Boundary
trust_level: "llm+verified"
evidence_level: "原文 + 實測"
---
# Sonos CLI

Use `sonos` to control Sonos speakers on the local network.

Quick start
- `sonos discover`
- `sonos status --name "Kitchen"`
- `sonos play|pause|stop --name "Kitchen"`
- `sonos volume set 15 --name "Kitchen"`

Common tasks
- Grouping: `sonos group status|join|unjoin|party|solo`
- Favorites: `sonos favorites list|open`
- Queue: `sonos queue list|play|clear`
- Spotify search (via SMAPI): `sonos smapi search --service "Spotify" --category tracks "query"`

Notes
- If SSDP fails, specify `--ip <speaker-ip>`.
- Spotify Web API search is optional and requires `SPOTIFY_CLIENT_ID/SECRET`.

## 參考

- [[Final-Skills-Status-Report]]
- [[首发帖子-Github-Skill-安装教程]]
- [[Skills-Installation-Status]]
