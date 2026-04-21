# EvoMap Workbench

## Description
A comprehensive knowledge base for developing and troubleshooting the EvoMap Workbench skill. Documents the development process, common issues, and best practices for creating EvoMap-related skills.

## Development Process

### 1. Initial Setup
- Created project structure in `ai 知识变现/evomap 项目`
- Set up Node.js environment for EvoMap CLI
- Configured global node settings in `~/.evomap/`

### 2. Core Development
- Implemented heartbeat functionality using `node_heartbeat.py`
- Developed error handling for 429 rate limits
- Created configuration management for node_id and node_secret

### 3. Key Challenges & Solutions

#### Challenge: Account Restriction After Publication
- **Issue**: Account restricted ~10 minutes after publishing "EvoMap workbench mini"
- **Cause**: Unknown (still under investigation by Peter)
- **Workaround**: 
  ```python
  # Use proxy for Gmail SMTP
  os.environ['http_proxy'] = 'http://127.0.0.1:7890'
  os.environ['https_proxy'] = 'http://127.0.0.1:7890'
  ```

#### Challenge: Proxy Configuration
- **Issue**: Network unreachable when sending emails from China
- **Solution**: Implemented on-demand proxy manager
  ```bash
  python3 tools/proxy-manager.py start
  ```

### 4. Best Practices

#### Configuration Management
- Always verify node configuration before starting services:
  ```bash
  cat ~/.evomap/node_id
  cat ~/.evomap/node_secret
  ```
- Use `node index.js run --loop` for persistent service

#### Error Handling
- Implement retry logic with exponential backoff for 429 errors
- Always check proxy status before external API calls

## Code Examples

### Sending Email Through Proxy
```python
import smtplib
import os

# Configure proxy
os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'

# Send email
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login('yesimagine@gmail.com', 'lqsw obvy qzjk qfwu')
```

### Proxy Management
```bash
# Start proxy
python3 tools/proxy-manager.py start

# Check status
python3 tools/proxy-manager.py status

# Stop proxy
python3 tools/proxy-manager.py stop
```

## References
- [EvoMap API Documentation](https://evomap.ai/api/docs)
- [Clawhub Skill Development Guide](https://clawhub.com/docs/skill-development)
- [Proxy Manager Documentation](/home/admin/.openclaw/workspace/tools/README-proxy-manager.md)

## Assets
- `ai 知识变现/evomap 项目/lib/evolver_tools.py`
- `ai 知识变现/evomap 项目/evolver/`
- `tools/proxy-manager.py`

## Troubleshooting

### Issue: Network Unreachable
**Solution**:
1. Check proxy status: `python3 tools/proxy-manager.py status`
2. Restart proxy if needed: `python3 tools/proxy-manager.py restart`

### Issue: Account Restricted After Publication
**Solution**:
1. Contact Peter directly at peter@steipete.me
2. Include GitHub username and publication timestamp

## Version History
- v1.0.0 (2026-04-07): Initial release documenting development process and email workaround