export interface BacktestRunRequest {
  name: string;
  model_keys: string[];
  start_issue_no: string;
  end_issue_no: string;
  initial_train_size: number;
  candidate_strategy: string;
}

export interface BacktestMetric {
  model_key: string;
  backtest_run_id?: number | null;
  total_predictions: number;
  avg_red_hits: number;
  blue_hit_rate: number;
  red_hit_distribution: Record<string, number>;
  prize_distribution: Record<string, number>;
  random_baseline_diff?: Record<string, number>;
  ranking_score: number;
}
