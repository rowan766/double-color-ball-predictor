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
        `Imported ${result.imported_count}: created ${result.created_count}, updated ${result.updated_count}, skipped ${result.skipped_count}`,
      );
      window.location.reload();
    } catch (error) {
      message.error(error instanceof Error ? error.message : 'Import failed');
    } finally {
      setImporting(false);
    }
  }

  return (
    <div className="page">
      <Typography.Title level={3}>Draw History</Typography.Title>
      <Space direction="vertical" size={12} className="import-panel">
        <Typography.Text type="secondary">
          Paste a JSON array or an object shaped like {'{ draws, overwrite }'}.
        </Typography.Text>
        <Input.TextArea
          rows={6}
          value={rawJson}
          onChange={(event) => setRawJson(event.target.value)}
          placeholder='[{"issue_no":"2024001","draw_date":"2024-01-02","red_numbers":[1,2,3,4,5,6],"blue_number":7}]'
        />
        <Button type="primary" loading={importing} disabled={!rawJson.trim()} onClick={handleImport}>
          Import Draws
        </Button>
      </Space>
      <Table
        rowKey="issue_no"
        loading={loading}
        dataSource={draws}
        columns={[
          { title: 'Issue', dataIndex: 'issue_no' },
          { title: 'Draw Date', dataIndex: 'draw_date' },
          { title: 'Red Balls', dataIndex: 'red_numbers', render: (value: number[]) => value.join(', ') },
          { title: 'Blue Ball', dataIndex: 'blue_number' },
          { title: 'Red Sum', dataIndex: 'red_sum' },
          { title: 'Span', dataIndex: 'red_span' },
        ]}
      />
    </div>
  );
}
