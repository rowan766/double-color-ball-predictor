export interface CandidateNumbers {
  red_numbers: number[];
  blue_number: number;
  score?: number;
  red_hit_count?: number | null;
  blue_hit?: boolean | null;
  prize_level?: string | null;
}

export interface PredictionRunRequest {
  target_issue_no: string;
  train_until_issue_no: string;
  model_keys?: string[];
  candidate_strategy?: string;
  candidate_count?: number;
}

export interface ModelPrediction {
  model_key: string;
  target_issue_no: string;
  train_until_issue_no: string;
  draw_datetime?: string | null;
  red_probabilities: Record<number, number>;
  blue_probabilities: Record<number, number>;
  candidate_numbers: CandidateNumbers[];
  prediction_run_id?: number | null;
  run_type?: string | null;
  best_red_hit_count?: number | null;
  best_blue_hit?: boolean | null;
  evaluated_at?: string | null;
}
