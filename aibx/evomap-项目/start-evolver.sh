#!/bin/bash
# EvoMap Evolver 启动脚本（带完整配置）

cd /home/admin/.openclaw/workspace/ai\ 知识变现/evomap\ 项目

# 停止旧进程
kill $(cat evolver.pid 2>/dev/null) 2>/dev/null
rm -f evolver.pid
sleep 2

# 配置环境变量
export A2A_NODE_ID='node_67c3b8b37becd262'
export A2A_NODE_SECRET='8cad4ac975ba7408b9c96f66c2dcfd3e2cd6479e84519a976b111f459858ef86'
export EVOMAP_HUB_URL='https://evomap.ai'
export EVOMAP_MEMORY_DIR='/home/admin/.openclaw/workspace/ai 知识变现/evomap 项目/memory'

echo "   A2A_NODE_ID: $A2A_NODE_ID"

# 创建必要目录
mkdir -p memory
mkdir -p logs

# 启动 evolver
echo "🚀 启动 evolver..."
echo "   Node ID: $EVOMAP_NODE_ID"
echo "   Hub URL: $EVOMAP_HUB_URL"
echo ""

nohup evolver run --loop > logs/evolver.log 2>&1 &

EVOLVER_PID=$!
echo $EVOLVER_PID > evolver.pid

echo "✅ evolver 已启动 (PID: $EVOLVER_PID)"
echo ""
echo "📝 日志：logs/evolver.log"
echo "🛑 停止：kill $EVOLVER_PID 或 rm evolver.pid"
echo ""
echo "等待 10 秒查看初始日志..."
sleep 10
tail -50 logs/evolver.log
