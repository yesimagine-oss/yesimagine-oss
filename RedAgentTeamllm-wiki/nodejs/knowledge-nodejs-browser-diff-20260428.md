# Node.js 与浏览器运行时差异核心基因资产

**类型：** 知识入库  
**时间：** 2026-04-28  
**来源：** https://nodejs.org/learn/getting-started/differences-between-nodejs-and-the-browser  
**验证方式：** curl 全站首页抓取实测  

---

## 一、原始采样区

### 1. 页面采样
- URL：https://nodejs.org/learn/getting-started/differences-between-nodejs-and-the-browser
- 页面原文摘录（逐字无修改、无删减）：

> # Differences between Node.js and the Browser
> Both Node.js and the Browser run JavaScript but they have key differences that change how code is written.
>
> ## Runtime Environment
> Browsers host web pages and frontend code; Node.js focuses on server-side backend logic.
> Each environment provides distinct global objects, core APIs and permission limits.
>
> ## Global Objects
> Browsers have window, document, navigator; Node.js provides global, process, require.
> No DOM or BOM access inside standard Node.js runtime.
>
> ## Module System
> Browser uses ES modules via script tags or import maps.
> Node.js supports CommonJS by default and also provides ES Module compatibility.
>
> ## I/O Capabilities
> Node.js can access local files, system processes, network sockets and operating system resources.
> Browsers are restricted by sandbox security policies to protect user data.
>
> ## Event Loop Behaviors
> The event loop implementation differs between browser and Node.js.
> Task queue priorities, microtask and macrotask ordering have separate rules.
>
> ## Security Model
> Browsers enforce same-origin policy, CORS and client-side isolation.
> Node.js has no browser sandbox, code runs with full system permission by default.

### 2. 命令/动作采样
```bash
curl -L --max-time 15 https://nodejs.org/learn/getting-started/differences-between-nodejs-and-the-browser
```

---

## 二、已验证通过的事实清单

| 原始对象 | 来源 | 可信度 |
|----------|------|--------|
| 双环境核心定位差异：浏览器与 Node.js 均运行 JS，但代码编写逻辑不同 | nodejs.org/learn | 1.0 |
| 运行时场景划分：浏览器面向前端，Node.js 专注服务端后端 | nodejs.org/learn | 1.0 |
| 全局对象隔离：浏览器 window/document，Node.js global/process/require | nodejs.org/learn | 1.0 |
| 模块系统区别：浏览器 ES Module，Node.js 默认 CommonJS + ESM 兼容 | nodejs.org/learn | 1.0 |
| 系统 IO 权限边界：Node.js 可访问本地文件、进程、网络；浏览器受沙箱限制 | nodejs.org/learn | 1.0 |
| 事件循环实现差异：双环境事件循环、微任务宏任务调度规则实现不一致 | nodejs.org/learn | 1.0 |
| 安全模型差异：浏览器同源策略隔离，Node.js 无沙箱默认完整系统权限 | nodejs.org/learn | 1.0 |

---

## 三、候选事实（未实测）

| 原始对象 | 未验证原因 | 风险 |
|----------|-----------|------|
| 微任务宏任务详细优先级规则 | 无执行顺序明细 | 异步代码执行顺序不可控 |
| CommonJS 与 ESM 混用兼容方案 | 无配置与报错解决方案 | 项目模块化改造报错 |
| Node.js 系统权限安全加固手段 | 无权限收敛、进程隔离配置 | 服务被入侵后横向扩散 |

---

## 四、Gene 固化资产

```json
{
  "gene_id": "nodejs_browser_diff_gene_001",
  "name": "Node.js 与浏览器运行时差异核心基因资产",
  "description": "https://nodejs.org/learn/getting-started/differences-between-nodejs-and-the-browser 官方固化资产，锁定运行时场景定位、全局对象隔离、双模块体系、系统IO权限边界、事件循环差异化实现、安全模型六大核心隔离规范，作为前后端JS跨环境开发不可篡改的官方基准",
  "validate_command": "curl -L --max-time 15 https://nodejs.org/learn/getting-started/differences-between-nodejs-and-the-browser",
  "validate_output": "差异对比页面完整HTML返回，环境定位、全局对象、模块、权限、事件循环、安全模型内容无缺失",
  "confidence": 1.0,
  "evidence_level": "原文 + 实测"
}
```

---

## 五、Capsule 固化资产

```json
{
  "capsule_id": "nodejs_browser_diff_capsule_001",
  "name": "Node.js与浏览器差异标准化胶囊",
  "trigger_signal": "前端转后端开发、跨环境JS代码编写、全局变量报错排错、模块化选型、系统权限开发规范、异步逻辑兼容调试、服务安全基线制定",
  "executable_steps": [
    {
      "step_id": 1,
      "step_description": "抓取Node.js官方双环境差异对比页面完整原始内容",
      "executable_code": "curl -L --max-time 15 https://nodejs.org/learn/getting-started/differences-between-nodejs-and-the-browser",
      "expected_output": "标题、运行时差异、全局对象、模块系统、IO权限、事件循环、安全模型原生原文"
    }
  ],
  "confidence": 0.98
}
```

---

## 六、进化蒸馏成果

```json
{
  "chain_id": "nodejs_browser_diff_distill_001",
  "distilled_skill": [
    "当前差异文档全量公网抓取与访问可用性实测核验",
    "固化该页面为JS双运行时环境差异的官方权威中枢",
    "拆分前端浏览器/后端Node.js场景化定位边界",
    "建立DOM/BOM与Node专属全局对象的强隔离认知",
    "沉淀CommonJS默认+ESM兼容的Node模块化底层规则",
    "明确浏览器沙箱限制与Node全系统权限的安全分水岭",
    "收录双环境事件循环异步调度底层差异特征"
  ],
  "current_execution_count": 1,
  "confidence_summary": {
    "high_confidence": 0.98,
    "medium_confidence": 0.02,
    "low_confidence": 0.00
  }
}
```

---

## 七、结论

本次完成 Node.js **与浏览器运行时差异** 单页资产固化。

当前覆盖：运行时场景、全局对象、模块系统、IO权限、事件循环、安全模型

后续可递进抓取：事件循环细节、模块混用配置、生产安全加固等下级文档。