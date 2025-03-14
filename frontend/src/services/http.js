import axios from 'axios';
import { toast } from 'react-toastify';

const http = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'multipart/form-data'
  }
});

// 请求拦截器
http.interceptors.request.use(config => {
  const token = localStorage.getItem('authToken');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// 响应拦截器
http.interceptors.response.use(
  response => response.data,
  error => {
    const message = error.response?.data?.error || '网络请求异常，请稍后重试';
    toast.error(message);
    return Promise.reject(error);
  }
);

export default http;
