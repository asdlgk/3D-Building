
---

### 3. 项目入口文档 (`README.md`)
```markdown
# 3D校园在线建模平台

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Build Status](https://travis-ci.com/yourname/3d-campus.svg?branch=main)](https://travis-ci.com/yourname/3d-campus)

基于AI的校园场景快速三维重建平台，支持教学楼、操场等典型场景的自动化建模。

## ✨ 核心功能
- &zwnj;**智能场景分类**&zwnj;：EfficientNetV2模型实现90%+准确率
- &zwnj;**算法动态调度**&zwnj;：根据场景类型自动匹配最佳建模算法
- &zwnj;**实时进度追踪**&zwnj;：WebSocket推送建模全流程状态
- &zwnj;**多格式输出**&zwnj;：支持GLB/GLTF/OBJ等工业标准格式

## 🚀 快速启动
### 前置需求
- Python 3.8+ & Node.js 16+
- PostgreSQL 12+
- Redis 6+

```bash
# 克隆仓库
git clone https://github.com/yourname/3d-campus.git
cd 3d-campus

# 安装依赖
cd backend && pip install -r requirements.txt
cd ../frontend && npm install

# 配置环境变量（复制并修改示例文件）
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env

# 启动服务
cd backend && flask run --port 5000
cd frontend && npm run dev
