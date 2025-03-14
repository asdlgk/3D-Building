import { useDropzone } from 'react-dropzone';
import { uploadChunk } from '../../services/api';

export default function Uploader({ onProgress }) {
  const { getRootProps, getInputProps } = useDropzone({
    accept: {'image/*': ['.jpg', '.png']},
    maxSize: 100 * 1024 * 1024, // 100MB
    onDrop: async files => {
      const file = files;
      const chunkSize = 5 * 1024 * 1024; // 5MB分块
      const totalChunks = Math.ceil(file.size / chunkSize);
      
      for (let i = 0; i < totalChunks; i++) {
        const chunk = file.slice(i * chunkSize, (i+1)*chunkSize);
        const formData = new FormData();
        formData.append('file', chunk);
        formData.append('chunkIndex', i);
        formData.append('totalChunks', totalChunks);
        formData.append('fileId', file.name + Date.now());

        await uploadChunk(formData, progress => {
          onProgress((i / totalChunks) + (progress.loaded / progress.total) * (1 / totalChunks))
        });
      }
    }
  });

  return (
    <div {...getRootProps()} className="dropzone">
      <input {...getInputProps()} />
      <p>拖拽图片至此或点击上传</p>
    </div>
  )
}
