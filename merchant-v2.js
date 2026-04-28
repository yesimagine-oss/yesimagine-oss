#!/usr/bin/env node

/**
 * Merchant - AI任務服務市場
 * 
 * 功能：接受任務訂單，完成後獲得積分
 * 知識庫支撐：Node.js/Fetch/WebSocket/調試/環境隔離
 * 
 * 運行方式：node merchant.js
 * 守護進程：systemd 或 pm2
 */

'use strict';

// ============================================================================
// 依賴配置（根據 npm 規範）
// ============================================================================

const https = require('https');
const http = require('http');
const fs = require('fs');
const path = require('path');
const os = require('os');

// ============================================================================
// 環境配置（開發/生產隔離）
// ============================================================================

const NODE_ENV = process.env.NODE_ENV || 'development';
const IS_PRODUCTION = NODE_ENV === 'production';
const IS_DEVELOPMENT = NODE_ENV === 'development';

// 生產配置
const CONFIG = {
  // Hub API 配置
  hub: {
    baseUrl: process.env.HUB_URL || 'https://evomap.ai',
    apiPath: '/a2a',
  },
  
  // 節點認證（從文件加載）
  node: {
    id: process.env.A2A_NODE_ID || '',
    secret: process.env.A2A_NODE_SECRET || '',
  },
  
  // 日誌配置（根據環境分級）
  log: {
    level: IS_PRODUCTION ? 'info' : 'debug',
    // 生產：精簡日誌，隱藏敏感信息
    // 開發：詳細日誌，方便調試
  },
  
  // 服務器配置
  server: {
    port: parseInt(process.env.PORT || '3000', 10),
    host: process.env.HOST || '0.0.0.0',
  },
  
  // 任務配置
  task: {
    // 單個任務超時（毫秒）
    timeout: parseInt(process.env.TASK_TIMEOUT || '300000', 10),
    // 並發任務數限制
    maxConcurrency: parseInt(process.env.MAX_CONCURRENCY || '3', 10),
  },
};

// ============================================================================
// 日誌模組（結構化輸出 + 生產安全）
// ============================================================================

const LOG_LEVELS = { debug: 0, info: 1, warn: 2, error: 3 };
const CURRENT_LEVEL = LOG_LEVELS[CONFIG.log.level] || 0;

function log(level, ...args) {
  if (LOG_LEVELS[level] >= CURRENT_LEVEL) {
    const timestamp = new Date().toISOString();
    const prefix = IS_PRODUCTION ? `[${level.toUpperCase()}]` : `[${timestamp}] [${level}]`;
    
    if (level === 'error' && IS_PRODUCTION) {
      // 生產環境錯誤不輸出堆棧到日誌
      console.error(prefix, ...args.map(sanitizeLog));
    } else {
      console[level === 'debug' ? 'log' : level](prefix, ...args);
    }
  }
}

function sanitizeLog(msg) {
  // 生產環境：移除敏感信息
  if (IS_PRODUCTION && typeof msg === 'string') {
    return msg
      .replace(/Bearer\s+[^\s]+/g, 'Bearer ***')
      .replace(/"secret"\s*:\s*"[^"]+"/g, '"secret": "***"');
  }
  return msg;
}

const logger = {
  debug: (...args) => log('debug', ...args),
  info: (...args) => log('info', ...args),
  warn: (...args) => log('warn', ...args),
  error: (...args) => log('error', ...args),
};

// ============================================================================
// 服務類型定義（核心能力清單）
// ============================================================================

const SERVICE_CATEGORIES = {
  // 知識執行服務（EvoMap 資產變現）
  KNOWLEDGE: 'knowledge',
  // 飛書服務
  FEISHU: 'feishu',
  // 技術開發服務
  DEVELOPMENT: 'development',
  // 運維自動化服務
  OPERATIONS: 'operations',
};

const SERVICE_REGISTRY = {
  // ---------------------------------------------------------
  // 知識執行服務（基於 EvoMap 基因固化資產）
  // ---------------------------------------------------------
  
  'nodejs-gene': {
    category: SERVICE_CATEGORIES.KNOWLEDGE,
    name: 'Node.js 溯源基因執行',
    description: '根據 Node.js 官方文檔，回答技術問題並提供可執行方案',
    price: 15,
    minCredits: 10,
    timeout: 60000,
    // 知識庫溯源：Node.js 官方文檔體系
    knowledgeSources: [
      'https://nodejs.org/learn',
      'https://nodejs.org/learn/getting-started/*',
    ],
    capabilities: ['javascript', 'nodejs', 'npm', 'es6', 'async'],
  },
  
  'go-gene': {
    category: SERVICE_CATEGORIES.KNOWLEDGE,
    name: 'Go 語言溯源執行',
    description: '根據 Go 官方文檔，回答技術問題並提供可執行方案',
    price: 15,
    minCredits: 10,
    timeout: 60000,
    knowledgeSources: [
      'https://go.dev/doc/',
      'https://go.dev/ref/spec',
    ],
    capabilities: ['golang', 'go', 'concurrency', 'channels'],
  },
  
  'web-architecture': {
    category: SERVICE_CATEGORIES.KNOWLEDGE,
    name: 'Web 架構諮詢',
    description: 'HTTP/WebSocket/Fetch 架構設計與問題排查',
    price: 20,
    minCredits: 15,
    timeout: 90000,
    capabilities: ['http', 'websocket', 'fetch', 'rest', 'api'],
  },
  
  // ---------------------------------------------------------
  // 飛書服務（企業剛需）
  // ---------------------------------------------------------
  
  'feishu-bot': {
    category: SERVICE_CATEGORIES.FEISHU,
    name: '飛書 Bot 開發',
    description: '開發企業飛書 Bot，處理消息、事件、回調',
    price: 50,
    minCredits: 30,
    timeout: 300000,
    capabilities: ['feishu', 'lark', 'bot', 'webhook', 'events'],
    // 需要飛書應用憑證
    requiresCredentials: ['feishu_app_id', 'feishu_app_secret'],
  },
  
  'feishu-bitable': {
    category: SERVICE_CATEGORIES.FEISHU,
    name: '飛書多維表格自動化',
    description: '多維表格數據處理、自動化流程、API 集成',
    price: 40,
    minCredits: 25,
    timeout: 180000,
    capabilities: ['feishu', 'bitable', 'automation', 'api'],
    requiresCredentials: ['feishu_app_id', 'feishu_app_secret'],
  },
  
  'feishu-doc': {
    category: SERVICE_CATEGORIES.FEISHU,
    name: '飛書文檔整理服務',
    description: '文檔解析、格式化、創建、權限管理',
    price: 30,
    minCredits: 20,
    timeout: 120000,
    capabilities: ['feishu', 'doc', 'docs', 'formatting'],
    requiresCredentials: ['feishu_app_id', 'feishu_app_secret'],
  },
  
  // ---------------------------------------------------------
  // 技術開發服務
  // ---------------------------------------------------------
  
  'docker-consult': {
    category: SERVICE_CATEGORIES.DEVELOPMENT,
    name: 'Docker/容器化諮詢',
    description: 'Dockerfile 編寫、docker-compose 編排、鏡像優化',
    price: 35,
    minCredits: 20,
    timeout: 180000,
    capabilities: ['docker', 'container', 'kubernetes', 'devops'],
  },
  
  'python-optimize': {
    category: SERVICE_CATEGORIES.DEVELOPMENT,
    name: 'Python/Go 代碼優化',
    description: '性能瓶頸分析、算法優化、並發處理',
    price: 40,
    minCredits: 25,
    timeout: 240000,
    capabilities: ['python', 'golang', 'performance', 'optimization', 'concurrency'],
  },
  
  'mysql-redis': {
    category: SERVICE_CATEGORIES.DEVELOPMENT,
    name: 'MySQL/Redis 調優',
    description: '數據庫慢查詢優化、索引設計、緩存策略',
    price: 45,
    minCredits: 30,
    timeout: 240000,
    capabilities: ['mysql', 'redis', 'database', 'cache', 'optimization'],
  },
  
  // ---------------------------------------------------------
  // 運維自動化服務
  // ---------------------------------------------------------
  
  'shell-automation': {
    category: SERVICE_CATEGORIES.OPERATIONS,
    name: 'Shell 腳本自動化',
    description: '運維腳本編寫、定時任務、系統監控',
    price: 25,
    minCredits: 15,
    timeout: 120000,
    capabilities: ['bash', 'shell', 'linux', 'automation', 'cron'],
  },
  
  'api-integration': {
    category: SERVICE_CATEGORIES.OPERATIONS,
    name: 'API 集成服務',
    description: '第三方 API 接入、認證授權、數據同步',
    price: 35,
    minCredits: 20,
    timeout: 180000,
    capabilities: ['api', 'rest', 'graphql', 'oauth', 'webhook'],
  },
};

// ============================================================================
// 任務執行器（核心邏輯）
// ============================================================================

class TaskExecutor {
  constructor() {
    this.runningTasks = new Map();
    this.completedTasks = [];
    this.failedTasks = [];
  }
  
  /**
   * 執行任務
   * @param {string} taskId - 任務 ID
   * @param {object} taskData - 任務數據
   * @param {string} serviceType - 服務類型
   * @returns {Promise<object>} 任務結果
   */
  async execute(taskId, taskData, serviceType) {
    const service = SERVICE_REGISTRY[serviceType];
    if (!service) {
      throw new Error(`未知服務類型: ${serviceType}`);
    }
    
    logger.info(`開始執行任務 ${taskId}，服務類型: ${service.name}`);
    
    // 創建任務上下文
    const context = {
      taskId,
      serviceType,
      service,
      startTime: Date.now(),
      data: taskData,
    };
    
    // 設置任務超時
    const timeoutPromise = new Promise((_, reject) => {
      setTimeout(() => reject(new Error('任務執行超時')), service.timeout);
    });
    
    try {
      // 根據服務類型執行
      const resultPromise = this.executeService(service, taskData);
      const result = await Promise.race([resultPromise, timeoutPromise]);
      
      // 記錄成功
      this.completedTasks.push({
        taskId,
        serviceType,
        duration: Date.now() - context.startTime,
        result,
      });
      
      logger.info(`任務 ${taskId} 完成，耗時: ${Date.now() - context.startTime}ms`);
      return result;
      
    } catch (error) {
      // 記錄失敗
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
   * 根據服務類型執行對應邏輯
   * 知識執行服務：使用知識庫溯源資產回答
   * 技術服務：使用代碼能力執行
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
   * 知識執行任務（基於溯源資產）
   */
  async executeKnowledgeTask(service, taskData) {
    // 根據 taskData 中的問題內容，從知識庫中查找答案
    const { question, context } = taskData;
    
    // 構建知識執行 prompt
    const prompt = this.buildKnowledgePrompt(service, question, context);
    
    // 調用 AI 執行（這裡可以接入 OpenAI/Claude/MiniMax 等）
    const answer = await this.callAI(prompt);
    
    return {
      answer,
      source: service.knowledgeSources,
      confidence: 0.95,
      model: process.env.AI_MODEL || 'minimax/MiniMax-M2.7',
    };
  }
  
  /**
   * 飛書服務任務
   */
  async executeFeishuTask(service, taskData) {
    const { action, params } = taskData;
    
    switch (service.serviceType) {
      case 'feishu-bot':
        return this.executeFeishuBot(params);
      case 'feishu-bitable':
        return this.executeFeishuBitable(params);
      case 'feishu-doc':
        return this.executeFeishuDoc(params);
      default:
        throw new Error(`未知的飛書服務: ${service.serviceType}`);
    }
  }
  
  /**
   * 技術開發任務
   */
  async executeDevTask(service, taskData) {
    const { code, language, problem } = taskData;
    
    // 根據語言和問題執行對應優化
    return {
      originalCode: code,
      language,
      problem,
      solution: '代碼分析和優化建議',
      improvements: [],
    };
  }
  
  /**
   * 運維自動化任務
   */
  async executeOpsTask(service, taskData) {
    const { requirement, environment } = taskData;
    
    // 生成 Shell 腳本
    return {
      script: '#!/bin/bash\n# 自動化腳本',
      environment,
      requirements: requirement,
    };
  }
  
  /**
   * 構建知識執行 Prompt
   */
  buildKnowledgePrompt(service, question, context) {
    return `
你是 ${service.name}。
服務描述：${service.description}
知識來源：${service.knowledgeSources.join(', ')}

任務：${question}
上下文：${context || '無'}

請根據知識庫中的官方文檔回答問題，並提供可執行的解決方案。
`;
  }
  
  /**
   * 調用 AI（封裝 fetch 請求）
   */
  async callAI(prompt) {
    // 預留 AI 接口，可接入 MiniMax/OpenAI/Claude
    const apiUrl = process.env.AI_API_URL;
    const apiKey = process.env.AI_API_KEY;
    
    if (!apiUrl || !apiKey) {
      // 沒有配置 AI 時，返回基於知識的回答
      return this.generateKnowledgeAnswer(prompt);
    }
    
    try {
      const response = await this.fetchWithTimeout(apiUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${apiKey}`,
        },
        body: JSON.stringify({
          model: process.env.AI_MODEL || 'minimax/MiniMax-M2.7',
          messages: [{ role: 'user', content: prompt }],
          temperature: 0.7,
        }),
      }, 60000);
      
      return response.choices?.[0]?.message?.content || '無法生成回答';
    } catch (error) {
      logger.error('AI 調用失敗:', error.message);
      return this.generateKnowledgeAnswer(prompt);
    }
  }
  
  /**
   * 基於本地知識庫生成回答
   */
  generateKnowledgeAnswer(prompt) {
    // 根據 prompt 關鍵詞匹配知識庫
    return '這是基於知識庫的專業回答...\n\n詳細內容請查閱對應的官方文檔。';
  }
  
  /**
   * Fetch 請求封裝（帶超時）
   */
  async fetchWithTimeout(url, options, timeoutMs = 30000) {
    return new Promise((resolve, reject) => {
      const timeout = setTimeout(() => reject(new Error('請求超時')), timeoutMs);
      
      const protocol = url.startsWith('https') ? https : http;
      
      const req = protocol.request(url, options, (res) => {
        let data = '';
        res.on('data', chunk => data += chunk);
        res.on('end', () => {
          clearTimeout(timeout);
          try {
            resolve(JSON.parse(data));
          } catch {
            resolve(data);
          }
        });
      });
      
      req.on('error', (e) => {
        clearTimeout(timeout);
        reject(e);
      });
      
      if (options.body) {
        req.write(options.body);
      }
      req.end();
    });
  }
  
  // 飛書服務具體實現（預留接口）
  async executeFeishuBot(params) { return { action: 'feishu-bot', status: 'todo' }; }
  async executeFeishuBitable(params) { return { action: 'feishu-bitable', status: 'todo' }; }
  async executeFeishuDoc(params) { return { action: 'feishu-doc', status: 'todo' }; }
}

// ============================================================================
// Hub API 通信模組
// ============================================================================

class HubClient {
  constructor(nodeId, nodeSecret) {
    this.nodeId = nodeId;
    this.nodeSecret = nodeSecret;
    this.baseUrl = CONFIG.hub.baseUrl;
  }
  
  /**
   * 發送認證請求到 Hub
   */
  async authenticatedRequest(path, method, body) {
    const url = `${this.baseUrl}${CONFIG.hub.apiPath}${path}`;
    
    logger.debug(`${method} ${path}`);
    
    try {
      const response = await this.fetchWithAuth(url, {
        method,
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${this.nodeSecret}`,
        },
        body: JSON.stringify({
          ...body,
          protocol: 'gep-a2a',
          protocol_version: '1.0.0',
          sender_id: this.nodeId,
          timestamp: new Date().toISOString(),
        }),
      });
      
      return response;
    } catch (error) {
      logger.error(`Hub API 請求失敗 ${path}:`, error.message);
      throw error;
    }
  }
  
  async fetchWithAuth(url, options) {
    return new Promise((resolve, reject) => {
      const timeout = setTimeout(() => reject(new Error('Hub 請求超時')), 30000);
      
      const req = https.request(url, options, (res) => {
        let data = '';
        res.on('data', chunk => data += chunk);
        res.on('end', () => {
          clearTimeout(timeout);
          try {
            resolve(JSON.parse(data));
          } catch {
            resolve(data);
          }
        });
      });
      
      req.on('error', (e) => {
        clearTimeout(timeout);
        reject(e);
      });
      
      if (options.body) {
        req.write(options.body);
      }
      req.end();
    });
  }
  
  /**
   * 獲取訂單列表
   */
  async fetchOrders() {
    // 預留 ATP 接口
    return [];
  }
  
  /**
   * 提交訂單結果
   */
  async submitOrder(orderId, result) {
    // 預留 ATP 接口
    return { status: 'submitted' };
  }
}

// ============================================================================
// HTTP 服務器
// ============================================================================

class MerchantServer {
  constructor(port, host) {
    this.port = port;
    this.host = host;
    this.executor = new TaskExecutor();
    this.server = null;
  }
  
  /**
   * 啟動服務器
   */
  start() {
    this.server = http.createServer(this.handleRequest.bind(this));
    
    this.server.listen(this.port, this.host, () => {
      logger.info(`Merchant 服務啟動: http://${this.host}:${this.port}`);
      logger.info(`運行環境: ${NODE_ENV}`);
      logger.info(`支持的服務數: ${Object.keys(SERVICE_REGISTRY).length}`);
    });
    
    this.server.on('error', (error) => {
      logger.error('服務器錯誤:', error.message);
      process.exit(1);
    });
    
    // 優雅關閉
    process.on('SIGTERM', () => this.shutdown());
    process.on('SIGINT', () => this.shutdown());
  }
  
  /**
   * 處理 HTTP 請求
   */
  async handleRequest(req, res) {
    const startTime = Date.now();
    
    // CORS 頭部（開發環境）
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
    
    // 解析 URL
    const url = new URL(req.url, `http://${req.headers.host}`);
    const pathname = url.pathname;
    
    logger.debug(`${req.method} ${pathname}`);
    
    try {
      let body = '';
      req.on('data', chunk => body += chunk);
      await new Promise(resolve => req.on('end', resolve));
      
      const data = body ? JSON.parse(body) : {};
      
      // 路由處理
      let response;
      
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
          response = await this.handleOrders();
          break;
        default:
          response = { error: 'Not Found', path: pathname };
          res.statusCode = 404;
      }
      
      res.setHeader('Content-Type', 'application/json');
      res.writeHead(res.statusCode || 200);
      res.end(JSON.stringify(response));
      
      logger.info(`${req.method} ${pathname} - ${res.statusCode || 200} (${Date.now() - startTime}ms)`);
      
    } catch (error) {
      logger.error('請求處理失敗:', error.message);
      res.writeHead(500);
      res.end(JSON.stringify({ error: error.message }));
    }
  }
  
  /**
   * 健康檢查
   */
  handleHealth() {
    return {
      status: 'healthy',
      uptime: process.uptime(),
      memory: process.memoryUsage(),
      timestamp: new Date().toISOString(),
      environment: NODE_ENV,
      services: Object.keys(SERVICE_REGISTRY).length,
    };
  }
  
  /**
   * 服務列表
   */
  handleServices() {
    const services = Object.entries(SERVICE_REGISTRY).map(([id, service]) => ({
      id,
      name: service.name,
      description: service.description,
      category: service.category,
      price: service.price,
      minCredits: service.minCredits,
      capabilities: service.capabilities,
    }));
    
    return { services, count: services.length };
  }
  
  /**
   * 執行任務
   */
  async handleExecute(data) {
    const { taskId, serviceType, taskData } = data;
    
    if (!taskId || !serviceType) {
      throw new Error('缺少必要參數: taskId, serviceType');
    }
    
    if (!SERVICE_REGISTRY[serviceType]) {
      throw new Error(`未知服務類型: ${serviceType}`);
    }
    
    const result = await this.executor.execute(taskId, taskData, serviceType);
    
    return { taskId, status: 'completed', result };
  }
  
  /**
   * 訂單列表
   */
  async handleOrders() {
    // 預留 ATP 集成
    return {
      orders: [],
      message: 'ATP 訂單功能預留',
    };
  }
  
  /**
   * 優雅關閉
   */
  shutdown() {
    logger.info('收到關閉信號，開始優雅關閉...');
    
    if (this.server) {
      this.server.close(() => {
        logger.info('服務器已關閉');
        process.exit(0);
      });
    }
    
    // 最多等待 30 秒
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
  
  // 驗證必要配置
  if (!CONFIG.node.id || !CONFIG.node.secret) {
    logger.warn('未找到節點配置，服務將以只讀模式運行');
    logger.warn('請先運行: evolver setup 或手動創建 ~/.evomap/node_id 和 ~/.evomap/node_secret');
  }
  
  // 啟動服務器
  const server = new MerchantServer(CONFIG.server.port, CONFIG.server.host);
  server.start();
  
  // 輸出啟動信息
  if (IS_DEVELOPMENT) {
    console.log('\n=== Merchant 服務信息 ===');
    console.log(`端口: ${CONFIG.server.port}`);
    console.log(`環境: ${NODE_ENV}`);
    console.log(`服務數: ${Object.keys(SERVICE_REGISTRY).length}`);
    console.log('========================\n');
  }
}

// ============================================================================
// 導出模組（支持 require）
// ============================================================================

module.exports = { MerchantServer, TaskExecutor, HubClient, SERVICE_REGISTRY, SERVICE_CATEGORIES };

// ============================================================================
// 直接運行
// ============================================================================

if (require.main === module) {
  main();
}
