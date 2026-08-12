export interface CandidateNumbers {
  red_numbers: number[];
  blue_number: number;
  score?: number;
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
  red_probabilities: Record<number, number>;
  blue_probabilities: Record<number, number>;
  candidate_numbers: CandidateNumbers[];
}
