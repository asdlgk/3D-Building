from abc import ABC, abstractmethod

class BaseAdapter(ABC):
    @property
    @abstractmethod
    def SUPPORTED_FORMATS(self):
        pass

    @abstractmethod
    def preprocess(self, input_path):
        """输入数据预处理"""
        pass

    @abstractmethod
    def convert_output(self, output_path):
        """输出结果格式转换"""
        pass

    @abstractmethod
    def cleanup(self):
        """释放计算资源"""
        pass
