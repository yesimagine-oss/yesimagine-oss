#!/bin/bash
# EvoMap 优化 Fetch 脚本 - 只免费浏览
# 使用 search_only=true 避免资产获取费用

NODE_SECRET="41d3e627a4fee83351274562ff11cec398885bdf023b1fa9da19cf690926010c"
NODE_ID="node_b83d6e6008dce32f"
TIMESTAMP=$(date +%s)

echo "=== EvoMap 优化 Fetch (免费浏览模式) ==="
echo "节点：$NODE_ID"
echo "时间：$(date)"
echo ""

# 步骤 1: 免费浏览资产摘要
echo "步骤 1: 免费浏览资产摘要 (search_only=true)..."
curl -s -X POST "https://evomap.ai/a2a/fetch" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $NODE_SECRET" \
  -d "{
    \"protocol\": \"gep-a2a\",
    \"protocol_version\": \"1.0.0\",
    \"message_type\": \"fetch\",
    \"message_id\": \"msg_${TIMESTAMP}_search_only\",
    \"sender_id\": \"$NODE_ID\",
    \"timestamp\": \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",
    \"payload\": {
      \"search_only\": true,
      \"asset_type\": \"Capsule\",
      \"limit\": 20
    }
  }" | jq -r '
    .payload.assets | length as $count |
    "发现 \($count) 个资产",
    "前 5 个资产摘要:",
    (.assets[:5][] | "  - \(.short_title) (GDI: \(.gdi_score))")
  ' 2>/dev/null || echo "获取失败"

echo ""

# 步骤 2: 如果有感兴趣的资产，使用 detailed=true 获取单个详情 (免费)
echo "步骤 2: 如需查看某个资产详情，使用以下命令:"
echo "  curl \"https://evomap.ai/a2a/assets/sha256:<asset_id>?detailed=true\""
echo ""
echo "示例:"
echo "  curl \"https://evomap.ai/a2a/assets/sha256:abc123...?detailed=true\""
echo ""

# 步骤 3: 显示当前配置
echo "=== 当前配置 ==="
echo "Fetch 模式：search_only (免费)"
echo "自动获取限制：0 (禁用)"
echo "每日预算：10 积分"
echo ""

# 步骤 4: 显示积分余额
echo "=== 积分状态 ==="
curl -s -X POST "https://evomap.ai/a2a/hello" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $NODE_SECRET" \
  -d "{
    \"protocol\": \"gep-a2a\",
    \"protocol_version\": \"1.0.0\",
    \"message_type\": \"hello\",
    \"message_id\": \"msg_${TIMESTAMP}_check_balance\",
    \"sender_id\": \"$NODE_ID\",
    \"timestamp\": \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",
    \"payload\": {
      \"env_fingerprint\": {\"evolver_version\": \"1.69.16\"}
    }
  }" | jq -r '.payload.credit_balance // "unknown"' 2>/dev/null

echo ""
echo "=== 完成 ==="
echo "提示：如需获取完整资产内容，请使用 detailed=true 端点 (免费)"
echo "      避免使用 fetch 获取多个完整资产 (收费)"
