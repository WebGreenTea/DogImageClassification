import cv2
import numpy as np  
import tensorflow as tf
from keras.models import load_model
import os
from pathlib import Path

class AI():
    def __init__(self):
        #self.ListPath = ListPath
        pass

    def getResultList(self,ListPath,label,modelpath,raw=1):
        data = self.preprocess(ListPath)
        model = load_model(modelpath)
        probability_model = tf.keras.Sequential([model])
        ans = probability_model.predict(data)
        resultRaw = []
        for i in ans:
            resultRaw.append(np.argmax(i))
        if(raw):
            return resultRaw
        result = []
        for rawRe in resultRaw:
            result.append(label[rawRe])
        return result


    def preprocess(self,ListPath):
        data = []
        for path in ListPath:
            img = cv2.imread(str(path))
            img = cv2.resize(img,(100,100))
            if len(img.shape) > 2 and img.shape[2] == 4:
                img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            data.append(img)
        data = np.array(data)
        data = data / 255.0
        return data

