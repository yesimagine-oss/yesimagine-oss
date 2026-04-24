---
category: evomap
created_at: '2026-04-20'
tags:
- evomap
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
# 🐳 EvoMap Workbench - Containerized Environment

This directory contains the scientifically optimized, containerized implementation of the EvoMap Workbench, designed for 100% consistent behavior across all platforms.

## 🚀 Quick Start

### Method 1: Docker (Recommended)
```bash
# Build the container
docker build -t evomap-workbench .

# Run with default settings
docker run -d --name evomap-workbench -p 7890:7890 -p 9090:9090 evomap-workbench

# Check logs
docker logs evomap-workbench
```

### Method 2: Docker Compose
```yaml
# docker-compose.yml
version: '3'
services:
  workbench:
    build: .
    ports:
      - "7890:7890"  # Proxy port
      - "9090:9090"  # Clash API
    environment:
      - MOCK_SERVER=true
    volumes:
      - ~/.evomap:/root/.evomap
      - ~/.config/mihomo:/root/.config/mihomo
    restart: unless-stopped
```

## 🔧 Configuration

The container automatically:
- Generates node_id/node_secret on first run
- Configures proxy for China network conditions
- Validates all dependencies
- Starts evolution monitoring system

## 🧪 Verification

Run comprehensive tests:
```bash
# Execute all verification tests
./VERIFICATION/run_all_tests.sh
```

Test results are displayed in real-time. All tests must pass for a successful deployment.

## 📁 Directory Structure
```
RECREATION/
├── Dockerfile             # Container definition
├── config.yaml            # Proxy configuration
├── entrypoint.sh          # Startup script
├── README.md              # This file
└── VERIFICATION/         # Automated testing suite
    ├── test_proxy_connectivity.py
    ├── test_node_credentials.py
    ├── test_dependencies.py
    └── run_all_tests.sh
```

## ✅ Expected Outcomes

| Metric | Target |
|--------|--------|
| First-Time Success Rate | 99.8% |
| Cross-Platform Consistency | 100% |
| Setup Time | <2 minutes |
| Maintenance Effort | Minimal |

## 💡 Pro Tips

1. **For production use**: Remove `MOCK_SERVER` environment variable
2. **To reset credentials**: Delete `~/.evomap/*` and restart
3. **To update**: Pull latest code and rebuild container
4. **For debugging**: Check container logs with `docker logs evomap-workbench`

> "Containerization isn't just technology - it's scientific precision for software deployment." - RedOpenClaw

## 相關文檔

- [[clawbrowser-readme]]
- [[README-proxy-on-demand]]
- [[README-proxy-manager]]
