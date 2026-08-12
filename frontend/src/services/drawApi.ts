import { http } from './http';
import type { LotteryDraw, LotteryDrawImportRequest, LotteryDrawImportResult } from '../types/draw';

export async function fetchDraws() {
  const response = await http.get<LotteryDraw[]>('/draws');
  return response.data;
}

export async function fetchLatestDraw() {
  const response = await http.get<LotteryDraw>('/draws/latest');
  return response.data;
}

export async function importDraws(payload: LotteryDrawImportRequest) {
  const response = await http.post<LotteryDrawImportResult>('/draws/import', payload);
  return response.data;
}
