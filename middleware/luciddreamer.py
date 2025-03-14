import json
from pathlib import Path
from .base_adapter import AlgorithmAdapter
from typing import Dict, Any

class LucidDreamerAdapter(AlgorithmAdapter):
    """LucidDreamer算法适配实现"""
    
    def build_command(self, input_path: str, output_dir: str) -> str:
        return (
            f"source /opt/venv/bin/activate && "
            f"python scripts/inference.py --input {input_path} "
            f"--output {output_dir} --format glb"
        )

    def process_output(self, output_dir: str) -> Dict[str, Any]:
        output_path = Path(output_dir) / "output.glb"
        metadata_path = Path(output_dir) / "metadata.json"
        
        if not output_path.exists():
            raise FileNotFoundError("未找到生成模型文件")
            
        with open(metadata_path) as f:
            metadata = json.load(f)
            
        return {
            "model_type": "glb",
            "model_path": str(output_path),
            "bounding_box": metadata.get("bbox", []),
            "textures": metadata.get("textures", [])
        }
