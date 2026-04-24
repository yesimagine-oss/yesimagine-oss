---
category: evomap
created_at: '2026-04-14'
tags:
- evomap
- evomap
- workbench
- beginner
- guide
- config
title: Beginner Guide
type: general
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
# 🐣 EvoMap Workbench - Beginner's Guide

## First 5 Minutes
```bash
# 1. Clone repository
git clone https://github.com/your-repo/evomap-workbench.git

# 2. Build container (takes ~3 minutes)
docker build -t evomap-workbench .

# 3. Run with auto-configuration
docker run -d -p 7890:7890 evomap-workbench

# 4. Verify
curl --proxy http://localhost:7890 https://evomap.ai
```

## Common Tasks
| Command | Purpose |
|---------|---------|
| `docker exec workbench evomapper status` | Check node status |
| `./VERIFICATION/run_all_tests.sh` | Run all checks |
| `vim ~/.config/mihomo/config.yaml` | Edit proxy settings |

## Troubleshooting
```bash
# Reset everything
docker stop evomap-workbench && docker rm evomap-workbench
rm -rf ~/.evomap/*
```

## 參考

- [[EvoMap 用戶手冊]]
- [[OpenClaw 完全指南]]


## 相關文檔

- [[INSTALL-VALIDATOR-GUIDE]]
- [[21-user_guide_image_analysis_skill]]
- [[session-manager-ai-guide]]
