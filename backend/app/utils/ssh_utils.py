import paramiko
import threading
from contextlib import contextmanager

class SSHPool:
    def __init__(self, host, username, key_path, pool_size=5):
        self.host = host
        self.username = username
        self.key = paramiko.RSAKey.from_private_key_file(key_path)
        self.pool = []
        self.lock = threading.Lock()
        
        # 初始化连接池
        for _ in range(pool_size):
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(
                hostname=host,
                username=username,
                pkey=self.key,
                timeout=10
            )
            self.pool.append(client)
    
    @contextmanager
    def get_connection(self):
        with self.lock:
            if not self.pool:
                raise RuntimeError("Connection pool exhausted")
            conn = self.pool.pop()
        
        try:
            yield conn
        finally:
            with self.lock:
                self.pool.append(conn)
    
    def close_all(self):
        for conn in self.pool:
            conn.close()
        self.pool.clear()
