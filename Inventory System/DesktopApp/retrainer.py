import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator

import os
import shutil

def retrainer():
  try:
    USB_PATH = "/media/gufran/GsHDD/Work/Projects/Robotics-Lab-Smart-Inventory-System/Inventory System/Panel"
    DATA_DIR = USB_PATH + '/Images'
    TRAIN_DIR = DATA_DIR + '/train'
    MODEL_DIR = USB_PATH+"/Model"

    if os.path.exists(MODEL_DIR): shutil.rmtree(MODEL_DIR)
    os.mkdir(MODEL_DIR)

    if os.path.exists(TRAIN_DIR): shutil.rmtree(TRAIN_DIR)
    os.mkdir(TRAIN_DIR)

    items = []
    items = list(os.listdir(DATA_DIR))
    items.remove("train")

    for i in items:os.mkdir(TRAIN_DIR + "/" + i)

    for item in items:
      item_path = DATA_DIR + "/" + item
      identifier_folders = os.listdir(item_path)

      image_name = 0
      for i in identifier_folders:
        images = os.listdir(item_path+'/'+i)
        for im in images:
          shutil.copy2(item_path+'/'+i+'/'+im, TRAIN_DIR+'/'+item)
          os.rename(TRAIN_DIR+'/'+ item+'/'+im, TRAIN_DIR+'/'+ item +'/'+str(image_name)+".jpg")
          image_name+=1

    train_batches = ImageDataGenerator(preprocessing_function=tf.keras.applications.vgg16.preprocess_input) \
        .flow_from_directory(directory=TRAIN_DIR, target_size=(224, 224), classes=items, batch_size=5)

    mbase = tf.keras.applications.mobilenet_v2.MobileNetV2(input_shape=(224, 224, 3),include_top=False, weights='imagenet')
    mbase.trainable = False

    model = tf.keras.Sequential()
    model.add(mbase)
    model.add(tf.keras.layers.Flatten())
    model.add(tf.keras.layers.Dense(256, activation='relu'))
    model.add(tf.keras.layers.Dense(len(items), activation='softmax'))

    model.compile(optimizer='adam',loss='categorical_crossentropy',metrics=['accuracy'])

    model.fit(
        x=train_batches,
        steps_per_epoch=len(train_batches),
        epochs=5,
        verbose=1    
    )
    model.save(MODEL_DIR+'/model.h5', 'w')

    print("\nModel Saved!")

    with open(MODEL_DIR+ '/labels.txt', 'w') as f:
      f.write("|".join(items))
    
    print("Done!")

    return "Done! You may now safely remove the USB"
  except:
    return "There was an error. Please try again."
