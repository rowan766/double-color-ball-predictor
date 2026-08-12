export interface FrequencyItem {
  number: number;
  count: number;
  frequency: number;
}

export interface AnalysisSummary {
  total_draws: number;
  red_frequency: FrequencyItem[];
  blue_frequency: FrequencyItem[];
}
