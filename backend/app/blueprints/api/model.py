from flask import Blueprint, send_from_directory
from app.config import Config

bp = Blueprint('model', __name__)

@bp.route('/<path:filename>', methods=['GET'])
def download_model(filename):
    # 验证文件路径防止目录遍历攻击
    if '..' in filename or filename.startswith('/'):
        return {"error": "Invalid filename"}, 400
        
    return send_from_directory(
        directory=Config.OUTPUT_FOLDER,
        path=filename,
        as_attachment=True,
        conditional=True
    )
