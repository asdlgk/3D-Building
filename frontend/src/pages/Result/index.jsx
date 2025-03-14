import { useParams } from 'react-router-dom'
import { useAppContext } from '../../contexts/AppContext'
import ModelViewer from './ModelViewer'
import StatusPanel from './StatusPanel'
import { useEffect } from 'react'
import { getTaskStatus } from '../../services/api'

export default function ResultPage() {
  const { taskId } = useParams()
  const { state, dispatch } = useAppContext()

  useEffect(() => {
    const fetchTask = async () => {
      try {
        const data = await getTaskStatus(taskId)
        dispatch({ 
          type: 'UPDATE_PROGRESS', 
          payload: data 
        })
      } catch (error) {
        console.error('获取任务状态失败:', error)
      }
    }

    const interval = setInterval(fetchTask, 3000)
    return () => clearInterval(interval)
  }, [taskId])

  return (
    <div className="result-container grid md:grid-cols-[1fr_300px] gap-6 h-[calc(100vh-80px)]">
      <div className="model-viewer bg-gray-50 rounded-xl p-4">
        {state.currentTask.modelUrl ? (
          <ModelViewer modelUrl={state.currentTask.modelUrl} />
        ) : (
          <div className="flex items-center justify-center h-full">
            <p className="text-gray-500">模型加载中...</p>
          </div>
        )}
      </div>
      
      <div className="status-panel overflow-y-auto">
        <StatusPanel />
      </div>
    </div>
  )
}
