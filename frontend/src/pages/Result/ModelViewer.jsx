import { useEffect, useRef } from 'react';
import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/GLTFLoader.js';

export default function ModelViewer({ modelUrl }) {
  const containerRef = useRef();
  const sceneRef = useRef(new THREE.Scene());
  const rendererRef = useRef();
  
  useEffect(() => {
    // 初始化渲染器
    rendererRef.current = new THREE.WebGLRenderer({ antialias: true });
    rendererRef.current.setSize(800, 600);
    containerRef.current.appendChild(rendererRef.current.domElement);

    // 设置相机
    const camera = new THREE.PerspectiveCamera(75, 800/600, 0.1, 1000);
    camera.position.z = 5;

    // 添加环境光
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
    sceneRef.current.add(ambientLight);

    // 加载模型
    if (modelUrl) {
      new GLTFLoader().load(modelUrl, gltf => {
        sceneRef.current.add(gltf.scene);
        animate();
      });
    }

    // 动画循环
    const animate = () => {
      requestAnimationFrame(animate);
      rendererRef.current.render(sceneRef.current, camera);
    };

    return () => {
      containerRef.current.removeChild(rendererRef.current.domElement);
    };
  }, [modelUrl]);

  return <div ref={containerRef} className="model-viewer-container" />;
}
