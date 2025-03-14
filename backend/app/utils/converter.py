import subprocess
import os

def convert_to_glb(input_path, output_dir):
    """将任意3D模型转换为glTF 2.0格式"""
    output_path = os.path.join(
        output_dir,
        f"{os.path.splitext(os.path.basename(input_path))}.glb"
    )
    
    try:
        subprocess.run([
            'ctmconv', 
            input_path, 
            output_path,
            '--format', 'glb'
        ], check=True)
        
        return output_path
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"模型转换失败: {str(e)}")
