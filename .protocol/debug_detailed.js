#!/usr/bin/env node
/**
 * 🚀 發布並打印詳細錯誤
 */

const https = require('https');
const crypto = require('crypto');
const { computeAssetId, canonicalize } = require('/home/admin/.openclaw/workspace/evolver/src/gep/contentHash.js');

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
    summary: 'Red Agent Team｜🦞RedOpenClaw...生活太快⚡️...老逼快跑💨... Debug capsule',
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

// 打印 canonical JSON
const cleanCapsule = { ...capsule };
delete cleanCapsule.asset_id;
const canonical = canonicalize(cleanCapsule);

console.log('🔍 Capsule Canonical JSON:');
console.log(canonical);
console.log('');

const localAssetId = computeAssetId(capsule);
console.log('本地 asset_id:', localAssetId);
console.log('');

capsule.asset_id = localAssetId;

const bundle = {
    assets: [{
        type: 'Gene',
        schema_version: '1.5.0',
        category: 'innovate',
        signals_match: ['test'],
        summary: 'Red Agent Team｜🦞RedOpenClaw...生活太快⚡️...老逼快跑💨... Test',
        strategy: ['test'],
        validation: ['echo test'],
        metadata: { test: true },
        asset_id: 'sha256:test'
    }, capsule],
    chain_id: 'chain_debug_20260413',
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

    console.log('📤 發送發布請求...\n');
    const result = await sendRequest(`${HUB_URL}/a2a/publish`, envelope, headers);

    console.log('📥 狀態碼:', result.status);
    console.log('📥 響應:', JSON.stringify(result.data, null, 2));
}

main();
