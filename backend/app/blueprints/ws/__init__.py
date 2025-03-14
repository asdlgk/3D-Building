from flask_socketio import emit
from app.extensions import socketio

@socketio.on('connect')
def handle_connect():
    emit('status', {'message': 'Connected'})

@socketio.on('subscribe_task')
def handle_subscribe_task(data):
    from app.core.task_queue import TaskQueue
    task_id = data['task_id']
    
    def progress_callback(task_info):
        socketio.emit('task_update', {
            'task_id': task_id,
            'status': task_info['status'],
            'progress': task_info.get('progress', 0)
        })
    
    TaskQueue.add_listener(task_id, progress_callback)
