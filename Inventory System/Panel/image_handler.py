import cv2
import numpy as np
import os
import shutil

dilation_kernel = np.ones((7,7), np.uint8)
blur_kernel = (5,5)
fgbg = cv2.createBackgroundSubtractorMOG2()

images_dir = "/media/gufran/GsHDD/Work/Projects/InventoryManagementSystem/Panel/Images"

def process(img):
    img = cv2.blur(img, blur_kernel)
    fgmask = fgbg.apply(img)
    dilated_mask = cv2.dilate(fgmask,dilation_kernel,iterations = 15)

    rows, cols, _ = img.shape
    black_bg = np.zeros((rows, cols, 1), dtype = "uint8")
    foreground = cv2.bitwise_or(img, img, mask = dilated_mask)

    output = foreground + black_bg

    return output

def save_images(imgs, identifier_no):
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

def del_last_entry(item_name):
    l = os.listdir(images_dir+"/"+item_name)
    shutil.rmtree(images_dir+"/"+item_name+"/"+str(len(l)), ignore_errors=True)

def handle_register_abort(item_name):
    shutil.rmtree(images_dir+"/"+item_name, ignore_errors=True)


'''
---------------------------------------------------------------------------------

dilation_kernel = np.ones((7,7), np.uint8)
blur_kernel = (5,5)

fgbg = cv2.createBackgroundSubtractorMOG2()
cap = cv2.VideoCapture(0)

while True:
    img = cv2.flip(cap.read()[1], 1)
    img = cv2.blur(img, blur_kernel)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    fgmask = fgbg.apply(img)
    dilated_mask = cv2.dilate(fgmask,dilation_kernel,iterations = 15)

    rows, cols, channels = img.shape
    black_bg = np.zeros((rows, cols, 1), dtype = "uint8")
    foreground = cv2.bitwise_or(img, img, mask = dilated_mask)

    output = foreground + black_bg
    cv2.imshow('res', output)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()
'''