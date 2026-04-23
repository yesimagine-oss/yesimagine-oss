#!/usr/bin/env node
/**
 * 测试范老师的指引：使用 /a2a/validate 接口获取正确的 asset_id
 * 
 * 步骤：
 * 1. 调用 POST /a2a/validate（与 publish 相同的请求结构）
 * 2. 从响应中提取 computed_assets[].computed_asset_id
 * 3. 替换错误的 asset_id 为正确的 computed_asset_id
 * 4. 调用 POST /a2a/publish
 */

const crypto = require('crypto');
const fs = require('fs');
const https = require('https');

const NODE_ID = 'node_67c3b8b37becd262';
const NODE_SECRET = 'bcc7b8e55de75908ae237155cf52a11ac8925b42931e29ea0882b1d456fc7c3a';
const BASE_URL = 'https://evomap.ai';

function canonicalize(obj) {
  if (obj === null || obj === undefined) return 'null';
  if (typeof obj === 'boolean') return obj ? 'true' : 'false';
  if (typeof obj === 'number') {
    if (!Number.isFinite(obj)) return 'null';
    return String(obj);
  }
  if (typeof obj === 'string') return JSON.stringify(obj);
  if (Array.isArray(obj)) {
    return '[' + obj.map(canonicalize).join(',') + ']';
  }
  if (typeof obj === 'object') {
    const keys = Object.keys(obj).sort();
    const pairs = [];
    for (const k of keys) {
      pairs.push(JSON.stringify(k) + ':' + canonicalize(obj[k]));
    }
    return '{' + pairs.join(',') + '}';
  }
  return 'null';
}

function computeAssetId(obj) {
  const clean = {...obj};
  delete clean.asset_id;
  const canonical = canonicalize(clean);
  const hash = crypto.createHash('sha256').update(canonical, 'utf8').digest('hex');
  return 'sha256:' + hash;
}

function post(url, data) {
  return new Promise((resolve, reject) => {
    const options = {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${NODE_SECRET}`
      },
      timeout: 90000
    };
    
    const req = https.request(url, options, (res) => {
      let body = '';
      res.on('data', chunk => body += chunk);
      res.on('end', () => {
        try {
          resolve({ status: res.statusCode, data: JSON.parse(body) });
        } catch (e) {
          resolve({ status: res.statusCode, data: { raw: body } });
        }
      });
    });
    
    req.on('error', reject);
    req.on('timeout', () => { req.destroy(); reject(new Error('Timeout')); });
    req.write(JSON.stringify(data));
    req.end();
  });
}

async function testValidate() {
  console.log('='.repeat(60));
  console.log('🧪 测试范老师的指引：使用 /a2a/validate 接口');
  console.log('='.repeat(60));
  
  // 创建一个简单的测试 Gene
  const testGene = {
    type: 'Gene',
    schema_version: '1.6.0',
    category: 'optimize',
    summary: 'Test Gene for validate',
    signals_match: ['test', 'validate'],
    strategy: ['Test strategy 1', 'Test strategy 2'],
    confidence: 0.9,
    blast_radius: { files: 1, lines: 10 },
    domain: 'test',
    env_fingerprint: { arch: 'x64', platform: 'linux' }
  };
  
  // 创建一个简单的测试 Capsule
  const testCapsule = {
    type: 'Capsule',
    schema_version: '1.6.0',
    trigger: ['test', 'validate'],
    gene: null,
    summary: 'Test Capsule for validate',
    content: 'Test content for validate interface testing.',
    strategy: ['Test strategy 1', 'Test strategy 2'],
    diff: 'diff --git a/test.py b/test.py\nnew file mode 100644\nindex 0000000..1234567\n--- /dev/null\n+++ b/test.py\n@@ -0,0 +1,3 @@\n+# Test file\n+print("Hello")\n+',
    confidence: 0.9,
    blast_radius: { files: 1, lines: 3 },
    outcome: { status: 'success', score: 0.9 },
    domain: 'test',
    env_fingerprint: { arch: 'x64', platform: 'linux' }
  };
  
  // 计算本地 asset_id
  console.log('\n📝 本地计算的 asset_id:');
  const localGeneId = computeAssetId(testGene);
  testGene.asset_id = localGeneId;
  console.log(`  Gene: ${localGeneId}`);
  
  testCapsule.gene = localGeneId;
  const localCapsuleId = computeAssetId(testCapsule);
  testCapsule.asset_id = localCapsuleId;
  console.log(`  Capsule: ${localCapsuleId}`);
  
  // 构建 validate 请求
  const timestamp = new Date().toISOString();
  const validatePayload = {
    protocol: 'gep-a2a',
    protocol_version: '1.0.0',
    message_type: 'validate',
    message_id: `msg_${Date.now()}_validate_test`,
    sender_id: NODE_ID,
    timestamp: timestamp,
    payload: {
      assets: [testGene, testCapsule]
    }
  };
  
  console.log('\n📤 调用 /a2a/validate...');
  console.log('请求结构:');
  console.log(JSON.stringify(validatePayload, null, 2).substring(0, 500) + '...');
  
  try {
    const validateResult = await post(`${BASE_URL}/a2a/validate`, validatePayload);
    
    console.log(`\n📊 响应状态：${validateResult.status}`);
    console.log('完整响应:');
    console.log(JSON.stringify(validateResult.data, null, 2));
    
    if (validateResult.status === 200 && validateResult.data.computed_assets) {
      console.log('\n✅ Validate 成功！');
      console.log('\n📝 Hub 计算的 computed_asset_id:');
      
      const hubGeneId = validateResult.data.computed_assets[0]?.computed_asset_id;
      const hubCapsuleId = validateResult.data.computed_assets[1]?.computed_asset_id;
      
      console.log(`  Gene: ${hubGeneId}`);
      console.log(`  Capsule: ${hubCapsuleId}`);
      
      // 对比
      console.log('\n🔍 对比本地 vs Hub:');
      console.log(`  Gene: ${localGeneId === hubGeneId ? '✅ 一致' : '❌ 不一致'}`);
      if (localGeneId !== hubGeneId) {
        console.log(`    本地：${localGeneId}`);
        console.log(`    Hub:   ${hubGeneId}`);
      }
      
      console.log(`  Capsule: ${localCapsuleId === hubCapsuleId ? '✅ 一致' : '❌ 不一致'}`);
      if (localCapsuleId !== hubCapsuleId) {
        console.log(`    本地：${localCapsuleId}`);
        console.log(`    Hub:   ${hubCapsuleId}`);
      }
      
      return {
        success: true,
        hubGeneId,
        hubCapsuleId,
        localGeneId,
        localCapsuleId
      };
    } else {
      console.log('\n⚠️ Validate 失败');
      if (validateResult.data.error) {
        console.log(`  错误：${validateResult.data.error}`);
      }
      if (validateResult.data.details) {
        console.log(`  详情：${JSON.stringify(validateResult.data.details)}`);
      }
      if (validateResult.data.correction) {
        console.log(`  建议：${validateResult.data.correction.fix}`);
      }
      
      return { success: false, error: validateResult.data.error };
    }
  } catch (error) {
    console.log(`\n❌ 异常：${error.message}`);
    return { success: false, error: error.message };
  }
}

async function main() {
  const result = await testValidate();
  
  console.log('\n' + '='.repeat(60));
  console.log('📊 测试结果总结');
  console.log('='.repeat(60));
  
  if (result.success) {
    console.log('✅ Validate 接口可用！');
    console.log('✅ 可以获取 Hub 计算的正确 asset_id！');
    console.log('\n下一步：');
    console.log('1. 使用 hubGeneId 和 hubCapsuleId 替换错误的 asset_id');
    console.log('2. 调用 /a2a/publish 提交');
  } else {
    console.log('❌ Validate 接口不可用或返回错误');
    console.log(`错误：${result.error}`);
    console.log('\n可能原因：');
    console.log('1. /a2a/validate 接口需要不同的请求格式');
    console.log('2. 需要额外的权限或配置');
    console.log('3. 接口暂时不可用');
  }
  
  console.log('\n' + '='.repeat(60));
}

main();
