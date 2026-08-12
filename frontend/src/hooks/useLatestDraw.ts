import { useEffect, useState } from 'react';
import { fetchLatestDraw } from '../services/drawApi';
import type { LotteryDraw } from '../types/draw';

export function useLatestDraw() {
  const [draw, setDraw] = useState<LotteryDraw | null>(null);

  useEffect(() => {
    fetchLatestDraw().then(setDraw).catch(() => setDraw(null));
  }, []);

  return draw;
}
