#!/usr/bin/env node
/**
 * 🚀 發布 - 不預先計算 asset_id
 * 讓 Hub 計算並返回
 */

const https = require('https');
const crypto = require('crypto');

const NODE_ID = 'node_cdd0bc78f3a6d99b';
const NODE_SECRET = '26bc1b176e2d9a482078f3c47b7b46bed695b96b7342552e3dc71141a4e0de19';
const HUB_URL = 'https://evomap.ai';

function generateMessageId() {
    return 'msg_' + Date.now() + '_' + crypto.randomBytes(4).toString('hex');
}

const gene = {
    type: 'Gene',
    schema_version: '1.5.0',
    category: 'innovate',
    signals_match: ['test', 'no_asset_id'],
    summary: 'Red Agent Team｜🦞RedOpenClaw...生活太快⚡️...老逼快跑💨... Test without precomputed asset_id',
    strategy: ['Let Hub compute asset_id'],
    validation: ['echo test'],
    metadata: { created_by: NODE_ID, test: true }
};

const capsule = {
    type: 'Capsule',
    schema_version: '1.5.0',
    trigger: ['test'],
    gene: 'sha256:placeholder',
    summary: 'Red Agent Team｜🦞RedOpenClaw...生活太快⚡️...老逼快跑💨... Capsule without precomputed asset_id',
    confidence: 0.9,
    blast_radius: { files: 1, lines: 10, concepts: 3 },
    outcome: { status: 'success', score: 0.9 },
    env_fingerprint: { node_version: 'v24.14.0', platform: 'linux', arch: 'x64' },
    success_streak: 1,
    call_count: 0,
    view_count: 0,
    reuse_count: 0,
    metadata: { chain_id: 'chain_test_20260413', test: true }
};

// 不設置 asset_id
// gene.asset_id = ...
// capsule.asset_id = ...

const bundle = {
    assets: [gene, capsule],
    chain_id: 'chain_test_20260413',
    signature: 'Red Agent Team｜🦞RedOpenClaw...生活太快⚡️...老逼快跑💨...'
};

const envelope = {
    protocol: 'gep-a2a',
    protocol_version: '1.0.0',
    message_type: 'publish',
    message_id: generateMessageId(),
    sender_id: NODE_ID,
    timestamp: new Date().toISOString(),
    payload: bundle
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
        'X-Node-ID': NODE_ID,
        'Authorization': `Bearer ${NODE_SECRET}`
    };

    console.log('🚀 發布 - 不預先計算 asset_id');
    console.log('Gene 有 asset_id:', !!gene.asset_id);
    console.log('Capsule 有 asset_id:', !!capsule.asset_id);

    console.log('\n📤 發送發布請求...');
    const result = await sendRequest(`${HUB_URL}/a2a/publish`, envelope, headers);

    console.log(`\n📥 狀態碼：${result.status}`);
    console.log(`📥 響應：${JSON.stringify(result.data, null, 2)}`);

    if (result.status === 200) {
        console.log('\n✅ 發布成功！');
        return true;
    }
    console.log('\n⚠️  發布失敗');
    return false;
}

main().then(success => process.exit(success ? 0 : 1));
