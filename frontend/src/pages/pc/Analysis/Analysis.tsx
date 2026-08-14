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
    <div className="page compact-page">
      <Typography.Title level={4} className="page-title">
        数据分析
      </Typography.Title>
      <Row gutter={[12, 12]}>
        <Col xs={24} lg={12}>
          <Card title="红球出现频率">
            <FrequencyBarChart data={summary?.red_frequency ?? []} color="#d92d20" />
            <Table
              size="small"
              rowKey="number"
              pagination={false}
              scroll={{ x: 360 }}
              dataSource={summary?.red_frequency ?? []}
              columns={[
                { title: '号码', dataIndex: 'number' },
                { title: '出现次数', dataIndex: 'count' },
                { title: '频率', dataIndex: 'frequency', render: (v: number) => `${(v * 100).toFixed(2)}%` },
              ]}
            />
          </Card>
        </Col>
        <Col xs={24} lg={12}>
          <Card title="蓝球出现频率">
            <FrequencyBarChart data={summary?.blue_frequency ?? []} color="#1570ef" />
            <Table
              size="small"
              rowKey="number"
              pagination={false}
              scroll={{ x: 360 }}
              dataSource={summary?.blue_frequency ?? []}
              columns={[
                { title: '号码', dataIndex: 'number' },
                { title: '出现次数', dataIndex: 'count' },
                { title: '频率', dataIndex: 'frequency', render: (v: number) => `${(v * 100).toFixed(2)}%` },
              ]}
            />
          </Card>
        </Col>
      </Row>
    </div>
  );
}
