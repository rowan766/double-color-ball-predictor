import { http } from './http';
import type { BacktestMetric, BacktestRunRequest } from '../types/backtest';

export async function runBacktest(payload: BacktestRunRequest) {
  const response = await http.post<BacktestMetric[]>('/backtests/run', payload);
  return response.data;
}

export async function fetchLeaderboard() {
  const response = await http.get<BacktestMetric[]>('/backtests/leaderboard');
  return response.data;
}
