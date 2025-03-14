# backend/app/ml_models/scene_classification/train.py
import tensorflow as tf
from tensorflow.keras import layers
from tensorflow.keras.preprocessing.image import ImageDataGenerator

def build_model(input_shape=(384, 384, 3), num_classes=4):
    base_model = tf.keras.applications.EfficientNetV2S(
        include_top=False,
        weights='imagenet',
        input_shape=input_shape
    )
    base_model.trainable = False  # 冻结基础模型
    
    inputs = tf.keras.Input(shape=input_shape)
    x = base_model(inputs, training=False)
    x = layers.GlobalAveragePooling2D()(x)
    x = layers.Dense(256, activation='relu')(x)
    outputs = layers.Dense(num_classes, activation='softmax')(x)
    
    return tf.keras.Model(inputs, outputs)

# 数据增强配置
train_datagen = ImageDataGenerator(
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    horizontal_flip=True
)

# 编译模型
model = build_model()
model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

# 开始训练
model.fit(
    train_datagen.flow_from_directory('dataset/train'),
    epochs=10,
    validation_data=ImageDataGenerator().flow_from_directory('dataset/val')
)
