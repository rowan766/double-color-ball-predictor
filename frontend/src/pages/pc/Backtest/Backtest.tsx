import { Button, Card, Form, Input, InputNumber, Select, Table, Typography, message } from 'antd';
import { useEffect, useState } from 'react';
import { fetchLeaderboard, runBacktest } from '../../../services/backtestApi';
import type { BacktestMetric } from '../../../types/backtest';

export function Backtest() {
  const [metrics, setMetrics] = useState<BacktestMetric[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchLeaderboard().then(setMetrics).catch(() => setMetrics([]));
  }, []);

  async function handleFinish(values: {
    name: string;
    model_keys: string[];
    start_issue_no: string;
    end_issue_no: string;
    initial_train_size: number;
  }) {
    try {
      setLoading(true);
      const result = await runBacktest({ ...values, candidate_strategy: 'top_k' });
      setMetrics(result);
    } catch (error) {
      message.error(error instanceof Error ? error.message : 'Backtest failed');
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="page">
      <Typography.Title level={3}>Backtest</Typography.Title>
      <Card>
        <Form layout="inline" onFinish={handleFinish}>
          <Form.Item name="name" initialValue="V1 Backtest" label="Name">
            <Input />
          </Form.Item>
          <Form.Item name="start_issue_no" rules={[{ required: true }]} label="Start">
            <Input placeholder="2024001" />
          </Form.Item>
          <Form.Item name="end_issue_no" rules={[{ required: true }]} label="End">
            <Input placeholder="2024050" />
          </Form.Item>
          <Form.Item name="initial_train_size" initialValue={100} label="Train Size">
            <InputNumber min={5} />
          </Form.Item>
          <Form.Item name="model_keys" initialValue={['random_baseline', 'statistical']} label="Models">
            <Select
              mode="multiple"
              style={{ minWidth: 280 }}
              options={[
                { value: 'random_baseline', label: 'Random Baseline' },
                { value: 'statistical', label: 'Statistical' },
                { value: 'logistic_regression', label: 'Logistic Regression' },
                { value: 'lightgbm', label: 'LightGBM' },
                { value: 'xgboost', label: 'XGBoost' },
              ]}
            />
          </Form.Item>
          <Button type="primary" htmlType="submit" loading={loading}>
            Run
          </Button>
        </Form>
      </Card>
      <Card title="Leaderboard" className="result-stack">
        <Table
          rowKey={(row) => `${row.model_key}-${row.backtest_run_id ?? 'latest'}`}
          dataSource={metrics}
          columns={[
            { title: 'Model', dataIndex: 'model_key' },
            { title: 'Predictions', dataIndex: 'total_predictions' },
            { title: 'Avg Red Hits', dataIndex: 'avg_red_hits', render: (v: number) => v.toFixed(3) },
            { title: 'Blue Hit Rate', dataIndex: 'blue_hit_rate', render: (v: number) => `${(v * 100).toFixed(2)}%` },
            { title: 'Score', dataIndex: 'ranking_score', render: (v: number) => v.toFixed(3) },
          ]}
        />
      </Card>
    </div>
  );
}
