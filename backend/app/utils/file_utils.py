import os
import hashlib
from datetime import datetime
from werkzeug.utils import secure_filename

def generate_file_hash(file_path):
    """生成文件SHA256哈希值"""
    sha256 = hashlib.sha256()
    with open(file_path, 'rb') as f:
        while chunk := f.read(4096):
            sha256.update(chunk)
    return sha256.hexdigest()

def safe_save_upload(file_stream, save_dir):
    """安全保存上传文件"""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    original_name = secure_filename(file_stream.filename)
    file_ext = original_name.rsplit('.', 1)[-1].lower()
    
    # 生成唯一文件名
    unique_name = f"{timestamp}_{os.urandom(4).hex()}.{file_ext}"
    save_path = os.path.join(save_dir, unique_name)
    
    # 分块写入
    chunk_size = 4096
    with open(save_path, 'wb') as f:
        while chunk := file_stream.read(chunk_size):
            f.write(chunk)
    
    return {
        'original_name': original_name,
        'saved_path': save_path,
        'file_hash': generate_file_hash(save_path)
    }
