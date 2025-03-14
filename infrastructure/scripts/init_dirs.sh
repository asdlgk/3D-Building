#!/bin/bash

# 创建后端存储目录
mkdir -p backend/app/static/{uploads,outputs}
chmod 755 backend/app/static/uploads

# 创建日志目录
mkdir -p backend/app/logs
touch backend/app/logs/app.log
chmod 644 backend/app/logs/app.log

# 前端构建目录
mkdir -p frontend/dist

echo "✅ 目录结构初始化完成"
