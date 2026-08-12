import { Card, Col, Row, Table, Typography } from 'antd';
import { useEffect, useState } from 'react';
import { FrequencyBarChart } from '../../../components/charts/FrequencyBarChart';
import { fetchAnalysisSummary } from '../../../services/analysisApi';
import type { AnalysisSummary } from '../../../types/analysis';

export function Analysis() {
  const [summary, setSummary] = useState<AnalysisSummary | null>(null);

  useEffect(() => {
    fetchAnalysisSummary().then(setSummary).catch(() => setSummary(null));
  }, []);

  return (
    <div className="page">
      <Typography.Title level={3}>Analysis</Typography.Title>
      <Row gutter={[16, 16]}>
        <Col span={12}>
          <Card title="Red Frequency">
            <FrequencyBarChart data={summary?.red_frequency ?? []} color="#d92d20" />
            <Table
              size="small"
              rowKey="number"
              pagination={false}
              dataSource={summary?.red_frequency ?? []}
              columns={[
                { title: 'Number', dataIndex: 'number' },
                { title: 'Count', dataIndex: 'count' },
                { title: 'Frequency', dataIndex: 'frequency', render: (v: number) => `${(v * 100).toFixed(2)}%` },
              ]}
            />
          </Card>
        </Col>
        <Col span={12}>
          <Card title="Blue Frequency">
            <FrequencyBarChart data={summary?.blue_frequency ?? []} color="#1570ef" />
            <Table
              size="small"
              rowKey="number"
              pagination={false}
              dataSource={summary?.blue_frequency ?? []}
              columns={[
                { title: 'Number', dataIndex: 'number' },
                { title: 'Count', dataIndex: 'count' },
                { title: 'Frequency', dataIndex: 'frequency', render: (v: number) => `${(v * 100).toFixed(2)}%` },
              ]}
            />
          </Card>
        </Col>
      </Row>
    </div>
  );
}
