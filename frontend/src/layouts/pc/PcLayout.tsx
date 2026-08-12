import { BarChartOutlined, DashboardOutlined, ExperimentOutlined, HistoryOutlined, ThunderboltOutlined } from '@ant-design/icons';
import { Layout, Menu, Typography } from 'antd';
import { Outlet, useLocation, useNavigate } from 'react-router-dom';

const { Header, Sider, Content } = Layout;

const items = [
  { key: '/dashboard', icon: <DashboardOutlined />, label: 'Dashboard' },
  { key: '/draws', icon: <HistoryOutlined />, label: '历史开奖' },
  { key: '/analysis', icon: <BarChartOutlined />, label: '数据分析' },
  { key: '/prediction', icon: <ThunderboltOutlined />, label: '模型预测' },
  { key: '/backtest', icon: <ExperimentOutlined />, label: '回测' },
];

export function PcLayout() {
  const navigate = useNavigate();
  const location = useLocation();

  return (
    <Layout className="app-shell">
      <Sider width={220} theme="light">
        <div className="brand">双色球实验平台</div>
        <Menu
          mode="inline"
          selectedKeys={[location.pathname]}
          items={items}
          onClick={({ key }) => navigate(key)}
        />
      </Sider>
      <Layout>
        <Header className="topbar">
          <Typography.Text strong>严谨预测、Walk-Forward 回测、随机基线对照</Typography.Text>
        </Header>
        <Content className="content">
          <Outlet />
        </Content>
      </Layout>
    </Layout>
  );
}
