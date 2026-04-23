#!/usr/bin/env node

import { google } from 'googleapis';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const CREDENTIALS_PATH = path.join(__dirname, 'credentials.json');
const TOKEN_PATH = path.join(__dirname, 'token.json');
const SCOPES = ['https://www.googleapis.com/auth/gmail.readonly'];

const AUTH_CODE = "4/0AfrIepAB6dlaBR8AFHNi_0vfrf5anlCPehiwq1fhiQmWkhwO33lC9klNe8Jr7_9kiUI-yg";

async function authorize() {
  console.log('🔐 Gmail API 授权中...\n');
  
  const credentials = JSON.parse(fs.readFileSync(CREDENTIALS_PATH, 'utf8'));
  const { client_secret, client_id, redirect_uris } = credentials.installed;
  
  const oauth2Client = new google.auth.OAuth2(
    client_id,
    client_secret,
    redirect_uris[0]
  );
  
  try {
    const { tokens } = await oauth2Client.getToken(AUTH_CODE);
    fs.writeFileSync(TOKEN_PATH, JSON.stringify(tokens, null, 2));
    
    console.log('✅ 授权成功！');
    console.log(`📍 Token 已保存到：${TOKEN_PATH}`);
    console.log('\n📧 现在可以访问你的 Gmail 了！\n');
    
  } catch (error) {
    console.error('❌ 授权失败:', error.message);
    console.error('\n可能原因：');
    console.error('   1. 授权码已过期（授权码只能使用一次）');
    console.error('   2. 授权码不完整');
    console.error('   3. 测试用户未正确配置');
    console.error('\n请重新获取授权码再试。');
    process.exit(1);
  }
}

authorize();
