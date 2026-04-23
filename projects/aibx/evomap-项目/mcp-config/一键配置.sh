#!/bin/bash
# 一键配置脚本 - 零基础专用
# 运行此脚本，按提示操作即可完成配置

echo ""
echo "============================================================"
echo "🚀 EvoMap 一键配置工具"
echo "============================================================"
echo ""
echo "适用人群：完全不懂计算机的用户"
echo "预计时间：10-15 分钟"
echo ""
echo "============================================================"
echo ""

# ========== 步骤 1: 检查环境 ==========
echo "📋 步骤 1: 检查环境..."
echo "------------------------------------------------------------"

# 检查 Python
if command -v python3 &> /dev/null; then
    echo "✅ Python3: 已安装"
else
    echo "❌ Python3 未安装，请先安装 Python 3.6+"
    echo "   下载地址：https://www.python.org/downloads/"
    exit 1
fi

# 检查 Git
if command -v git &> /dev/null; then
    echo "✅ Git: 已安装"
else
    echo "⚠️  Git 未安装（可选）"
fi

echo ""

# ========== 步骤 2: GITHUB_TOKEN 配置 ==========
echo "🔑 步骤 2: 配置 GITHUB_TOKEN..."
echo "------------------------------------------------------------"
echo ""
echo "请按以下步骤操作："
echo ""
echo "1. 打开浏览器，访问：https://github.com/settings/tokens"
echo ""
echo "2. 点击 'Generate new token' → 'Generate new token (classic)'"
echo ""
echo "3. 填写信息："
echo "   - Note: EvoMap"
echo "   - Expiration: No expiration"
echo ""
echo "4. 勾选以下 3 个权限："
echo "   ✅ repo"
echo "   ✅ workflow"
echo "   ✅ read:org"
echo ""
echo "5. 点击 'Generate token'"
echo ""
echo "6. 复制 token（格式：ghp_xxxxxxxxxxxx）"
echo ""

# 等待用户操作
echo "完成后，按回车继续..."
read

# 输入 Token
echo -n "请输入你的 GITHUB_TOKEN: "
read -s GITHUB_TOKEN_INPUT
echo ""

# 验证 Token 格式
if [[ $GITHUB_TOKEN_INPUT == ghp_* ]]; then
    echo "✅ Token 格式正确"
else
    echo "⚠️  Token 格式可能不正确（应该以 ghp_开头）"
    echo "   是否继续？(y/n)"
    read -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "❌ 配置取消"
        exit 1
    fi
fi

echo ""

# ========== 步骤 3: 数据库配置 ==========
echo "🗄️  步骤 3: 配置数据库..."
echo "------------------------------------------------------------"
echo ""
echo "推荐使用在线数据库（无需安装）："
echo ""
echo "1. 打开浏览器，访问：https://neon.tech"
echo ""
echo "2. 点击 'Sign Up'，使用 Google 账号登录"
echo ""
echo "3. 点击 'Create a project'"
echo "   - Project name: evomap"
echo "   - 点击 'Create project'"
echo ""
echo "4. 复制 'Connection string'"
echo "   （格式：postgresql://user:password@host/neondb）"
echo ""

# 等待用户操作
echo "完成后，按回车继续..."
read

# 输入数据库连接
echo -n "请输入 DATABASE_URL: "
read DATABASE_URL_INPUT
echo ""

# 验证数据库连接格式
if [[ $DATABASE_URL_INPUT == postgresql://* ]]; then
    echo "✅ 数据库连接格式正确"
else
    echo "⚠️  数据库连接可能不正确（应该以 postgresql://开头）"
    echo "   是否继续？(y/n)"
    read -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "❌ 配置取消"
        exit 1
    fi
fi

echo ""

# ========== 步骤 4: 创建配置文件 ==========
echo "📝 步骤 4: 创建配置文件..."
echo "------------------------------------------------------------"

# 配置文件路径
ENV_FILE="/home/admin/.openclaw/workspace/ai 知识变现/evomap 项目/.env"

# 创建 .env 文件
cat > "$ENV_FILE" << EOF
# EvoMap 生产环境配置
# 创建时间：$(date '+%Y-%m-%d %H:%M:%S')

# GitHub Token
GITHUB_TOKEN='$GITHUB_TOKEN_INPUT'

# PostgreSQL 数据库连接
DATABASE_URL='$DATABASE_URL_INPUT'

# EvoMap 配置（已配置好，无需修改）
EVOMAP_API_KEY='bcc7b8e55de75908ae237155cf52a11ac8925b42931e29ea0882b1d456fc7c3a'
EVOMAP_NODE_ID='node_67c3b8b37becd262'
EOF

echo "✅ 配置文件已创建：$ENV_FILE"
echo ""

# ========== 步骤 5: 测试配置 ==========
echo "🧪 步骤 5: 测试配置..."
echo "------------------------------------------------------------"
echo ""

# 进入项目目录
cd "/home/admin/.openclaw/workspace/ai 知识变现/evomap 项目" || exit 1

# 加载环境变量
export $(grep -v '^#' .env | xargs)

# 创建日志目录
mkdir -p logs

# 运行测试
echo "运行 A2A 客户端测试..."
echo ""

python3 a2a-client/a2a_client.py

# 检查测试结果
if [ $? -eq 0 ]; then
    echo ""
    echo "============================================================"
    echo "✅ 配置成功！"
    echo "============================================================"
    echo ""
    echo "下一步:"
    echo "1. 发布第一个 Gene:"
    echo "   python3 a2a-client/publish-first-gene.py"
    echo ""
    echo "2. 查看 Marketplace:"
    echo "   访问：https://evomap.ai/marketplace"
    echo "   搜索 Node ID: node_67c3b8b37becd262"
    echo ""
    echo "3. 开始赚取积分:"
    echo "   - 发布资产 → 获得积分"
    echo "   - 完成任务 → 获得积分"
    echo "   - 社区互动 → 获得积分"
    echo ""
else
    echo ""
    echo "============================================================"
    echo "⚠️  测试失败"
    echo "============================================================"
    echo ""
    echo "可能原因:"
    echo "1. GITHUB_TOKEN 不正确"
    echo "2. DATABASE_URL 不正确"
    echo "3. 网络连接问题"
    echo ""
    echo "解决方法:"
    echo "1. 检查 .env 文件中的配置是否正确"
    echo "2. 重新运行此脚本"
    echo "3. 联系技术人员求助"
    echo ""
fi

echo ""
echo "配置完成！"
echo ""
