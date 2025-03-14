from .base_adapter import AlgorithmAdapter
from .luciddreamer import LucidDreamerAdapter
from .wonder3d import Wonder3DAdapter
from .dust3r import Dust3RAdapter
from .triposr import TripoSRAdapter
from typing import Type

class AdapterFactory:
    """带缓存的适配器工厂"""
    _adapters = {}
    
    @classmethod
    def get_adapter(cls, algorithm_type: str) -> Type[AlgorithmAdapter]:
        if algorithm_type not in cls._adapters:
            cls._register_adapters()
        return cls._adapters[algorithm_type]
    
    @classmethod
    def _register_adapters(cls):
        """注册所有适配器类型"""
        cls._adapters.update({
            "luciddreamer": LucidDreamerAdapter,
            "wonder3d": Wonder3DAdapter,
            "dust3r": Dust3RAdapter,
            "triposr": TripoSRAdapter
        })

def create_adapter(algorithm_type: str, **kwargs) -> AlgorithmAdapter:
    """创建适配器实例"""
    adapter_class = AdapterFactory.get_adapter(algorithm_type.lower())
    return adapter_class(
        host=kwargs['host'],
        port=kwargs['port'],
        username=kwargs['username'],
        key_path=kwargs['key_path']
    )
