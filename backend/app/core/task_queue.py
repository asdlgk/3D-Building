from celery import shared_task
from app.extensions import celery
from app.utils.ssh_utils import SSHPool
from middleware import TripoSRAdapter

@shared_task
def process_upload_task(file_path, algorithm_type='triposr'):
    ssh_pool = SSHPool(
        host=current_app.config['AUTODL_HOST'],
        username="admin",
        key_path=current_app.config['SSH_KEY_PATH']
    )
    
    with ssh_pool.get_connection() as ssh:
        # 传输文件到GPU服务器
        sftp = ssh.open_sftp()
        remote_path = f"/data/inputs/{os.path.basename(file_path)}"
        sftp.put(file_path, remote_path)
        
        # 执行模型转换
        with AlgorithmPool.get_adapter(algorithm_type, ssh) as adapter:
            result = adapter.convert_output(remote_path)
            
            # 下载生成模型
            local_output = os.path.join(
                current_app.config['OUTPUT_FOLDER'],
                os.path.basename(result['file_url'])
            )
            sftp.get(result['file_url'], local_output)
            
    return {
        'status': 'success',
        'model_path': local_output,
        'metadata': result['metadata']
    }
