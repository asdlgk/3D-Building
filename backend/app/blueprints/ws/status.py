from flask_socketio import Namespace, emit
from app.extensions import socketio

class StatusNamespace(Namespace):
    def on_connect(self):
        print(f'Client connected: {request.sid}')
        
    def on_subscribe_task(self, data):
        """订阅任务状态更新"""
        task_id = data['task_id']
        self.join_room(task_id)
        emit('status', {'message': f'Subscribed to task {task_id}'})
        
    def on_disconnect(self):
        print(f'Client disconnected: {request.sid}')

# 注册命名空间
socketio.on_namespace(StatusNamespace('/status'))
