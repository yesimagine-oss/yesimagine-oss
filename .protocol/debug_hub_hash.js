#!/usr/bin/env node
/**
 * 🔍 調試：發送驗證請求，讓 Hub 告訴我們它計算的 hash
 */

const https = require('https');
const crypto = require('crypto');

const { computeAssetId } = require('/home/admin/.openclaw/workspace/evolver/src/gep/contentHash.js');

const NODE_ID = 'node_cdd0bc78f3a6d99b';
const NODE_SECRET = '26bc1b176e2d9a482078f3c47b7b46bed695b96b7342552e3dc71141a4e0de19';
const HUB_URL = 'https://evomap.ai';

function generateMessageId() {
    return 'msg_' + Date.now() + '_' + crypto.randomBytes(4).toString('hex');
}

const capsule = {
    type: 'Capsule',
    schema_version: '1.5.0',
    trigger: ['test'],
    gene: 'sha256:test',
    summary: 'Red Agent Team｜🦞RedOpenClaw...生活太快⚡️...老逼快跑💨... Debug capsule for hash verification',
    confidence: 0.9,
    blast_radius: { files: 1, lines: 10, concepts: 3 },
    outcome: { status: 'success', score: 0.9 },
    env_fingerprint: { node_version: 'v24.14.0', platform: 'linux', arch: 'x64' },
    success_streak: 1,
    call_count: 0,
    view_count: 0,
    reuse_count: 0,
    metadata: { chain_id: 'chain_debug_20260413', test: true }
};

const localAssetId = computeAssetId(capsule);

console.log('🔍 調試：Hub hash 計算');
console.log('='.repeat(60));
console.log('\n本地計算的 asset_id:', localAssetId);

// 創建驗證請求
const validatePayload = {
    assets: [capsule]
};

const envelope = {
    protocol: 'gep-a2a',
    protocol_version: '1.0.0',
    message_type: 'validate',
    message_id: generateMessageId(),
    sender_id: NODE_ID,
    timestamp: new Date().toISOString(),
    payload: validatePayload
};

function sendRequest(url, data, headers) {
    return new Promise((resolve, reject) => {
        const options = {
            hostname: new URL(url).hostname,
            port: 443,
            path: new URL(url).pathname,
            method: 'POST',
            headers: { 'Content-Type': 'application/json', ...headers }
        };
        const req = https.request(options, (res) => {
            let body = '';
            res.on('data', chunk => body += chunk);
            res.on('end', () => {
                try { resolve({ status: res.statusCode, data: JSON.parse(body) }); }
                catch (e) { resolve({ status: res.statusCode, data: body }); }
            });
        });
        req.on('error', reject);
        req.write(JSON.stringify(data));
        req.end();
    });
}

async function main() {
    const headers = {
        'Content-Type': 'application/json',
        'X-Node-ID': NODE_ID,
        'Authorization': `Bearer ${NODE_SECRET}`
    };

    console.log('\n📤 發送驗證請求...');
    const result = await sendRequest(`${HUB_URL}/a2a/validate`, envelope, headers);

    console.log(`\n📥 狀態碼：${result.status}`);
    console.log(`📥 響應：${JSON.stringify(result.data, null, 2)}`);

    // 如果驗證失敗，Hub 會告訴我們它計算的 hash
    if (result.status === 422 && result.data.error === 'capsule_asset_id_verification_failed') {
        console.log('\n💡 Hub 的 correction 對象可能包含線索');
    }
}

main();
