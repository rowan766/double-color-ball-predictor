import { http } from './http';
import type { ModelPrediction, PredictionRunRequest } from '../types/prediction';

export async function runPrediction(payload: PredictionRunRequest) {
  const response = await http.post<ModelPrediction[]>('/predictions/run', payload);
  return response.data;
}

export async function fetchLatestPredictions() {
  const response = await http.get<ModelPrediction[]>('/predictions/latest');
  return response.data;
}

export async function runAutoNextPrediction() {
  const response = await http.post<ModelPrediction[]>('/predictions/auto-next');
  return response.data;
}
