#!/bin/bash
# 生产环境一键配置脚本
# 自动配置 GITHUB_TOKEN 和 PostgreSQL

echo "============================================================"
echo "🚀 生产环境一键配置"
echo "============================================================"
echo ""

# ========== 1. 检查环境 ==========
echo "📋 步骤 1: 检查环境..."
echo "------------------------------------------------------------"

# 检查 Node.js
if command -v node &> /dev/null; then
    echo "✅ Node.js: $(node --version)"
else
    echo "❌ Node.js 未安装，请先安装 Node.js 18+"
    exit 1
fi

# 检查 Python
if command -v python3 &> /dev/null; then
    echo "✅ Python3: $(python3 --version)"
else
    echo "❌ Python3 未安装"
    exit 1
fi

# 检查 psql
if command -v psql &> /dev/null; then
    echo "✅ PostgreSQL 客户端：已安装"
else
    echo "⚠️  PostgreSQL 客户端未安装"
    echo "   安装命令：sudo apt-get install postgresql-client"
fi

echo ""

# ========== 2. 创建 GITHUB_TOKEN 配置 ==========
echo "🔑 步骤 2: 配置 GITHUB_TOKEN..."
echo "------------------------------------------------------------"

# 检查是否已配置
if [ -n "$GITHUB_TOKEN" ]; then
    echo "✅ GITHUB_TOKEN 已配置"
    echo "   测试连接..."
    curl -s -H "Authorization: token $GITHUB_TOKEN" https://api.github.com/user | grep -q "login" && echo "   ✅ GitHub API 连接成功" || echo "   ❌ GitHub API 连接失败"
else
    echo "⚠️  GITHUB_TOKEN 未配置"
    echo ""
    echo "请按以下步骤创建和配置："
    echo "1. 访问：https://github.com/settings/tokens"
    echo "2. 点击 'Generate new token (classic)'"
    echo "3. 选择 scopes: repo, workflow, read:org"
    echo "4. 生成 token，复制 token 值"
    echo "5. 添加到 ~/.bashrc:"
    echo ""
    echo "   export GITHUB_TOKEN='ghp_xxxxxxxxxxxx'"
    echo ""
    echo "6. 生效：source ~/.bashrc"
    echo ""
    read -p "是否现在打开 GitHub Token 页面？(y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "🌐 请在浏览器中打开：https://github.com/settings/tokens"
    fi
fi

echo ""

# ========== 3. 配置 PostgreSQL ==========
echo "🗄️  步骤 3: 配置 PostgreSQL..."
echo "------------------------------------------------------------"

# 检查是否已配置
if [ -n "$DATABASE_URL" ]; then
    echo "✅ DATABASE_URL 已配置"
    echo "   测试连接..."
    psql $DATABASE_URL -c "SELECT version();" &> /dev/null && echo "   ✅ PostgreSQL 连接成功" || echo "   ❌ PostgreSQL 连接失败"
else
    echo "⚠️  DATABASE_URL 未配置"
    echo ""
    echo "请按以下步骤配置："
    echo "1. 安装 PostgreSQL 客户端（如果未安装）:"
    echo "   sudo apt-get update && sudo apt-get install postgresql-client"
    echo ""
    echo "2. 创建数据库:"
    echo "   psql -U postgres"
    echo "   CREATE DATABASE evomap;"
    echo "   CREATE USER evomap_user WITH PASSWORD 'your_password';"
    echo "   GRANT ALL PRIVILEGES ON DATABASE evomap TO evomap_user;"
    echo "   \\q"
    echo ""
    echo "3. 配置连接字符串:"
    echo "   export DATABASE_URL='postgresql://evomap_user:your_password@localhost:5432/evomap'"
    echo ""
    echo "4. 添加到 ~/.bashrc 永久生效"
    echo ""
fi

echo ""

# ========== 4. 创建 .env 文件 ==========
echo "📝 步骤 4: 创建 .env 文件..."
echo "------------------------------------------------------------"

ENV_FILE="/home/admin/.openclaw/workspace/ai 知识变现/evomap 项目/.env"

cat > $ENV_FILE << EOF
# EvoMap 生产环境配置
# 创建时间：$(date '+%Y-%m-%d %H:%M:%S')

# GitHub Token
# 获取：https://github.com/settings/tokens
GITHUB_TOKEN='ghp_xxxxxxxxxxxx'

# PostgreSQL 连接
# 格式：postgresql://user:password@host:port/database
DATABASE_URL='postgresql://evomap_user:your_password@localhost:5432/evomap'

# EvoMap 配置
EVOMAP_API_KEY='bcc7b8e55de75908ae237155cf52a11ac8925b42931e29ea0882b1d456fc7c3a'
EVOMAP_NODE_ID='node_67c3b8b37becd262'
EOF

echo "✅ .env 文件已创建：$ENV_FILE"
echo ""
echo "⚠️  请编辑 .env 文件，填入真实的 GITHUB_TOKEN 和 DATABASE_URL"
echo ""

# ========== 5. 测试 Production Agent ==========
echo "🧪 步骤 5: 测试 Production Agent..."
echo "------------------------------------------------------------"

cd /home/admin/.openclaw/workspace/ai\ 知识变现/evomap\ 项目

# 加载环境变量
if [ -f .env ]; then
    echo "📂 加载 .env 文件..."
    export $(grep -v '^#' .env | xargs)
fi

# 创建日志目录
mkdir -p logs

# 运行测试
echo "🚀 运行 Production Agent 测试..."
python3 agent-hooks/production-agent.py

echo ""
echo "============================================================"
echo "✅ 配置完成！"
echo "============================================================"
echo ""
echo "下一步:"
echo "1. 编辑 .env 文件，填入真实的 GITHUB_TOKEN 和 DATABASE_URL"
echo "2. 运行：source ~/.bashrc"
echo "3. 测试：python3 agent-hooks/production-agent.py"
echo ""
