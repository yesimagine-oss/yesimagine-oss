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
    
    const text = await page.evaluate(() => document.body.innerText);
    console.log('页面文本前 300 字:');
    console.log(text.substring(0, 300));
    
    if (text.includes('环境异常') || text.includes('验证')) {
        console.log('\n❌ 遇到验证页面');
    } else {
        console.log('\n✅ 可能是正常页面');
    }
    
    await browser.close();
})();
