import logging
from abc import ABC, abstractmethod
from paramiko import SSHClient, AutoAddPolicy, SFTPClient
from paramiko.ssh_exception import SSHException
from typing import Optional, Dict, Any, List
import tempfile
import os
import time

class AlgorithmAdapter(ABC):
    """增强版算法适配器基类，支持连接池预热和性能监控"""
    
    _connection_pool: List[SSHClient] = []
    _pool_lock = threading.Lock()
    
    def __init__(self, host: str, port: int, username: str, key_path: str):
        self.host = host
        self.port = port
        self.username = username
        self.key_path = key_path
        self.max_connections = 8  # 根据AutoDL实例规格调整
        self.logger = logging.getLogger(self.__class__.__name__)
        self._warmup_pool()

    def _warmup_pool(self):
        """预启动连接池"""
        with self._pool_lock:
            while len(self._connection_pool) < self.max_connections:
                try:
                    ssh = self._create_new_connection()
                    self._connection_pool.append(ssh)
                except Exception as e:
                    self.logger.warning(f"连接池预热失败: {str(e)}")
                    break

    def _get_connection(self) -> SSHClient:
        """智能获取连接，带有重试机制"""
        retries = 3
        for _ in range(retries):
            with self._pool_lock:
                if self._connection_pool:
                    ssh = self._connection_pool.pop()
                    if self._check_connection(ssh):
                        return ssh
                    else:
                        ssh.close()
            time.sleep(1)
        return self._create_new_connection()

    def _return_connection(self, ssh: SSHClient):
        """安全归还连接"""
        with self._pool_lock:
            if len(self._connection_pool) < self.max_connections and self._check_connection(ssh):
                self._connection_pool.append(ssh)
            else:
                ssh.close()

    @abstractmethod
    def build_command(self, input_path: str, output_dir: str) -> str:
        """构造算法CLI命令"""
        pass

    @abstractmethod
    def process_output(self, output_dir: str) -> dict:
        """统一输出格式规范：
        {
            "model_type": "glb|gltf|obj",
            "model_path": "本地文件路径",
            "metadata": {
                "textures": list, 
                "materials": list,
                "bounding_box": [x,y,z,w,h,d]
            }
        }
        """
        pass

    def _secure_upload(self, sftp: SFTPClient, local_path: str, remote_path: str):
        """加密分块上传"""
        CHUNK_SIZE = 1024 * 1024  # 1MB
        with open(local_path, 'rb') as f:
            with tempfile.NamedTemporaryFile() as encrypted_file:
                while chunk := f.read(CHUNK_SIZE):
                    encrypted_chunk = self._encrypt(chunk)  # 实现加密方法
                    encrypted_file.write(encrypted_chunk)
                encrypted_file.seek(0)
                sftp.put(encrypted_file.name, remote_path)

    def execute(self, local_file_path: str) -> Dict[str, Any]:
        """执行完整处理流程（带性能监控）"""
        start_time = time.time()
        ssh = self._get_connection()
        try:
            # 上传文件
            remote_input = ""
            with ssh.open_sftp() as sftp:
                remote_input = f"/tmp/{os.path.basename(local_file_path)}"
                self._secure_upload(sftp, local_file_path, remote_input)

            # 执行命令
            output_dir = f"/tmp/output_{int(time.time())}"
            cmd = self.build_command(remote_input, output_dir)
            self.logger.info(f"Executing command: {cmd}")
            
            stdin, stdout, stderr = ssh.exec_command(cmd, timeout=600)
            exit_status = stdout.channel.recv_exit_status()
            
            if exit_status != 0:
                error_msg = stderr.read().decode()
                self.logger.error(f"Algorithm error: {error_msg}")
                raise RuntimeError(f"{self.__class__.__name__} failed: {error_msg}")

            # 下载结果
            with tempfile.TemporaryDirectory() as tmp_dir:
                with ssh.open_sftp() as sftp:
                    for filename in sftp.listdir(output_dir):
                        remote_path = f"{output_dir}/{filename}"
                        local_path = os.path.join(tmp_dir, filename)
                        sftp.get(remote_path, local_path)
                
                result = self.process_output(tmp_dir)
                result["performance"] = {
                    "total_time": time.time() - start_time,
                    "model_size": os.path.getsize(result["model_path"])
                }
                return result
                
        finally:
            self._return_connection(ssh)
            # 清理远程文件
            with ssh.open_sftp() as sftp:
                sftp.remove(remote_input)
                sftp.rmdir(output_dir)
