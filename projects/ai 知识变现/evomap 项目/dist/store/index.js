/**
 * EvoMap Store - 状态管理导出
 *
 * ✅ 所有 Store 都使用柯里化调用：createStore<Type>()((set) => ...)
 */
// Types
export * from './types';
// Individual Stores
export { default as heatmapStore } from './heatmap-store';
export { default as claimStore } from './claim-store';
export { default as creditStore } from './credit-store';
export { default as nodeStore } from './node-store';
// App Store (组合所有 Store)
export { default as appStore, subscribeToAllStores, initializeApp, } from './app-store';
// ============================================================================
// 使用示例
// ============================================================================
/*
// 1. 导入 Store
import { appStore, heatmapStore, claimStore, creditStore, nodeStore } from './store';

// 2. 初始化应用
await initializeApp();

// 3. 访问状态
const heatmapData = heatmapStore.getState().data;
const claimStatus = claimStore.getState().status;
const creditBalance = creditStore.getState().balance;
const nodeStatus = nodeStore.getState().health.status;

// 4. 调用 Actions
heatmapStore.getState().fetchData();
claimStore.getState().claimTask('task_001');
creditStore.getState().addTransaction({ type: 'earn', amount: 100, description: 'Task completed' });
nodeStore.getState().checkHealth();

// 5. 订阅状态变化
const unsubscribe = heatmapStore.subscribe((state) => {
  console.log('Heatmap data changed:', state.data);
});

// 6. 使用选择器
const p0Opportunities = heatmapStore.getState().getP0Opportunities();
const completionRate = claimStore.getState().getCompletionRate();
const isOnline = nodeStore.getState().isOnline();

// 7. 使用 App Store（组合所有 Store）
appStore.getState().syncAllStores();
const report = appStore.getState().supervisorReport;

// 8. 订阅所有 Store 的变化
const unsubscribeAll = subscribeToAllStores((state) => {
  console.log('Any store changed:', state);
});
*/
// ============================================================================
// React Hooks（如果使用 React）
// ============================================================================
/*
// 需要安装：npm install zustand

import { useStore } from 'zustand';

// Heatmap Hook
export function useHeatmap() {
  return useStore(heatmapStore);
}

// Claim Hook
export function useClaim() {
  return useStore(claimStore);
}

// Credit Hook
export function useCredit() {
  return useStore(creditStore);
}

// Node Hook
export function useNode() {
  return useStore(nodeStore);
}

// 使用示例：
function HeatmapComponent() {
  const { data, isLoading, fetchData, getP0Opportunities } = useHeatmap();
  
  useEffect(() => {
    fetchData();
  }, []);
  
  const p0Topics = getP0Opportunities();
  
  return (
    <div>
      {isLoading ? 'Loading...' : JSON.stringify(data)}
      {p0Topics.map(topic => (
        <div key={topic.topic}>{topic.topic}</div>
      ))}
    </div>
  );
}
*/
//# sourceMappingURL=index.js.map