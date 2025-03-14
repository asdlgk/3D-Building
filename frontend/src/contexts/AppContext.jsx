import React, { createContext, useContext, useReducer } from 'react';
import { toast } from 'react-toastify';

const AppContext = createContext();

const initialState = {
  currentTask: null,
  userSession: {
    token: localStorage.getItem('authToken') || null,
    recentTasks: JSON.parse(localStorage.getItem('recentTasks')) || []
  },
  modelViewerSettings: {
    ambientLight: 0.5,
    showWireframe: false
  }
};

function reducer(state, action) {
  switch (action.type) {
    case 'START_TASK':
      return {
        ...state,
        currentTask: {
          id: action.payload.taskId,
          status: 'processing',
          progress: 0
        }
      };
    case 'UPDATE_PROGRESS':
      return {
        ...state,
        currentTask: {
          ...state.currentTask,
          progress: action.payload.progress,
          status: action.payload.status
        }
      };
    case 'SAVE_SESSION':
      localStorage.setItem('authToken', action.payload.token);
      localStorage.setItem('recentTasks', JSON.stringify(action.payload.tasks));
      return {
        ...state,
        userSession: {
          ...state.userSession,
          ...action.payload
        }
      };
    default:
      return state;
  }
}

export function AppProvider({ children }) {
  const [state, dispatch] = useReducer(reducer, initialState);

  return (
    <AppContext.Provider value={{ state, dispatch }}>
      {children}
    </AppContext.Provider>
  );
}

export const useAppContext = () => useContext(AppContext);
