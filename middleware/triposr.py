import trimesh
from pathlib import Path
from .base_adapter import AlgorithmAdapter
from typing import Dict, Any

class TripoSRAdapter(AlgorithmAdapter):
    """轻量化模型适配，支持自动格式转换"""
    
    def build_command(self, input_path: str, output_dir: str) -> str:
        return (
            f"source /opt/triposr/bin/activate && "
            f"python process.py --input {input_path} "
            f"--output {output_dir}/output.obj --simplify"
        )

    def process_output(self, output_dir: str) -> Dict[str, Any]:
        obj_path = Path(output_dir) / "output.obj"
        if not obj_path.exists():
            raise FileNotFoundError("TripoSR输出文件缺失")
            
        # 转换为glb格式
        mesh = trimesh.load(obj_path)
        glb_path = Path(output_dir) / "output.glb"
        mesh.export(glb_path)
        
        return {
            "model_type": "glb",
            "model_path": str(glb_path),
            "metadata": {
                "vertices": len(mesh.vertices),
                "faces": len(mesh.faces),
                "bounding_box": mesh.bounding_box.extents.tolist()
            }
        }
