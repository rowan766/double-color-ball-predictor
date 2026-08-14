import { Button, Card, Form, Input, Select, Space, Table, Typography, message } from 'antd';
import { useEffect, useState } from 'react';
import { fetchLatestDraw } from '../../../services/drawApi';
import { runPrediction } from '../../../services/predictionApi';
import type { ModelPrediction } from '../../../types/prediction';

function getNextIssueNo(issueNo: string) {
  const next = Number(issueNo) + 1;
  return next.toString().padStart(issueNo.length, '0');
}

const modelNameMap: Record<string, string> = {
  optimized_ensemble: '优化融合模型',
  random_baseline: '随机基线',
  statistical: '统计模型',
  logistic_regression: '逻辑回归',
  lightgbm: 'LightGBM 模型',
  xgboost: 'XGBoost 模型',
};

export function Prediction() {
  const [form] = Form.useForm();
  const [predictions, setPredictions] = useState<ModelPrediction[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchLatestDraw()
      .then((latestDraw) => {
        form.setFieldsValue({
          train_until_issue_no: latestDraw.issue_no,
          target_issue_no: getNextIssueNo(latestDraw.issue_no),
        });
      })
      .catch(() => {
        message.warning('未找到最新开奖数据，请先导入历史数据。');
      });
  }, [form]);

  async function handleFinish(values: { target_issue_no: string; train_until_issue_no: string; model_keys: string[] }) {
    try {
      setLoading(true);
      const result = await runPrediction({
        ...values,
        candidate_strategy: 'optimized',
        candidate_count: 5,
      });
      setPredictions(result);
    } catch (error) {
      message.error(error instanceof Error ? error.message : '预测失败');
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="page">
      <Typography.Title level={3}>模型预测</Typography.Title>
      <Card>
        <Form form={form} layout="inline" onFinish={handleFinish}>
          <Form.Item name="target_issue_no" rules={[{ required: true }]} label="预测期号">
            <Input placeholder="下一期开奖期号" />
          </Form.Item>
          <Form.Item name="train_until_issue_no" rules={[{ required: true }]} label="训练截止期号">
            <Input placeholder="最新已开奖期号" />
          </Form.Item>
          <Form.Item name="model_keys" initialValue={['optimized_ensemble']} label="模型">
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
            运行预测
          </Button>
        </Form>
      </Card>
      <Space direction="vertical" size={16} className="result-stack">
        {predictions.map((prediction) => (
          <Card key={prediction.model_key} title={modelNameMap[prediction.model_key] ?? prediction.model_key}>
            <Table
              size="small"
              rowKey={(row) => `${row.red_numbers.join('-')}-${row.blue_number}`}
              pagination={false}
              dataSource={prediction.candidate_numbers}
              columns={[
                { title: '红球', dataIndex: 'red_numbers', render: (v: number[]) => v.join(', ') },
                { title: '蓝球', dataIndex: 'blue_number' },
                { title: '评分', dataIndex: 'score', render: (v: number) => v?.toFixed(4) },
              ]}
            />
          </Card>
        ))}
      </Space>
    </div>
  );
}
