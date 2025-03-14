import json
import numpy as np
from pathlib import Path
from .base_adapter import AlgorithmAdapter
from typing import Dict, Any

class Wonder3DAdapter(AlgorithmAdapter):
    """处理Wonder3D的网格生成算法"""
    
    def build_command(self, input_path: str, output_dir: str) -> str:
        return (
            f"source /workspace/venv/bin/activate && "
            f"python inference.py --image {input_path} "
            f"--output {output_dir} --format gltf --resolution 2048"
        )

    def process_output(self, output_dir: str) -> Dict[str, Any]:
        output_path = next(Path(output_dir).glob("*.gltf"))
        material_files = list(Path(output_dir).glob("*.bin"))
        
        with open(output_path.with_suffix('.json')) as f:
            metadata = json.load(f)
            
        return {
            "model_type": "gltf",
            "model_path": str(output_path),
            "metadata": {
                "textures": [str(p) for p in Path(output_dir).glob("*.png")],
                "materials": [str(p) for p in material_files],
                "bounding_box": metadata.get("bbox", [0,0,0,1,1,1])
            }
        }
