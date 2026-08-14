# 部署更新说明

本文档用于把本地代码更新发布到已经部署好的服务器。

本项目生产环境目前由两部分组成：

- 后端：`docker-compose.prod.yml` 中的 `backend` 服务
- 前端：构建后的静态文件部署到服务器目录 `/home/ecs-user/apps/double-color-ball-predictor/frontend-dist`

## 1. 本地提交本次代码

先在本地项目根目录查看改动：

```bash
git status
```

只提交本次预测优化相关文件：

```bash
git add README.md
git add backend/app/ml/backtesting/backtest_runner.py
git add backend/app/ml/models/registry.py
git add backend/app/ml/models/optimized_ensemble_model.py
git add backend/app/ml/prediction/candidate_generator.py
git add backend/app/services/prediction_service.py
git add frontend/src/pages/pc/Backtest/Backtest.tsx
git add frontend/src/pages/pc/Dashboard/Dashboard.tsx
git add frontend/src/pages/pc/Overview/Overview.tsx
git add frontend/src/pages/pc/Prediction/Prediction.tsx
git add frontend/src/pages/pc/PredictionReview/PredictionReview.tsx
```

再次确认暂存区：

```bash
git status
```

提交：

```bash
git commit -m "Add optimized ensemble prediction strategy"
```

推送到远程仓库：

```bash
git push
```

## 2. 登录服务器并进入项目目录

登录服务器：

```bash
ssh ecs-user@你的服务器IP
```

进入项目目录：

```bash
cd /home/ecs-user/apps/double-color-ball-predictor
```

拉取最新代码：

```bash
git pull
```

确认代码已更新：

```bash
git status
```

## 3. 更新后端服务

本次后端新增了 `optimized_ensemble` 模型和 `optimized` 候选生成策略，需要重新构建后端镜像。

在服务器项目根目录执行：

```bash
docker compose -f docker-compose.prod.yml up -d --build backend
```

查看容器状态：

```bash
docker compose -f docker-compose.prod.yml ps
```

查看后端日志：

```bash
docker compose -f docker-compose.prod.yml logs -f --tail=100 backend
```

如果服务器使用旧版 `docker-compose` 命令，则改用：

```bash
docker-compose -f docker-compose.prod.yml up -d --build backend
docker-compose -f docker-compose.prod.yml ps
docker-compose -f docker-compose.prod.yml logs -f --tail=100 backend
```

## 4. 更新前端静态文件

本次也修改了前端页面，所以前端需要重新构建并覆盖生产静态目录。

进入前端目录：

```bash
cd /home/ecs-user/apps/double-color-ball-predictor/frontend
```

安装依赖。如果服务器已经安装过且 `node_modules` 存在，可以跳过这一步：

```bash
npm install
```

构建前端：

```bash
npm run build
```

回到项目根目录：

```bash
cd /home/ecs-user/apps/double-color-ball-predictor
```

清空旧静态文件：

```bash
rm -rf /home/ecs-user/apps/double-color-ball-predictor/frontend-dist/*
```

复制新的构建产物：

```bash
cp -r frontend/dist/* /home/ecs-user/apps/double-color-ball-predictor/frontend-dist/
```

检查静态文件是否已更新：

```bash
ls -lah /home/ecs-user/apps/double-color-ball-predictor/frontend-dist
```

## 5. 重载 Nginx

检查 Nginx 配置：

```bash
sudo nginx -t
```

重载 Nginx：

```bash
sudo systemctl reload nginx
```

## 6. 验证接口和页面

检查后端健康接口：

```bash
curl http://127.0.0.1:18000/api/v1/health
```

检查线上页面：

```bash
curl -I https://abc.zmtd.net.cn
```

浏览器打开：

```text
https://abc.zmtd.net.cn
```

进入预测页面，确认模型下拉框里有：

```text
优化融合模型
```

## 7. 本次更新是否需要数据库迁移

本次没有修改数据库表结构，不需要手动执行迁移。

生产后端容器启动命令里已经包含：

```bash
alembic upgrade head
```

所以执行：

```bash
docker compose -f docker-compose.prod.yml up -d --build backend
```

时会自动检查并应用已有迁移。

## 8. 回滚命令

如果更新后需要回滚，先查看提交记录：

```bash
git log --oneline -5
```

回到上一个提交：

```bash
git reset --hard HEAD~1
```

重新构建后端：

```bash
docker compose -f docker-compose.prod.yml up -d --build backend
```

重新构建并覆盖前端：

```bash
cd frontend
npm run build
cd ..
rm -rf /home/ecs-user/apps/double-color-ball-predictor/frontend-dist/*
cp -r frontend/dist/* /home/ecs-user/apps/double-color-ball-predictor/frontend-dist/
sudo systemctl reload nginx
```
