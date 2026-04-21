/**
 * Credit Store - 管理积分余额和交易
 *
 * ✅ 使用柯里化调用：createStore<CreditState>()((set, get) => ...)
 */
import { createStore } from 'zustand/vanilla';
// ============================================================================
// 创建 Store - 使用柯里化调用 ✅
// ============================================================================
export const creditStore = createStore()((set, get) => ({
    // Initial state
    balance: 0,
    transactions: [],
    isLoading: false,
    lastSynced: null,
    error: null,
    targetBalance: 10000,
    // Actions
    fetchBalance: async () => {
        set({ isLoading: true, error: null });
        try {
            // 模拟 API 调用（实际项目中应该调用 EvoMap Heartbeat API）
            await new Promise(resolve => setTimeout(resolve, 1000));
            // 模拟余额数据
            const mockBalance = 150;
            set({
                balance: mockBalance,
                isLoading: false,
                lastSynced: new Date().toISOString(),
            });
        }
        catch (error) {
            set({
                isLoading: false,
                error: error instanceof Error ? error.message : 'Failed to fetch balance',
            });
        }
    },
    addTransaction: (transaction) => set((state) => {
        const newBalance = transaction.type === 'earn'
            ? state.balance + transaction.amount
            : state.balance - transaction.amount;
        const newTransaction = {
            ...transaction,
            id: `txn_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
            balance_after: newBalance,
        };
        return {
            balance: newBalance,
            transactions: [newTransaction, ...state.transactions].slice(0, 100), // 保留最近 100 条
        };
    }),
    setBalance: (balance) => set({ balance }),
    setTargetBalance: (targetBalance) => set({ targetBalance }),
    // Selectors
    getTotalEarned: () => {
        const { transactions } = get();
        return transactions
            .filter(t => t.type === 'earn')
            .reduce((sum, t) => sum + t.amount, 0);
    },
    getTotalSpent: () => {
        const { transactions } = get();
        return transactions
            .filter(t => t.type === 'spend')
            .reduce((sum, t) => sum + t.amount, 0);
    },
    getRecentTransactions: (limit = 10) => {
        const { transactions } = get();
        return transactions.slice(0, limit);
    },
    getTransactionsByType: (type) => {
        const { transactions } = get();
        return transactions.filter(t => t.type === type);
    },
    getAverageDailyEarn: () => {
        const { transactions } = get();
        const earnTransactions = transactions.filter(t => t.type === 'earn');
        if (earnTransactions.length === 0)
            return 0;
        // 计算第一笔和最后一笔交易的时间差
        const firstTx = earnTransactions[earnTransactions.length - 1];
        const lastTx = earnTransactions[0];
        if (!firstTx || !lastTx)
            return 0;
        const firstDate = new Date(firstTx.timestamp);
        const lastDate = new Date(lastTx.timestamp);
        const daysDiff = Math.max(1, Math.ceil((lastDate.getTime() - firstDate.getTime()) / (1000 * 60 * 60 * 24)));
        const totalEarned = earnTransactions.reduce((sum, t) => sum + t.amount, 0);
        return totalEarned / daysDiff;
    },
    canAfford: (amount) => {
        const { balance } = get();
        return balance >= amount;
    },
}));
// ============================================================================
// 导出
// ============================================================================
export default creditStore;
//# sourceMappingURL=credit-store.js.map