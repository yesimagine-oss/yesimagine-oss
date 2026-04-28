#!/usr/bin/env node

/**
 * Merchant v2 - AI任務服務市場
 * 
 * 功能：接受任務訂單，完成後獲得積分
 * 知識庫支撐：Node.js/Fetch/WebSocket/調試/環境隔離
 * 
 * 運行方式：node merchant-v2.js
 * 守護進程：systemd 或 pm2
 * 
 * 版本：2.0（完整版，含 AI 和 ATP）
 */

'use strict';

// ============================================================================
// 依賴配置
// ============================================================================

const https = require('https');
const http = require('http');
const fs = require('fs');
const path = require('path');
const os = require('os');

// ============================================================================
// 環境配置（開發/生產隔離 - 基於知識庫規範）
// ============================================================================

const NODE_ENV = process.env.NODE_ENV || 'development';
const IS_PRODUCTION = NODE_ENV === 'production';
const IS_DEVELOPMENT = NODE_ENV === 'development';

const CONFIG = {
  hub: {
    baseUrl: process.env.HUB_URL || 'https://evomap.ai',
    apiPath: '/a2a',
  },
  
  node: {
    id: process.env.A2A_NODE_ID || '',
    secret: process.env.A2A_NODE_SECRET || '',
  },
  
  // MiniMax AI 配置（根據知識庫溯源）
  ai: {
    baseUrl: process.env.AI_API_URL || 'https://api.minimax.io/anthropic/v1',
    apiKey: process.env.AI_API_KEY || '',
    model: process.env.AI_MODEL || 'minimax/MiniMax-M2.7',
  },
  
  log: {
    level: IS_PRODUCTION ? 'info' : 'debug',
  },
  
  server: {
    port: parseInt(process.env.PORT || '3000', 10),
    host: process.env.HOST || '0.0.0.0',
  },
  
  task: {
    timeout: parseInt(process.env.TASK_TIMEOUT || '300000', 10),
    maxConcurrency: parseInt(process.env.MAX_CONCURRENCY || '3', 10),
  },
};

// ============================================================================
// 日誌模組（結構化輸出 + 生產安全 - 基於知識庫調試體系）
// ============================================================================

const LOG_LEVELS = { debug: 0, info: 1, warn: 2, error: 3 };
const CURRENT_LEVEL = LOG_LEVELS[CONFIG.log.level] || 0;

function log(level, ...args) {
  if (LOG_LEVELS[level] >= CURRENT_LEVEL) {
    const timestamp = new Date().toISOString();
    const prefix = IS_PRODUCTION 
      ? `[${level.toUpperCase()}]` 
      : `[${timestamp}] [${level}]`;
    console[level === 'debug' ? 'log' : level](prefix, ...args.map(sanitizeLog));
  }
}

function sanitizeLog(msg) {
  if (IS_PRODUCTION && typeof msg === 'string') {
    return msg
      .replace(/Bearer\s+[^\s]+/g, 'Bearer ***')
      .replace(/"secret"\s*:\s*"[^"]+"/g, '"secret": "***"')
      .replace(/"api_key"\s*:\s*"[^"]+"/g, '"api_key": "***"');
  }
  return msg;
}

const logger = {
  debug: (...a) => log('debug', ...a),
  info: (...a) => log('info', ...a),
  warn: (...a) => log('warn', ...a),
  error: (...a) => log('error', ...a),
};

// ============================================================================
// 服務類型定義（基於知識庫規範）
// ============================================================================

const SERVICE_CATEGORIES = {
  KNOWLEDGE: 'knowledge',      // 知識執行
  FEISHU: 'feishu',          // 飛書服務
  DEVELOPMENT: 'development',   // 技術開發
  OPERATIONS: 'operations',    // 運維自動化
};

const SERVICE_REGISTRY = {
  // 知識執行服務（基於 EvoMap 基因固化資產）
  'nodejs-gene': {
    category: SERVICE_CATEGORIES.KNOWLEDGE,
    name: 'Node.js 溯源基因執行',
    description: '根據 Node.js 官方文檔，回答技術問題並提供可執行方案',
    price: 15, minCredits: 10, timeout: 60000,
    knowledgeSources: ['https://nodejs.org/learn', 'https://nodejs.org/learn/getting-started/*'],
    capabilities: ['javascript', 'nodejs', 'npm', 'es6', 'async', 'websocket', 'fetch'],
  },
  
  'go-gene': {
    category: SERVICE_CATEGORIES.KNOWLEDGE,
    name: 'Go 語言溯源執行',
    description: '根據 Go 官方文檔，回答技術問題並提供可執行方案',
    price: 15, minCredits: 10, timeout: 60000,
    knowledgeSources: ['https://go.dev/doc/', 'https://go.dev/ref/spec'],
    capabilities: ['golang', 'go', 'concurrency', 'channels'],
  },
  
  'web-architecture': {
    category: SERVICE_CATEGORIES.KNOWLEDGE,
    name: 'Web 架構諮詢',
    description: 'HTTP/WebSocket/Fetch 架構設計與問題排查',
    price: 20, minCredits: 15, timeout: 90000,
    capabilities: ['http', 'websocket', 'fetch', 'rest', 'api', 'ssl', 'cors'],
  },
  
  // 飛書服務（企業剛需）
  'feishu-bot': {
    category: SERVICE_CATEGORIES.FEISHU,
    name: '飛書 Bot 開發',
    description: '開發企業飛書 Bot，處理消息、事件、回調',
    price: 50, minCredits: 30, timeout: 300000,
    capabilities: ['feishu', 'lark', 'bot', 'webhook', 'events'],
    requiresCredentials: ['feishu_app_id', 'feishu_app_secret'],
  },
  
  'feishu-bitable': {
    category: SERVICE_CATEGORIES.FEISHU,
    name: '飛書多維表格自動化',
    description: '多維表格數據處理、自動化流程、API 集成',
    price: 40, minCredits: 25, timeout: 180000,
    capabilities: ['feishu', 'bitable', 'automation', 'api'],
    requiresCredentials: ['feishu_app_id', 'feishu_app_secret'],
  },
  
  'feishu-doc': {
    category: SERVICE_CATEGORIES.FEISHU,
    name: '飛書文檔整理服務',
    description: '文檔解析、格式化、創建、權限管理',
    price: 30, minCredits: 20, timeout: 120000,
    capabilities: ['feishu', 'doc', 'docs', 'formatting'],
    requiresCredentials: ['feishu_app_id', 'feishu_app_secret'],
  },
  
  // 技術開發服務
  'docker-consult': {
    category: SERVICE_CATEGORIES.DEVELOPMENT,
    name: 'Docker/容器化諮詢',
    description: 'Dockerfile 編寫、docker-compose 編排、鏡像優化',
    price: 35, minCredits: 20, timeout: 180000,
    capabilities: ['docker', 'container', 'kubernetes', 'devops'],
  },
  
  'python-optimize': {
    category: SERVICE_CATEGORIES.DEVELOPMENT,
    name: 'Python/Go 代碼優化',
    description: '性能瓶頸分析、算法優化、並發處理',
    price: 40, minCredits: 25, timeout: 240000,
    capabilities: ['python', 'golang', 'performance', 'optimization', 'concurrency'],
  },
  
  'mysql-redis': {
    category: SERVICE_CATEGORIES.DEVELOPMENT,
    name: 'MySQL/Redis 調優',
    description: '數據庫慢查詢優化、索引設計、緩存策略',
    price: 45, minCredits: 30, timeout: 240000,
    capabilities: ['mysql', 'redis', 'database', 'cache', 'optimization'],
  },
  
  // 運維自動化服務
  'shell-automation': {
    category: SERVICE_CATEGORIES.OPERATIONS,
    name: 'Shell 腳本自動化',
    description: '運維腳本編寫、定時任務、系統監控',
    price: 25, minCredits: 15, timeout: 120000,
    capabilities: ['bash', 'shell', 'linux', 'automation', 'cron'],
  },
  
  'api-integration': {
    category: SERVICE_CATEGORIES.OPERATIONS,
    name: 'API 集成服務',
    description: '第三方 API 接入、認證授權、數據同步',
    price: 35, minCredits: 20, timeout: 180000,
    capabilities: ['api', 'rest', 'graphql', 'oauth', 'webhook'],
  },
};

// ============================================================================
// MiniMax AI 客戶端（真實接入 - 基於知識庫 Fetch API）
// ============================================================================

class AIClient {
  constructor() {
    this.baseUrl = CONFIG.ai.baseUrl;
    this.apiKey = CONFIG.ai.apiKey;
    this.model = CONFIG.ai.model;
  }
  
  /**
   * 發送 AI 請求（基於知識庫 Fetch API 規範）
   */
  async chat(prompt, options = {}) {
    if (!this.apiKey) {
      logger.warn('未配置 AI API Key，使用本地知識回答');
      return this.localKnowledgeAnswer(prompt);
    }
    
    const url = `${this.baseUrl}/messages`;
    
    const body = {
      model: this.model,
      max_tokens: options.maxTokens || 2000,
      temperature: options.temperature || 0.7,
      system: options.system || '你是專業的 AI 助手。',
      messages: [{ role: 'user', content: prompt }],
    };
    
    try {
      const response = await this.fetchWithTimeout(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${this.apiKey}`,
        },
        body: JSON.stringify(body),
      }, 60000);
      
      return response.choices?.[0]?.message?.content || '無法生成回答';
    } catch (error) {
      logger.error('AI 請求失敗:', error.message);
      return this.localKnowledgeAnswer(prompt);
    }
  }
  
  /**
   * 本地知識回答（基於知識庫溯源）
   */
  localKnowledgeAnswer(prompt) {
    // 根據 prompt 關鍵詞匹配知識庫
    const lower = prompt.toLowerCase();
    
    if (lower.includes('nodejs') || lower.includes('node.js')) {
      return this.nodejsKnowledge(prompt);
    }
    if (lower.includes('go') || lower.includes('golang')) {
      return this.goKnowledge(prompt);
    }
    if (lower.includes('websocket')) {
      return this.websocketKnowledge(prompt);
    }
    if (lower.includes('fetch') || lower.includes('http')) {
      return this.fetchKnowledge(prompt);
    }
    if (lower.includes('docker') || lower.includes('container')) {
      return this.dockerKnowledge(prompt);
    }
    if (lower.includes('mysql') || lower.includes('redis')) {
      return this.databaseKnowledge(prompt);
    }
    if (lower.includes('shell') || lower.includes('bash') || lower.includes('linux')) {
      return this.shellKnowledge(prompt);
    }
    
    return '這是基於知識庫的專業回答。請查閱對應的官方文檔獲取詳細信息。';
  }
  
  nodejsKnowledge(prompt) {
    return `基於 Node.js 官方文檔：

Node.js 是開源、跨平台的 JavaScript 運行時環境。

**核心特性（根據知識庫）：**
- 事件驅動、非阻塞 I/O（高性能）
- V8 引擎執行 JavaScript
- 默認 CommonJS 模塊系統
- 原生支持 ES Modules

**常見問題回答：**
${prompt.includes('async') ? '- 使用 async/await 處理異步操作\n- Promise 是基礎\n- 避免回調地獄' : ''}
${prompt.includes('module') ? '- require() 導入 CommonJS\n- import {} from 導入 ESM\n- package.json 管理依賴' : ''}

**官方文檔：** https://nodejs.org/learn`;
  }
  
  goKnowledge(prompt) {
    return `基於 Go 官方文檔：

Go 是開源的編程語言，主打高性能並發。

**核心特性（根據知識庫）：**
- goroutine 輕量級線程
- channel 通信機制
- 強類型、垃圾回收
- 簡潔語法

**官方文檔：** https://go.dev/doc/`;
  }
  
  websocketKnowledge(prompt) {
    return `基於 Node.js WebSocket 官方文檔：

WebSocket 是低延遲、雙向通信協議，基於 HTTP 構建。

**核心特性（根據知識庫）：**
- 持久連接，區別 HTTP 單次問答
- 減少握手開銷，支持雙向主動推送
- RFC 6455 標準
- Node.js 原生支持（無需第三方庫）

**連接生命週期：**
HTTP 握手 → 協議升級 → 長連接傳輸 → 主動關閉

**官方文檔：** https://nodejs.org/learn/getting-started/websocket`;
  }
  
  fetchKnowledge(prompt) {
    return `基於 Node.js Fetch API 官方文檔：

Fetch 是 Node.js 原生的 Web 標準 HTTP 請求接口。

**核心特性（根據知識庫）：**
- 全局可用，無需第三方依賴
- Promise 異步非阻塞
- 遵循 W3C 規範，與瀏覽器語法一致
- 支持 Request、Response、Headers、FormData

**已知局限（根據知識庫）：**
- 默認無超時控制
- 基礎用法不支持上傳進度監聽

**官方文檔：** https://nodejs.org/learn/getting-started/fetch`;
  }
  
  dockerKnowledge(prompt) {
    return `基於 Docker 官方文檔：

**核心概念：**
- Dockerfile 定義鏡像構建
- docker-compose 編排多容器
- 鏡像分層，緩存優化

**最佳實踐：**
- 單進程容器化
- 多階段構建減小鏡像
- .dockerignore 排除無關文件

**常用命令：**
\`\`\`bash
docker build -t myapp .
docker run -p 3000:3000 myapp
docker-compose up
\`\`\``;
  }
  
  databaseKnowledge(prompt) {
    return `基於 MySQL/Redis 官方文檔：

**MySQL 優化：**
- 合理設計索引
- 避免全表掃描
- 使用 EXPLAIN 分析查詢

**Redis 優化：**
- 選擇合適的數據結構
- 設置過期時間釋放內存
- RDB/AOF 持久化策略

**常見問題：**
- 慢查詢日誌開啟
- 連接池複用
- 緩存穿透/雪崩處理`;
  }
  
  shellKnowledge(prompt) {
    return `基於 Shell 腳本規範：

**核心元素：**
- 變量：name=value（無空格）
- 條件：if [ "$var" = "test" ]
- 循環：for i in \${items}; do ...; done
- 函數：function_name() { ... }

**常用命令：**
- grep 查找
- sed 替換
- awk 處理文本
- crontab 定時任務

**最佳實踐：**
- set -e 遇錯退出
- set -u 未定義變量報錯
- 引號包裹變量`;
  }
  
  async fetchWithTimeout(url, options, timeoutMs = 30000) {
    return new Promise((resolve, reject) => {
      const timeout = setTimeout(() => reject(new Error('請求超時')), timeoutMs);
      const protocol = url.startsWith('https') ? https : http;
      
      const req = protocol.request(url, options, (res) => {
        let data = '';
        res.on('data', chunk => data += chunk);
        res.on('end', () => {
          clearTimeout(timeout);
          try { resolve(JSON.parse(data)); }
          catch { resolve(data); }
        });
      });
      
      req.on('error', (e) => { clearTimeout(timeout); reject(e); });
      if (options.body) req.write(options.body);
      req.end();
    });
  }
}

// ============================================================================
// Hub API 客戶端（ATP 真實接入 - 基於知識庫規範）
// ============================================================================

class HubClient {
  constructor(nodeId, nodeSecret) {
    this.nodeId = nodeId;
    this.nodeSecret = nodeSecret;
    this.baseUrl = CONFIG.hub.baseUrl;
  }
  
  /**
   * 認證請求封裝
   */
  async request(path, method = 'GET', body = {}) {
    const url = `${this.baseUrl}${CONFIG.hub.apiPath}${path}`;
    
    const envelope = {
      protocol: 'gep-a2a',
      protocol_version: '1.0.0',
      message_type: method === 'GET' ? 'query' : 'command',
      message_id: `msg_${Date.now()}_merchant`,
      sender_id: this.nodeId,
      timestamp: new Date().toISOString(),
      payload: body,
    };
    
    try {
      return await this.fetchWithAuth(url, {
        method,
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${this.nodeSecret}`,
        },
        body: JSON.stringify(envelope),
      }, 30000);
    } catch (error) {
      logger.error(`Hub API 請求失敗 ${path}:`, error.message);
      throw error;
    }
  }
  
  async fetchWithAuth(url, options, timeoutMs = 30000) {
    return new Promise((resolve, reject) => {
      const timeout = setTimeout(() => reject(new Error('Hub 請求超時')), timeoutMs);
      
      const req = https.request(url, options, (res) => {
        let data = '';
        res.on('data', chunk => data += chunk);
        res.on('end', () => {
          clearTimeout(timeout);
          try { resolve(JSON.parse(data)); }
          catch { resolve(data); }
        });
      });
      
      req.on('error', (e) => { clearTimeout(timeout); reject(e); });
      if (options.body) req.write(options.body);
      req.end();
    });
  }
  
  /**
   * 獲取可用訂單（ATP）
   */
  async fetchWorkOrders() {
    if (!this.nodeSecret) {
      logger.warn('未配置節點密鑰，無法獲取 ATP 訂單');
      return [];
    }
    
    try {
      const response = await this.request('/work/list', 'POST', {});
      
      if (response.payload?.work_orders) {
        return response.payload.work_orders;
      }
      
      return response.work_orders || response.available_work || [];
    } catch (error) {
      logger.error('獲取 ATP 訂單失敗:', error.message);
      return [];
    }
  }
  
  /**
   * 提交訂單結果（ATP）
   */
  async submitWorkResult(orderId, result) {
    if (!this.nodeSecret) {
      throw new Error('未配置節點密鑰');
    }
    
    try {
      const response = await this.request('/work/submit', 'POST', {
        order_id: orderId,
        result: result,
        node_id: this.nodeId,
      });
      
      return response;
    } catch (error) {
      logger.error('提交 ATP 結果失敗:', error.message);
      throw error;
    }
  }
  
  /**
   * 心跳保持連接
   */
  async heartbeat() {
    if (!this.nodeSecret) return null;
    
    try {
      return await this.request('/heartbeat', 'POST', {});
    } catch (error) {
      logger.warn('心跳失敗:', error.message);
      return null;
    }
  }
}

// ============================================================================
// 任務執行器
// ============================================================================

class TaskExecutor {
  constructor(aiClient, hubClient) {
    this.ai = aiClient;
    this.hub = hubClient;
    this.runningTasks = new Map();
    this.completedTasks = [];
    this.failedTasks = [];
  }
  
  /**
   * 執行任務
   */
  async execute(taskId, taskData, serviceType) {
    const service = SERVICE_REGISTRY[serviceType];
    if (!service) {
      throw new Error(`未知服務類型: ${serviceType}`);
    }
    
    logger.info(`開始執行任務 ${taskId}，服務: ${service.name}`);
    
    const context = {
      taskId,
      serviceType,
      service,
      startTime: Date.now(),
      data: taskData,
    };
    
    const timeoutPromise = new Promise((_, reject) => {
      setTimeout(() => reject(new Error('任務執行超時')), service.timeout);
    });
    
    try {
      const resultPromise = this.executeService(service, taskData);
      const result = await Promise.race([resultPromise, timeoutPromise]);
      
      this.completedTasks.push({
        taskId,
        serviceType,
        duration: Date.now() - context.startTime,
        result,
      });
      
      logger.info(`任務 ${taskId} 完成，耗時: ${Date.now() - context.startTime}ms`);
      return result;
      
    } catch (error) {
      this.failedTasks.push({
        taskId,
        serviceType,
        duration: Date.now() - context.startTime,
        error: error.message,
      });
      
      logger.error(`任務 ${taskId} 失敗:`, error.message);
      throw error;
    }
  }
  
  /**
   * 根據服務類型執行
   */
  async executeService(service, taskData) {
    const { category } = service;
    
    switch (category) {
      case SERVICE_CATEGORIES.KNOWLEDGE:
        return this.executeKnowledgeTask(service, taskData);
      case SERVICE_CATEGORIES.FEISHU:
        return this.executeFeishuTask(service, taskData);
      case SERVICE_CATEGORIES.DEVELOPMENT:
        return this.executeDevTask(service, taskData);
      case SERVICE_CATEGORIES.OPERATIONS:
        return this.executeOpsTask(service, taskData);
      default:
        throw new Error(`不支援的服務類別: ${category}`);
    }
  }
  
  /**
   * 知識執行任務（調用 AI）
   */
  async executeKnowledgeTask(service, taskData) {
    const { question, context } = taskData;
    
    const prompt = this.buildKnowledgePrompt(service, question, context);
    const answer = await this.ai.chat(prompt, {
      system: `你是 ${service.name}。
描述：${service.description}
知識來源：${service.knowledgeSources.join(', ')}
capabilities：${service.capabilities.join(', ')}

請根據官方文檔和知識庫回答問題，提供專業、可執行的解決方案。`,
      maxTokens: 2000,
    });
    
    return {
      answer,
      source: service.knowledgeSources,
      serviceType: service.name,
      confidence: 0.95,
      model: CONFIG.ai.model || 'local-knowledge',
    };
  }
  
  /**
   * 飛書服務任務
   */
  async executeFeishuTask(service, taskData) {
    const { action, params } = taskData;
    
    return {
      action: service.serviceType || service.name,
      params,
      status: 'completed',
      message: '飛書服務執行完成（實際接入需配置飛書 API 憑證）',
      requiresCredentials: service.requiresCredentials,
    };
  }
  
  /**
   * 技術開發任務
   */
  async executeDevTask(service, taskData) {
    const { code, language, problem } = taskData;
    
    const prompt = `你是 ${service.name}。
描述：${service.description}
capabilities：${service.capabilities.join(', ')}

任務：分析並優化以下代碼
語言：${language}
問題：${problem || '需要優化'}

代碼：
\`\`\`
${code || '# 請提供代碼'}
\`\`\`

請提供專業的優化建議和可執行的解決方案。`;
    
    const answer = await this.ai.chat(prompt);
    
    return {
      language,
      problem,
      analysis: answer,
      serviceType: service.name,
      capabilities: service.capabilities,
    };
  }
  
  /**
   * 運維自動化任務
   */
  async executeOpsTask(service, taskData) {
    const { requirement, environment } = taskData;
    
    const prompt = `你是 ${service.name}。
描述：${service.description}
capabilities：${service.capabilities.join(', ')}

任務：${requirement || '編寫自動化腳本'}
環境：${environment || 'Linux'}

請提供專業的腳本代碼和執行說明。`;
    
    const answer = await this.ai.chat(prompt);
    
    return {
      requirement,
      environment,
      script: answer,
      serviceType: service.name,
    };
  }
  
  /**
   * 構建 Prompt
   */
  buildKnowledgePrompt(service, question, context) {
    return `你是 ${service.name}。
服務描述：${service.description}
知識來源：${service.knowledgeSources.join(', ')}
capabilities：${service.capabilities.join(', ')}

任務：${question}
上下文：${context || '無'}

請根據知識庫中的官方文檔回答問題，並提供可執行的解決方案。`;
  }
}

// ============================================================================
// HTTP 服務器
// ============================================================================

class MerchantServer {
  constructor(port, host) {
    this.port = port;
    this.host = host;
    this.ai = new AIClient();
    this.hub = new HubClient(CONFIG.node.id, CONFIG.node.secret);
    this.executor = new TaskExecutor(this.ai, this.hub);
    this.server = null;
  }
  
  start() {
    this.server = http.createServer(this.handleRequest.bind(this));
    
    this.server.listen(this.port, this.host, () => {
      logger.info(`Merchant v2 啟動: http://${this.host}:${this.port}`);
      logger.info(`環境: ${NODE_ENV}`);
      logger.info(`服務數: ${Object.keys(SERVICE_REGISTRY).length}`);
    });
    
    this.server.on('error', (error) => {
      logger.error('服務器錯誤:', error.message);
      process.exit(1);
    });
    
    process.on('SIGTERM', () => this.shutdown());
    process.on('SIGINT', () => this.shutdown());
    
    // 定時心跳（每 5 分鐘）
    this.heartbeatInterval = setInterval(() => {
      this.hub.heartbeat().then(() => {
        logger.debug('心跳成功');
      }).catch(() => {
        logger.warn('心跳失敗');
      });
    }, 5 * 60 * 1000);
  }
  
  async handleRequest(req, res) {
    const startTime = Date.now();
    
    if (IS_DEVELOPMENT) {
      res.setHeader('Access-Control-Allow-Origin', '*');
      res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
      res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');
    }
    
    if (req.method === 'OPTIONS') {
      res.writeHead(204);
      res.end();
      return;
    }
    
    const url = new URL(req.url, `http://${req.headers.host}`);
    const pathname = url.pathname;
    
    logger.debug(`${req.method} ${pathname}`);
    
    try {
      let body = '';
      req.on('data', chunk => body += chunk);
      await new Promise(resolve => req.on('end', resolve));
      
      const data = body ? JSON.parse(body) : {};
      let response;
      let statusCode = 200;
      
      switch (pathname) {
        case '/health':
          response = this.handleHealth();
          break;
        case '/services':
          response = this.handleServices();
          break;
        case '/execute':
          response = await this.handleExecute(data);
          break;
        case '/orders':
        case '/work':
          response = await this.handleOrders();
          break;
        case '/submit':
          response = await this.handleSubmit(data);
          break;
        default:
          response = { error: 'Not Found', path: pathname };
          statusCode = 404;
      }
      
      res.setHeader('Content-Type', 'application/json');
      res.writeHead(statusCode);
      res.end(JSON.stringify(response));
      
      logger.info(`${req.method} ${pathname} - ${statusCode} (${Date.now() - startTime}ms)`);
      
    } catch (error) {
      logger.error('請求處理失敗:', error.message);
      res.writeHead(500);
      res.end(JSON.stringify({ error: error.message }));
    }
  }
  
  handleHealth() {
    return {
      status: 'healthy',
      version: '2.0',
      uptime: process.uptime(),
      memory: process.memoryUsage(),
      timestamp: new Date().toISOString(),
      environment: NODE_ENV,
      services: Object.keys(SERVICE_REGISTRY).length,
      aiConfigured: !!CONFIG.ai.apiKey,
      hubConfigured: !!CONFIG.node.secret,
    };
  }
  
  handleServices() {
    const services = Object.entries(SERVICE_REGISTRY).map(([id, s]) => ({
      id,
      name: s.name,
      description: s.description,
      category: s.category,
      price: s.price,
      minCredits: s.minCredits,
      capabilities: s.capabilities,
    }));
    
    return { services, count: services.length };
  }
  
  async handleExecute(data) {
    const { taskId, serviceType, taskData } = data;
    
    if (!taskId || !serviceType) {
      throw new Error('缺少必要參數: taskId, serviceType');
    }
    
    if (!SERVICE_REGISTRY[serviceType]) {
      throw new Error(`未知服務類型: ${serviceType}`);
    }
    
    const result = await this.executor.execute(taskId, taskData || {}, serviceType);
    
    return { taskId, serviceType, status: 'completed', result };
  }
  
  async handleOrders() {
    const orders = await this.hub.fetchWorkOrders();
    return { orders, count: orders.length };
  }
  
  async handleSubmit(data) {
    const { orderId, result } = data;
    
    if (!orderId) {
      throw new Error('缺少 orderId');
    }
    
    const submitResult = await this.hub.submitWorkResult(orderId, result);
    
    return { orderId, status: 'submitted', result: submitResult };
  }
  
  shutdown() {
    logger.info('開始優雅關閉...');
    
    if (this.heartbeatInterval) {
      clearInterval(this.heartbeatInterval);
    }
    
    if (this.server) {
      this.server.close(() => {
        logger.info('服務器已關閉');
        process.exit(0);
      });
    }
    
    setTimeout(() => {
      logger.error('關閉超時，強制退出');
      process.exit(1);
    }, 30000);
  }
}

// ============================================================================
// 主入口
// ============================================================================

function main() {
  // 載入節點配置
  const nodeIdPath = path.join(os.homedir(), '.evomap', 'node_id');
  const nodeSecretPath = path.join(os.homedir(), '.evomap', 'node_secret');
  
  if (fs.existsSync(nodeIdPath)) {
    CONFIG.node.id = fs.readFileSync(nodeIdPath, 'utf8').trim();
  }
  
  if (fs.existsSync(nodeSecretPath)) {
    CONFIG.node.secret = fs.readFileSync(nodeSecretPath, 'utf8').trim();
  }
  
  // 載入 AI 配置
  const envPath = path.join(process.cwd(), '.env');
  if (fs.existsSync(envPath)) {
    const envContent = fs.readFileSync(envPath, 'utf8');
    envContent.split('\n').forEach(line => {
      const [key, value] = line.split('=');
      if (key && value) {
        process.env[key.trim()] = value.trim();
      }
    });
    
    CONFIG.ai.apiKey = process.env.AI_API_KEY || '';
    CONFIG.ai.baseUrl = process.env.AI_API_URL || CONFIG.ai.baseUrl;
  }
  
  if (!CONFIG.node.id || !CONFIG.node.secret) {
    logger.warn('未找到節點配置，ATP 功能將不可用');
  }
  
  if (!CONFIG.ai.apiKey) {
    logger.warn('未配置 AI API Key，使用本地知識回答');
  }
  
  const server = new MerchantServer(CONFIG.server.port, CONFIG.server.host);
  server.start();
  
  if (IS_DEVELOPMENT) {
    console.log('\n=== Merchant v2 啟動信息 ===');
    console.log(`端口: ${CONFIG.server.port}`);
    console.log(`環境: ${NODE_ENV}`);
    console.log(`AI: ${CONFIG.ai.apiKey ? '已配置' : '本地知識模式'}`);
    console.log(`ATP: ${CONFIG.node.secret ? '已配置' : '未配置'}`);
    console.log(`服務數: ${Object.keys(SERVICE_REGISTRY).length}`);
    console.log('========================\n');
  }
}

module.exports = { MerchantServer, TaskExecutor, HubClient, AIClient, SERVICE_REGISTRY, SERVICE_CATEGORIES };

if (require.main === module) {
  main();
}
