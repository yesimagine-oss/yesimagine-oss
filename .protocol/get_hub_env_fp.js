#!/usr/bin/env node
/**
 * 🚀 使用 Hub 返回的 env_fingerprint 格式
 * 從 hello 響應中獲取 Hub 期望的格式
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

// 先發送 hello 獲取 Hub 的 env_fingerprint
function sendHello() {
    return new Promise((resolve, reject) => {
        const envelope = {
            protocol: 'gep-a2a',
            protocol_version: '1.0.0',
            message_type: 'hello',
            message_id: generateMessageId(),
            sender_id: NODE_ID,
            timestamp: new Date().toISOString(),
            payload: {}
        };
        
        const options = {
            hostname: 'evomap.ai',
            port: 443,
            path: '/a2a/hello',
            method: 'POST',
            headers: { 'Content-Type': 'application/json' }
        };
        
        const req = https.request(options, (res) => {
            let body = '';
            res.on('data', chunk => body += chunk);
            res.on('end', () => {
                try { resolve(JSON.parse(body)); }
                catch (e) { resolve(body); }
            });
        });
        req.on('error', reject);
        req.write(JSON.stringify(envelope));
        req.end();
    });
}

async function main() {
    console.log('='.repeat(60));
    console.log('🚀 從 hello 響應獲取 Hub 的 env_fingerprint');
    console.log('='.repeat(60));
    
    console.log('\n📤 發送 hello 請求...');
    const helloResult = await sendHello();
    
    console.log('\n📥 Hello 響應:');
    console.log(JSON.stringify(helloResult, null, 2));
    
    // 提取 env_fingerprint
    const envFp = helloResult.payload?.env_fingerprint;
    if (envFp) {
        console.log('\n✅ Hub 的 env_fingerprint:');
        console.log(JSON.stringify(envFp, null, 2));
    }
}

main();
