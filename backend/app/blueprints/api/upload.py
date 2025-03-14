from flask import Blueprint, request, current_app
from werkzeug.utils import secure_filename
from datetime import datetime
import os

bp = Blueprint('upload', __name__, url_prefix='/api/upload')

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1).lower() in ALLOWED_EXTENSIONS

@bp.route('', methods=['POST'])
def upload_image():
    # 校验文件
    if 'image' not in request.files:
        return {'error': 'No file part'}, 400
    file = request.files['image']
    if file.filename == '':
        return {'error': 'No selected file'}, 400
    
    # 生成唯一文件名
    if file and allowed_file(file.filename):
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"{timestamp}_{secure_filename(file.filename)}"
        save_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(save_path)
        
        # 触发场景分类任务
        from app.core import task_queue
        task_id = task_queue.add_task(filename)
        
        return {'task_id': task_id, 'filename': filename}, 200
    else:
        return {'error': 'File type not allowed'}, 415
