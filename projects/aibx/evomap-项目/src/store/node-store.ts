/**
 * Node Store - 管理节点健康状态
 * 
 * ✅ 使用柯里化调用：createStore<NodeState>()((set, get) => ...)
 */

import { createStore } from 'zustand/vanilla';
import type { NodeHealth } from './types';

// ============================================================================
// Node 状态
// ============================================================================

export interface NodeState {
  // 节点信息
  nodeId: string;
  hubNodeId: string | null;
  ownerUserId: string | null;
  
  // 健康状态
  health: NodeHealth;
  
  // 统计
  totalHeartbeats: number;
  failedHeartbeats: number;
  lastHeartbeatResponse: any | null;
  
  // 加载状态
  isChecking: boolean;
  lastChecked: string | null;
  error: string | null;
  
  // 配置
  heartbeatInterval: number; // milliseconds
  autoReconnect: boolean;
  
  // Actions
  checkHealth: () => Promise<void>;
  updateHealth: (health: Partial<NodeHealth>) => void;
  setNodeInfo: (info: { nodeId: string; hubNodeId?: string; ownerUserId?: string }) => void;
  recordHeartbeat: (success: boolean, response?: any) => void;
  setHeartbeatInterval: (interval: number) => void;
  setAutoReconnect: (enabled: boolean) => void;
  
  // 选择器
  isOnline: () => boolean;
  getUptime: () => number;
  getSuccessRate: () => number;
  shouldReconnect: () => boolean;
  getStatusColor: () => string;
}

// ============================================================================
// 创建 Store - 使用柯里化调用 ✅
// ============================================================================

export const nodeStore = createStore<NodeState>()((set, get) => ({
  // Initial state
  nodeId: 'node_67c3b8b37becd262',
  hubNodeId: null,
  ownerUserId: null,
  health: {
    status: 'unknown',
    lastHeartbeat: null,
    survivalStatus: 'unknown',
    uptime: 0,
  },
  totalHeartbeats: 0,
  failedHeartbeats: 0,
  lastHeartbeatResponse: null,
  isChecking: false,
  lastChecked: null,
  error: null,
  heartbeatInterval: 900000, // 15 minutes
  autoReconnect: true,
  
  // Actions
  checkHealth: async () => {
    set({ isChecking: true, error: null });
    
    try {
      // 模拟 Heartbeat API 调用
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      // 模拟响应
      const mockResponse = {
        status: 'ok',
        survival_status: 'alive',
        credit_balance: 150,
        next_heartbeat_ms: 900000,
      };
      
      set({
        health: {
          status: 'online',
          lastHeartbeat: new Date().toISOString(),
          survivalStatus: 'alive',
          uptime: get().health.uptime + 1,
        },
        isChecking: false,
        lastChecked: new Date().toISOString(),
        lastHeartbeatResponse: mockResponse,
        hubNodeId: (mockResponse as any).hub_node_id || 'hub_0f978bbe1fb5',
        heartbeatInterval: mockResponse.next_heartbeat_ms,
      });
    } catch (error) {
      set({
        health: {
          ...get().health,
          status: 'error',
        },
        isChecking: false,
        error: error instanceof Error ? error.message : 'Health check failed',
        failedHeartbeats: get().failedHeartbeats + 1,
      });
    }
  },
  
  updateHealth: (health) => set((state) => ({
    health: { ...state.health, ...health },
  })),
  
  setNodeInfo: (info) => set((state) => ({
    nodeId: info.nodeId || state.nodeId,
    hubNodeId: info.hubNodeId || state.hubNodeId,
    ownerUserId: info.ownerUserId || state.ownerUserId,
  })),
  
  recordHeartbeat: (success, response) => set((state) => ({
    totalHeartbeats: state.totalHeartbeats + 1,
    failedHeartbeats: success ? state.failedHeartbeats : state.failedHeartbeats + 1,
    lastHeartbeatResponse: response || null,
    health: {
      ...state.health,
      status: success ? 'online' : 'offline',
      lastHeartbeat: new Date().toISOString(),
      survivalStatus: success ? 'alive' : 'offline',
    },
  })),
  
  setHeartbeatInterval: (heartbeatInterval) => set({ heartbeatInterval }),
  
  setAutoReconnect: (autoReconnect) => set({ autoReconnect }),
  
  // Selectors
  isOnline: () => {
    const { health } = get();
    return health.status === 'online' || health.survivalStatus === 'alive';
  },
  
  getUptime: () => get().health.uptime,
  
  getSuccessRate: () => {
    const { totalHeartbeats, failedHeartbeats } = get();
    if (totalHeartbeats === 0) return 1.0;
    return (totalHeartbeats - failedHeartbeats) / totalHeartbeats;
  },
  
  shouldReconnect: () => {
    const { health, autoReconnect } = get();
    return autoReconnect && (health.status === 'offline' || health.status === 'error');
  },
  
  getStatusColor: () => {
    const { health } = get();
    switch (health.status) {
      case 'online':
        return 'green';
      case 'offline':
        return 'red';
      case 'error':
        return 'orange';
      default:
        return 'gray';
    }
  },
}));

// ============================================================================
// 导出
// ============================================================================

export default nodeStore;
