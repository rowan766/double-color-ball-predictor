import { Card, Col, Row, Statistic, Typography } from 'antd';
import { useEffect, useState } from 'react';
import { fetchDashboard, type DashboardPayload } from '../../../services/dashboardApi';

export function Dashboard() {
  const [dashboard, setDashboard] = useState<DashboardPayload | null>(null);

  useEffect(() => {
    fetchDashboard().then(setDashboard).catch(() => setDashboard(null));
  }, []);

  return (
    <div className="page">
      <Typography.Title level={3}>Dashboard</Typography.Title>
      <Row gutter={[16, 16]}>
        <Col span={8}>
          <Card>
            <Statistic title="Historical Draws" value={dashboard?.total_draws ?? 0} />
          </Card>
        </Col>
        <Col span={8}>
          <Card>
            <Statistic title="Models" value={5} />
          </Card>
        </Col>
        <Col span={8}>
          <Card>
            <Statistic title="Backtest Predictions" value={0} />
          </Card>
        </Col>
      </Row>
    </div>
  );
}
