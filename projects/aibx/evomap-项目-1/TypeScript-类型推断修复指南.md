---
title: "Typescript 类型推断修复指南"
type: "general"
category: "general"
tags: ["general", "auto-generated"]
created_at: "2026-04-14"
version: "1.0"
---

# TypeScript 类型推断修复指南

**问题：** Zustand `createStore` 类型推断失败  
**解决：** 使用柯里化调用 `createStore<AppState>()((set) => ...)`

---

## ❌ 错误写法

```typescript
import { createStore } from 'zustand/vanilla';

interface AppState {
  count: number;
  increment: () => void;
}

// ❌ 错误：类型推断失败
const store = createStore<AppState>((set) => ({
  count: 0,
  increment: () => set((state) => ({ count: state.count + 1 })),
}));

// 错误信息：
// Type '() => void' is not assignable to type 'undefined'.
// Actions may not have correct types.
```

---

## ✅ 正确写法

```typescript
import { createStore } from 'zustand/vanilla';

interface AppState {
  count: number;
  increment: () => void;
}

// ✅ 正确：柯里化调用
const store = createStore<AppState>()((set) => ({
  count: 0,
  increment: () => set((state) => ({ count: state.count + 1 })),
}));

// 类型推断正确，actions 有正确的类型
```

---

## 🔍 为什么需要柯里化？

### 类型推断过程

**直接调用：**
```typescript
createStore<AppState>((set) => ...)
// TypeScript 尝试同时推断：
// 1. AppState 类型
// 2. StoreApi<AppState> 类型
// 3. StateCreator<AppState> 类型
// 可能导致冲突
```

**柯里化调用：**
```typescript
createStore<AppState>()((set) => ...)
// 第一步：createStore<AppState>() 返回一个类型化的工厂函数
// 第二步：工厂函数接受 (set) => ... 并正确推断类型
// 类型推断更清晰，不会冲突
```

---

## 📋 完整示例

参考 `example-store.ts` 文件，包含：

1. ✅ AppState 接口定义
2. ✅ 错误的 createStore 调用（注释）
3. ✅ 正确的柯里化调用
4. ✅ 使用示例（订阅、更新、获取状态）

---

## 🎯 在 EvoMap 项目中的应用

如果你要在 EvoMap 项目中添加 TypeScript 前端：

### 1. 安装依赖

```bash
cd /home/admin/.openclaw/workspace/ai 知识变现/evomap 项目
npm install zustand
npm install -D typescript @types/node @types/react
```

### 2. 创建 tsconfig.json

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "ESNext",
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "jsx": "react-jsx",
    "strict": true,
    "moduleResolution": "bundler",
    "skipLibCheck": true,
    "esModuleInterop": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules"]
}
```

### 3. 创建 Store

```typescript
// src/store/evomap-store.ts
import { createStore } from 'zustand/vanilla';

interface EvoMapState {
  // Heatmap 状态
  heatmapData: HeatmapData | null;
  
  // Claim 状态
  claimStatus: ClaimStatus;
  
  // 积分余额
  creditBalance: number;
  
  // Actions
  fetchHeatmap: () => Promise<void>;
  claimTask: (taskId: string) => Promise<boolean>;
  // ...
}

// ✅ 使用柯里化调用
export const evomapStore = createStore<EvoMapState>()((set, get) => ({
  heatmapData: null,
  claimStatus: { todayClaimed: 0, todayCompleted: 0 },
  creditBalance: 0,
  
  fetchHeatmap: async () => {
    // 实现...
  },
  
  claimTask: async (taskId) => {
    // 实现...
    return true;
  },
}));
```

---

## 📚 参考资料

- [Zustand 官方文档](https://github.com/pmndrs/zustand)
- [TypeScript 类型推断](https://www.typescriptlang.org/docs/handbook/type-inference.html)
- [示例文件](./example-store.ts)

---

**创建时间：** 2026-03-26 21:45  
**状态：** 已完成

## 參考

- [[EvoMap 用戶手冊]]
- [[OpenClaw 完全指南]]
