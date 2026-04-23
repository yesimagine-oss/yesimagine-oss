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
    await page.goto('https://mp.weixin.qq.com/s/jkepV1FRdAAeklOsUaLmew', { waitUntil: 'domcontentloaded' });
    
    const content = await page.content();
    console.log('页面标题:', await page.title());
    console.log('内容长度:', content.length);
    console.log('前 500 字符:', content.substring(0, 500));
    
    await browser.close();
})();
