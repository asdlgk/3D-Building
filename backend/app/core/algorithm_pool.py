import threading
from contextlib import contextmanager
from middleware import TripoSRAdapter, Wonder3DAdapter

class AlgorithmPool:
    _pools = {
        'triposr': [],
        'wonder3d': []
    }
    _lock = threading.Lock()
    
    @classmethod
    @contextmanager
    def get_adapter(cls, algorithm_type, ssh_client):
        with cls._lock:
            pool = cls._pools[algorithm_type]
            if pool:
                adapter = pool.pop()
            else:
                # 创建新实例
                if algorithm_type == 'triposr':
                    adapter = TripoSRAdapter(ssh_client)
                elif algorithm_type == 'wonder3d':
                    adapter = Wonder3DAdapter(ssh_client)
                
            try:
                yield adapter
            finally:
                pool.append(adapter)
