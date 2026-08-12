import { create } from 'zustand';

interface AppState {
  device: 'pc' | 'h5';
  setDevice: (device: 'pc' | 'h5') => void;
}

export const useAppStore = create<AppState>((set) => ({
  device: 'pc',
  setDevice: (device) => set({ device }),
}));
