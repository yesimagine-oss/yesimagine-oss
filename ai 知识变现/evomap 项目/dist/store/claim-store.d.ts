/**
 * Claim Store - 管理任务 Claim 状态
 *
 * ✅ 使用柯里化调用：createStore<ClaimState>()((set, get) => ...)
 */
import type { ClaimTask, ClaimStatus, ClaimHistory } from './types';
export interface ClaimState {
    availableTasks: ClaimTask[];
    claimedTasks: ClaimTask[];
    completedTasks: ClaimTask[];
    status: ClaimStatus;
    history: ClaimHistory[];
    isLoading: boolean;
    lastFetched: string | null;
    error: string | null;
    autoClaim: boolean;
    targetDailyClaim: number;
    fetchTasks: () => Promise<void>;
    claimTask: (taskId: string) => Promise<boolean>;
    completeTask: (taskId: string) => Promise<void>;
    updateStatus: (status: Partial<ClaimStatus>) => void;
    addToHistory: (entry: ClaimHistory) => void;
    setAutoClaim: (enabled: boolean) => void;
    setTargetDailyClaim: (target: number) => void;
    getAvailableP0Tasks: () => ClaimTask[];
    getCompletionRate: () => number;
    getConsecutiveZeroDays: () => number;
    shouldClaimNow: () => boolean;
}
export declare const claimStore: import("zustand/vanilla").StoreApi<ClaimState>;
export default claimStore;
//# sourceMappingURL=claim-store.d.ts.map