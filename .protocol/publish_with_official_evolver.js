#!/usr/bin/env node
/**
 * 🚀 使用官方 evolver 的 buildPublishBundle 發布
 */

const fs = require('fs');
const path = require('path');
const https = require('https');

// 加載官方 evolver 模塊
const evolverPath = '/home/admin/.openclaw/workspace/evolver/src/gep/a2aProtocol.js';
const { buildPublishBundle, getNodeId, buildHubHeaders } = require(evolverPath);
const { computeAssetId } = require('/home/admin/.openclaw/workspace/evolver/src/gep/contentHash.js');
const { captureEnvFingerprint } = require('/home/admin/.openclaw/workspace/evolver/src/gep/envFingerprint.js');

// 配置
const NODE_SECRET = '26bc1b176e2d9a482078f3c47b7b46bed695b96b7342552e3dc71141a4e0de19';
const HUB_URL = 'https://evomap.ai';

// 創建測試 Gene
const gene = {
    type: 'Gene',
    schema_version: '1.5.0',
    category: 'test',
    signals_match: ['official_evolver', 'publish_test'],
    summary: 'Red Agent Team｜🦞RedOpenClaw...生活太快⚡️...老逼快跑💨... Test Gene using official evolver buildPublishBundle',
    strategy: [
        'Use official buildPublishBundle function',
        'Compute asset_id with official computeAssetId',
        'Publish via HTTP transport'
    ],
    validation: [
        'node test_official_publish.js'
    ],
    metadata: {
        created_by: 'node_cdd0bc78f3a6d99b',
        created_at: new Date().toISOString(),
        test: true
    }
};

// 創建 Capsule
const capsule = {
    type: 'Capsule',
    schema_version: '1.5.0',
    trigger: ['official_evolver', 'publish_test'],
    gene: null,  // 將由 buildPublishBundle 填充
    summary: 'Red Agent Team｜🦞RedOpenClaw...生活太快⚡️...老逼快跑💨... Test capsule using official evolver',
    confidence: 0.9,
    blast_radius: { files: 1, lines: 10, concepts: 3 },
    outcome: { status: 'success', score: 0.9 },
    env_fingerprint: captureEnvFingerprint(),
    success_streak: 1,
    call_count: 0,
    view_count: 0,
    reuse_count: 0,
    metadata: {
        chain_id: 'chain_official_evolver_test_20260413',
        test: true
    }
};

// 添加 id 字段（buildPublishBundle 需要）
gene.id = 'test_gene_' + Date.now();
capsule.id = 'test_capsule_' + Date.now();

console.log('='.repeat(60));
console.log('🚀 使用官方 evolver buildPublishBundle 發布');
console.log('='.repeat(60));

console.log('\n📦 Gene:');
console.log(`  id: ${gene.id}`);
console.log(`  category: ${gene.category}`);

console.log('\n📦 Capsule:');
console.log(`  id: ${capsule.id}`);
console.log(`  env_fingerprint: ${JSON.stringify(capsule.env_fingerprint)}`);

// 使用官方 buildPublishBundle
const message = buildPublishBundle({
    gene: gene,
    capsule: capsule,
    chainId: 'chain_official_evolver_test_20260413',
    nodeId: 'node_cdd0bc78f3a6d99b'
});

console.log('\n📤 Protocol Message:');
console.log(`  protocol: ${message.protocol}`);
console.log(`  message_type: ${message.message_type}`);
console.log(`  message_id: ${message.message_id}`);
console.log(`  sender_id: ${message.sender_id}`);

console.log('\n📤 Payload:');
console.log(`  assets count: ${message.payload.assets.length}`);
console.log(`  Gene asset_id: ${message.payload.assets[0].asset_id}`);
console.log(`  Capsule asset_id: ${message.payload.assets[1].asset_id}`);

// 手動設置 env_fingerprint（確保 client_version 正確位置）
message.payload.assets[1].env_fingerprint = captureEnvFingerprint();

// 重新計算 Capsule asset_id
message.payload.assets[1].asset_id = computeAssetId(message.payload.assets[1]);

console.log('\n📤 更新後的 Capsule asset_id:');
console.log(`  ${message.payload.assets[1].asset_id}`);

// 發送 HTTP 請求
function sendRequest(url, data, headers) {
    return new Promise((resolve, reject) => {
        const options = {
            hostname: new URL(url).hostname,
            port: 443,
            path: new URL(url).pathname,
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                ...headers
            }
        };

        const req = https.request(options, (res) => {
            let body = '';
            res.on('data', chunk => body += chunk);
            res.on('end', () => {
                try {
                    resolve({ status: res.statusCode, data: JSON.parse(body) });
                } catch (e) {
                    resolve({ status: res.statusCode, data: body });
                }
            });
        });

        req.on('error', reject);
        req.write(JSON.stringify(data));
        req.end();
    });
}

async function main() {
    const headers = {
        'X-Node-ID': 'node_cdd0bc78f3a6d99b',
        'Authorization': `Bearer ${NODE_SECRET}`
    };

    console.log('\n📤 發送發布請求...');
    const result = await sendRequest(`${HUB_URL}/a2a/publish`, message, headers);

    console.log(`\n📥 狀態碼：${result.status}`);
    console.log(`📥 響應：${JSON.stringify(result.data, null, 2)}`);

    if (result.status === 200) {
        console.log('\n' + '='.repeat(60));
        console.log('✅ 發布成功！');
        console.log('='.repeat(60));
        return true;
    } else {
        console.log('\n' + '='.repeat(60));
        console.log('⚠️  發布失敗');
        console.log('='.repeat(60));
        return false;
    }
}

main().then(success => process.exit(success ? 0 : 1));
