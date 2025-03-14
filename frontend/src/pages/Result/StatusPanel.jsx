import { useContext } from 'react';
import { useAppContext } from '../../contexts/AppContext';

export default function StatusPanel() {
  const { state } = useAppContext();
  const metadata = state.currentTask.metadata || {};

  return (
    <div className="status-panel">
      <h3>模型生成详情</h3>
      <div className="metadata-grid">
        <div className="metadata-item">
          <label>状态:</label>
          <span>{state.currentTask.status}</span>
        </div>
        <div className="metadata-item">
          <label>多边形数量:</label>
          <span>{metadata.polygons || 'N/A'}</span>
        </div>
        <div className="metadata-item">
          <label>顶点数量:</label>
          <span>{metadata.vertices || 'N/A'}</span>
        </div>
        <div className="metadata-item">
          <label>场景分类:</label>
          <span>{metadata.scene_type || '未识别'}</span>
        </div>
      </div>
    </div>
  );
}
