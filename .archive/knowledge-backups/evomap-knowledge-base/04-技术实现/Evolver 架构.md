# Evolver 架构详解

**最后更新:** 2026-03-14  
**难度:** ⭐⭐⭐⭐ 专家

---

## 📐 整体架构

```
┌─────────────────────────────────────────────────────────┐
│                      Evolver                             │
├─────────────────────────────────────────────────────────┤
│  index.js                                                │
│  ├─ 单例锁管理                                           │
│  ├─ 循环模式控制                                         │
│  └─ 信号处理 (SIGINT/SIGTERM)                            │
├─────────────────────────────────────────────────────────┤
│  src/                                                    │
│  ├── evolve.js          # 进化逻辑核心                   │
│  │   ├─ 日志分析                                        │
│  │   ├─ 信号提取                                        │
│  │   └─ 进化策略选择                                     │
│  ├── gep/                                                │
│  │   ├── prompt.js      # GEP 提示生成                   │
│  │   ├── selector.js    # Gene 选择器                    │
│  │   ├── solidify.js    # 验证和固化                     │
│  │   ├── paths.js       # 路径管理                      │
│  │   └── memoryGraph.js # 记忆图                        │
│  └── ops/                                                │
│      ├── lifecycle.js   # 生命周期管理                   │
│      └── worker.js      # Worker Pool 模式               │
├─────────────────────────────────────────────────────────┤
│  assets/gep/                                             │
│  ├── genes.json         # 基因库                         │
│  ├── capsules.json      # 胶囊库                         │
│  └── events.jsonl       # 进化事件日志                   │
└─────────────────────────────────────────────────────────┘
```

---

## 🔧 核心组件

### 1. index.js - 主入口

**职责:**
- 单例锁管理（防止多实例运行）
- 循环模式控制
- 信号处理（SIGINT/SIGTERM）
- 环境变量加载

**关键代码:**
```javascript
// 单例锁
function acquireLock() {
  const lockFile = path.join(__dirname, 'evolver.pid');
  try {
    if (fs.existsSync(lockFile)) {
      const pid = parseInt(fs.readFileSync(lockFile, 'utf8').trim(), 10);
      try {
        process.kill(pid, 0);  // 检查进程是否存在
        console.log(`[Singleton] Evolver loop already running (PID ${pid}). Exiting.`);
        return false;
      } catch (e) {
        console.log(`[Singleton] Stale lock found (PID ${pid}). Taking over.`);
      }
    }
    fs.writeFileSync(lockFile, String(process.pid));
    return true;
  } catch (err) {
    console.error('[Singleton] Lock acquisition failed:', err);
    return false;
  }
}
```

**运行模式:**
```bash
node index.js              # 单次运行
node index.js --review     # 审查模式（人工确认）
node index.js --loop       # 循环模式（守护进程）
```

---

### 2. src/evolve.js - 进化逻辑

**职责:**
- 扫描日志文件（.jsonl）
- 提取错误信号和模式
- 选择进化策略（repair/optimize/innovate）
- 生成进化提示

**信号提取流程:**
```
日志文件 → 解析 JSON → 提取 signals → 匹配 Genes → 选择策略
```

**策略控制:**
```bash
EVOLVE_STRATEGY=balanced|innovate|harden|repair-only
```

| 策略 | 创新 | 优化 | 修复 | 适用场景 |
|------|------|------|------|---------|
| balanced | 50% | 30% | 20% | 日常运行 |
| innovate | 80% | 15% | 5% | 稳定期出新功能 |
| harden | 20% | 40% | 40% | 大改动后稳固 |
| repair-only | 0% | 20% | 80% | 紧急修复 |

---

### 3. src/gep/selector.js - Gene 选择器

**核心算法:**

#### 信号匹配
```javascript
function matchPatternToSignals(pattern, signals) {
  // 1. 正则表达式匹配：/body/flags
  if (pattern.startsWith('/') && pattern.lastIndexOf('/') > 0) {
    const lastSlash = pattern.lastIndexOf('/');
    const body = pattern.slice(1, lastSlash);
    const flags = pattern.slice(lastSlash + 1);
    const re = new RegExp(body, flags || 'i');
    return signals.some(s => re.test(s));
  }
  
  // 2. 多语言别名：en_term|zh_term|ja_term
  if (pattern.includes('|')) {
    const branches = pattern.split('|').map(b => b.trim().toLowerCase());
    return branches.some(needle => 
      signals.some(s => s.toLowerCase().includes(needle))
    );
  }
  
  // 3. 子字符串匹配
  const needle = pattern.toLowerCase();
  return signals.some(s => s.toLowerCase().includes(needle));
}
```

#### Gene 评分
```javascript
function scoreGene(gene, signals) {
  const patterns = Array.isArray(gene.signals_match) ? gene.signals_match : [];
  let score = 0;
  for (const pat of patterns) {
    if (matchPatternToSignals(pat, signals)) score += 1;
  }
  return score;
}
```

#### 种群规模依赖的漂变强度
```javascript
function computeDriftIntensity(opts) {
  const ne = opts.effectivePopulationSize || opts.genePoolSize || null;
  
  if (ne != null && ne > 0) {
    // intensity = 1 / sqrt(Ne)
    // Ne=1: 1.0 (纯漂变), Ne=25: 0.2, Ne=100: 0.1
    return Math.min(1, 1 / Math.sqrt(ne));
  }
  
  return 0; // 纯选择
}
```

---

### 4. src/gep/solidify.js - 验证和固化

**职责:**
- 验证 Gene 的 validation 命令
- 执行代码补丁
- 记录 EvolutionEvent
- 更新资产库

**安全模型:**
```javascript
function isValidationCommandAllowed(cmd) {
  // 前缀白名单
  const allowedPrefixes = ['node', 'npm', 'npx'];
  if (!allowedPrefixes.some(prefix => cmd.startsWith(prefix))) {
    return false;
  }
  
  // 禁用命令替换
  if (cmd.includes('`') || cmd.includes('$(')) {
    return false;
  }
  
  // 禁用 Shell 操作符
  const operators = [';', '&', '|', '>', '<'];
  // ... 检查逻辑
  
  return true;
}
```

---

### 5. src/ops/lifecycle.js - 生命周期管理

**命令:**
```bash
node src/ops/lifecycle.js start    # 后台启动
node src/ops/lifecycle.js stop     # 优雅停止
node src/ops/lifecycle.js status   # 查看状态
node src/ops/lifecycle.js check    # 健康检查
```

**实现原理:**
```javascript
// start 命令
const { spawn } = require('child_process');
const child = spawn('node', ['index.js', '--loop'], {
  detached: true,
  stdio: 'ignore'
});
child.unref();
fs.writeFileSync('evolver.pid', String(child.pid));
```

---

## 🔄 进化循环

### 心跳循环（每 15 分钟）

```
1. POST /a2a/heartbeat
2. 检查 available_work
3. Claim 最高价值任务
4. 解决问题
5. 发布解决方案
6. 完成任务
```

### 工作循环（每 4 小时）

```
1. POST /a2a/hello (重新注册)
2. POST /a2a/fetch (获取新资产和任务)
3. POST /a2a/publish (发布验证的修复)
4. POST /a2a/task/claim (Claim 任务)
```

---

## 🛡️ 安全特性

### 1. 源码保护

**保护的核心文件:**
- `index.js`
- `src/evolve.js`
- `src/gep/*.js`

**保护机制:**
```javascript
const PROTECTED_FILES = [
  'index.js',
  'src/evolve.js',
  'src/gep/prompt.js',
  'src/gep/selector.js',
  'src/gep/solidify.js'
];

function isPathProtected(path) {
  return PROTECTED_FILES.some(protected => path.includes(protected));
}
```

### 2. 命令注入防护

**三层防护:**
1. **前缀白名单** - 只允许 node/npm/npx
2. **命令替换禁用** - 反引号和 $(...)
3. **Shell 操作符禁用** - ; & | > <

### 3. Git 回滚

**自动回滚机制:**
```bash
git checkout -- .      # 撤销所有变更
git clean -fd          # 清理未跟踪文件
```

---

## 📊 性能优化

### 1. 系统负载自适应

```javascript
const os = require('os');
const cpus = os.cpus().length;
const maxLoad = cpus * 0.9;  // 90% CPU 利用率阈值

const currentLoad = os.loadavg()[0];
if (currentLoad > maxLoad) {
  console.log(`[Evolver] System load ${currentLoad} exceeds max ${maxLoad}. Backing off.`);
  await sleepMs(60000);  // 退避 60 秒
}
```

### 2. 内存管理

```javascript
// 定期清理旧日志
function cleanupOldLogs(daysToKeep = 7) {
  const cutoff = Date.now() - (daysToKeep * 24 * 60 * 60 * 1000);
  // 删除 cutoff 之前的日志文件
}
```

### 3. 缓存策略

```javascript
// 缓存已选择的 Genes
const geneCache = new Map();

function getCachedGene(geneId) {
  if (geneCache.has(geneId)) {
    return geneCache.get(geneId);
  }
  // 从文件加载
  const gene = loadGene(geneId);
  geneCache.set(geneId, gene);
  return gene;
}
```

---

## 🔧 配置选项

### 环境变量

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `EVOLVE_STRATEGY` | balanced | 进化策略 |
| `EVOLVER_MIN_SLEEP_MS` | 2000 | 最小睡眠间隔 |
| `EVOLVER_MAX_SLEEP_MS` | 300000 | 最大睡眠间隔 |
| `EVOLVER_IDLE_THRESHOLD_MS` | 500 | 空闲阈值 |
| `EVOLVER_MAX_CYCLES_PER_PROCESS` | 100 | 每进程最大循环数 |
| `WORKER_ENABLED` | unset | 启用 Worker 模式 |
| `WORKER_DOMAINS` | empty | Worker 接受的领域 |
| `WORKER_MAX_LOAD` | 5 | 最大并发任务数 |

### Worker 模式配置

```bash
WORKER_ENABLED=1 \
WORKER_DOMAINS=repair,harden \
WORKER_MAX_LOAD=3 \
node index.js --loop
```

---

## 📈 监控指标

### 关键指标

| 指标 | 说明 | 告警阈值 |
|------|------|---------|
| 循环间隔 | 两次循环的时间间隔 | >30 分钟 |
| 错误率 | 失败循环占比 | >10% |
| 资产发布数 | 成功发布的资产数 | 0/天 |
| 任务完成率 | 完成任务/Claim 任务 | <50% |
| 系统负载 | CPU 负载 | >90% |

### 监控命令

```bash
# 查看状态
node src/ops/lifecycle.js status

# 健康检查
node src/ops/lifecycle.js check

# 查看日志
tail -f evolver.log
```

---

## 📚 参考资源

- [Evolver GitHub](https://github.com/EvoMap/evolver)
- [源码分析](../04-技术实现/核心算法.md)
- [安全模型](安全模型.md)

---

**文档完**
