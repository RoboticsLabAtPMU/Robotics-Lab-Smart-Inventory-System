import tensorflow as tf
import numpy as np
from keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import requests

model_path = "/media/gufran/GsHDD/Work/Projects/Robotics-Lab-Smart-Inventory-System/Inventory System/Panel/Model"
predict_path = "/media/gufran/GsHDD/Work/Projects/Robotics-Lab-Smart-Inventory-System/Inventory System/Panel"

def predict():
    model = tf.keras.models.load_model(model_path+'/model.h5')

    batches = ImageDataGenerator(preprocessing_function=tf.keras.applications.mobilenet_v2.preprocess_input).flow_from_directory(directory=predict_path, target_size=(224,224), classes=["Predict"])
    res = list(model.predict(batches))

    f = open(model_path+'/labels.txt','r')
    labels = list(f.read().split('|'))

    res_pred = np.array(res[0])
    for i in res: res_pred += i

    res_pred=list(res_pred)
    pred_index = res_pred.index(max(res_pred))

    return labels[pred_index]

def check_in(uid, item_name):
    url = 'http://172.16.154.120:8000/checkin'
    data = {"id":uid,"item":item_name}
    x = requests.post(url,data=data)

def check_out(uid, item_name):
    url = 'http://172.16.154.120:8000/checkout'
    data = {"id":uid,"item":item_name}
    x = requests.post(url,data=data)

def register(name, amount):
    url = 'http://172.16.154.120:8000/register'
    data = {"name":name,"amount":amount}
    x = requests.post(url,data=data)

def check_item_existence(name):
    url = 'http://172.16.154.120:8000/item'
    data = {"name":name}
    x = requests.post(url,data=data)

    return x.text
