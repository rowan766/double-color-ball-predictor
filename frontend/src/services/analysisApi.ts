import { http } from './http';
import type { AnalysisSummary } from '../types/analysis';

export async function fetchAnalysisSummary() {
  const response = await http.get<AnalysisSummary>('/analysis/summary');
  return response.data;
}

export async function fetchHotCold() {
  const response = await http.get('/analysis/hot-cold');
  return response.data;
}

export async function fetchOmission() {
  const response = await http.get('/analysis/omission');
  return response.data;
}
