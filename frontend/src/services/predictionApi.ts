import { http } from './http';
import type { ModelPrediction, PredictionRunRequest } from '../types/prediction';

export async function runPrediction(payload: PredictionRunRequest) {
  const response = await http.post<ModelPrediction[]>('/predictions/run', payload);
  return response.data;
}
