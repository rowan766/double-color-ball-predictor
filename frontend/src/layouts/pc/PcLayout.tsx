import {
  BarChartOutlined,
  DashboardOutlined,
  ExperimentOutlined,
} from '@ant-design/icons';
import { Button, Layout, Menu, Typography } from 'antd';
import { Outlet, useLocation, useNavigate } from 'react-router-dom';

const { Header, Sider, Content } = Layout;

const items = [
  { key: '/prediction', icon: <ExperimentOutlined />, label: '预测评估' },
  { key: '/overview', icon: <DashboardOutlined />, label: '数据概览' },
  { key: '/analysis', icon: <BarChartOutlined />, label: '数据分析' },
];

export function PcLayout() {
  const navigate = useNavigate();
  const location = useLocation();
  const selectedKey =
    location.pathname === '/dashboard' || location.pathname === '/draws'
      ? '/overview'
      : location.pathname === '/backtest'
        ? '/prediction'
        : location.pathname;

  return (
    <Layout className="app-shell">
      <Sider width={220} theme="light" className="desktop-sider">
        <div className="brand">双色球实验平台</div>
        <Menu
          mode="inline"
          selectedKeys={[selectedKey]}
          items={items}
          onClick={({ key }) => navigate(key)}
        />
      </Sider>
      <Layout className="main-layout">
        <Header className="topbar">
          <Typography.Text strong>双色球预测实验台</Typography.Text>
        </Header>
        <Content className="content">
          <Outlet />
        </Content>
        <nav className="mobile-tabbar">
          {items.map((item) => (
            <Button
              key={item.key}
              type={selectedKey === item.key ? 'primary' : 'text'}
              icon={item.icon}
              onClick={() => navigate(item.key)}
            >
              {item.label}
            </Button>
          ))}
        </nav>
      </Layout>
    </Layout>
  );
}
