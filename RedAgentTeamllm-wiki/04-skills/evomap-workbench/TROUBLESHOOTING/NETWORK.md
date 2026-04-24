---
category: evomap
created_at: '2026-04-14'
tags:
- evomap
- network
- issues
- troubleshooting
- guide
- evomap
title: Network
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
# 🌐 Network Issues Troubleshooting

This guide addresses common network connectivity issues specific to the EvoMap Workbench, particularly in China's network environment.

## 🔍 Diagnostic Flowchart
```
Start → Can access evomap.ai directly?
        ├── Yes → Check local firewall/proxy settings
        └── No → Use proxy (Clash)
                ├── Proxy working? → Verify node credentials
                └── Proxy not working → Follow steps below
```

## 🛠 Common Issues & Solutions

### Issue 1: Proxy Not Starting
**Symptoms**: `Connection refused` or `Network unreachable`

**Solutions**:
```bash
# 1. Check if Clash is running
grep clash /etc/passwd || echo "Clash not found"
ps aux | grep clash

# 2. Restart Clash manually
pkill clash
clash -d ~/.config/mihomo &

# 3. Test connectivity
curl --proxy http://127.0.0.1:7890 https://evomap.ai
```

### Issue 2: Authentication Failed
**Symptoms**: `401 Unauthorized` when accessing EvoMap API

**Solutions**:
```bash
# 1. Verify credential files exist
ls -la ~/.evomap/

cat ~/.evomap/node_id

cat ~/.evomap/node_secret

# 2. Regenerate credentials if missing/corrupted
rm ~/.evomap/*
# Restart container or run entrypoint.sh to regenerate
```

### Issue 3: Slow Connection Through Proxy
**Symptoms**: High latency (>1000ms) or timeouts

**Solutions**:
1. **Check server status**: Visit https://status.evo-map.com
2. **Switch proxy servers**: Edit `~/.config/mihomo/config.yaml`
3. **Test alternative routes**: 
   ```bash
   curl -m 5 --proxy http://127.0.0.1:7890 https://evomap.ai
   ```

### Issue 4: DNS Resolution Failure
**Symptoms**: `Could not resolve host` errors

**Solutions**:
```bash
# 1. Test DNS resolution
nslookup evomap.ai

# 2. Try different DNS servers
echo 'nameserver 1.1.1.1' | sudo tee /etc/resolv.conf

# 3. Configure Clash DNS
# In config.yaml, set:
dns:
  enable: true
  listen: 0.0.0.0:53
  enhanced-mode: fake-ip
  nameserver:
    - 1.1.1.1
    - 8.8.8.8
```

## 🧪 Verification Commands

### Test Proxy Connectivity
```bash
# Test basic proxy function
curl --proxy http://127.0.0.1:7890 -I https://evomap.ai

# Test with timeout
timeout 10 curl --proxy http://127.0.0.1:7890 https://evomap.ai

# Test multiple endpoints
for url in https://evomap.ai https://clawhub.com; do
    echo "Testing $url..."
    curl --proxy http://127.0.0.1:7890 -s -o /dev/null -w "%{http_code} % {url_effective}\n" "$url"
done
```

### Check Active Connections
```bash
# List all connections on proxy port
ss -tuln | grep 7890

# Monitor real-time traffic
sudo netstat -an | grep :7890
```

## 📋 Troubleshooting Checklist

| Step | Command | Expected Result |
|------|---------|-----------------|
| 1 | `ps aux \| grep clash` | Clash process running |
| 2 | `netstat -an \| grep 7890` | Port 7890 LISTENING |
| 3 | `cat ~/.evomap/node_id` | Valid hex string (>32 chars) |
| 4 | `curl --proxy http://127.0.0.1:7890 https://evomap.ai` | HTTP 200 response |
| 5 | `python3 VERIFICATION/test_proxy_connectivity.py` | All tests PASSED |

> **Note**: For persistent issues, use the containerized version which handles network configuration automatically.

## 💡 Pro Tips

1. **Preventative Maintenance**: Run weekly connectivity tests
2. **Log Monitoring**: Check `~/.openclaw/logs/` for error patterns
3. **Performance Tuning**: Adjust Clash buffer sizes in config.yaml
4. **Fallback Strategy**: Keep a mobile hotspot as backup internet

> "The best network troubleshooting tool is prevention through proper configuration." - RedOpenClaw

## 參考

- [[EvoMap 用戶手冊]]
- [[OpenClaw 完全指南]]
