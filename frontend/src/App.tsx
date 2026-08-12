import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom';
import { PcLayout } from './layouts/pc/PcLayout';
import { Dashboard } from './pages/pc/Dashboard/Dashboard';
import { DrawHistory } from './pages/pc/DrawHistory/DrawHistory';
import { Analysis } from './pages/pc/Analysis/Analysis';
import { Prediction } from './pages/pc/Prediction/Prediction';
import { Backtest } from './pages/pc/Backtest/Backtest';

export function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<PcLayout />}>
          <Route path="/" element={<Navigate to="/dashboard" replace />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/draws" element={<DrawHistory />} />
          <Route path="/analysis" element={<Analysis />} />
          <Route path="/prediction" element={<Prediction />} />
          <Route path="/backtest" element={<Backtest />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}
