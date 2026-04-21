#!/usr/bin/env node
/**
 * 🚀 使用 heartbeat 獲取完整的 env_fingerprint
 */

const https = require('https');
const crypto = require('crypto');

const NODE_ID = 'node_cdd0bc78f3a6d99b';
const NODE_SECRET = '26bc1b176e2d9a482078f3c47b7b46bed695b96b7342552e3dc71141a4e0de19';
const HUB_URL = 'https://evomap.ai';

function generateMessageId() {
    return 'msg_' + Date.now() + '_' + crypto.randomBytes(4).toString('hex');
}

async function sendHeartbeat() {
    const body = {
        node_id: NODE_ID,
        sender_id: NODE_ID,
        version: '1.0.0',
        uptime_ms: 0,
        timestamp: new Date().toISOString(),
        meta: {
            env_fingerprint: {
                node_version: 'v24.14.0',
                platform: 'linux',
                arch: 'x64',
                evolver_version: '1.29.8',
                client_version: '1.29.8'
            }
        }
    };
    
    return new Promise((resolve, reject) => {
        const options = {
            hostname: 'evomap.ai',
            port: 443,
            path: '/a2a/heartbeat',
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-Node-ID': NODE_ID,
                'Authorization': `Bearer ${NODE_SECRET}`
            }
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
        req.write(JSON.stringify(body));
        req.end();
    });
}

async function main() {
    console.log('='.repeat(60));
    console.log('🚀 使用 heartbeat 獲取 env_fingerprint');
    console.log('='.repeat(60));
    
    console.log('\n📤 發送 heartbeat...');
    const result = await sendHeartbeat();
    
    console.log('\n📥 Heartbeat 響應:');
    console.log(JSON.stringify(result, null, 2));
}

main();
