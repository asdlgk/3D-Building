import { io } from 'socket.io-client';
import { useEffect } from 'react';
import { useAppContext } from '../contexts/AppContext';

const socket = io(import.meta.env.VITE_WS_URL, {
  autoConnect: false,
  reconnectionDelay: 3000,
});

export const useSocket = () => {
  const { dispatch } = useAppContext();
  
  useEffect(() => {
    socket.connect();
    
    const handleTaskUpdate = (data) => {
      dispatch({
        type: 'UPDATE_PROGRESS',
        payload: {
          progress: data.progress,
          status: data.status
        }
      });
    };

    socket.on('task_update', handleTaskUpdate);
    
    return () => {
      socket.off('task_update', handleTaskUpdate);
      socket.disconnect();
    };
  }, [dispatch]);
  
  return { socket };
};
