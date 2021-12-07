#%%
######################### 導入套件（Start） ##########################
import os, sys
from keras import layers
import pandas as pd
import numpy as np
from cv2 import cv2
######################### 導入套件（End） ##########################

#%%
######################### 基本設定（Start） ##########################

# 資料路徑
IMG_PATH = "training_data"

# 影像大小
IMAGE_SIZE = (224, 224)

# 影像類別數
NUM_CLASSES = 5

# 若 GPU 記憶體不足，可調降 batch size 或凍結更多層網路
BATCH_SIZE = 16

######################### 基本設定（End） ##########################

#%%
######################### 資料處理（Start） ##########################
from keras.preprocessing.image import ImageDataGenerator

# 訓練資料 Normalization & 擴增
train_datagen = ImageDataGenerator(rescale=1./255,              # Normalization
                                   rotation_range=5,            # 隨機旋轉
                                   brightness_range=[0.2, 1.8], # 隨機調整亮度
                                   width_shift_range=0.01,      # 隨機左右平移
                                   height_shift_range=0.01,     # 隨機上下平移
                                   zoom_range=[0.9, 1.1],       # 隨機縮放
                                   fill_mode="constant"         # 補齊因擴增而導致的空缺
                                   )        

# 訓練資料讀取
train_batches = train_datagen.flow_from_directory(IMG_PATH + '/train',
                                                  target_size=IMAGE_SIZE,
                                                  class_mode='categorical',
                                                  shuffle=True,
                                                  batch_size=BATCH_SIZE)

# 驗證資料 Normalization
valid_datagen = ImageDataGenerator(rescale=1./255)

# 驗證資料讀取
valid_batches = valid_datagen.flow_from_directory(IMG_PATH + '/valid',
                                                  target_size=IMAGE_SIZE,
                                                  class_mode='categorical',
                                                  shuffle=False,
                                                  batch_size=BATCH_SIZE)


# 顯示 label
print(train_batches.class_indices)

######################### 資料處理（End） ##########################


#%%
########################## 模型建構（Start） ##########################

# 導入訓練用套件
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers.normalization import BatchNormalization
from keras.layers import Conv2D, MaxPool2D, ZeroPadding2D
from keras.optimizers import SGD, Adam

import keras

#%%
vgg16_model = keras.applications.vgg16.VGG16() # 讀取 vgg16

model = Sequential()

# 加載 vgg16 到自己的模型
for layer in vgg16_model.layers[:-1]: # 除了最後一層 1000 的分類
    model.add(layer)

model.summary()

#%%
# 凍結預訓練權重
for layer in model.layers:
    layer.trainable = False

# 添加自己分類數量到最後一層
model.add(Dense(NUM_CLASSES, activation='softmax'))

#%%

# 將最後 3 層可訓練

model.layers[-3].trainable = True # 4096 : 全連接層
model.layers[-2].trainable = True # 4096 : 全連接層
model.layers[-1].trainable = True #    5 : 分類層(最後一層)

model.summary()

########################## 模型建構（End） ##########################


#%%
########################## 訓練模型（Start）##########################
adam = Adam(lr = 0.0001)
model.compile(loss='categorical_crossentropy',
              optimizer = adam,
              metrics=['accuracy'])

#%%

# 訓練 5 回
NUM_EPOCHS = 5

train_history = model.fit_generator(train_batches,
                        steps_per_epoch = train_batches.samples // BATCH_SIZE,
                        validation_data = valid_batches, 
                        validation_steps = valid_batches.samples // BATCH_SIZE,
                        epochs = NUM_EPOCHS)

########################## 訓練模型（End）##########################

                                                                                                                                                                                                                                                                     #%%
########################## 儲存模型 & 權重（Start）##########################

#%%
save_path = "SaveModel/"

save_model_name = save_path + "model/model.h5"
save_weight_name = save_path + "weight/weight.h5"

model.save(save_model_name)
model.save_weights(save_weight_name)

print("Saved model to disk")

########################## 儲存模型 & 權重（End）##########################
#%%