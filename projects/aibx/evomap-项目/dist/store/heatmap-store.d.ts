/**
 * Heatmap Store - 管理 Topic Heatmap 数据
 *
 * ✅ 使用柯里化调用：createStore<HeatmapState>()((set, get) => ...)
 */
import type { HeatmapData, HeatmapTopic, HeatmapSaturated, HeatmapOpportunity } from './types';
export interface HeatmapState {
    data: HeatmapData | null;
    isLoading: boolean;
    lastUpdated: string | null;
    error: string | null;
    filterPriority: 'all' | 'P0' | 'P1' | 'P2';
    filterType: 'all' | 'recommended' | 'saturated' | 'opportunity';
    fetchData: () => Promise<void>;
    setData: (data: HeatmapData) => void;
    setLoading: (loading: boolean) => void;
    setError: (error: string | null) => void;
    setFilterPriority: (priority: HeatmapState['filterPriority']) => void;
    setFilterType: (type: HeatmapState['filterType']) => void;
    getRecommendedTopics: () => HeatmapTopic[];
    getHighCompetitionTopics: () => HeatmapSaturated[];
    getOpportunitySignals: () => HeatmapOpportunity[];
    getP0Opportunities: () => HeatmapTopic[];
    shouldAvoidTopic: (topic: string) => boolean;
}
export declare const heatmapStore: import("zustand/vanilla").StoreApi<HeatmapState>;
export default heatmapStore;
//# sourceMappingURL=heatmap-store.d.ts.map