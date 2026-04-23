---
category: llm
created_at: '2026-04-20'
tags:
- llm
- auto-generated
title: Readme
type: article
version: '1.0'

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
# agent-browser Daemon Benchmarks

Compares command latency and system metrics between the **Node.js daemon** (published npm version) and the **Rust native daemon** (built from source), running inside a [Vercel Sandbox](https://vercel.com/docs/sandbox) microVM.

## What it measures

**Command latency** -- per-scenario timing with warmup, multiple iterations, and stddev:

- `navigate` -- page load round-trip
- `snapshot` -- accessibility tree generation
- `screenshot` -- viewport capture
- `evaluate` -- JavaScript execution
- `click` -- element interaction
- `fill` -- form input
- `agent-loop` -- snapshot/click/snapshot cycle (typical AI agent pattern)
- `full-workflow` -- realistic 7-command sequence

**System metrics** -- collected while the daemon is running:

- Cold start time (daemon spawn + browser launch)
- Binary size and total distribution size (including browser download)
- Daemon RSS and peak RSS (separated from browser process memory)
- Browser RSS (Chrome processes, same for both daemons)
- Daemon CPU time
- Process counts

## Prerequisites

- Node.js 18+
- pnpm
- Vercel Sandbox credentials (token, team ID, project ID)

## Setup

```bash
cd benchmarks
pnpm install
cp .env.example .env
```

Fill in your Vercel Sandbox credentials in `.env`:

```
SANDBOX_VERCEL_TOKEN=your_token
SANDBOX_VERCEL_TEAM_ID=your_team_id
SANDBOX_VERCEL_PROJECT_ID=your_project_id
```

## Usage

```bash
pnpm bench                             # 10 iterations, 1 warmup, 8 vCPUs
pnpm bench -- --iterations 20          # more iterations for tighter stats
pnpm bench -- --warmup 2               # extra warmup iterations
pnpm bench -- --json                   # write results.json
pnpm bench -- --branch main            # build native from a different branch
pnpm bench -- --vcpus 16               # more vCPUs (faster Rust build)
```

## How it works

1. Creates a Vercel Sandbox (Amazon Linux, configurable vCPUs)
2. Installs Chromium system dependencies
3. **Phase 1 -- Node.js daemon**: installs `agent-browser` from npm (last version with the Node daemon), runs all scenarios, collects metrics
4. **Phase 2 -- Rust native daemon**: installs Rust toolchain, clones the repo, runs `cargo build --release`, replaces the binary, runs the same scenarios, collects metrics
5. Prints comparison tables and optionally writes `results.json`

## Interpreting results

**Command latency** is dominated by Chrome (CDP round-trips), not the daemon. Both daemons are thin relays between the CLI and Chrome, so per-command speedups are typically small. The stddev column helps distinguish real differences from noise.

**Where the native daemon wins** is in cold start (no Node.js runtime to boot), daemon memory (single Rust binary vs V8 heap), and distribution size (no Playwright dependency).

The **daemon RSS** metric isolates the daemon process memory from Chrome. This is the apples-to-apples comparison -- both daemons talk to the same Chrome, but Node.js adds ~140 MB of V8 overhead while the Rust daemon uses ~7 MB.

**Distribution size** includes the daemon plus its browser download. The Node version includes the npm package + Playwright's bundled Chromium. The Rust version is just the binary + Chrome for Testing.


## 相關文檔

- [[clawbrowser-readme]]
- [[README-proxy-on-demand]]
- [[README-proxy-manager]]
