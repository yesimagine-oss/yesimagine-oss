# EvoMap Zustand Store

完整的状态管理解决方案，使用 Zustand 和 TypeScript。

## 📦 特性

- ✅ **TypeScript 支持** - 完整的类型定义
- ✅ **柯里化调用** - 使用 `createStore<Type>()((set) => ...)` 解决类型推断问题
- ✅ **模块化设计** - 5 个独立的 Store
- ✅ **组合模式** - App Store 组合所有 Store
- ✅ **零依赖** - 仅需 Zustand

## 📁 文件结构

```
src/store/
├── types.ts              # 类型定义
├── heatmap-store.ts      # Heatmap 数据管理
├── claim-store.ts        # Claim 任务管理
├── credit-store.ts       # 积分余额管理
├── node-store.ts         # 节点状态管理
├── app-store.ts          # 组合所有 Store
├── index.ts              # 导出文件
└── README.md             # 本文档
```

## 🚀 快速开始

### 1. 安装依赖

```bash
npm install zustand
```

### 2. 导入 Store

```typescript
import {
  appStore,
  heatmapStore,
  claimStore,
  creditStore,
  nodeStore,
  initializeApp,
} from './store';
```

### 3. 初始化应用

```typescript
// 应用启动时初始化
await initializeApp();
```

### 4. 访问状态

```typescript
// 获取 Heatmap 数据
const heatmapData = heatmapStore.getState().data;

// 获取 Claim 状态
const claimStatus = claimStore.getState().status;

// 获取积分余额
const balance = creditStore.getState().balance;

// 获取节点状态
const nodeStatus = nodeStore.getState().health.status;
```

### 5. 调用 Actions

```typescript
// 获取 Heatmap 数据
await heatmapStore.getState().fetchData();

// Claim 任务
const success = await claimStore.getState().claimTask('task_001');

// 添加交易记录
creditStore.getState().addTransaction({
  type: 'earn',
  amount: 100,
  description: 'Task completed',
});

// 检查节点健康
await nodeStore.getState().checkHealth();
```

### 6. 订阅状态变化

```typescript
// 订阅单个 Store
const unsubscribe = heatmapStore.subscribe((state) => {
  console.log('Heatmap changed:', state.data);
});

// 稍后取消订阅
unsubscribe();

// 订阅所有 Store
import { subscribeToAllStores } from './store';

const unsubscribeAll = subscribeToAllStores((state) => {
  console.log('Any store changed:', state);
});
```

### 7. 使用选择器

```typescript
// 获取 P0 机会
const p0Opportunities = heatmapStore.getState().getP0Opportunities();

// 获取完成率
const completionRate = claimStore.getState().getCompletionRate();

// 检查是否在线
const isOnline = nodeStore.getState().isOnline();

// 检查是否能负担
const canAfford = creditStore.getState().canAfford(100);
```

## 📊 Store 说明

### Heatmap Store

管理 Topic Heatmap 数据。

**状态：**
- `data` - Heatmap 数据
- `isLoading` - 加载状态
- `filterPriority` - 优先级过滤器
- `filterType` - 类型过滤器

**Actions：**
- `fetchData()` - 获取 Heatmap 数据
- `setData(data)` - 设置数据
- `setFilterPriority(priority)` - 设置优先级过滤
- `getP0Opportunities()` - 获取 P0 机会
- `shouldAvoidTopic(topic)` - 检查是否应避免的话题

### Claim Store

管理任务 Claim 状态。

**状态：**
- `availableTasks` - 可用任务
- `claimedTasks` - 已 Claim 任务
- `status` - Claim 状态
- `autoClaim` - 是否自动 Claim

**Actions：**
- `fetchTasks()` - 获取任务列表
- `claimTask(taskId)` - Claim 任务
- `completeTask(taskId)` - 完成任务
- `getAvailableP0Tasks()` - 获取 P0 任务
- `shouldClaimNow()` - 检查是否应该 Claim

### Credit Store

管理积分余额和交易。

**状态：**
- `balance` - 积分余额
- `transactions` - 交易记录
- `targetBalance` - 目标余额

**Actions：**
- `fetchBalance()` - 获取余额
- `addTransaction(transaction)` - 添加交易
- `getTotalEarned()` - 获取总收入
- `getAverageDailyEarn()` - 获取日均收入
- `canAfford(amount)` - 检查是否能负担

### Node Store

管理节点健康状态。

**状态：**
- `nodeId` - 节点 ID
- `health` - 健康状态
- `heartbeatInterval` - 心跳间隔

**Actions：**
- `checkHealth()` - 检查健康
- `recordHeartbeat(success, response)` - 记录心跳
- `isOnline()` - 检查是否在线
- `getSuccessRate()` - 获取成功率
- `shouldReconnect()` - 检查是否应重连

### App Store

组合所有 Store 的主 Store。

**Actions：**
- `initialize()` - 初始化所有 Store
- `syncAllStores()` - 同步所有 Store
- `generateSupervisorReport()` - 生成监管报告

## 🔧 TypeScript 类型推断修复

### ❌ 错误写法

```typescript
const store = createStore<AppState>((set) => ({
  // ...
}));
// 错误：类型推断失败
```

### ✅ 正确写法

```typescript
const store = createStore<AppState>()((set) => ({
  // ...
}));
// 正确：柯里化调用，类型推断正确
```

**原因：** 柯里化调用分两步进行类型推断，避免类型冲突。

## 📝 完整示例

```typescript
import { initializeApp, heatmapStore, claimStore } from './store';

// 初始化
await initializeApp();

// 获取 P0 机会
const p0Topics = heatmapStore.getState().getP0Opportunities();
console.log('P0 Opportunities:', p0Topics);

// Claim P0 任务
const p0Tasks = claimStore.getState().getAvailableP0Tasks();
for (const task of p0Tasks) {
  const success = await claimStore.getState().claimTask(task.task_id);
  if (success) {
    console.log(`Claimed task: ${task.title}`);
  }
}

// 订阅状态变化
heatmapStore.subscribe((state) => {
  if (state.data) {
    console.log('Heatmap updated:', state.data.timestamp);
  }
});
```

## 🎯 最佳实践

1. **使用选择器** - 使用 `getP0Opportunities()` 而不是直接访问数据
2. **错误处理** - 在 Action 中捕获并处理错误
3. **订阅清理** - 组件卸载时取消订阅
4. **类型安全** - 始终使用 TypeScript 类型
5. **柯里化调用** - 始终使用 `createStore<Type>()((set) => ...)`

## 📚 参考资料

- [Zustand 官方文档](https://github.com/pmndrs/zustand)
- [TypeScript 类型推断](https://www.typescriptlang.org/docs/handbook/type-inference.html)
- [类型定义](./types.ts)

---

**创建时间：** 2026-03-26 21:50  
**状态：** ✅ 完成
