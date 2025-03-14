from .base_adapter import BaseAdapter

class TripoSRAdapter(BaseAdapter):
    SUPPORTED_FORMATS = {'jpg', 'png', 'jpeg'}
    
    def __init__(self, ssh_client):
        self.ssh = ssh_client
        self.remote_path = "/opt/TripoSR"
        
    def preprocess(self, input_path):
        # 传输文件到GPU服务器
        sftp = self.ssh.open_sftp()
        remote_input = f"{self.remote_path}/inputs/{os.path.basename(input_path)}"
        sftp.put(input_path, remote_input)
        return remote_input
    
    def convert_output(self, input_path):
        # 执行推理命令
        cmd = f"cd {self.remote_path} && python inference.py --input {input_path}"
        stdin, stdout, stderr = self.ssh.exec_command(cmd)
        
        if exit_code := stdout.channel.recv_exit_status():
            raise RuntimeError(f"TripoSR执行失败: {stderr.read().decode()}")
            
        # 获取输出文件
        output_file = f"{self.remote_path}/outputs/{os.path.basename(input_path)}.glb"
        return {
            'file_url': output_file,
            'metadata': self._parse_metadata(stdout.read().decode())
        }
    
    def _parse_metadata(self, log):
        return {
            'polygons': int(log.split('Generated ').split(' polygons')),
            'vertices': int(log.split('with ').split(' vertices'))
        }
