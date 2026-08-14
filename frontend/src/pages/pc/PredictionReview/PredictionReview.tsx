import { Button, Card, Form, Input, InputNumber, Select, Space, Table, Tabs, Typography, message } from 'antd';
import { useEffect, useState } from 'react';
import { fetchLeaderboard, runBacktest } from '../../../services/backtestApi';
import { fetchLatestPredictions, runAutoNextPrediction } from '../../../services/predictionApi';
import type { BacktestMetric } from '../../../types/backtest';
import type { ModelPrediction } from '../../../types/prediction';

const modelNameMap: Record<string, string> = {
  random_baseline: '随机基线',
  statistical: '统计模型',
  logistic_regression: '逻辑回归',
  lightgbm: 'LightGBM 模型',
  xgboost: 'XGBoost 模型',
};

const modelOptions = [
  { value: 'statistical', label: '统计模型' },
  { value: 'lightgbm', label: 'LightGBM 模型' },
  { value: 'xgboost', label: 'XGBoost 模型' },
  { value: 'random_baseline', label: '随机基线' },
  { value: 'logistic_regression', label: '逻辑回归' },
];

export function PredictionReview() {
  const [predictionForm] = Form.useForm();
  const [predictions, setPredictions] = useState<ModelPrediction[]>([]);
  const [metrics, setMetrics] = useState<BacktestMetric[]>([]);
  const [predicting, setPredicting] = useState(false);
  const [backtesting, setBacktesting] = useState(false);

  useEffect(() => {
    fetchLeaderboard().then(setMetrics).catch(() => setMetrics([]));
    fetchLatestPredictions().then(setPredictions).catch(() => setPredictions([]));
  }, []);

  async function handlePrediction() {
    try {
      setPredicting(true);
      const result = await runAutoNextPrediction();
      if (result.length > 0) {
        setPredictions(result);
        message.success('已生成最新待开奖预测');
      } else {
        const latest = await fetchLatestPredictions();
        setPredictions(latest);
        message.info('最新待开奖预测已存在');
      }
    } catch (error) {
      message.error(error instanceof Error ? error.message : '预测失败');
    } finally {
      setPredicting(false);
    }
  }

  async function handleBacktest(values: {
    name: string;
    model_keys: string[];
    start_issue_no: string;
    end_issue_no: string;
    initial_train_size: number;
  }) {
    try {
      setBacktesting(true);
      const result = await runBacktest({ ...values, candidate_strategy: 'top_k' });
      setMetrics(result);
    } catch (error) {
      message.error(error instanceof Error ? error.message : '回测失败');
    } finally {
      setBacktesting(false);
    }
  }

  return (
    <div className="page compact-page">
      <Typography.Title level={4} className="page-title">
        预测评估
      </Typography.Title>
      <Tabs
        items={[
          {
            key: 'prediction',
            label: '预测结果',
            children: (
              <>
                <Card className="action-card">
                  <Form form={predictionForm} layout="inline" onFinish={handlePrediction}>
                    <Button type="primary" htmlType="submit" loading={predicting}>
                      生成最新待开奖预测
                    </Button>
                  </Form>
                </Card>
                <Space direction="vertical" size={16} className="result-stack">
                  {predictions.map((prediction) => (
                    <Card
                      key={`${prediction.prediction_run_id}-${prediction.model_key}`}
                      className="prediction-card"
                      title={
                        <Space size={16} wrap>
                          <span>{modelNameMap[prediction.model_key] ?? prediction.model_key}</span>
                          <Typography.Text type="secondary">开奖时间：{prediction.draw_datetime ?? '-'}</Typography.Text>
                        </Space>
                      }
                    >
                      <Table
                        size="small"
                        rowKey={(row) => `${row.red_numbers.join('-')}-${row.blue_number}`}
                        pagination={false}
                        dataSource={prediction.candidate_numbers}
                        scroll={{ x: 760 }}
                        columns={[
                          { title: '红球', dataIndex: 'red_numbers', render: (v: number[]) => v.join(', ') },
                          { title: '蓝球', dataIndex: 'blue_number' },
                          { title: '评分', dataIndex: 'score', render: (v: number) => v?.toFixed(4) },
                          { title: '红球命中', dataIndex: 'red_hit_count', render: (v: number | null) => v ?? '-' },
                          {
                            title: '蓝球命中',
                            dataIndex: 'blue_hit',
                            render: (v: boolean | null) => (v == null ? '-' : v ? '是' : '否'),
                          },
                          { title: '奖级', dataIndex: 'prize_level', render: (v: string | null) => v ?? '-' },
                        ]}
                      />
                    </Card>
                  ))}
                </Space>
              </>
            ),
          },
          {
            key: 'backtest',
            label: '模型命中评估',
            children: (
              <>
                <Card className="action-card">
                  <Form layout="inline" onFinish={handleBacktest}>
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
                    <Form.Item name="model_keys" initialValue={['statistical', 'lightgbm', 'xgboost']} label="模型">
                      <Select mode="multiple" style={{ minWidth: 280 }} options={modelOptions} />
                    </Form.Item>
                    <Button type="primary" htmlType="submit" loading={backtesting}>
                      运行回测
                    </Button>
                  </Form>
                </Card>
                <Card title="模型排行榜" className="result-stack">
                  <Table
                    rowKey={(row) => `${row.model_key}-${row.backtest_run_id ?? 'latest'}`}
                    dataSource={metrics}
                    scroll={{ x: 760 }}
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
              </>
            ),
          },
        ]}
      />
    </div>
  );
}
