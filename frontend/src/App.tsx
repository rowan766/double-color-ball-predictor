import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom';
import { PcLayout } from './layouts/pc/PcLayout';
import { Analysis } from './pages/pc/Analysis/Analysis';
import { Overview } from './pages/pc/Overview/Overview';
import { PredictionReview } from './pages/pc/PredictionReview/PredictionReview';

export function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<PcLayout />}>
          <Route path="/" element={<Navigate to="/prediction" replace />} />
          <Route path="/overview" element={<Overview />} />
          <Route path="/dashboard" element={<Navigate to="/overview" replace />} />
          <Route path="/draws" element={<Navigate to="/overview" replace />} />
          <Route path="/analysis" element={<Analysis />} />
          <Route path="/prediction" element={<PredictionReview />} />
          <Route path="/backtest" element={<Navigate to="/prediction" replace />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}
