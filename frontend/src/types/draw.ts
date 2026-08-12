export interface LotteryDraw {
  id: number;
  issue_no: string;
  draw_date: string;
  red_numbers: number[];
  blue_number: number;
  red_sum?: number;
  red_span?: number;
  source?: string;
}

export interface LotteryDrawCreate {
  issue_no: string;
  draw_date: string;
  red_numbers: number[];
  blue_number: number;
  source?: string;
}

export interface LotteryDrawImportRequest {
  draws: LotteryDrawCreate[];
  overwrite: boolean;
}

export interface LotteryDrawImportResult {
  imported_count: number;
  created_count: number;
  updated_count: number;
  skipped_count: number;
  latest_issue_no?: string | null;
}
