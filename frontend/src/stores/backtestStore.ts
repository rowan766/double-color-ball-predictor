import { create } from 'zustand';
import type { BacktestMetric } from '../types/backtest';

interface BacktestState {
  metrics: BacktestMetric[];
  setMetrics: (metrics: BacktestMetric[]) => void;
}

export const useBacktestStore = create<BacktestState>((set) => ({
  metrics: [],
  setMetrics: (metrics) => set({ metrics }),
}));
