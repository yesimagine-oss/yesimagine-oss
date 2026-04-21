/**
 * Credit Store - 管理积分余额和交易
 *
 * ✅ 使用柯里化调用：createStore<CreditState>()((set, get) => ...)
 */
import type { CreditTransaction } from './types';
export interface CreditState {
    balance: number;
    transactions: CreditTransaction[];
    isLoading: boolean;
    lastSynced: string | null;
    error: string | null;
    targetBalance: number;
    fetchBalance: () => Promise<void>;
    addTransaction: (transaction: Omit<CreditTransaction, 'id' | 'balance_after'>) => void;
    setBalance: (balance: number) => void;
    setTargetBalance: (target: number) => void;
    getTotalEarned: () => number;
    getTotalSpent: () => number;
    getRecentTransactions: (limit?: number) => CreditTransaction[];
    getTransactionsByType: (type: 'earn' | 'spend') => CreditTransaction[];
    getAverageDailyEarn: () => number;
    canAfford: (amount: number) => boolean;
}
export declare const creditStore: import("zustand/vanilla").StoreApi<CreditState>;
export default creditStore;
//# sourceMappingURL=credit-store.d.ts.map