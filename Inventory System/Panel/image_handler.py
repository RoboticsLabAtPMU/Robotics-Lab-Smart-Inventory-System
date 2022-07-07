import cv2
import numpy as np
import os
import shutil

dilation_kernel = np.ones((7,7), np.uint8)
blur_kernel = (5,5)
fgbg = cv2.createBackgroundSubtractorMOG2()

images_dir = "/media/gufran/GsHDD/Work/Projects/Robotics-Lab-Smart-Inventory-System/Inventory System/Panel/Images"
predict_dir = "/media/gufran/GsHDD/Work/Projects/Robotics-Lab-Smart-Inventory-System/Inventory System/Panel/Predict"

def process(img):
    img = cv2.blur(img, blur_kernel)
    fgmask = fgbg.apply(img)
    dilated_mask = cv2.dilate(fgmask,dilation_kernel,iterations = 15)

    rows, cols, _ = img.shape
    black_bg = np.zeros((rows, cols, 1), dtype = "uint8")
    foreground = cv2.bitwise_or(img, img, mask = dilated_mask)

    output = foreground + black_bg

    output = cv2.resize(output, (224,224), interpolation = cv2.INTER_AREA)

    return output

def save_images_from_register(imgs, identifier_no):
    if not os.path.exists(images_dir):
        os.mkdir(images_dir)
    
    if not os.path.exists(images_dir+"/"+imgs[0]["name"]):
        os.mkdir(images_dir+"/"+imgs[0]["name"])

    if os.path.exists(images_dir+"/"+imgs[0]["name"]+"/"+str(identifier_no)):        
        os.rmdir(images_dir+"/"+imgs[0]["name"]+"/"+str(identifier_no))
        
    os.mkdir(images_dir+"/"+imgs[0]["name"]+"/"+str(identifier_no))

    for obj in imgs:
        path = "{dir}/{oname}/{ino}/{oname}{oid}.jpg".format(dir=images_dir,oname=obj["name"],oid=obj["id"],ino=identifier_no)
        cv2.imwrite(path, obj["image"])

def save_images_from_check_io(imgs):
    if os.path.exists(predict_dir):shutil.rmtree(predict_dir)
    os.mkdir(predict_dir)
    
    for obj in imgs:
        path = "{dir}/{oid}.jpg".format(dir=predict_dir,oid=obj["id"])
        cv2.imwrite(path, obj["image"])

def del_last_entry(item_name):
    l = os.listdir(images_dir+"/"+item_name)
    shutil.rmtree(images_dir+"/"+item_name+"/"+str(len(l)), ignore_errors=True)

def handle_register_abort(item_name):
    shutil.rmtree(images_dir+"/"+item_name, ignore_errors=True)