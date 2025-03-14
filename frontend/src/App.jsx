import { useEffect } from 'react';
import { Routes, Route, useLocation, useNavigate } from 'react-router-dom';
import { AppProvider } from './contexts/AppContext';
import HomePage from './pages/Home';
import ResultPage from './pages/Result';
import './assets/styles/main.css';

export default function App() {
  const location = useLocation();
  const navigate = useNavigate();

  // 路由守卫
  useEffect(() => {
    const authToken = localStorage.getItem('authToken');
    if (!authToken && location.pathname !== '/login') {
      navigate('/login');
    }
  }, [location]);

  return (
    <AppProvider>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/result/:taskId" element={<ResultPage />} />
      </Routes>
    </AppProvider>
  );
}
