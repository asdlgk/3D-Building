import React, { useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { uploadImage } from '../../services/api';

export default function Uploader({ onUploadStart, onUploadSuccess }) {
  const onDrop = useCallback(async (acceptedFiles) => {
    const file = acceptedFiles;
    if (!file) return;

    try {
      onUploadStart();
      const response = await uploadImage(file);
      onUploadSuccess(response.data.task_id);
    } catch (error) {
      console.error('Upload failed:', error);
    }
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.png', '.jpg', '.jpeg']
    },
    maxFiles: 1
  });

  return (
    <div {...getRootProps()} className={`dropzone ${isDragActive ? 'active' : ''}`}>
      <input {...getInputProps()} />
      {isDragActive ? (
        <p>释放文件开始上传...</p>
      ) : (
        <p>拖拽图片至此，或点击选择文件</p>
      )}
    </div>
  );
}
