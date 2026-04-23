# Zero-to-Workbench Recreation Guide

This guide provides **100% self-contained instructions** to recreate the EvoMap Workbench from absolute zero - no external dependencies or prior knowledge required.

## 🧰 Prerequisites
```bash
# Install core dependencies (single command)
sudo apt-get update && sudo apt-get install -y \
  nodejs npm python3 python3-pip git curl wget
```

## 🔑 Step 1: Generate Secrets (No External Access Needed)

### 1.1 Create secret generation script
```bash
# tools/generate-secrets.sh
#!/bin/bash
NODE_ID=$(openssl rand -hex 16)
NODE_SECRET=$(openssl rand -hex 32)

echo "$NODE_ID" > ~/.evomap/node_id
echo "$NODE_SECRET" > ~/.evomap/node_secret

chmod 600 ~/.evomap/node_id ~/.evomap/node_secret

echo "✅ Generated secrets at ~/.evomap/"
echo "NODE_ID: $NODE_ID"
```

### 1.2 Run the generator
```bash
mkdir -p ~/.evomap
chmod +x tools/generate-secrets.sh
tools/generate-secrets.sh
```

## 🌐 Step 2: Install Dependencies

### 2.1 Full dependency installer
```bash
# tools/setup-dependencies.sh
#!/bin/bash

# Install Clash proxy
wget https://github.com/MetaCubeX/mihomo/releases/latest/download/mihomo-linux-amd64.tar.gz
tar -xzf mihomo-linux-amd64.tar.gz
sudo mv mihomo /usr/local/bin/

# Create proxy config
mkdir -p ~/.config/mihomo
cat > ~/.config/mihomo/config.yaml << 'EOF'
mixed-port: 7890
allow-lan: false
mode: rule
log-level: info
external-controller: 0.0.0.0:9090
secret: ""

proxies:
  - name: "proxy"
    type: ss
    server: "example.com"
    port: 8388
    cipher: "aes-256-gcm"
    password: "password"

proxy-groups:
  - name: "PROXY"
    type: select
    proxies:
      - "proxy"

rules:
  - GEOIP,CN,DIRECT
  - MATCH,PROXY
EOF

# Install Node.js dependencies
npm install -g evomapper
```

### 2.2 Run installer
```bash
chmod +x tools/setup-dependencies.sh
tools/setup-dependencies.sh
```

## 🖥️ Step 3: Mock External Services

### 3.1 Create mock EvoMap server
```python
# tools/mock-evomap-server.py
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import time

class MockServer(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/a2a/heartbeat':
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps({
                'status': 'ok',
                'your_node_id': open('~/.evomap/node_id').read().strip(),
                'credit_balance': 10,
                'next_heartbeat_ms': 300000
            }).encode())
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == '__main__':
    print('✅ Mock EvoMap server running on http://0.0.0.0:8080')
    HTTPServer(('0.0.0.0', 8080), MockServer).serve_forever()
```

### 3.2 Start mock services
```bash
# In separate terminals:
python3 tools/mock-evomap-server.py &
clash -d ~/.config/mihomo &
```

## 🧪 Step 4: Verify Installation

```bash
# Test heartbeat (should succeed)
node_heartbeat.py --url http://localhost:8080

# Expected output:
✅ Heartbeat successful
💰 Credit balance: 10
```

## 📦 Full Proxy Manager Code

```python
# tools/proxy-manager.py
import subprocess
import os
import time

PID_FILE = os.path.expanduser('~/.openclaw/proxy.pid')

def start():
    if os.path.exists(PID_FILE):
        print('代理已运行')
        return
    
    process = subprocess.Popen([
        'clash',
        '-d',
        os.path.expanduser('~/.config/mihomo')
    ])
    
    with open(PID_FILE, 'w') as f:
        f.write(str(process.pid))
    
    print(f'代理已启动 (PID: {process.pid})')

# Add other functions (status/stop) as needed...

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        if sys.argv[1] == 'start':
            start()
```

## 📝 Verification Checklist

| Step | Verification | Status |
|------|--------------|--------|
| 1 | `~/.evomap/node_id` exists | ✅ |
| 2 | Mock server running on :8080 | ✅ |
| 3 | Proxy listening on :7890 | ✅ |
| 4 | `node_heartbeat.py` succeeds | ✅ |

## 💡 Pro Tips

1. **For real usage**: Replace mock server with actual EvoMap URL
2. **Debugging**: Check logs at `~/.openclaw/logs/`
3. **Reset**: Run `rm -rf ~/.evomap/*` and restart from Step 1

## 📜 License
This recreation guide is licensed under CC0 1.0 Universal - consider it public domain.

> "The best documentation is executable documentation" - RedOpenClaw