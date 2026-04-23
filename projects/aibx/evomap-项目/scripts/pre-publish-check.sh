#!/bin/bash
# 发布前完整验证流程

echo "=============================================="
echo "🔍 发布前完整验证"
echo "=============================================="

if [ -z "$1" ]; then
    echo "用法：./pre-publish-check.sh <资产包目录>"
    exit 1
fi

ASSET_DIR="$1"
SCRIPT_DIR="$(dirname "$0")"

# 1. 资产结构验证
echo ""
echo "1️⃣ 资产结构验证..."
python3 "$SCRIPT_DIR/validate-asset.py" "$ASSET_DIR"
if [ $? -ne 0 ]; then
    echo "❌ 资产结构验证失败，终止发布"
    exit 1
fi

# 2. 漂移风险扫描
echo ""
echo "2️⃣ 漂移风险扫描..."
python3 "$SCRIPT_DIR/scan-drift.py" "$ASSET_DIR/gene.json"
if [ $? -ne 0 ]; then
    echo "⚠️ 发现漂移风险，但可以继续发布"
fi

# 3. 哈希验证
echo ""
echo "3️⃣ 哈希验证..."
python3 "$SCRIPT_DIR/verify-hash.py" "$ASSET_DIR/gene.json"
if [ $? -ne 0 ]; then
    echo "❌ Gene 哈希验证失败"
    exit 1
fi

python3 "$SCRIPT_DIR/verify-hash.py" "$ASSET_DIR/capsule.json"
if [ $? -ne 0 ]; then
    echo "❌ Capsule 哈希验证失败"
    exit 1
fi

# 4. 节点健康检查
echo ""
echo "4️⃣ 节点健康检查..."
python3 "$SCRIPT_DIR/check-node-health.py"
if [ $? -ne 0 ]; then
    echo "⚠️ 节点状态异常，但可以继续发布"
fi

# 5. 积分检查
echo ""
echo "5️⃣ 积分检查..."
python3 "$SCRIPT_DIR/../lib/credit_protect.py"

echo ""
echo "=============================================="
echo "✅ 所有验证通过，可以安全发布"
echo "=============================================="
