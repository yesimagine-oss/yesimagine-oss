/**
 * App Store - 组合所有 Store 的主 Store
 *
 * ✅ 使用柯里化调用：createStore<AppState>()((set, get) => ...)
 */
import { heatmapStore } from './heatmap-store';
import { claimStore } from './claim-store';
import { creditStore } from './credit-store';
import { nodeStore } from './node-store';
import type { SupervisorReport, AnalysisResult } from './types';
export interface AppState {
    supervisorReport: SupervisorReport | null;
    analysisResult: AnalysisResult | null;
    isInitializing: boolean;
    lastSynced: string | null;
    initialize: () => Promise<void>;
    syncAllStores: () => Promise<void>;
    generateSupervisorReport: () => SupervisorReport;
    getHeatmapStore: () => typeof heatmapStore;
    getClaimStore: () => typeof claimStore;
    getCreditStore: () => typeof creditStore;
    getNodeStore: () => typeof nodeStore;
}
export declare const appStore: import("zustand/vanilla").StoreApi<AppState>;
/**
 * 订阅所有 Store 的变化
 */
export declare function subscribeToAllStores(callback: (state: AppState) => void): () => void;
/**
 * 初始化应用
 */
export declare function initializeApp(): Promise<void>;
export default appStore;
//# sourceMappingURL=app-store.d.ts.map