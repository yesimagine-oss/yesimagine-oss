const playwright = require('playwright');

(async () => {
    const cookies = require('/home/admin/.openclaw/workspace/cookies/wechat-cookies.json');
    
    const browser = await playwright.chromium.launch({
        headless: true,
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    });
    
    const context = await browser.newContext();
    await context.addCookies(cookies);
    
    const page = await context.newPage();
    
    // 测试腾讯新闻的公众号文章
    const testUrls = [
        'https://mp.weixin.qq.com/s/2DzKqANd8M3sVqXz8cVJhQ',
        'https://mp.weixin.qq.com/s/pbs9Z8ZqfvLlQbTpE9QJOA',
    ];
    
    for (const url of testUrls) {
        console.log('\n测试:', url);
        try {
            await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 20000 });
            const text = await page.evaluate(() => document.body.innerText);
            
            if (text.includes('环境异常') || text.includes('验证')) {
                console.log('❌ 验证页面');
            } else if (text.length > 500) {
                console.log('✅ 成功！内容长度:', text.length);
                console.log('标题:', await page.title());
                break;
            } else {
                console.log('⚠️ 内容太少:', text.length);
            }
        } catch (e) {
            console.log('❌ 错误:', e.message);
        }
    }
    
    await browser.close();
})();
