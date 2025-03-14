# 3D校园建模平台架构设计

## 系统拓扑
```mermaid
graph TD
    A[用户浏览器] -->|HTTPS| B[Nginx]
    B -->|API请求| C[Flask应用集群]
    B -->|WebSocket| D[WebSocket Manager]
    C -->|算法调度| E[AutoDL算法实例池]
    E -->|SSH隧道| F[LucidDreamer]
    E -->|SSH隧道| G[Wonder3D]
    C -->|数据库| H[(PostgreSQL)]
    C -->|文件存储| I[阿里云OSS]
    D -->|状态推送| A
