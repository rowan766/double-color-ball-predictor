# double-color-ball-predictor

A data-driven Double Color Ball prediction and backtesting system based on historical lottery data.

The project is designed as a rigorous experiment platform, not as a claim that historical lottery data can reliably predict future draws. Every model must be compared against a Random Baseline through walk-forward backtesting.

## Stack

- Frontend: React, TypeScript, Vite, Zustand, Axios, Ant Design, Ant Design Mobile, ECharts
- Backend: Python, FastAPI, PostgreSQL, SQLAlchemy, Alembic, Pydantic
- ML: Pandas, NumPy, Scikit-learn, LightGBM, XGBoost

## Structure

```text
backend/   FastAPI, database models, services, ML, backtesting
frontend/  React app with shared services, types, stores, hooks
docs/      Architecture notes
scripts/   Utility scripts
```

## Local Development

Copy the environment file:

```bash
cp .env.example .env
```

Start PostgreSQL and backend:

```bash
docker compose up --build
```

Run migrations:

```bash
cd backend
alembic upgrade head
```

Start the frontend:

```bash
cd frontend
npm install
npm run dev
```

## Backend Checks

```bash
cd backend
pip install -e ".[dev]"
pytest
```

## Current V1 Status

Implemented:

- Monorepo project skeleton
- FastAPI app and `/api/v1/health`
- Core database table models and initial Alembic migration
- API layer skeleton for draws, analysis, models, predictions, and backtests
- ML model registry with V1 model keys
- Random Baseline probability output
- Candidate generation skeleton
- Walk-forward/backtest module boundaries
- React/Vite frontend shell with PC pages
- Shared frontend API services, types, stores, and hooks
- Historical draw import API with idempotent create/update by issue number
- Draw-level feature recalculation during import
- Draw History import UI for JSON payloads
- Number-level feature engineering for red and blue balls
- Statistical, Logistic Regression, LightGBM, and XGBoost model classes
- Optional dependency fallback from ML classifiers to the statistical model
- Persisted prediction runs and model predictions
- Walk-forward backtesting with result and metric persistence
- Backtest leaderboard API and frontend table
- ECharts frequency charts on the analysis page

Next implementation step:

- Add a trusted external draw-data sync source
- Add scheduled prediction and after-draw evaluation jobs
- Expand frontend charts for omissions, trends, and model probability heatmaps
