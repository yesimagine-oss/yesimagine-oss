#!/usr/bin/env node
/**
 * 📦 Content Collector - 內容收藏系統（Playwright 版）
 * 
 * 作者：麻小
 * 版本：3.0.0
 * 創建：2026-03-18
 * 更新：2026-03-18（集成 Playwright 方案）
 * 
 * 核心功能：
 * 1. 微信文章抓取（Playwright 瀏覽器自動化）
 * 2. 普通網頁收藏（web_fetch 或 Playwright）
 * 3. 內容提取（Cheerio HTML 解析）
 * 4. Markdown 轉換（Turndown）
 * 5. 圖片下載（可選）
 * 6. 項目自動關聯
 * 7. 結構化存儲
 */

const { chromium } = require('playwright');
const cheerio = require('cheerio');
const TurndownService = require('turndown');
const fs = require('fs');
const path = require('path');
const https = require('https');

// ==================== 配置區 ====================

const CONFIG = {
    // 收藏庫目錄（支持環境變量，Docker 優先）
    collectionsDir: process.env.COLLECTIONS_DIR || path.join(process.env.HOME || '~', '.openclaw/workspace/collections'),
    
    // Cookie 配置（微信文章用）
    cookies: {
        // Cookie 文件路徑（JSON 格式）
        filePath: process.env.WECHAT_COOKIES_PATH || path.join(process.env.HOME || '~', '.openclaw/workspace/cookies/wechat-cookies.json'),
        // 是否使用 Cookie
        enabled: process.env.WECHAT_COOKIES_ENABLED === 'true'
    },
    
    // 瀏覽器配置
    browser: {
        headless: true,
        timeout: 30000,
        userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    },
    
    // 圖片下載配置
    images: {
        download: true,
        dir: 'images'
    },
    
    // 項目關鍵詞（自動關聯）
    projects: {
        'wemp-ops': ['公眾號', '寫作', '文章', '排版', '內容運營', '微信'],
        'xiaohongshu-ops': ['小紅書', '筆記', '種草', '配圖', '短內容'],
        'content-collector': ['收藏', '知識管理', '素材庫', '內容采集']
    }
};

// ==================== 核心類 ====================

class ContentCollector {
    constructor(options = {}) {
        this.config = { ...CONFIG, ...options };
        this.ensureDirectories();
    }
    
    /**
     * 確保存儲目錄存在
     */
    ensureDirectories() {
        const dirs = [
            this.config.collectionsDir,
            path.join(this.config.collectionsDir, 'wechat'),
            path.join(this.config.collectionsDir, 'articles'),
            path.join(this.config.collectionsDir, 'images'),
        ];
        
        dirs.forEach(dir => {
            if (!fs.existsSync(dir)) {
                fs.mkdirSync(dir, { recursive: true });
                console.log(`📁 創建目錄：${dir}`);
            }
        });
    }
    
    /**
     * 載入 Cookie
     * @returns {Array} Cookie 數組
     */
    loadCookies() {
        const cookiePath = this.config.cookies.filePath;
        
        if (!fs.existsSync(cookiePath)) {
            throw new Error(`Cookie 文件不存在：${cookiePath}`);
        }
        
        const cookieData = fs.readFileSync(cookiePath, 'utf-8');
        const cookies = JSON.parse(cookieData);
        
        // 確保 Cookie 格式正確
        if (!Array.isArray(cookies)) {
            throw new Error('Cookie 文件格式錯誤，應該是數組');
        }
        
        // 過濾微信相關的 Cookie
        const wechatCookies = cookies.filter(cookie => 
            cookie.domain && (
                cookie.domain.includes('qq.com') ||
                cookie.domain.includes('wechat.com')
            )
        );
        
        console.log(`🔍 找到 ${wechatCookies.length}/${cookies.length} 個微信相關 Cookie`);
        
        return wechatCookies;
    }
    
    /**
     * 收藏內容的主入口
     * @param {string} url - 內容鏈接
     * @returns {Promise<Object>} 收藏結果
     */
    async collect(url) {
        console.log(`📦 開始收藏：${url}`);
        
        try {
            // 步驟 1: 識別內容類型
            const category = this.identifyType(url);
            console.log(`📋 內容類型：${category}`);
            
            // 步驟 2: 抓取內容
            const result = await this.fetchContent(url, category);
            if (!result.success) {
                return {
                    success: false,
                    message: `❌ 抓取失敗：${result.error}`
                };
            }
            
            // 步驟 3: 提取元數據
            const metadata = this.extractMetadata(result.data, url, category);
            
            // 步驟 4: 下載圖片（可選）
            let imageResults = [];
            if (this.config.images.download && result.data.images?.length > 0) {
                imageResults = await this.downloadImages(result.data.images, metadata.slug, category);
            }
            
            // 步驟 5: 保存到文件
            const filePath = this.saveToFile(metadata, result.data.content, imageResults, category);
            
            // 步驟 6: 更新索引
            this.updateIndex(metadata);
            
            return {
                success: true,
                title: metadata.title,
                category: category,
                file_path: filePath,
                images_count: imageResults.length,
                related_projects: metadata.related_projects,
                message: `✅ 已收藏：${metadata.title}`
            };
            
        } catch (error) {
            console.error('❌ 收藏失敗:', error.message);
            return {
                success: false,
                message: `❌ 異常：${error.message}`
            };
        }
    }
    
    /**
     * 識別內容類型
     */
    identifyType(url) {
        if (url.includes('mp.weixin.qq.com')) {
            return 'wechat';
        }
        return 'articles';
    }
    
    /**
     * 抓取內容
     */
    async fetchContent(url, category) {
        if (category === 'wechat') {
            return await this.fetchWeChat(url);
        } else {
            return await this.fetchWebpage(url);
        }
    }
    
    /**
     * 抓取微信文章（核心功能）
     */
    async fetchWeChat(url) {
        console.log('🚀 啟動瀏覽器抓取微信文章...');
        
        let browser = null;
        
        try {
            // 檢測是否在 Docker 環境中
            const isDocker = fs.existsSync('/.dockerenv') || process.env.CONTAINER === 'true';
            if (isDocker) {
                console.log('🐳 檢測到 Docker 環境，使用優化配置');
            }
            
            // 1. 啟動瀏覽器
            console.log('🌐 啟動 Chromium...');
            browser = await chromium.launch({
                headless: this.config.browser.headless,
                // Docker 環境需要特殊配置
                args: [
                    '--no-sandbox',
                    '--disable-setuid-sandbox',
                    '--disable-dev-shm-usage',
                    '--disable-accelerated-2d-canvas',
                    '--no-first-run',
                    '--no-zygote',
                    '--disable-gpu'
                ],
                // Docker 環境中可能需要超時更長
                timeout: isDocker ? 60000 : 30000
            });
            
            // 2. 創建瀏覽器上下文
            const contextOptions = {
                userAgent: this.config.browser.userAgent,
                viewport: { width: 1920, height: 1080 }
            };
            
            // 注入 Cookie（如果啟用）
            if (this.config.cookies.enabled) {
                console.log('🍪 正在載入 Cookie...');
                try {
                    const cookies = this.loadCookies();
                    if (cookies && cookies.length > 0) {
                        contextOptions.cookies = cookies;
                        console.log(`✅ 已載入 ${cookies.length} 個 Cookie`);
                    } else {
                        console.log('⚠️  Cookie 文件為空，將不使用 Cookie');
                    }
                } catch (error) {
                    console.log('⚠️  Cookie 載入失敗:', error.message);
                    console.log('💡 提示：請先運行導出工具獲取 Cookie');
                }
            }
            
            const context = await browser.newContext(contextOptions);
            
            const page = await context.newPage();
            
            // 3. 訪問頁面
            console.log('⏳ 加載頁面...');
            await page.goto(url, {
                waitUntil: 'networkidle',
                timeout: this.config.browser.timeout
            });
            
            // 4. 等待正文加載（關鍵！）
            console.log('⏳ 等待正文加載...');
            
            // 微信文章可能的選擇器（按優先級排序）
            const selectors = [
                '#js_content',           // 標準微信文章
                '.rich_media_content',   // 舊版微信
                'article.rich_media_area', // 另一種結構
                '.js_article_content',   // 移動版
                'section[class*="rich_media"]', // 通用選擇器
                '[data-role="body"]',    // 數據屬性
                'article',               // 語義化標籤
                '#content',              // 通用內容區
                'body'                   // 最後手段
            ];
            
            let contentSelector = null;
            
            for (const selector of selectors) {
                try {
                    await page.waitForSelector(selector, { timeout: 3000, state: 'visible' });
                    contentSelector = selector;
                    console.log(`✅ 找到正文選擇器：${selector}`);
                    break;
                } catch (e) {
                    continue;
                }
            }
            
            if (!contentSelector) {
                // 如果都沒有，截圖調試並等待更久
                console.log('⚠️  未找到標準選擇器，截圖調試...');
                try {
                    await page.screenshot({ path: '/tmp/wechat-debug.png', fullPage: true });
                    console.log('📸 調試截圖已保存：/tmp/wechat-debug.png');
                } catch (e) {
                    console.log('⚠️  截圖失敗:', e.message);
                }
                
                await page.waitForTimeout(5000);
                contentSelector = 'body';
                console.log('⚠️  使用 body 作為最後手段');
            }
            
            // 額外等待確保動態內容加載（微信文章可能有延遲加載）
            await page.waitForTimeout(3000);
            
            // 滾動頁面確保所有內容加載
            console.log('📜 滾動頁面加載延遲內容...');
            await page.evaluate(() => {
                window.scrollTo(0, document.body.scrollHeight);
            });
            await page.waitForTimeout(2000);
            await page.evaluate(() => {
                window.scrollTo(0, 0);
            });
            await page.waitForTimeout(1000);
            
            // 5. 獲取頁面 HTML
            console.log('📄 提取頁面內容...');
            const html = await page.content();
            
            // 6. 使用 Cheerio 解析 HTML
            const $ = cheerio.load(html);
            
            // 7. 提取元數據
            const title = $('h1.rich_media_title').text().trim();
            const author = $('#js_name').text().trim();
            const publishTime = $('#publish_time').text().trim();
            
            console.log(`✅ 標題：${title}`);
            console.log(`✅ 作者：${author}`);
            
            // 8. 提取正文 HTML
            let contentHtml = $('#js_content').html();
            
            // 9. 清理不需要的元素
            const $content = cheerio.load(`<div>${contentHtml}</div>`);
            $content('script, style').remove();
            contentHtml = $content('div').html();
            
            // 10. 提取圖片
            const images = [];
            $('#js_content img').each((i, el) => {
                const src = $(el).attr('data-src') || $(el).attr('src');
                if (src) {
                    images.push(src);
                }
            });
            
            // 11. 轉換為 Markdown
            console.log('📝 轉換為 Markdown...');
            const turndown = new TurndownService({
                headingStyle: 'atx',
                bulletListMarker: '-',
                codeBlockStyle: 'fenced'
            });
            
            const content = turndown.turndown(contentHtml);
            
            console.log(`✅ 提取完成！正文 ${content.length} 字符，${images.length} 張圖片`);
            
            await browser.close();
            
            return {
                success: true,
                data: {
                    title,
                    author,
                    publishTime,
                    content,
                    images,
                    wordCount: content.length,
                    originalUrl: url,
                    fetchTime: new Date().toISOString()
                }
            };
            
        } catch (error) {
            console.error('❌ 抓取失敗:', error.message);
            
            if (browser) {
                await browser.close();
            }
            
            return {
                success: false,
                error: error.message
            };
        }
    }
    
    /**
     * 抓取普通網頁
     */
    async fetchWebpage(url) {
        console.log('📄 使用 Playwright 抓取網頁...');
        
        let browser = null;
        
        try {
            browser = await chromium.launch({
                headless: this.config.browser.headless,
                args: ['--no-sandbox', '--disable-setuid-sandbox']
            });
            
            const context = await browser.newContext({
                userAgent: this.config.browser.userAgent
            });
            
            const page = await context.newPage();
            
            await page.goto(url, {
                waitUntil: 'networkidle',
                timeout: this.config.browser.timeout
            });
            
            const html = await page.content();
            const $ = cheerio.load(html);
            
            // 提取標題
            const title = $('h1').first().text().trim() || $('title').text().trim();
            
            // 提取正文（嘗試多個選擇器）
            let contentHtml = $('article').html() || $('main').html() || $('body').html();
            
            // 轉換為 Markdown
            const turndown = new TurndownService({
                headingStyle: 'atx',
                bulletListMarker: '-',
                codeBlockStyle: 'fenced'
            });
            
            const content = turndown.turndown(contentHtml);
            
            // 提取圖片
            const images = [];
            $('img').each((i, el) => {
                const src = $(el).attr('src') || $(el).attr('data-src');
                if (src && src.startsWith('http')) {
                    images.push(src);
                }
            });
            
            await browser.close();
            
            return {
                success: true,
                data: {
                    title,
                    content,
                    images,
                    originalUrl: url,
                    fetchTime: new Date().toISOString()
                }
            };
            
        } catch (error) {
            console.error('❌ 抓取失敗:', error.message);
            
            if (browser) {
                await browser.close();
            }
            
            return {
                success: false,
                error: error.message
            };
        }
    }
    
    /**
     * 提取元數據
     */
    extractMetadata(data, url, category) {
        const title = data.title || '未命名文章';
        
        // 生成 slug
        const slug = this.generateSlug(title);
        
        // 項目自動關聯
        const relatedProjects = this.matchProjects(title, data.content);
        
        return {
            title: title,
            author: data.author || '未知',
            pub_date: data.publishTime || null,
            url: url,
            category: category,
            slug: slug,
            date: new Date().toISOString().split('T')[0],
            timestamp: new Date().toISOString(),
            summary: data.content.substring(0, 200) + '...',
            keywords: this.extractKeywords(title),
            related_projects: relatedProjects
        };
    }
    
    /**
     * 生成 URL 友好的 slug
     */
    generateSlug(title) {
        // 移除特殊字符，保留中文
        let slug = title.replace(/[^\w\s\u4e00-\u9fff-]/g, '');
        // 替換空格為連字符
        slug = slug.replace(/\s+/g, '-');
        // 限制長度
        return slug.substring(0, 50).toLowerCase();
    }
    
    /**
     * 提取關鍵詞
     */
    extractKeywords(text) {
        const words = text.split(/[,,.!?.\s]+/);
        return words.filter(w => w.length >= 2).slice(0, 5);
    }
    
    /**
     * 項目自動關聯
     */
    matchProjects(title, content) {
        const matched = [];
        const text = `${title} ${content}`;
        
        for (const [project, keywords] of Object.entries(this.config.projects)) {
            for (const kw of keywords) {
                if (text.includes(kw)) {
                    matched.push(project);
                    break;
                }
            }
        }
        
        return matched;
    }
    
    /**
     * 下載圖片
     */
    async downloadImages(images, slug, category) {
        console.log(`🖼️  開始下載 ${images.length} 張圖片...`);
        
        const imageDir = path.join(
            this.config.collectionsDir,
            category,
            CONFIG.images.dir,
            slug
        );
        
        if (!fs.existsSync(imageDir)) {
            fs.mkdirSync(imageDir, { recursive: true });
        }
        
        const results = [];
        
        for (let i = 0; i < images.length; i++) {
            const url = images[i];
            const filename = `${String(i + 1).padStart(2, '0')}-image.png`;
            const filePath = path.join(imageDir, filename);
            
            try {
                await this.downloadFile(url, filePath);
                results.push({
                    index: i,
                    success: true,
                    path: path.join(category, CONFIG.images.dir, slug, filename),
                    url: url
                });
                console.log(`  ✅ 下載 ${i + 1}/${images.length}: ${filename}`);
            } catch (error) {
                results.push({
                    index: i,
                    success: false,
                    error: error.message,
                    url: url
                });
                console.log(`  ❌ 下載失敗 ${i + 1}/${images.length}: ${error.message}`);
            }
            
            // 延遲避免觸發頻率限制
            await this.delay(500);
        }
        
        return results.filter(r => r.success);
    }
    
    /**
     * 下載文件
     */
    downloadFile(url, filePath) {
        return new Promise((resolve, reject) => {
            const file = fs.createWriteStream(filePath);
            
            https.get(url, (response) => {
                if (response.statusCode !== 200) {
                    reject(new Error(`下載失敗：${response.statusCode}`));
                    return;
                }
                
                response.pipe(file);
                file.on('finish', () => {
                    file.close();
                    resolve(filePath);
                });
            }).on('error', reject);
        });
    }
    
    /**
     * 延遲
     */
    delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
    
    /**
     * 保存到文件
     */
    saveToFile(metadata, content, imageResults, category) {
        const filename = `${metadata.date}-${metadata.slug}.md`;
        const dirPath = path.join(this.config.collectionsDir, category);
        const filePath = path.join(dirPath, filename);
        
        // 生成 frontmatter
        let frontmatter = `---
title: "${metadata.title}"
url: "${metadata.url}"
author: "${metadata.author}"
date: ${metadata.date}
`;
        
        if (metadata.pub_date) {
            frontmatter += `published: "${metadata.pub_date}"
`;
        }
        
        frontmatter += `tags: [${metadata.keywords.join(', ')}]
related_projects: [${metadata.related_projects.map(p => `"${p}"`).join(', ')}]
collected_at: ${metadata.timestamp}
---

`;
        
        // 添加作者和日期信息
        let header = '';
        if (metadata.author !== '未知' || metadata.pub_date) {
            header += `**作者**: ${metadata.author}\n\n`;
            if (metadata.pub_date) {
                header += `**發布日期**: ${metadata.pub_date}\n\n`;
            }
        }
        
        // 添加插圖章節
        let imagesSection = '';
        if (imageResults.length > 0) {
            imagesSection = '\n\n## 🖼️ 插圖\n\n';
            imageResults.forEach(img => {
                imagesSection += `![插圖](${img.path})\n`;
            });
        }
        
        // 寫入文件
        fs.writeFileSync(filePath, frontmatter + header + content + imagesSection, 'utf-8');
        
        console.log(`💾 已保存：${filePath}`);
        return filePath;
    }
    
    /**
     * 更新索引
     */
    updateIndex(metadata) {
        const indexPath = path.join(this.config.collectionsDir, 'index.md');
        
        let indexContent = '';
        if (fs.existsSync(indexPath)) {
            indexContent = fs.readFileSync(indexPath, 'utf-8');
        } else {
            indexContent = '# 📚 收藏索引\n\n';
        }
        
        // 添加新條目
        const newEntry = `- [${metadata.title}](${metadata.category}/${metadata.date}-${metadata.slug}.md) ${metadata.keywords.map(kw => `#${kw}`).join(' ')}\n`;
        
        const dateSection = `\n## ${metadata.date}\n\n`;
        if (!indexContent.includes(dateSection)) {
            indexContent += dateSection;
        }
        
        indexContent += newEntry;
        
        fs.writeFileSync(indexPath, indexContent, 'utf-8');
        
        console.log(`📑 已更新索引：${indexPath}`);
    }
}

// ==================== 導出 ====================

module.exports = { ContentCollector };

// ==================== 命令行入口 ====================

if (require.main === module) {
    const url = process.argv[2];
    
    if (!url) {
        console.log('用法：node index.js <URL>');
        console.log('示例：node index.js https://mp.weixin.qq.com/s/xxx');
        process.exit(1);
    }
    
    const collector = new ContentCollector();
    collector.collect(url).then(result => {
        if (result.success) {
            console.log('\n✅ 收藏成功！');
            console.log(`📄 標題：${result.title}`);
            console.log(`📁 位置：${result.file_path}`);
            console.log(`🖼️  圖片：${result.images_count} 張`);
            if (result.related_projects.length > 0) {
                console.log(`🎯 關聯項目：${result.related_projects.join(', ')}`);
            }
        } else {
            console.error('\n❌ 收藏失敗:', result.message);
            process.exit(1);
        }
    });
}
