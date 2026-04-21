#!/usr/bin/env node
/**
 * 🍪 微信 Cookie 導出工具
 * 
 * 用途：幫助用戶從瀏覽器導出微信公眾號的 Cookie
 * 使用：node export-cookies.js
 * 
 * 步驟：
 * 1. 運行此腳本
 * 2. 掃描二維碼或手動登錄微信公眾號
 * 3. 自動保存 Cookie 到文件
 */

const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const readline = require('readline');

// ==================== 配置 ====================

const COOKIES_DIR = path.join(process.env.HOME || '~', '.openclaw/workspace/cookies');
const COOKIES_FILE = path.join(COOKIES_DIR, 'wechat-cookies.json');
const WECHAT_URL = 'https://mp.weixin.qq.com';

// ==================== 工具函數 ====================

function ensureDir(dir) {
    if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true });
        console.log(`📁 創建目錄：${dir}`);
    }
}

function saveCookies(cookies, filePath) {
    const json = JSON.stringify(cookies, null, 2);
    fs.writeFileSync(filePath, json, 'utf-8');
    console.log(`✅ Cookie 已保存：${filePath}`);
    console.log(`📊 總共 ${cookies.length} 個 Cookie`);
}

function loadCookies(filePath) {
    if (fs.existsSync(filePath)) {
        const json = fs.readFileSync(filePath, 'utf-8');
        return JSON.parse(json);
    }
    return null;
}

// ==================== 主程序 ====================

async function exportCookies() {
    console.log('🍪 微信 Cookie 導出工具\n');
    console.log('📋 用途：從微信公眾號導出 Cookie，用於自動化抓取');
    console.log('🔒 安全提示：Cookie 包含登錄信息，請妥善保管，不要分享給他人\n');
    
    // 檢查現有 Cookie
    if (fs.existsSync(COOKIES_FILE)) {
        const existing = loadCookies(COOKIES_FILE);
        if (existing && existing.length > 0) {
            console.log(`⚠️  發現現有 Cookie 文件：${COOKIES_FILE}`);
            console.log(`📊 包含 ${existing.length} 個 Cookie`);
            console.log('\n選項：');
            console.log('  1. 使用現有 Cookie (直接返回)');
            console.log('  2. 重新導出 Cookie (覆蓋現有)');
            console.log('');
            
            const answer = await question('請選擇 (1/2): ');
            if (answer === '1') {
                console.log('✅ 使用現有 Cookie');
                return;
            }
        }
    }
    
    let browser = null;
    
    try {
        // 啟動瀏覽器
        console.log('\n🌐 啟動瀏覽器...');
        browser = await chromium.launch({
            headless: false, // 使用可見模式，讓用戶手動登錄
            args: [
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-dev-shm-usage'
            ]
        });
        
        const context = await browser.newContext({
            userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            viewport: { width: 1920, height: 1080 }
        });
        
        const page = await context.newPage();
        
        console.log(`\n📱 正在打開微信公眾號後台...`);
        console.log('💡 提示：請使用微信掃碼登錄，或輸入賬號密碼登錄');
        console.log('⏳ 等待登錄完成...\n');
        
        // 打開微信公眾號後台
        await page.goto(WECHAT_URL, { waitUntil: 'networkidle' });
        
        // 等待用戶登錄（最長 5 分鐘）
        console.log('⏰ 請在 5 分鐘內完成登錄...');
        console.log('登錄後任意導航一個頁面（如"發表文章"）然後告訴我...\n');
        
        // 等待用戶確認
        await question('✅ 登錄完成後，按回車繼續...');
        
        // 再訪問一個頁面確保 Cookie 完整
        console.log('\n🔄 正在獲取完整 Cookie...');
        try {
            await page.goto('https://mp.weixin.qq.com/cgi-bin/home', { 
                waitUntil: 'networkidle',
                timeout: 10000 
            });
            await page.waitForTimeout(2000);
        } catch (e) {
            console.log('⚠️  二級頁面加載失敗，繼續使用當前 Cookie');
        }
        
        // 獲取所有 Cookie
        const cookies = await context.cookies();
        
        if (cookies.length === 0) {
            console.log('\n❌ 未獲取到 Cookie，請確認是否成功登錄');
            return;
        }
        
        // 保存 Cookie
        ensureDir(COOKIES_DIR);
        saveCookies(cookies, COOKIES_FILE);
        
        // 驗證 Cookie
        console.log('\n🔍 驗證 Cookie...');
        const wechatCookies = cookies.filter(c => 
            c.domain && (c.domain.includes('qq.com') || c.domain.includes('wechat.com'))
        );
        
        if (wechatCookies.length > 0) {
            console.log(`✅ 驗證成功！找到 ${wechatCookies.length} 個微信相關 Cookie`);
            
            // 顯示關鍵 Cookie（隱藏值）
            const importantCookies = ['slave_user', 'slave_sid', 'uin', 'key', 'pass_ticket'];
            console.log('\n📋 關鍵 Cookie:');
            importantCookies.forEach(name => {
                const cookie = cookies.find(c => c.name === name);
                if (cookie) {
                    const maskedValue = cookie.value.substring(0, 10) + '...';
                    console.log(`  ✅ ${name}: ${maskedValue}`);
                }
            });
            
            console.log('\n✅ Cookie 導出完成！');
            console.log('\n📖 下一步：');
            console.log('  1. 設置環境變量：export WECHAT_COOKIES_ENABLED=true');
            console.log('  2. 運行抓取：node index.js "https://mp.weixin.qq.com/s/xxx"');
            console.log('  3. 或使用 Docker：docker run -e WECHAT_COOKIES_ENABLED=true ...');
            
        } else {
            console.log('⚠️  未找到微信相關 Cookie，可能登錄有問題');
            console.log('💡 請確認登錄的是微信公眾號後台 (mp.weixin.qq.com)');
        }
        
    } catch (error) {
        console.error('❌ 錯誤:', error.message);
    } finally {
        if (browser) {
            await browser.close();
        }
    }
}

// 命令行輸入
const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

function question(query) {
    return new Promise(resolve => {
        rl.question(query, answer => {
            resolve(answer);
        });
    });
}

// 運行
if (require.main === module) {
    exportCookies().then(() => {
        rl.close();
        process.exit(0);
    });
}

module.exports = { exportCookies };
