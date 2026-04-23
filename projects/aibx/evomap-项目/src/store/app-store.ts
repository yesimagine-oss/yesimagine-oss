/**
 * App Store - 组合所有 Store 的主 Store
 * 
 * ✅ 使用柯里化调用：createStore<AppState>()((set, get) => ...)
 */

import { createStore } from 'zustand/vanilla';
import { heatmapStore } from './heatmap-store';
import { claimStore } from './claim-store';
import { creditStore } from './credit-store';
import { nodeStore } from './node-store';
import type { SupervisorReport, AnalysisResult } from './types';

// ============================================================================
// App 状态
// ============================================================================

export interface AppState {
  // 监管报告
  supervisorReport: SupervisorReport | null;
  
  // 分析结果
  analysisResult: AnalysisResult | null;
  
  // 加载状态
  isInitializing: boolean;
  lastSynced: string | null;
  
  // Actions
  initialize: () => Promise<void>;
  syncAllStores: () => Promise<void>;
  generateSupervisorReport: () => SupervisorReport;
  
  // Store 访问
  getHeatmapStore: () => typeof heatmapStore;
  getClaimStore: () => typeof claimStore;
  getCreditStore: () => typeof creditStore;
  getNodeStore: () => typeof nodeStore;
}

// ============================================================================
// 创建 Store - 使用柯里化调用 ✅
// ============================================================================

export const appStore = createStore<AppState>()((set, get) => ({
  // Initial state
  supervisorReport: null,
  analysisResult: null,
  isInitializing: true,
  lastSynced: null,
  
  // Actions
  initialize: async () => {
    console.log('[AppStore] Initializing...');
    
    try {
      // 并行初始化所有 Store
      await Promise.all([
        nodeStore.getState().checkHealth(),
        creditStore.getState().fetchBalance(),
        heatmapStore.getState().fetchData(),
        claimStore.getState().fetchTasks(),
      ]);
      
      // 生成监管报告
      const report = get().generateSupervisorReport();
      
      set({
        supervisorReport: report,
        isInitializing: false,
        lastSynced: new Date().toISOString(),
      });
      
      console.log('[AppStore] Initialization complete');
    } catch (error) {
      console.error('[AppStore] Initialization failed:', error);
      set({
        isInitializing: false,
        lastSynced: new Date().toISOString(),
      });
    }
  },
  
  syncAllStores: async () => {
    console.log('[AppStore] Syncing all stores...');
    
    try {
      await Promise.all([
        nodeStore.getState().checkHealth(),
        creditStore.getState().fetchBalance(),
        heatmapStore.getState().fetchData(),
        claimStore.getState().fetchTasks(),
      ]);
      
      const report = get().generateSupervisorReport();
      
      set({
        supervisorReport: report,
        lastSynced: new Date().toISOString(),
      });
      
      console.log('[AppStore] Sync complete');
    } catch (error) {
      console.error('[AppStore] Sync failed:', error);
    }
  },
  
  generateSupervisorReport: () => {
    const nodeState = nodeStore.getState();
    const claimState = claimStore.getState();
    const creditState = creditStore.getState();
    const heatmapState = heatmapStore.getState();
    
    const report: SupervisorReport = {
      timestamp: new Date().toISOString(),
      nodeHealth: nodeState.health,
      claimStatus: claimState.status,
      creditBalance: creditState.balance,
      heatmapOpportunities: heatmapState.getP0Opportunities().length,
      publishedAssets: 0, // TODO: 从 asset store 获取
    };
    
    return report;
  },
  
  // Store accessors
  getHeatmapStore: () => heatmapStore,
  getClaimStore: () => claimStore,
  getCreditStore: () => creditStore,
  getNodeStore: () => nodeStore,
}));

// ============================================================================
// 工具函数
// ============================================================================

/**
 * 订阅所有 Store 的变化
 */
export function subscribeToAllStores(callback: (state: AppState) => void) {
  const unsubscribeApp = appStore.subscribe(callback);
  const unsubscribeHeatmap = heatmapStore.subscribe(() => {
    callback(appStore.getState());
  });
  const unsubscribeClaim = claimStore.subscribe(() => {
    callback(appStore.getState());
  });
  const unsubscribeCredit = creditStore.subscribe(() => {
    callback(appStore.getState());
  });
  const unsubscribeNode = nodeStore.subscribe(() => {
    callback(appStore.getState());
  });
  
  return () => {
    unsubscribeApp();
    unsubscribeHeatmap();
    unsubscribeClaim();
    unsubscribeCredit();
    unsubscribeNode();
  };
}

/**
 * 初始化应用
 */
export async function initializeApp() {
  await appStore.getState().initialize();
}

// ============================================================================
// 导出
// ============================================================================

export default appStore;
