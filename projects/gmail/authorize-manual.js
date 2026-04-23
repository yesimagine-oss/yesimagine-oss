#!/usr/bin/env node

/**
 * Gmail API OAuth2 手动授权脚本
 * 适用于无法自动打开浏览器的环境
 */

import { google } from 'googleapis';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import readline from 'readline';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const CREDENTIALS_PATH = path.join(__dirname, 'credentials.json');
const TOKEN_PATH = path.join(__dirname, 'token.json');
const SCOPES = ['https://www.googleapis.com/auth/gmail.readonly'];

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout,
});

function question(query) {
  return new Promise(resolve => {
    rl.question(query, resolve);
  });
}

async function authorizeManual() {
  console.log('🔐 Gmail API 手动授权工具\n');
  
  // 检查凭据文件
  if (!fs.existsSync(CREDENTIALS_PATH)) {
    console.error('❌ 错误：找不到 credentials.json');
    process.exit(1);
  }
  
  // 检查现有 token
  if (fs.existsSync(TOKEN_PATH)) {
    console.log('⚠️  发现已有的 token.json');
    const answer = await question('是否要重新授权？(y/N): ');
    
    if (answer.toLowerCase() === 'y' || answer.toLowerCase() === 'yes') {
      fs.unlinkSync(TOKEN_PATH);
      console.log('🗑️  已删除旧 token\n');
    } else {
      console.log('✅ 使用现有 token');
      console.log(`📍 Token 位置：${TOKEN_PATH}`);
      rl.close();
      process.exit(0);
    }
  }
  
  const credentials = JSON.parse(fs.readFileSync(CREDENTIALS_PATH, 'utf8'));
  const { client_secret, client_id, redirect_uris } = credentials.installed;
  
  const oauth2Client = new google.auth.OAuth2(
    client_id,
    client_secret,
    redirect_uris[0]
  );
  
  const authUrl = oauth2Client.generateAuthUrl({
    access_type: 'offline',
    scope: SCOPES,
  });
  
  console.log('📝 请按以下步骤完成授权：\n');
  console.log('1️⃣  在浏览器中打开以下 URL：');
  console.log(`   ${authUrl}\n`);
  console.log('2️⃣  登录你的 Google 账号（yesimagine@gmail.com）');
  console.log('3️⃣  点击"允许"授权');
  console.log('4️⃣  复制浏览器地址栏中的授权码（code= 后面的部分）\n');
  
  const code = await question('请输入授权码：');
  
  try {
    const { tokens } = await oauth2Client.getToken(code);
    
    // 保存 token
    fs.writeFileSync(TOKEN_PATH, JSON.stringify(tokens, null, 2));
    
    console.log('\n✅ 授权成功！');
    console.log(`📍 Token 已保存到：${TOKEN_PATH}`);
    console.log('\n⚠️  重要提示：');
    console.log('   - token.json 包含敏感信息，不要分享给他人');
    console.log('   - Token 过期后会自动刷新，无需重新授权');
    console.log('   - 如需撤销授权，访问：https://myaccount.google.com/permissions\n');
    
  } catch (error) {
    console.error('\n❌ 授权失败:', error.message);
    console.error('请检查授权码是否正确，或重新开始流程。');
  }
  
  rl.close();
}

authorizeManual();
