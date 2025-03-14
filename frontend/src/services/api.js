import http from './http'

export const api = {
  // 文件上传
  uploadPhotos: async (formData, onUploadProgress) => {
    const response = await http.post('/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
      onUploadProgress: progressEvent => {
        const percent = Math.round(
          (progressEvent.loaded * 100) / progressEvent.total
        )
        onUploadProgress(percent)
      }
    })
    return response.data.taskId
  },

  // 获取任务状态
  getTaskStatus: taskId => http.get(`/tasks/${taskId}`),

  // 下载生成模型
  downloadModel: modelUrl => http.get(`/download/${modelUrl}`, {
    responseType: 'blob'
  }),

  // 场景分类预测
  predictScene: async imageFile => {
    const formData = new FormData()
    formData.append('image', imageFile)
    return http.post('/predict/scene', formData)
  }
}
