import { useContext } from 'react';
import { useAppContext } from '../../contexts/AppContext';
import Uploader from '../../components/Uploader';
import CameraGuide from './CameraGuide';

export default function HomePage() {
  const { dispatch } = useAppContext();
  
  const handleUploadStart = () => {
    dispatch({ type: 'START_TASK' });
  };
  
  const handleUploadSuccess = (taskId) => {
    window.location.href = `/result/${taskId}`;
  };

  return (
    <div className="home-container">
      <h1>校园场景3D建模平台</h1>
      <div className="upload-section">
        <Uploader 
          onUploadStart={handleUploadStart}
          onUploadSuccess={handleUploadSuccess}
        />
        <CameraGuide />
      </div>
    </div>
  );
}
