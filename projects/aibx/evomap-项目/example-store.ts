/**
 * Zustand Store 示例 - 展示正确的类型推断写法
 * 
 * 问题：直接使用 createStore<AppState>((set) => ...) 会导致类型推断错误
 * 解决：使用柯里化调用 createStore<AppState>()((set) => ...)
 */

import { createStore } from 'zustand/vanilla';

// ============================================================================
// 应用状态定义
// ============================================================================

interface AppState {
  // Heatmap 数据
  heatmapData: {
    totalSignals: number;
    hotCount: number;
    warmCount: number;
    coldCount: number;
    recommended: Array<{ topic: string; status: string; priority: string }>;
  } | null;
  
  // Claim 状态
  claimStatus: {
    todayClaimed: number;
    todayCompleted: number;
    completionRate: number;
  };
  
  // 积分余额
  creditBalance: number;
  
  // 节点状态
  nodeStatus: 'online' | 'offline' | 'unknown';
  
  // Actions
  setHeatmapData: (data: AppState['heatmapData']) => void;
  updateClaimStatus: (claimed: number, completed: number) => void;
  setCreditBalance: (balance: number) => void;
  setNodeStatus: (status: AppState['nodeStatus']) => void;
}

// ============================================================================
// ❌ 错误写法 - 类型推断失败
// ============================================================================

/*
const wrongStore = createStore<AppState>((set) => ({
  heatmapData: null,
  claimStatus: {
    todayClaimed: 0,
    todayCompleted: 0,
    completionRate: 1.0,
  },
  creditBalance: 0,
  nodeStatus: 'unknown',
  setHeatmapData: (data) => set({ heatmapData: data }),
  updateClaimStatus: (claimed, completed) => set((state) => ({
    claimStatus: {
      todayClaimed: claimed,
      todayCompleted: completed,
      completionRate: claimed > 0 ? completed / claimed : 1.0,
    },
  })),
  setCreditBalance: (balance) => set({ creditBalance: balance }),
  setNodeStatus: (status) => set({ nodeStatus: status }),
}));
// 错误信息：Type inference fails, actions may not have correct types
*/

// ============================================================================
// ✅ 正确写法 - 柯里化调用
// ============================================================================

const appStore = createStore<AppState>()((set) => ({
  // Initial state
  heatmapData: null,
  claimStatus: {
    todayClaimed: 0,
    todayCompleted: 0,
    completionRate: 1.0,
  },
  creditBalance: 0,
  nodeStatus: 'unknown',
  
  // Actions
  setHeatmapData: (data) => set({ heatmapData: data }),
  
  updateClaimStatus: (claimed, completed) => set((state) => ({
    claimStatus: {
      todayClaimed: claimed,
      todayCompleted: completed,
      completionRate: claimed > 0 ? completed / claimed : 1.0,
    },
  })),
  
  setCreditBalance: (balance) => set({ creditBalance: balance }),
  
  setNodeStatus: (status) => set({ nodeStatus: status }),
}));

// ============================================================================
// 使用示例
// ============================================================================

// 订阅状态变化
appStore.subscribe((state) => {
  console.log('Node status changed:', state.nodeStatus);
});

// 更新 Heatmap 数据
appStore.getState().setHeatmapData({
  totalSignals: 10000,
  hotCount: 1945,
  warmCount: 8055,
  coldCount: 0,
  recommended: [
    { topic: '抖音带货', status: 'High demand, no supply', priority: 'P0' },
    { topic: '直播间搭建', status: 'High demand, no supply', priority: 'P0' },
  ],
});

// 更新 Claim 状态
appStore.getState().updateClaimStatus(2, 2);

// 更新积分余额
appStore.getState().setCreditBalance(150);

// 更新节点状态
appStore.getState().setNodeStatus('online');

// 获取当前状态
const currentState = appStore.getState();
console.log('Current state:', currentState);

// ============================================================================
// 导出
// ============================================================================

export type { AppState };
export { appStore };
