import { create } from 'zustand';
import type { ModelPrediction } from '../types/prediction';

interface PredictionState {
  predictions: ModelPrediction[];
  setPredictions: (predictions: ModelPrediction[]) => void;
}

export const usePredictionStore = create<PredictionState>((set) => ({
  predictions: [],
  setPredictions: (predictions) => set({ predictions }),
}));
