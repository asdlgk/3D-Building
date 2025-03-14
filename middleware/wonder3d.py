import paramiko
from .base_adapter import BaseAdapter

class Wonder3DAdapter(BaseAdapter):
    SUPPORTED_FORMATS = {'png'}
    TIMEOUT = 600  # 10分钟超时
    
    def __init__(self, ssh_client):
        self.ssh = ssh_client
        self.remote_script = "/opt/Wonder3D/run.sh"
        
    def preprocess(self, input_path):
        # 传输文件到计算节点
        sftp = self.ssh.open_sftp()
        remote_input = f"/data/inputs/{os.path.basename(input_path)}"
        sftp.put(input_path, remote_input)
        return remote_input
    
    def convert_output(self, input_path):
        # 执行模型推理
        cmd = f"bash {self.remote_script} --input {input_path}"
        stdin, stdout, stderr = self.ssh.exec_command(cmd, timeout=self.TIMEOUT)
        
        # 获取输出文件
        output_file = input_path.replace('inputs', 'outputs') + '.glb'
        return {
            'file_url': output_file,
            'metadata': self._parse_logs(stdout.read().decode())
        }
    
    def _parse_logs(self, log_data):
        return {
            'processing_time': float(log_data.split('Time:').split('s').strip())
        }
