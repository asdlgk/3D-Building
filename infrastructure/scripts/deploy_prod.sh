#!/bin/bash

# 蓝绿部署脚本
TIMESTAMP=$(date +%Y%m%d%H%M%S)
DEPLOY_DIR="/var/www/3d-campus/$TIMESTAMP"

# 构建前端
cd frontend
npm install
npm run build
cp -R dist/* $DEPLOY_DIR/frontend/

# 构建后端
cd ../backend
python -m venv $DEPLOY_DIR/venv
source $DEPLOY_DIR/venv/bin/activate
pip install -r requirements.txt

# 切换符号链接
ln -sfn $DEPLOY_DIR /var/www/3d-campus/current

# 重启服务
systemctl restart 3d-campus.service

echo "✅ 生产环境部署完成: $TIMESTAMP"
