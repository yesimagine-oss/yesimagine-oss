---
description: Feishu-integrated wrapper for the capability-evolver. Manages the evolution
  loop lifecycle (start/stop/ensure), sends rich Feishu card reports, and provides
  dashboard visualization. Use when running evolver with Feishu reporting or when
  managing the evolution daemon.
name: feishu-evolver-wrapper

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
# Feishu Evolver Wrapper

A lightweight wrapper for the `capability-evolver` skill.
It injects the Feishu reporting environment variables (`EVOLVE_REPORT_TOOL`) to enable rich card reporting in the Master's environment.

## Usage

```bash
# Run the evolution loop
node skills/feishu-evolver-wrapper/index.js

# Generate Evolution Dashboard (Markdown)
node skills/feishu-evolver-wrapper/visualize_dashboard.js

# Lifecycle Management (Start/Stop/Status/Ensure)
node skills/feishu-evolver-wrapper/lifecycle.js status
```

## Architecture

- **Evolution Loop**: Runs the GEP evolution cycle with Feishu reporting.
- **Dashboard**: Visualizing metrics and history from `assets/gep/events.jsonl`.
- **Export History**: Exports raw history to Feishu Docs.
- **Watchdog**: Managed via OpenClaw Cron job `evolver_watchdog_robust` (runs `lifecycle.js ensure` every 10 min).
  - Replaces fragile system crontab logic.
  - Ensures the loop restarts if it crashes or hangs.

## 參考

- [[Final-Skills-Status-Report]]
- [[首发帖子-Github-Skill-安装教程]]
- [[Skills-Installation-Status]]
