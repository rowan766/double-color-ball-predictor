import { useEffect, useState } from 'react';
import { fetchDraws } from '../services/drawApi';
import { useDrawStore } from '../stores/drawStore';

export function useDraws() {
  const { draws, setDraws } = useDrawStore();
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    setLoading(true);
    fetchDraws()
      .then(setDraws)
      .catch(() => setDraws([]))
      .finally(() => setLoading(false));
  }, [setDraws]);

  return { draws, loading };
}
