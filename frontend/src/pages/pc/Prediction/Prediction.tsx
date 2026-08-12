import { Button, Card, Form, Input, Select, Space, Table, Typography, message } from 'antd';
import { useState } from 'react';
import { runPrediction } from '../../../services/predictionApi';
import type { ModelPrediction } from '../../../types/prediction';

export function Prediction() {
  const [predictions, setPredictions] = useState<ModelPrediction[]>([]);
  const [loading, setLoading] = useState(false);

  async function handleFinish(values: { target_issue_no: string; train_until_issue_no: string; model_keys: string[] }) {
    try {
      setLoading(true);
      const result = await runPrediction({
        ...values,
        candidate_strategy: 'mixed',
        candidate_count: 5,
      });
      setPredictions(result);
    } catch (error) {
      message.error(error instanceof Error ? error.message : 'Prediction failed');
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="page">
      <Typography.Title level={3}>Prediction</Typography.Title>
      <Card>
        <Form layout="inline" onFinish={handleFinish}>
          <Form.Item name="target_issue_no" rules={[{ required: true }]} label="Target Issue">
            <Input placeholder="2024002" />
          </Form.Item>
          <Form.Item name="train_until_issue_no" rules={[{ required: true }]} label="Train Until">
            <Input placeholder="2024001" />
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
      <Space direction="vertical" size={16} className="result-stack">
        {predictions.map((prediction) => (
          <Card key={prediction.model_key} title={prediction.model_key}>
            <Table
              size="small"
              rowKey={(row) => `${row.red_numbers.join('-')}-${row.blue_number}`}
              pagination={false}
              dataSource={prediction.candidate_numbers}
              columns={[
                { title: 'Red Balls', dataIndex: 'red_numbers', render: (v: number[]) => v.join(', ') },
                { title: 'Blue Ball', dataIndex: 'blue_number' },
                { title: 'Score', dataIndex: 'score', render: (v: number) => v?.toFixed(4) },
              ]}
            />
          </Card>
        ))}
      </Space>
    </div>
  );
}
