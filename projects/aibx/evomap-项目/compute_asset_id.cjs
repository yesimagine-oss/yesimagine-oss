#!/usr/bin/env node
/**
 * EvoMap Asset ID 计算器
 * 使用 JavaScript 的 JSON.stringify 计算 canonical hash
 * 确保与 EvoMap Hub 完全一致
 * 
 * 使用方式:
 *   node compute_asset_id.js '{"type":"Gene",...}'
 *   echo '{"type":"Gene",...}' | node compute_asset_id.js --stdin
 */

const crypto = require('crypto');

// 深度克隆并排序对象 key
function sortObjectKeys(obj) {
    if (obj === null || typeof obj !== 'object') {
        return obj;
    }
    
    if (Array.isArray(obj)) {
        return obj.map(sortObjectKeys);
    }
    
    const sortedObj = {};
    Object.keys(obj).sort().forEach(key => {
        sortedObj[key] = sortObjectKeys(obj[key]);
    });
    
    return sortedObj;
}

// 计算 asset_id
function computeAssetId(data) {
    // 移除 asset_id 字段（如果存在）
    const dataCopy = { ...data };
    delete dataCopy.asset_id;
    
    // 深度排序所有 key
    const sortedData = sortObjectKeys(dataCopy);
    
    // Canonical JSON 序列化（与 Hub 一致）
    const canonical = JSON.stringify(sortedData);
    
    // SHA256 哈希
    const hash = crypto.createHash('sha256').update(canonical).digest('hex');
    
    return `sha256:${hash}`;
}

// CLI 入口
function main() {
    let inputData;
    
    if (process.argv.includes('--stdin')) {
        // 从 stdin 读取
        inputData = fs.readFileSync(0, 'utf-8').trim();
    } else if (process.argv.length > 2) {
        // 从命令行参数读取
        inputData = process.argv[2];
    } else {
        console.error('Usage:');
        console.error('  node compute_asset_id.js \'{"type":"Gene",...}\'');
        console.error('  echo \'{"type":"Gene",...}\' | node compute_asset_id.js --stdin');
        process.exit(1);
    }
    
    try {
        const data = JSON.parse(inputData);
        const assetId = computeAssetId(data);
        console.log(assetId);
    } catch (error) {
        console.error('Error:', error.message);
        process.exit(1);
    }
}

main();
