#!/bin/bash
# entrypoint.sh - Container startup script for EvoMap Workbench

set -e  # Exit on any error

# Create required directories
mkdir -p ~/.evomap
mkdir -p ~/.config/mihomo

# Generate node_id and node_secret if they don't exist
if [ ! -f ~/.evomap/node_id ] || [ ! -f ~/.evomap/node_secret ]; then
    echo "🔐 Generating new node credentials..."
    NODE_ID=$(openssl rand -hex 16)
    NODE_SECRET=$(openssl rand -hex 32)
    
    echo "$NODE_ID" > ~/.evomap/node_id
    echo "$NODE_SECRET" > ~/.evomap/node_secret
    
    chmod 600 ~/.evomap/node_id ~/.evomap/node_secret
    
    echo "✅ Generated new node credentials"
    echo "Node ID: $NODE_ID"
fi

# Ensure config.yaml exists
if [ ! -f ~/.config/mihomo/config.yaml ]; then
    echo "🔧 Copying default proxy configuration"
    cp /app/RECREATION/config.yaml ~/.config/mihomo/config.yaml
fi

# Start Clash proxy in background
echo "🚀 Starting Clash proxy..."
clash -d ~/.config/mihomo &
CLASH_PID=$!

# Wait for proxy to be ready
echo "⏱️ Waiting for proxy to initialize..."
sleep 5

# Test proxy connectivity
echo "📡 Testing proxy connectivity..."
if curl --proxy http://127.0.0.1:7890 -m 10 -I https://evomap.ai > /dev/null 2>&1; then
    echo "✅ Proxy is working correctly"
else
    echo "❌ Proxy test failed"
    exit 1
fi

# Run validation checks
echo "🔍 Running system validation..."
python3 tools/validators/proxy_validator.py
python3 tools/validators/node_validator.py
python3 tools/validators/dependency_validator.py

# Start evolution monitor
echo "🧠 Starting evolution monitoring..."
python3 tools/evolution_monitor.py &
EVOLUTION_PID=$!

# Start mock server for development/testing
if [ "$MOCK_SERVER" = "true" ]; then
    echo "🧪 Starting mock EvoMap server..."
    python3 tools/mock-evomap-server.py &
fi

# Keep container running
echo "✅ EvoMap Workbench is ready!"
echo "Proxy available on port 7890"
echo "Clash API on port 9090"

# Trap SIGTERM and SIGINT to stop background processes
trap 'kill $CLASH_PID $EVOLUTION_PID; exit' TERM INT

# Wait indefinitely (keep container alive)
tail -f /dev/null