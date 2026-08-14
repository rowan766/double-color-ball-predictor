import { Button, Card, Col, Input, Modal, Row, Statistic, Table, Typography, message } from 'antd';
import { useEffect, useState } from 'react';
import { useDraws } from '../../../hooks/useDraws';
import { fetchDashboard, type DashboardPayload } from '../../../services/dashboardApi';
import { importDraws } from '../../../services/drawApi';

export function Overview() {
  const { draws, loading } = useDraws();
  const [dashboard, setDashboard] = useState<DashboardPayload | null>(null);
  const [rawJson, setRawJson] = useState('');
  const [importing, setImporting] = useState(false);
  const [importOpen, setImportOpen] = useState(false);

  useEffect(() => {
    fetchDashboard().then(setDashboard).catch(() => setDashboard(null));
  }, []);

  async function handleImport() {
    try {
      setImporting(true);
      const parsed = JSON.parse(rawJson);
      const payload = Array.isArray(parsed) ? { draws: parsed, overwrite: true } : parsed;
      const result = await importDraws(payload);
      message.success(
        `导入完成：共 ${result.imported_count} 期，新增 ${result.created_count} 期，更新 ${result.updated_count} 期，跳过 ${result.skipped_count} 期`,
      );
      setImportOpen(false);
      window.location.reload();
    } catch (error) {
      message.error(error instanceof Error ? error.message : '导入失败');
    } finally {
      setImporting(false);
    }
  }

  return (
    <div className="page compact-page">
      <Typography.Title level={4} className="page-title">
        数据概览
      </Typography.Title>
      <Row gutter={[12, 12]} className="overview-stats">
        <Col xs={24} sm={8}>
          <Card className="stat-card">
            <Statistic title="历史开奖期数" value={dashboard?.total_draws ?? 0} />
          </Card>
        </Col>
        <Col xs={24} sm={8}>
          <Card className="stat-card">
            <Statistic title="模型数量" value={5} />
          </Card>
        </Col>
        <Col xs={24} sm={8}>
          <Card className="stat-card">
            <Statistic title="最新期号" value={draws[0]?.issue_no ?? '-'} />
          </Card>
        </Col>
      </Row>

      <Card
        title="历史开奖数据"
        className="result-stack data-card"
        extra={
          <Button type="primary" onClick={() => setImportOpen(true)}>
            导入开奖数据
          </Button>
        }
      >
        <Table
          size="small"
          rowKey="issue_no"
          loading={loading}
          dataSource={draws}
          scroll={{ x: 720 }}
          columns={[
            { title: '期号', dataIndex: 'issue_no' },
            { title: '开奖日期', dataIndex: 'draw_date' },
            { title: '红球', dataIndex: 'red_numbers', render: (value: number[]) => value.join(', ') },
            { title: '蓝球', dataIndex: 'blue_number' },
            { title: '红球和值', dataIndex: 'red_sum' },
            { title: '跨度', dataIndex: 'red_span' },
          ]}
        />
      </Card>
      <Modal
        title="导入开奖数据"
        open={importOpen}
        onOk={handleImport}
        okText="开始导入"
        confirmLoading={importing}
        okButtonProps={{ disabled: !rawJson.trim() }}
        onCancel={() => setImportOpen(false)}
        destroyOnClose
      >
        <Input.TextArea
          rows={8}
          value={rawJson}
          onChange={(event) => setRawJson(event.target.value)}
          placeholder='[{"issue_no":"2024001","draw_date":"2024-01-02","red_numbers":[1,2,3,4,5,6],"blue_number":7}]'
        />
      </Modal>
    </div>
  );
}
