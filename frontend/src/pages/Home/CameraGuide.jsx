import { Dialog } from '@headlessui/react'
import { useAppContext } from '../../contexts/AppContext'
import examplePhoto from '../../assets/images/photo-example.jpg'

export default function CameraGuide() {
  const { state, dispatch } = useAppContext()

  return (
    <Dialog
      open={state.showCameraGuide}
      onClose={() => dispatch({ type: 'CLOSE_GUIDE' })}
      className="relative z-50"
    >
      <div className="fixed inset-0 bg-black/30" />
      <div className="fixed inset-0 flex items-center justify-center p-4">
        <Dialog.Panel className="w-full max-w-2xl rounded-xl bg-white p-8">
          <Dialog.Title className="text-2xl font-semibold mb-4">
            拍照指引
          </Dialog.Title>
          
          <div className="space-y-4">
            <div className="flex gap-4 items-start">
              <div className="w-24 h-24 bg-gray-100 rounded-lg overflow-hidden">
                <img 
                  src={examplePhoto} 
                  alt="示例照片"
                  className="object-cover h-full w-full"
                />
              </div>
              <div className="flex-1">
                <h4 className="font-medium mb-2">最佳实践</h4>
                <ul className="list-disc pl-6 text-gray-600 space-y-1">
                  <li>保持主体建筑在画面中心</li>
                  <li>相邻照片需有30%重叠区域</li>
                  <li>避免强逆光拍摄</li>
                </ul>
              </div>
            </div>

            <div className="bg-blue-50 p-4 rounded-lg">
              <h4 className="font-medium text-blue-800 mb-2">注意事项</h4>
              <p className="text-blue-700 text-sm">
                拍摄时请保持设备水平，建议使用三脚架稳定手机。环绕建筑拍摄时保持相同高度和距离。
              </p>
            </div>
          </div>

          <div className="mt-6 flex justify-end">
            <button
              onClick={() => dispatch({ type: 'CLOSE_GUIDE' })}
              className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
            >
              开始拍摄
            </button>
          </div>
        </Dialog.Panel>
      </div>
    </Dialog>
  )
}
