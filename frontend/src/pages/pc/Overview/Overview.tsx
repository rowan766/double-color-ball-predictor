import { Button, Card, Col, Empty, Input, Modal, Row, Segmented, Space, Statistic, Table, Typography, message } from 'antd';
import { useEffect, useMemo, useState } from 'react';
import { useDraws } from '../../../hooks/useDraws';
import { fetchDashboard, type DashboardPayload } from '../../../services/dashboardApi';
import { importDraws } from '../../../services/drawApi';
import type { LotteryDraw } from '../../../types/draw';

type DisplayMode = 'table' | 'chart';

interface DrawTrendChartProps {
  data: LotteryDraw[];
}

function DrawTrendChart({ data }: DrawTrendChartProps) {
  const chartData = useMemo(() => [...data].reverse(), [data]);
  const redColumns = Array.from({ length: 33 }, (_, index) => index + 1);
  const blueColumns = Array.from({ length: 16 }, (_, index) => index + 1);
  const cellSize = 26;
  const rowHeight = 26;
  const redWidth = redColumns.length * cellSize;
  const blueWidth = blueColumns.length * cellSize;
  const bodyHeight = chartData.length * rowHeight;
  const redLines = [0, 1, 2, 3, 4, 5].map((ballIndex) =>
    chartData
      .map((item, rowIndex) => {
        const value = item.red_numbers[ballIndex];
        return `${(value - 0.5) * cellSize},${rowIndex * rowHeight + rowHeight / 2}`;
      })
      .join(' '),
  );
  const blueLine = chartData
    .map((item, rowIndex) => `${(item.blue_number - 0.5) * cellSize},${rowIndex * rowHeight + rowHeight / 2}`)
    .join(' ');

  if (data.length === 0) {
    return <Empty image={Empty.PRESENTED_IMAGE_SIMPLE} description="暂无开奖数据" />;
  }

  return (
    <div className="lottery-trend-scroll">
      <div className="lottery-trend-board">
        <div className="trend-header">
          <div className="trend-issue-title">期号</div>
          <div className="trend-zone trend-red-zone">
            <div className="trend-zone-title red-text">红球</div>
            <div className="trend-number-row" style={{ gridTemplateColumns: `repeat(${redColumns.length}, ${cellSize}px)` }}>
              {redColumns.map((number) => (
                <span key={number}>{String(number).padStart(2, '0')}</span>
              ))}
            </div>
          </div>
          <div className="trend-zone trend-blue-zone">
            <div className="trend-zone-title blue-text">蓝球</div>
            <div className="trend-number-row" style={{ gridTemplateColumns: `repeat(${blueColumns.length}, ${cellSize}px)` }}>
              {blueColumns.map((number) => (
                <span key={number}>{String(number).padStart(2, '0')}</span>
              ))}
            </div>
          </div>
        </div>

        <div className="trend-body">
          <div className="trend-issue-list">
            {chartData.map((item) => (
              <div className="trend-issue-cell" key={item.issue_no}>
                {item.issue_no}
              </div>
            ))}
          </div>

          <div className="trend-grid-panel" style={{ width: redWidth }}>
            <svg className="trend-lines" viewBox={`0 0 ${redWidth} ${bodyHeight}`} preserveAspectRatio="none">
              {redLines.map((points, index) => (
                <polyline key={index} points={points} fill="none" stroke="rgba(201, 24, 43, 0.52)" strokeWidth="1.1" />
              ))}
            </svg>
            <div className="trend-grid" style={{ gridTemplateColumns: `repeat(${redColumns.length}, ${cellSize}px)` }}>
              {chartData.flatMap((item) =>
                redColumns.map((number) => {
                  const hit = item.red_numbers.includes(number);
                  return (
                    <div className="trend-cell" key={`${item.issue_no}-red-${number}`}>
                      {hit ? <span className="trend-ball red-ball">{String(number).padStart(2, '0')}</span> : null}
                    </div>
                  );
                }),
              )}
            </div>
          </div>

          <div className="trend-grid-panel" style={{ width: blueWidth }}>
            <svg className="trend-lines" viewBox={`0 0 ${blueWidth} ${bodyHeight}`} preserveAspectRatio="none">
              <polyline points={blueLine} fill="none" stroke="rgba(29, 78, 216, 0.62)" strokeWidth="1.2" />
            </svg>
            <div className="trend-grid" style={{ gridTemplateColumns: `repeat(${blueColumns.length}, ${cellSize}px)` }}>
              {chartData.flatMap((item) =>
                blueColumns.map((number) => {
                  const hit = item.blue_number === number;
                  return (
                    <div className="trend-cell" key={`${item.issue_no}-blue-${number}`}>
                      {hit ? <span className="trend-ball blue-ball">{String(number).padStart(2, '0')}</span> : null}
                    </div>
                  );
                }),
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export function Overview() {
  const { draws, loading } = useDraws();
  const [dashboard, setDashboard] = useState<DashboardPayload | null>(null);
  const [rawJson, setRawJson] = useState('');
  const [importing, setImporting] = useState(false);
  const [importOpen, setImportOpen] = useState(false);
  const [displayMode, setDisplayMode] = useState<DisplayMode>('table');

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
            <Statistic title="模型数量" value={6} />
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
          <Space size={8} wrap>
            <Segmented
              size="small"
              value={displayMode}
              onChange={(value) => setDisplayMode(value as DisplayMode)}
              options={[
                { label: '表格展示', value: 'table' },
                { label: '图表展示', value: 'chart' },
              ]}
            />
            <Button type="primary" onClick={() => setImportOpen(true)}>
              导入开奖数据
            </Button>
          </Space>
        }
      >
        {displayMode === 'table' ? (
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
        ) : (
          <DrawTrendChart data={draws} />
        )}
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
