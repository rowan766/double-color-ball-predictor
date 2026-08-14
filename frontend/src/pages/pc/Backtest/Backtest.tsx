import { Button, Card, Form, Input, InputNumber, Select, Table, Typography, message } from 'antd';
import { useEffect, useState } from 'react';
import { fetchLeaderboard, runBacktest } from '../../../services/backtestApi';
import type { BacktestMetric } from '../../../types/backtest';

const modelNameMap: Record<string, string> = {
  optimized_ensemble: '优化融合模型',
  random_baseline: '随机基线',
  statistical: '统计模型',
  logistic_regression: '逻辑回归',
  lightgbm: 'LightGBM 模型',
  xgboost: 'XGBoost 模型',
};

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
      const result = await runBacktest({ ...values, candidate_strategy: 'optimized' });
      setMetrics(result);
    } catch (error) {
      message.error(error instanceof Error ? error.message : '回测失败');
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="page">
      <Typography.Title level={3}>回测评估</Typography.Title>
      <Card>
        <Form layout="inline" onFinish={handleFinish}>
          <Form.Item name="name" initialValue="V1 回测" label="名称">
            <Input />
          </Form.Item>
          <Form.Item name="start_issue_no" rules={[{ required: true }]} label="开始期号">
            <Input placeholder="2024001" />
          </Form.Item>
          <Form.Item name="end_issue_no" rules={[{ required: true }]} label="结束期号">
            <Input placeholder="2024050" />
          </Form.Item>
          <Form.Item name="initial_train_size" initialValue={100} label="初始训练期数">
            <InputNumber min={5} />
          </Form.Item>
          <Form.Item name="model_keys" initialValue={['optimized_ensemble', 'statistical']} label="模型">
            <Select
              mode="multiple"
              style={{ minWidth: 280 }}
              options={[
                { value: 'optimized_ensemble', label: '优化融合模型' },
                { value: 'random_baseline', label: '随机基线' },
                { value: 'statistical', label: '统计模型' },
                { value: 'logistic_regression', label: '逻辑回归' },
                { value: 'lightgbm', label: 'LightGBM 模型' },
                { value: 'xgboost', label: 'XGBoost 模型' },
              ]}
            />
          </Form.Item>
          <Button type="primary" htmlType="submit" loading={loading}>
            运行回测
          </Button>
        </Form>
      </Card>
      <Card title="模型排行榜" className="result-stack">
        <Table
          rowKey={(row) => `${row.model_key}-${row.backtest_run_id ?? 'latest'}`}
          dataSource={metrics}
          columns={[
            {
              title: '模型',
              dataIndex: 'model_key',
              render: (value: string) => modelNameMap[value] ?? value,
            },
            { title: '预测期数', dataIndex: 'total_predictions' },
            { title: '平均红球命中', dataIndex: 'avg_red_hits', render: (v: number) => v.toFixed(3) },
            { title: '蓝球命中率', dataIndex: 'blue_hit_rate', render: (v: number) => `${(v * 100).toFixed(2)}%` },
            { title: '评分', dataIndex: 'ranking_score', render: (v: number) => v.toFixed(3) },
          ]}
        />
      </Card>
    </div>
  );
}
