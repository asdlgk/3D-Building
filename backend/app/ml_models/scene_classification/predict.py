import tensorflow as tf
from PIL import Image
import numpy as np

MODEL_PATH = 'app/ml_models/scene_classification/efficientnetv2_model.h5'
LABELS = ['教学楼', '操场', '绿地', '其他']

# 加载预训练模型
model = tf.keras.models.load_model(MODEL_PATH)

def preprocess_image(image_path, target_size=(384, 384)):
    img = Image.open(image_path).convert('RGB')
    img = img.resize(target_size)
    img_array = tf.keras.preprocessing.image.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0)  # 添加批次维度
    return img_array

def classify_scene(image_path):
    try:
        processed_img = preprocess_image(image_path)
        predictions = model.predict(processed_img)
        confidence = np.max(predictions)
        class_index = np.argmax(predictions)
        
        if confidence < 0.9:
            return "其他", float(confidence)
        return LABELS[class_index], float(confidence)
    except Exception as e:
        print(f"Classification error: {str(e)}")
        return "其他", 0.0
