#%%
from cv2 import cv2
import os, sys
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from keras.preprocessing import image
import keras
import serial

#%%
ser = serial.Serial('com6', 9600) # com 需依照 Arduino 序列埠調整

#%%
########################### 在圖上顯示方框並擷取內容說明 ###########################
x1 = 230
y1 = 210
x2 = 415
y2 = 365

#%%
########################### 在圖上顯示方框並擷取內容說明 ###########################

########################### 即時擷取方框內影像 ###########################

#%%
IMAGE_SIZE = (224, 224)
cap = cv2.VideoCapture(1)

#%%
########################### 解決 keras 讀取 model 的 bug ###########################
import json
import h5py

def fix_layer0(filename, batch_input_shape, dtype):
    with h5py.File(filename, 'r+') as f:
        model_config = json.loads(f.attrs['model_config'].decode('utf-8'))
        layer0 = model_config['config']['layers'][0]['config']
        layer0['batch_input_shape'] = batch_input_shape
        layer0['dtype'] = dtype
        f.attrs['model_config'] = json.dumps(model_config).encode('utf-8')

fix_layer0('Savemodel/model/model.h5', [None, 224, 224, 3], 'float32')

########################### 解決 keras 讀取 model 的 bug ###########################

# 讀取 model
model = keras.models.load_model('/model.h5')
model.summary()

#%%
########################### 即時擷取方框內影像 ###########################
text = "" # 文字初始化

while(True):
    ret, frame = cap.read()
    frame = cv2.flip(frame,1) # 影像鏡像 => WebCam 的影像是相反的

    # 畫出圖上的方框
    rec_frame = cv2.rectangle(frame, (x1, y1), (x2, y2), (0,0,255), 2)
    
    # 取得 img_array 中間方框的內容
    rec_frame_array = rec_frame[y1:y2, x1:x2] # 取 numpy 中間值

    im_rgb = cv2.cvtColor(rec_frame_array, cv2.COLOR_BGR2RGB)
    img_1 = cv2.resize(im_rgb, IMAGE_SIZE, 1) # resize 
    img_2 = image.img_to_array(img_1) # 轉換成 numpy(這步可不執行)
    img_3 = np.expand_dims(img_2, axis=0) # 轉換為 4 維
    img_4 = img_3/255.0 # Normalize

    # 辨識
    preds = model.predict(img_4)

    close = preds[0][0]*100
    up = preds[0][4]*100
    down = preds[0][1]*100
    left = preds[0][2]*100
    right = preds[0][3]*100


    if close > 80 : 
        ser.write(b'0\n')
        text = "Close !"
        print(text)
    elif up > 80 :
        ser.write(b'8\n')
        text = "Up !"
        print(text)
    elif down > 80 :
        ser.write(b'2\n')
        text = "Down !"
        print(text)
    elif left > 80 :
        ser.write(b'4\n')
        text = "Left !"
        print(text)
    elif right > 80 :
        ser.write(b'6\n')
        text = "Right !" 
        print(text)

    cv2.rectangle(rec_frame, (0, 0), (240, 70), (255, 255, 255), -1)
    cv2.putText(rec_frame, text, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 2, cv2.LINE_AA)
   
    cv2.namedWindow("frame",0)
    cv2.imshow('frame', rec_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

########################### 即時擷取方框內影像 ###########################
#%%