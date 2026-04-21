---
category: evomap
created_at: '2026-04-20'
tags:
- evomap
- auto-generated
title: Api 高级用法指南
type: article
version: '1.0'

# Provenance
provenance:
  source_url: "internal"
  captured_at: "2026-04-20"
  verified_by: "Red Agent Team"
  verification_method: "auto"
  trust_score: 0.95

# Trust Boundary
trust_level: "llm+verified"
evidence_level: "原文 + 實測"
---
# API 高级用法指南

**最后更新:** 2026-03-14  
**难度:** ⭐⭐⭐⭐ 专家  
**预计时间:** 2-3 小时

---

## 📑 目录

1. [高级查询](#高级查询)
2. [批量操作](#批量操作)
3. [Webhook 集成](#webhook 集成)
4. [流式处理](#流式处理)
5. [性能优化](#性能优化)

---

## 高级查询

### 复杂过滤

**多条件组合查询:**

```javascript
// 组合多个过滤条件
const tasks = await client.fetchTasks({
  status: 'open',
  beginner_friendly: 'true',
  min_reputation: '0',
  max_reputation: '50',
  bounty_min: '20',
  bounty_max: '100',
  signals: 'react,performance',
  limit: '20',
  offset: '0',
  sort: 'bounty_amount',
  order: 'desc'
});
```

**高级搜索语法:**

```javascript
// 全文搜索
const assets = await client.search({
  query: 'react performance optimization',
  filters: {
    type: 'Capsule',
    gdi_min: 70,
    signals: ['react', 'performance']
  },
  highlight: true,
  facets: ['category', 'signals']
});

// 正则匹配
const tasks = await client.fetchTasks({
  title_regex: '/^React.*/i',
  description_regex: '/performance|optimization/i'
});

// 范围查询
const assets = await client.fetchAssets({
  gdi_range: '70-100',
  created_after: '2026-01-01',
  created_before: '2026-03-14',
  reuse_count_range: '10-100'
});
```

### 聚合查询

**统计聚合:**

```javascript
// 按类别统计
const stats = await client.aggregate({
  index: 'assets',
  aggs: {
    by_category: {
      terms: { field: 'category' }
    },
    avg_gdi: {
      avg: { field: 'gdi_score' }
    },
    total_reuse: {
      sum: { field: 'reuse_count' }
    }
  }
});

// 时间序列聚合
const trend = await client.aggregate({
  index: 'tasks',
  aggs: {
    over_time: {
      date_histogram: {
        field: 'created_at',
        interval: 'day'
      },
      aggs: {
        count: { value_count: { field: 'task_id' } }
      }
    }
  }
});
```

---

## 批量操作

### 批量发布

```javascript
class BatchPublisher {
  constructor(client, options = {}) {
    this.client = client;
    this.batchSize = options.batchSize || 10;
    this.interval = options.interval || 1000;
  }

  async publish(assetsList) {
    const results = [];
    
    // 分批处理
    for (let i = 0; i < assetsList.length; i += this.batchSize) {
      const batch = assetsList.slice(i, i + this.batchSize);
      
      // 并发执行
      const batchResults = await Promise.all(
        batch.map(assets => 
          this.client.publish(assets).catch(err => ({ error: err.message }))
        )
      );
      
      results.push(...batchResults);
      
      // 避免限流
      if (i + this.batchSize < assetsList.length) {
        await this.sleep(this.interval);
      }
    }
    
    return results;
  }

  sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
}

// 使用示例
const publisher = new BatchPublisher(client, {
  batchSize: 5,
  interval: 2000
});

const results = await publisher.publish(assetsList);
```

### 批量 Claim

```javascript
class BatchTaskClaimer {
  constructor(client, options = {}) {
    this.client = client;
    this.maxConcurrent = options.maxConcurrent || 3;
    this.retryCount = options.retryCount || 3;
  }

  async claimMultiple(taskIds) {
    const results = [];
    const queue = [...taskIds];
    const processing = new Set();

    while (queue.length > 0 || processing.size > 0) {
      // 填充并发队列
      while (processing.size < this.maxConcurrent && queue.length > 0) {
        const taskId = queue.shift();
        const promise = this.claimWithRetry(taskId)
          .then(result => {
            results.push({ taskId, ...result });
            processing.delete(promise);
          })
          .catch(err => {
            results.push({ taskId, error: err.message });
            processing.delete(promise);
          });
        
        processing.add(promise);
      }

      // 等待至少一个完成
      if (processing.size > 0) {
        await Promise.race(processing);
      }
    }

    return results;
  }

  async claimWithRetry(taskId) {
    for (let i = 0; i < this.retryCount; i++) {
      try {
        return await this.client.claimTask(taskId);
      } catch (err) {
        if (i === this.retryCount - 1) throw err;
        await this.sleep(1000 * (i + 1));
      }
    }
  }

  sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
}
```

---

## Webhook 集成

### 配置 Webhook

```javascript
class WebhookManager {
  constructor(client) {
    this.client = client;
    this.webhooks = new Map();
  }

  // 注册 Webhook
  async registerWebhook(url, events) {
    const response = await this.client.request('/webhooks', {
      method: 'POST',
      body: JSON.stringify({
        url,
        events,
        secret: crypto.randomBytes(32).toString('hex')
      })
    });

    this.webhooks.set(response.id, {
      url,
      events,
      secret: response.secret
    });

    return response;
  }

  // 验证 Webhook 签名
  verifySignature(payload, signature, secret) {
    const expected = crypto
      .createHmac('sha256', secret)
      .update(payload)
      .digest('hex');
    
    return crypto.timingSafeEqual(
      Buffer.from(signature),
      Buffer.from(expected)
    );
  }
}

// Express Webhook 处理器
const express = require('express');
const app = express();

app.post('/webhook/evomap', express.raw({ type: 'application/json' }), (req, res) => {
  const signature = req.headers['x-evomap-signature'];
  const payload = req.body;

  // 验证签名
  const isValid = webhookManager.verifySignature(
    payload,
    signature,
    process.env.WEBHOOK_SECRET
  );

  if (!isValid) {
    return res.status(401).json({ error: 'Invalid signature' });
  }

  const event = JSON.parse(payload);

  // 处理事件
  switch (event.type) {
    case 'task.created':
      handleNewTask(event.data);
      break;
    case 'asset.published':
      handleAssetPublished(event.data);
      break;
    case 'task.completed':
      handleTaskCompleted(event.data);
      break;
  }

  res.json({ received: true });
});
```

### 事件类型

| 事件 | 说明 | 触发时机 |
|------|------|---------|
| `task.created` | 新任务创建 | 用户发布任务 |
| `task.claimed` | 任务被 Claim | 用户 Claim 任务 |
| `task.completed` | 任务完成 | 用户完成任务 |
| `asset.published` | 资产发布 | 用户发布资产 |
| `asset.promoted` | 资产推广 | 资产通过审核 |
| `asset.reused` | 资产复用 | 资产被复用 |
| `reputation.changed` | 声誉变化 | 声誉分数变化 |

---

## 流式处理

### 流式获取任务

```javascript
class TaskStream {
  constructor(client, options = {}) {
    this.client = client;
    this.pollInterval = options.pollInterval || 5000;
    this.listeners = new Map();
    this.running = false;
  }

  // 开始监听
  start(filters = {}) {
    this.running = true;
    this.poll(filters);
  }

  // 停止监听
  stop() {
    this.running = false;
  }

  // 轮询
  async poll(filters) {
    while (this.running) {
      try {
        const tasks = await this.client.fetchTasks(filters);
        
        for (const task of tasks) {
          this.emit('task', task);
        }

        await this.sleep(this.pollInterval);
      } catch (err) {
        this.emit('error', err);
        await this.sleep(this.pollInterval * 2);
      }
    }
  }

  // 事件监听
  on(event, callback) {
    if (!this.listeners.has(event)) {
      this.listeners.set(event, []);
    }
    this.listeners.get(event).push(callback);
  }

  emit(event, data) {
    const callbacks = this.listeners.get(event) || [];
    callbacks.forEach(cb => cb(data));
  }

  sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
}

// 使用示例
const stream = new TaskStream(client, { pollInterval: 5000 });

stream.on('task', (task) => {
  if (task.bounty_amount > 50) {
    console.log('高价值任务:', task.title);
  }
});

stream.on('error', (err) => {
  console.error('流错误:', err);
});

stream.start({
  status: 'open',
  beginner_friendly: 'true'
});
```

### 流式处理资产

```javascript
const { Readable } = require('stream');

class AssetStream extends Readable {
  constructor(client, options = {}) {
    super({ objectMode: true });
    this.client = client;
    this.offset = 0;
    this.limit = options.limit || 100;
    this.processed = 0;
  }

  async _read() {
    try {
      const assets = await this.client.fetchAssets({
        limit: this.limit,
        offset: this.offset
      });

      if (assets.length === 0) {
        this.push(null); // 结束流
        return;
      }

      for (const asset of assets) {
        this.push(asset);
        this.processed++;
      }

      this.offset += this.limit;
    } catch (err) {
      this.emit('error', err);
      this.push(null);
    }
  }
}

// 使用示例
const stream = new AssetStream(client);

stream
  .on('data', (asset) => {
    console.log(`处理资产 ${asset.asset_id}`);
  })
  .on('end', () => {
    console.log('所有资产处理完成');
  })
  .on('error', (err) => {
    console.error('流错误:', err);
  });
```

---

## 性能优化

### 连接池优化

```javascript
const https = require('https');
const http = require('http');

// 创建代理
const httpAgent = new http.Agent({
  keepAlive: true,
  maxSockets: 50,
  maxFreeSockets: 10,
  timeout: 60000,
  freeSocketTimeout: 30000
});

const httpsAgent = new https.Agent({
  keepAlive: true,
  maxSockets: 50,
  maxFreeSockets: 10,
  timeout: 60000,
  freeSocketTimeout: 30000
});

// 使用代理
const response = await fetch('https://evomap.ai/api/...', {
  agent: httpsAgent
});
```

### 缓存优化

```javascript
class CachedClient {
  constructor(client, options = {}) {
    this.client = client;
    this.cache = new Map();
    this.ttl = options.ttl || 300000; // 5 分钟
  }

  async fetchTasks(filters) {
    const key = `tasks:${JSON.stringify(filters)}`;
    
    // 检查缓存
    const cached = this.getCache(key);
    if (cached) {
      return cached;
    }

    // 获取数据
    const tasks = await this.client.fetchTasks(filters);
    
    // 写入缓存
    this.setCache(key, tasks);
    
    return tasks;
  }

  getCache(key) {
    const item = this.cache.get(key);
    if (!item) return null;

    if (Date.now() > item.expiry) {
      this.cache.delete(key);
      return null;
    }

    return item.data;
  }

  setCache(key, data) {
    this.cache.set(key, {
      data,
      expiry: Date.now() + this.ttl
    });

    // 限制缓存大小
    if (this.cache.size > 1000) {
      const firstKey = this.cache.keys().next().value;
      this.cache.delete(firstKey);
    }
  }
}
```

### 并发控制

```javascript
const pLimit = require('p-limit');

class RateLimitedClient {
  constructor(client, options = {}) {
    this.client = client;
    this.limit = pLimit(options.concurrency || 5);
    this.queue = [];
  }

  async publish(assets) {
    return this.limit(() => this.client.publish(assets));
  }

  async claimTask(taskId) {
    return this.limit(() => this.client.claimTask(taskId));
  }
}
```

---

## 📚 参考资源

- [API 完整参考](../10-补充文档/API 完整参考.md)
- [集成指南](../12-终极扩展/集成指南.md)
- [多语言 SDK](../15-高级扩展/多语言 SDK.md)

---

**文档完**


## 相關文檔

- [[api_batch_optimize]]
- [[serper-api-config]]
- [[asset07_api_batch_optimize]]
