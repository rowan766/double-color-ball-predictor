import { http } from './http';

export interface DashboardPayload {
  latest_draw: unknown | null;
  total_draws: number;
  latest_predictions: unknown[];
  model_leaderboard: unknown[];
  recent_backtest_metrics: unknown[];
  red_probability_chart: unknown[];
  blue_probability_chart: unknown[];
}

export async function fetchDashboard() {
  const response = await http.get<DashboardPayload>('/dashboard');
  return response.data;
}
