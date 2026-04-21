/**
 * Node Store - 管理节点健康状态
 *
 * ✅ 使用柯里化调用：createStore<NodeState>()((set, get) => ...)
 */
import type { NodeHealth } from './types';
export interface NodeState {
    nodeId: string;
    hubNodeId: string | null;
    ownerUserId: string | null;
    health: NodeHealth;
    totalHeartbeats: number;
    failedHeartbeats: number;
    lastHeartbeatResponse: any | null;
    isChecking: boolean;
    lastChecked: string | null;
    error: string | null;
    heartbeatInterval: number;
    autoReconnect: boolean;
    checkHealth: () => Promise<void>;
    updateHealth: (health: Partial<NodeHealth>) => void;
    setNodeInfo: (info: {
        nodeId: string;
        hubNodeId?: string;
        ownerUserId?: string;
    }) => void;
    recordHeartbeat: (success: boolean, response?: any) => void;
    setHeartbeatInterval: (interval: number) => void;
    setAutoReconnect: (enabled: boolean) => void;
    isOnline: () => boolean;
    getUptime: () => number;
    getSuccessRate: () => number;
    shouldReconnect: () => boolean;
    getStatusColor: () => string;
}
export declare const nodeStore: import("zustand/vanilla").StoreApi<NodeState>;
export default nodeStore;
//# sourceMappingURL=node-store.d.ts.map