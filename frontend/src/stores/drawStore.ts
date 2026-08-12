import { create } from 'zustand';
import type { LotteryDraw } from '../types/draw';

interface DrawState {
  draws: LotteryDraw[];
  setDraws: (draws: LotteryDraw[]) => void;
}

export const useDrawStore = create<DrawState>((set) => ({
  draws: [],
  setDraws: (draws) => set({ draws }),
}));
