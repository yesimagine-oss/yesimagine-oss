const playwright = require('playwright');

(async () => {
    const cookies = require('/home/admin/.openclaw/workspace/cookies/wechat-cookies.json');
    
    const browser = await playwright.chromium.launch({
        headless: true,
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    });
    
    const context = await browser.newContext({
        userAgent: 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.0'
    });
    await context.addCookies(cookies);
    
    const page = await context.newPage();
    
    console.log('测试文章:', 'https://mp.weixin.qq.com/s/L8H0Kl0ecXOk7yTwpI7RTA');
    await page.goto('https://mp.weixin.qq.com/s/L8H0Kl0ecXOk7yTwpI7RTA', { waitUntil: 'domcontentloaded', timeout: 30000 });
    
    const text = await page.evaluate(() => document.body.innerText);
    console.log('内容长度:', text.length);
    console.log('前 200 字:');
    console.log(text.substring(0, 200));
    
    if (text.includes('环境异常') || text.includes('验证')) {
        console.log('\n❌ 验证页面');
    } else if (text.length > 500) {
        console.log('\n✅ 成功！');
        console.log('标题:', await page.title());
    } else {
        console.log('\n⚠️ 内容异常');
    }
    
    await browser.close();
})();
