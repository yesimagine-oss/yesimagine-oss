/**
 * EvoMap 状态管理 - 类型定义
 */
export interface HeatmapTopic {
    topic: string;
    status: string;
    priority: 'P0' | 'P1' | 'P2';
}
export interface HeatmapSaturated {
    signal: string;
    assets: number;
    density: number;
    action: 'avoid' | 'caution' | 'recommended';
}
export interface HeatmapOpportunity {
    signal: string;
    density: number;
    action: string;
}
export interface HeatmapData {
    timestamp: string;
    totalSignals: number;
    hotCount: number;
    warmCount: number;
    coldCount: number;
    recommended: HeatmapTopic[];
    topSaturated: HeatmapSaturated[];
    opportunitySignals: HeatmapOpportunity[];
}
export interface ClaimTask {
    task_id: string;
    title: string;
    signals: string;
    bounty_amount: number;
    min_reputation: number;
    status: 'open' | 'claimed' | 'completed';
}
export interface ClaimStatus {
    todayClaimed: number;
    todayCompleted: number;
    completionRate: number;
    consecutiveZeroDays: number;
}
export interface ClaimHistory {
    date: string;
    claimed_count: number;
    completed_count: number;
    failed_count: number;
}
export interface CreditTransaction {
    id: string;
    type: 'earn' | 'spend';
    amount: number;
    description: string;
    timestamp: string;
    balance_after: number;
}
export type NodeStatus = 'online' | 'offline' | 'unknown' | 'error';
export interface NodeHealth {
    status: NodeStatus;
    lastHeartbeat: string | null;
    survivalStatus: 'alive' | 'offline' | 'unknown';
    uptime: number;
}
export type AssetType = 'Gene' | 'Capsule' | 'EvolutionEvent';
export type AssetStatus = 'candidate' | 'promoted' | 'rejected' | 'published';
export interface PublishedAsset {
    id: string;
    type: AssetType;
    asset_id: string;
    summary: string;
    status: AssetStatus;
    publishedAt: string;
    gdiScore?: number;
    useCount?: number;
}
export interface SupervisorReport {
    timestamp: string;
    nodeHealth: NodeHealth;
    claimStatus: ClaimStatus;
    creditBalance: number;
    heatmapOpportunities: number;
    publishedAssets: number;
}
export interface AnalysisResult {
    timestamp: string;
    claimStats: {
        totalAttempts: number;
        successes: number;
        successRate: number;
    };
    heatmapStats: {
        historyDays: number;
        coldDiscoveries: number;
        p0Topics: Record<string, number>;
    };
    revenueStats: {
        daysWithData: number;
        avg7d: number;
        avg30d: number;
        trend: 'up' | 'down' | 'stable';
    };
    suggestions: Array<{
        category: string;
        priority: 'high' | 'medium' | 'low';
        issue: string;
        suggestion: string;
    }>;
}
//# sourceMappingURL=types.d.ts.map