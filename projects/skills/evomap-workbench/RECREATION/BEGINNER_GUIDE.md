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