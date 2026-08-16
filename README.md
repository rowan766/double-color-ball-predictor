# Double Color Ball Predictor / 双色球预测系统

A data-driven Double Color Ball prediction, analysis, and walk-forward backtesting system.

一个基于历史开奖数据的双色球数据分析、预测实验与滚动回测系统。

> This project is an experiment platform for data analysis and model evaluation. It does not claim that historical lottery data can reliably predict future lottery results.
>
> 本项目是一个数据分析和模型评估实验平台，不承诺历史开奖数据可以可靠预测未来开奖结果。

## Online Demo / 在线访问

- Website / 访问地址: [https://abc.zmtd.net.cn/](https://abc.zmtd.net.cn/)

## Features / 功能特性

- Historical draw data import and management
- Dashboard overview for draw counts, latest issue, and key statistics
- Lottery trend chart similar to the charts used in lottery shops
- Number frequency analysis with ECharts visualizations
- Prediction workflow with multiple model candidates
- Walk-forward backtesting and model leaderboard
- Backend API built with FastAPI
- PC and mobile-oriented frontend routes

---

- 历史开奖数据导入与管理
- 数据概览，包括历史期数、最新期号等核心指标
- 类似彩票站墙面走势图的开奖趋势图
- 基于 ECharts 的号码频率分析图表
- 多模型预测流程
- 滚动回测与模型排行榜
- 基于 FastAPI 的后端接口
- PC 与移动端页面路由

## Tech Stack / 技术栈

### Frontend / 前端

- React
- TypeScript
- Vite
- Zustand
- Axios
- Ant Design
- Ant Design Mobile
- ECharts

### Backend / 后端

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- Pydantic

### Machine Learning / 机器学习

- Pandas
- NumPy
- Scikit-learn
- LightGBM
- XGBoost

## Project Structure / 项目结构

```text
backend/    FastAPI app, database models, services, ML modules, backtesting
frontend/   React app, API services, types, stores, hooks, pages
docs/       Architecture notes and project documents
scripts/    Utility scripts
deploy/     Deployment examples and Nginx configuration
```

---

```text
backend/    FastAPI 应用、数据库模型、服务层、机器学习模块、回测模块
frontend/   React 应用、接口服务、类型定义、状态管理、Hooks、页面
docs/       架构说明与项目文档
scripts/    工具脚本
deploy/     部署示例与 Nginx 配置
```

## Local Development / 本地开发

### 1. Configure environment variables / 配置环境变量

```bash
cp .env.example .env
```

### 2. Start services / 启动服务

```bash
docker compose up --build
```

### 3. Run database migrations / 执行数据库迁移

```bash
cd backend
alembic upgrade head
```

### 4. Start frontend development server / 启动前端开发服务

```bash
cd frontend
npm install
npm run dev
```

## Backend Checks / 后端检查

```bash
cd backend
pip install -e ".[dev]"
pytest
```

## Current Status / 当前状态

Implemented / 已实现:

- Monorepo project skeleton / Monorepo 项目结构
- FastAPI application and `/api/v1/health` endpoint / FastAPI 应用与健康检查接口
- Core database models and Alembic migrations / 核心数据库模型与 Alembic 迁移
- APIs for draws, analysis, models, predictions, and backtests / 开奖、分析、模型、预测、回测接口
- Historical draw import with idempotent create/update by issue number / 按期号幂等导入与更新历史开奖数据
- Draw-level and number-level feature engineering / 开奖期级别与号码级别特征工程
- Statistical, Logistic Regression, LightGBM, XGBoost, and ensemble model classes / 统计模型、逻辑回归、LightGBM、XGBoost 与集成模型
- Random baseline for model comparison / 用于模型对比的随机基线
- Persisted prediction runs and model predictions / 预测任务与模型预测结果持久化
- Walk-forward backtesting with metric persistence / 滚动回测与指标持久化
- Backtest leaderboard API and frontend table / 回测排行榜接口与前端表格
- PC frontend pages for overview, prediction, analysis, and review / PC 端数据概览、预测、分析、复盘页面
- Lottery trend chart and frequency charts / 开奖走势图与频率图表

## Roadmap / 路线图

- Add trusted external draw-data synchronization / 接入可信外部开奖数据同步源
- Add scheduled prediction jobs / 增加定时预测任务
- Add after-draw evaluation jobs / 增加开奖后自动评估任务
- Expand charts for omissions, trends, and probability heatmaps / 扩展遗漏、趋势和概率热力图
- Improve mobile user experience / 优化移动端体验

## Disclaimer / 免责声明

Lottery results are random events. This project is intended for technical research, data analysis, and model backtesting only. Prediction results should not be treated as investment, gambling, or financial advice.

彩票开奖结果具有随机性。本项目仅用于技术研究、数据分析和模型回测，预测结果不应被视为投资、博彩或任何财务建议。

## License / 许可证

Not specified yet.

暂未声明许可证。
