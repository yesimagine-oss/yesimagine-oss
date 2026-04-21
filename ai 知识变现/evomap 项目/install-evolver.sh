#!/bin/bash
# EvoMap Evolver 一键安装脚本
# 自动安装、配置并启动 evolver

echo ""
echo "============================================================"
echo "🚀 EvoMap Evolver 一键安装"
echo "============================================================"
echo ""

# ========== 步骤 1: 检查 Node.js ==========
echo "📋 步骤 1: 检查 Node.js..."
echo "------------------------------------------------------------"

if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    echo "✅ Node.js: $NODE_VERSION"
else
    echo "❌ Node.js 未安装！"
    echo ""
    echo "请先安装 Node.js 18+:"
    echo "  访问：https://nodejs.org/"
    echo "  或运行：curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -"
    exit 1
fi

echo ""

# ========== 步骤 2: 安装 evolver ==========
echo "📦 步骤 2: 安装 evolver..."
echo "------------------------------------------------------------"

# 全局安装
npm install -g @evomap/evolver

if [ $? -eq 0 ]; then
    echo "✅ evolver 安装成功！"
    evolver --version
else
    echo "❌ evolver 安装失败！"
    echo ""
    echo "可能原因:"
    echo "  1. 网络问题（需要代理）"
    echo "  2. npm 权限问题"
    echo ""
    echo "解决方案:"
    echo "  方案 1: 使用 sudo"
    echo "    sudo npm install -g @evomap/evolver"
    echo ""
    echo "  方案 2: 修复 npm 权限"
    echo "    mkdir ~/.npm-global"
    echo "    npm config set prefix '~/.npm-global'"
    echo "    echo 'export PATH=~/.npm-global/bin:\$PATH' >> ~/.bashrc"
    echo "    source ~/.bashrc"
    exit 1
fi

echo ""

# ========== 步骤 3: 配置环境变量 ==========
echo "🔧 步骤 3: 配置环境变量..."
echo "------------------------------------------------------------"

# 检查是否已配置
if grep -q "EVOMAP_NODE_ID" ~/.bashrc; then
    echo "⚠️  环境变量已存在，跳过配置"
else
    echo "export EVOMAP_NODE_ID='node_67c3b8b37becd262'" >> ~/.bashrc
    echo "export EVOMAP_NODE_SECRET='bcc7b8e55de75908ae237155cf52a11ac8925b42931e29ea0882b1d456fc7c3a'" >> ~/.bashrc
    echo "✅ 环境变量已添加到 ~/.bashrc"
fi

# 立即生效
export EVOMAP_NODE_ID='node_67c3b8b37becd262'
export EVOMAP_NODE_SECRET='bcc7b8e55de75908ae237155cf52a11ac8925b42931e29ea0882b1d456fc7c3a'

echo "✅ 环境变量已配置"
echo "   EVOMAP_NODE_ID: $EVOMAP_NODE_ID"
echo ""

# ========== 步骤 4: 启动 evolver ==========
echo "🚀 步骤 4: 启动 evolver..."
echo "------------------------------------------------------------"

# 创建日志目录
mkdir -p /home/admin/.openclaw/workspace/ai\ 知识变现/evomap\ 项目/logs

# 后台启动 evolver
echo "后台启动 evolver..."
nohup evolver start > /home/admin/.openclaw/workspace/ai\ 知识变现/evomap\ 项目/logs/evolver.log 2>&1 &

EVOLVER_PID=$!
echo "✅ evolver 已启动（PID: $EVOLVER_PID）"
echo ""

# 等待 5 秒
echo "等待 evolver 初始化..."
sleep 5

# 检查日志
echo ""
echo "📝 最新日志:"
echo "------------------------------------------------------------"
tail -20 /home/admin/.openclaw/workspace/ai\ 知识变现/evomap\ 项目/logs/evolver.log

echo ""
echo "============================================================"
echo "✅ evolver 安装完成！"
echo "============================================================"
echo ""
echo "📊 状态检查:"
echo "  1. 访问：https://evomap.ai/agents/node_67c3b8b37becd262"
echo "  2. 刷新页面，应该显示 'active' 或 'online'"
echo ""
echo "📝 日志文件:"
echo "  /home/admin/.openclaw/workspace/ai 知识变现/evomap 项目/logs/evolver.log"
echo ""
echo "🛑 停止 evolver:"
echo "  kill $EVOLVER_PID"
echo "  或 evolver stop"
echo ""
echo "🔄 重启 evolver:"
echo "  evolver restart"
echo ""
echo "📋 查看状态:"
echo "  evolver status"
echo ""
echo "============================================================"
echo ""
