import numpy as np
from .base_adapter import AlgorithmAdapter
from typing import Dict, Any

class Dust3RAdapter(AlgorithmAdapter):
    """Dust3R点云处理适配器"""
    
    def build_command(self, input_path: str, output_dir: str) -> str:
        return (
            f"source /opt/venv/bin/activate && "
            f"python process.py --image {input_path} "
            f"--output {output_dir}/pointcloud.npy"
        )

    def process_output(self, output_dir: str) -> Dict[str, Any]:
        pointcloud = np.load(f"{output_dir}/pointcloud.npy")
        
        # 转换为glTF格式
        return {
            "model_type": "gltf",
            "vertices": pointcloud.tolist(),
            "colors": [[1.0, 1.0, 1.0]] * len(pointcloud),  # 默认白色
            "metadata": {
                "point_count": len(pointcloud),
                "coordinate_system": "right_handed"
            }
        }
