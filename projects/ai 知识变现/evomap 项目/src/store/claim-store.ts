/**
 * Claim Store - 管理任务 Claim 状态
 * 
 * ✅ 使用柯里化调用：createStore<ClaimState>()((set, get) => ...)
 */

import { createStore } from 'zustand/vanilla';
import type { ClaimTask, ClaimStatus, ClaimHistory } from './types';

// ============================================================================
// Claim 状态
// ============================================================================

export interface ClaimState {
  // 任务列表
  availableTasks: ClaimTask[];
  claimedTasks: ClaimTask[];
  completedTasks: ClaimTask[];
  
  // 状态
  status: ClaimStatus;
  history: ClaimHistory[];
  
  // 加载状态
  isLoading: boolean;
  lastFetched: string | null;
  error: string | null;
  
  // 配置
  autoClaim: boolean;
  targetDailyClaim: number;
  
  // Actions
  fetchTasks: () => Promise<void>;
  claimTask: (taskId: string) => Promise<boolean>;
  completeTask: (taskId: string) => Promise<void>;
  updateStatus: (status: Partial<ClaimStatus>) => void;
  addToHistory: (entry: ClaimHistory) => void;
  setAutoClaim: (enabled: boolean) => void;
  setTargetDailyClaim: (target: number) => void;
  
  // 选择器
  getAvailableP0Tasks: () => ClaimTask[];
  getCompletionRate: () => number;
  getConsecutiveZeroDays: () => number;
  shouldClaimNow: () => boolean;
}

// ============================================================================
// 创建 Store - 使用柯里化调用 ✅
// ============================================================================

export const claimStore = createStore<ClaimState>()((set, get) => ({
  // Initial state
  availableTasks: [],
  claimedTasks: [],
  completedTasks: [],
  status: {
    todayClaimed: 0,
    todayCompleted: 0,
    completionRate: 1.0,
    consecutiveZeroDays: 0,
  },
  history: [],
  isLoading: false,
  lastFetched: null,
  error: null,
  autoClaim: true,
  targetDailyClaim: 2,
  
  // Actions
  fetchTasks: async () => {
    set({ isLoading: true, error: null });
    
    try {
      // 模拟 API 调用（实际项目中应该调用 EvoMap API）
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      // 模拟任务数据
      const mockTasks: ClaimTask[] = [
        {
          task_id: 'task_001',
          title: '抖音带货选品策略',
          signals: '抖音带货，选品策略，电商运营',
          bounty_amount: 243,
          min_reputation: 50,
          status: 'open',
        },
        {
          task_id: 'task_002',
          title: '直播间搭建指南',
          signals: '直播间，搭建，技术指南',
          bounty_amount: 187,
          min_reputation: 40,
          status: 'open',
        },
      ];
      
      set({
        availableTasks: mockTasks,
        isLoading: false,
        lastFetched: new Date().toISOString(),
      });
    } catch (error) {
      set({
        isLoading: false,
        error: error instanceof Error ? error.message : 'Failed to fetch tasks',
      });
    }
  },
  
  claimTask: async (taskId) => {
    const { availableTasks, claimedTasks } = get();
    const task = availableTasks.find(t => t.task_id === taskId);
    
    if (!task) return false;
    
    try {
      // 模拟 Claim API 调用
      await new Promise(resolve => setTimeout(resolve, 500));
      
      set({
        availableTasks: availableTasks.filter(t => t.task_id !== taskId),
        claimedTasks: [...claimedTasks, { ...task, status: 'claimed' }],
        status: {
          ...get().status,
          todayClaimed: get().status.todayClaimed + 1,
        },
      });
      
      return true;
    } catch (error) {
      return false;
    }
  },
  
  completeTask: async (taskId) => {
    const { claimedTasks, completedTasks, status } = get();
    const task = claimedTasks.find(t => t.task_id === taskId);
    
    if (!task) return;
    
    try {
      // 模拟完成 API 调用
      await new Promise(resolve => setTimeout(resolve, 500));
      
      const newCompleted = status.todayCompleted + 1;
      const newClaimed = status.todayClaimed;
      
      set({
        claimedTasks: claimedTasks.filter(t => t.task_id !== taskId),
        completedTasks: [...completedTasks, { ...task, status: 'completed' }],
        status: {
          ...status,
          todayCompleted: newCompleted,
          completionRate: newClaimed > 0 ? newCompleted / newClaimed : 1.0,
        },
      });
    } catch (error) {
      console.error('Failed to complete task:', error);
    }
  },
  
  updateStatus: (status) => set((state) => ({
    status: { ...state.status, ...status },
  })),
  
  addToHistory: (entry) => set((state) => ({
    history: [...state.history, entry].slice(-30), // 保留最近 30 天
  })),
  
  setAutoClaim: (autoClaim) => set({ autoClaim }),
  
  setTargetDailyClaim: (targetDailyClaim) => set({ targetDailyClaim }),
  
  // Selectors
  getAvailableP0Tasks: () => {
    const { availableTasks } = get();
    // 根据 signals 判断是否 P0 机会
    const p0Signals = ['抖音带货', '直播间搭建', '短视频爆款', '达人合作'];
    return availableTasks.filter(task =>
      p0Signals.some(signal => task.signals.includes(signal))
    );
  },
  
  getCompletionRate: () => get().status.completionRate,
  
  getConsecutiveZeroDays: () => get().status.consecutiveZeroDays,
  
  shouldClaimNow: () => {
    const { status, autoClaim, targetDailyClaim } = get();
    
    if (!autoClaim) return false;
    if (status.todayClaimed >= targetDailyClaim) return false;
    if (new Date().getHours() >= 20) return false; // 20:00 后不 Claim
    
    return true;
  },
}));

// ============================================================================
// 导出
// ============================================================================

export default claimStore;
