import { Button, Input, Space, Table, Typography, message } from 'antd';
import { useState } from 'react';
import { useDraws } from '../../../hooks/useDraws';
import { importDraws } from '../../../services/drawApi';

export function DrawHistory() {
  const { draws, loading } = useDraws();
  const [rawJson, setRawJson] = useState('');
  const [importing, setImporting] = useState(false);

  async function handleImport() {
    try {
      setImporting(true);
      const parsed = JSON.parse(rawJson);
      const payload = Array.isArray(parsed) ? { draws: parsed, overwrite: true } : parsed;
      const result = await importDraws(payload);
      message.success(
        `导入完成：共 ${result.imported_count} 期，新增 ${result.created_count} 期，更新 ${result.updated_count} 期，跳过 ${result.skipped_count} 期`,
      );
      window.location.reload();
    } catch (error) {
      message.error(error instanceof Error ? error.message : '导入失败');
    } finally {
      setImporting(false);
    }
  }

  return (
    <div className="page">
      <Typography.Title level={3}>历史开奖</Typography.Title>
      <Space direction="vertical" size={12} className="import-panel">
        <Typography.Text type="secondary">
          粘贴 JSON 数组，或形如 {'{ draws, overwrite }'} 的导入对象。
        </Typography.Text>
        <Input.TextArea
          rows={6}
          value={rawJson}
          onChange={(event) => setRawJson(event.target.value)}
          placeholder='[{"issue_no":"2024001","draw_date":"2024-01-02","red_numbers":[1,2,3,4,5,6],"blue_number":7}]'
        />
        <Button type="primary" loading={importing} disabled={!rawJson.trim()} onClick={handleImport}>
          导入开奖数据
        </Button>
      </Space>
      <Table
        rowKey="issue_no"
        loading={loading}
        dataSource={draws}
        columns={[
          { title: '期号', dataIndex: 'issue_no' },
          { title: '开奖日期', dataIndex: 'draw_date' },
          { title: '红球', dataIndex: 'red_numbers', render: (value: number[]) => value.join(', ') },
          { title: '蓝球', dataIndex: 'blue_number' },
          { title: '红球和值', dataIndex: 'red_sum' },
          { title: '跨度', dataIndex: 'red_span' },
        ]}
      />
    </div>
  );
}
