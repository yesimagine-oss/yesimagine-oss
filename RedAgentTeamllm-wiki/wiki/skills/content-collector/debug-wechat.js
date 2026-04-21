#!/usr/bin/env node
/**
 * 🧪 微信文章調試腳本
 * 用途：截圖 + 打印 HTML 結構，幫助診斷選擇器問題
 */

const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

async function debugWeChat(url) {
    console.log('🔍 開始調試微信文章...');
    console.log('📎 URL:', url);
    
    let browser = null;
    
    try {
        // 啟動瀏覽器
        console.log('\n🌐 啟動 Chromium...');
        browser = await chromium.launch({
            headless: true,
            args: [
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-dev-shm-usage',
                '--disable-gpu'
            ]
        });
        
        const context = await browser.newContext({
            userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            viewport: { width: 1920, height: 1080 }
        });
        
        const page = await context.newPage();
        
        // 訪問頁面
        console.log('⏳ 加載頁面...');
        const response = await page.goto(url, {
            waitUntil: 'networkidle',
            timeout: 30000
        });
        
        console.log('📊 響應狀態:', response.status());
        
        // 截圖
        const screenshotPath = '/tmp/wechat-debug.png';
        console.log('📸 截取全屏...');
        await page.screenshot({ path: screenshotPath, fullPage: true });
        console.log('✅ 截圖已保存:', screenshotPath);
        
        // 獲取頁面標題
        const title = await page.title();
        console.log('📄 頁面標題:', title);
        
        // 檢查常見選擇器
        console.log('\n🔍 檢查選擇器...');
        const selectors = [
            '#js_content',
            '.rich_media_content',
            'article.rich_media_area',
            '.js_article_content',
            'section[class*="rich_media"]',
            '[data-role="body"]',
            'article',
            '#content',
            'h1.rich_media_title',
            '#js_name',
            '#publish_time'
        ];
        
        for (const selector of selectors) {
            try {
                const element = await page.$(selector);
                if (element) {
                    const text = await element.textContent();
                    console.log(`✅ ${selector}: 存在 (${text.length} 字符)`);
                    if (text.length < 200) {
                        console.log(`   內容：${text.trim().substring(0, 100)}`);
                    }
                } else {
                    console.log(`❌ ${selector}: 不存在`);
                }
            } catch (e) {
                console.log(`❌ ${selector}: 錯誤 - ${e.message}`);
            }
        }
        
        // 獲取 body HTML 前 1000 字符
        console.log('\n📄 Body HTML (前 1000 字符):');
        const bodyHtml = await page.innerHTML('body');
        console.log(bodyHtml.substring(0, 1000));
        
        // 檢查是否是錯誤頁面
        const bodyText = await page.innerText('body');
        if (bodyText.includes('已刪除') || bodyText.includes('無法訪問') || bodyText.includes('內容不存在')) {
            console.log('\n⚠️  檢測到錯誤頁面：文章可能已刪除或無法訪問');
        }
        
    } catch (error) {
        console.error('❌ 調試失敗:', error.message);
    } finally {
        if (browser) {
            await browser.close();
        }
    }
}

// 測試 URL
const testUrl = process.argv[2] || 'https://mp.weixin.qq.com/s/4pFM8ILPNOzfw9G_9rV5Dw';
debugWeChat(testUrl);
