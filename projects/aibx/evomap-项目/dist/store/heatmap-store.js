/**
 * Heatmap Store - 管理 Topic Heatmap 数据
 *
 * ✅ 使用柯里化调用：createStore<HeatmapState>()((set, get) => ...)
 */
import { createStore } from 'zustand/vanilla';
// ============================================================================
// 创建 Store - 使用柯里化调用 ✅
// ============================================================================
export const heatmapStore = createStore()((set, get) => ({
    // Initial state
    data: null,
    isLoading: false,
    lastUpdated: null,
    error: null,
    filterPriority: 'all',
    filterType: 'all',
    // Actions
    fetchData: async () => {
        set({ isLoading: true, error: null });
        try {
            // 从本地文件加载（实际项目中应该从 API 获取）
            const response = await fetch('/logs/heatmap-latest.json');
            if (!response.ok)
                throw new Error('Failed to fetch heatmap data');
            const data = await response.json();
            set({
                data,
                isLoading: false,
                lastUpdated: new Date().toISOString(),
            });
        }
        catch (error) {
            set({
                isLoading: false,
                error: error instanceof Error ? error.message : 'Unknown error',
            });
        }
    },
    setData: (data) => set({ data, lastUpdated: new Date().toISOString() }),
    setLoading: (isLoading) => set({ isLoading }),
    setError: (error) => set({ error }),
    setFilterPriority: (filterPriority) => set({ filterPriority }),
    setFilterType: (filterType) => set({ filterType }),
    // Selectors
    getRecommendedTopics: () => {
        const { data, filterPriority } = get();
        if (!data)
            return [];
        let topics = data.recommended;
        if (filterPriority !== 'all') {
            topics = topics.filter(t => t.priority === filterPriority);
        }
        return topics;
    },
    getHighCompetitionTopics: () => {
        const { data } = get();
        return data?.topSaturated || [];
    },
    getOpportunitySignals: () => {
        const { data } = get();
        return data?.opportunitySignals || [];
    },
    getP0Opportunities: () => {
        const { data } = get();
        return data?.recommended.filter(t => t.priority === 'P0') || [];
    },
    shouldAvoidTopic: (topic) => {
        const { data } = get();
        if (!data)
            return false;
        const avoidTopics = ['memory_growth', 'postgresql_perf', 'v8_profiler', 'silent_renew', 'react_perf'];
        return avoidTopics.some(avoid => topic.toLowerCase().includes(avoid.toLowerCase()));
    },
}));
// ============================================================================
// 导出
// ============================================================================
export default heatmapStore;
//# sourceMappingURL=heatmap-store.js.map