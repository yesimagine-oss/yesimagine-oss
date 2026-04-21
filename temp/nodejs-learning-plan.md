# 📚 Node.js + Playwright 学习计划

**创建时间:** 2026-03-15 12:55  
**目标:** 掌握 Node.js 基础和 Playwright 自动化

---

## 📅 5 天学习计划

### Day 1: JavaScript 基础

#### 上午 (2 小时)
- [ ] **变量与数据类型**
  ```javascript
  // let vs const vs var
  let name = "John";
  const age = 30;
  
  // 数据类型
  const str = "hello";
  const num = 42;
  const bool = true;
  const arr = [1, 2, 3];
  const obj = { key: "value" };
  ```

- [ ] **函数**
  ```javascript
  // 普通函数
  function greet(name) {
    return `Hello, ${name}!`;
  }
  
  // 箭头函数
  const greet = (name) => `Hello, ${name}!`;
  ```

#### 下午 (2 小时)
- [ ] **对象和数组操作**
  ```javascript
  // 解构
  const { name, age } = person;
  const [first, second] = array;
  
  // 数组方法
  const result = arr.map(x => x * 2);
  const filtered = arr.filter(x => x > 2);
  ```

- [ ] **模块系统**
  ```javascript
  // CommonJS
  const module = require('module');
  module.exports = something;
  
  // ES6 Modules
  import something from 'module';
  export default something;
  ```

#### 晚上 (1 小时)
- [ ] **练习:** 编写 10 个小练习
- [ ] **总结:** 记录学习笔记

---

### Day 2: 异步编程

#### 上午 (2 小时)
- [ ] **Callback**
  ```javascript
  function fetchData(callback) {
    setTimeout(() => {
      callback("data");
    }, 1000);
  }
  
  fetchData((data) => console.log(data));
  ```

- [ ] **Promise**
  ```javascript
  const promise = new Promise((resolve, reject) => {
    setTimeout(() => resolve("done"), 1000);
  });
  
  promise.then(result => console.log(result));
  ```

#### 下午 (2 小时)
- [ ] **Async/Await**
  ```javascript
  async function fetchData() {
    const result = await promise;
    return result;
  }
  ```

- [ ] **错误处理**
  ```javascript
  try {
    const result = await fetchData();
  } catch (error) {
    console.error(error);
  }
  ```

#### 晚上 (1 小时)
- [ ] **练习:** 异步编程练习
- [ ] **总结:** 记录难点

---

### Day 3: Node.js 基础

#### 上午 (2 小时)
- [ ] **Node.js 安装**
  ```bash
  # 使用 nvm 安装
  curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
  nvm install 18
  nvm use 18
  ```

- [ ] **npm 包管理**
  ```bash
  npm init -y
  npm install playwright
  npm install axios
  ```

#### 下午 (2 小时)
- [ ] **文件系统操作**
  ```javascript
  const fs = require('fs').promises;
  
  async function readFile() {
    const content = await fs.readFile('file.txt', 'utf8');
    console.log(content);
  }
  ```

- [ ] **路径处理**
  ```javascript
  const path = require('path');
  const fullPath = path.join(__dirname, 'file.txt');
  ```

#### 晚上 (1 小时)
- [ ] **练习:** 文件读写练习
- [ ] **总结:** Node.js 特性

---

### Day 4: Playwright 入门

#### 上午 (2 小时)
- [ ] **安装 Playwright**
  ```bash
  npm install -g playwright
  npx playwright install chromium
  ```

- [ ] **第一个脚本**
  ```javascript
  const { chromium } = require('playwright');
  
  (async () => {
    const browser = await chromium.launch();
    const page = await browser.newPage();
    await page.goto('https://example.com');
    console.log(await page.title());
    await browser.close();
  })();
  ```

#### 下午 (2 小时)
- [ ] **元素定位**
  ```javascript
  // CSS 选择器
  await page.click('.button');
  
  // XPath
  await page.click('//button[text()="Submit"]');
  
  // Text 选择器
  await page.click('text=Submit');
  ```

- [ ] **表单操作**
  ```javascript
  await page.fill('#username', 'user');
  await page.fill('#password', 'pass');
  await page.click('button[type="submit"]');
  ```

#### 晚上 (1 小时)
- [ ] **练习:** 自动化简单网页
- [ ] **总结:** Playwright API

---

### Day 5: 实战项目

#### 上午 (2 小时)
- [ ] **项目：微信文章读取**
  ```javascript
  const { chromium } = require('playwright');
  
  async function readWeChatArticle(url) {
    const browser = await chromium.launch();
    const page = await browser.newPage();
    await page.goto(url);
    
    const title = await page.$eval('#activity-name', el => el.textContent);
    const content = await page.$eval('#js_content', el => el.textContent);
    
    await browser.close();
    return { title, content };
  }
  ```

#### 下午 (2 小时)
- [ ] **完善项目**
  - 错误处理
  - 日志记录
  - 配置管理

#### 晚上 (1 小时)
- [ ] **总结:** 5 天学习总结
- [ ] **规划:** 下一步学习方向

---

## 📖 推荐资源

### 官方文档
- [Node.js 官方](https://nodejs.org/docs/)
- [Playwright 官方](https://playwright.dev/docs/intro)

### 中文教程
- [JavaScript.info 中文版](https://zh.javascript.info/)
- [Playwright 中文文档](https://playwright.bootcss.com/)

### 视频课程
- B 站搜索 "Node.js 教程"
- YouTube "Playwright Tutorial"

---

## 📝 每日记录模板

```markdown
## Day X - YYYY-MM-DD

### 学习内容
- 

### 练习代码
```javascript

```

### 遇到的问题
1. 

### 解决方案
1. 

### 明日计划
- 

```

---

**预计完成时间:** 2026-03-20  
**总学习时间:** 25 小时
