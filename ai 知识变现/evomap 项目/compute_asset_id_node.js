#!/usr/bin/env node
/**
 * 使用 Node.js 计算 asset_id (与 Hub 一致的序列化)
 */

const crypto = require('crypto');

// Gene 数据
const gene = {
    type: "Gene",
    schema_version: "1.5.0",
    category: "repair",
    signals_match: ["WebSocket", "disconnect", "reconnect"],
    summary: "WebSocket auto-reconnect with exponential backoff",
    strategy: [
        "Listen for WebSocket close events",
        "Implement exponential backoff (base 1s, max 30s)",
        "Add jitter ±20%",
        "Max 10 retries",
        "Reset on success"
    ],
    constraints: { max_files: 2, forbidden_paths: ["node_modules/"] },
    validation: ["node test.js"]
};

// 计算 asset_id: sha256(canonical_json(asset_without_asset_id))
// canonical_json = sorted keys at all levels
function canonicalStringify(obj) {
    if (obj === null || obj === undefined) return 'null';
    if (typeof obj !== 'object') return JSON.stringify(obj);
    
    if (Array.isArray(obj)) {
        return '[' + obj.map(item => canonicalStringify(item)).join(',') + ']';
    }
    
    // 对象：排序键
    const keys = Object.keys(obj).sort();
    const pairs = keys.map(key => {
        return JSON.stringify(key) + ':' + canonicalStringify(obj[key]);
    });
    
    return '{' + pairs.join(',') + '}';
}

// 排除 asset_id 字段
function withoutAssetId(obj) {
    const { asset_id, ...rest } = obj;
    return rest;
}

// 计算 hash
function computeAssetId(obj) {
    const clean = withoutAssetId(obj);
    const canonical = canonicalStringify(clean);
    const hash = crypto.createHash('sha256').update(canonical).digest('hex');
    return `sha256:${hash}`;
}

console.log("📋 Gene 对象:");
console.log(JSON.stringify(gene, null, 2));

console.log("\n📋 Canonical JSON:");
const canonical = canonicalStringify(gene);
console.log(canonical);

console.log("\n📋 Computed asset_id:");
const assetId = computeAssetId(gene);
console.log(assetId);

console.log("\n📋 长度信息:");
console.log(`   Canonical: ${canonical.length} 字符`);
console.log(`   asset_id: ${assetId.length} 字符`);
