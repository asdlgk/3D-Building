from .base_adapter import BaseAdapter
import json

class TripoSRAdapter(BaseAdapter):
    SUPPORTED_FORMATS = ['glb', 'obj']
    
    def __init__(self, ssh_client):
        self.ssh = ssh_client
        self.remote_script = "/opt/TripoSR/run.py"
    
    def convert_output(self, remote_output_path):
        # 执行远程命令
        stdin, stdout, stderr = self.ssh.exec_command(
            f"python {self.remote_script} --input {remote_output_path}"
        )
        raw_data = stdout.read().decode()
        
        # 解析输出
        return {
            "model_type": "glb",
            "file_url": json.loads(raw_data)['result_path'],
            "metadata": {
                "vertices": json.loads(raw_data)['vertex_count'],
                "textures": True
            }
        }
