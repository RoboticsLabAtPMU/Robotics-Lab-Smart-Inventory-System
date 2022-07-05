import cv2
import numpy as np

dir = "/home/gufran/Pictures/resistor.jpg"

def empty(a):
    pass



cv2.namedWindow("TrackBars")
cv2.resizeWindow("TrackBars",640,240)
cv2.createTrackbar("Hue Min","TrackBars",0,179,empty)
cv2.createTrackbar("Hue Max","TrackBars",19,179,empty)
cv2.createTrackbar("Sat Min","TrackBars",110,255,empty)
cv2.createTrackbar("Sat Max","TrackBars",240,255,empty)
cv2.createTrackbar("Val Min","TrackBars",153,255,empty)
cv2.createTrackbar("Val Max","TrackBars",255,255,empty)

h_min = cv2.getTrackbarPos("Hue Min","TrackBars")
h_max = cv2.getTrackbarPos("Hue Max", "TrackBars")
s_min = cv2.getTrackbarPos("Sat Min", "TrackBars")
s_max = cv2.getTrackbarPos("Sat Max", "TrackBars")
v_min = cv2.getTrackbarPos("Val Min", "TrackBars")
v_max = cv2.getTrackbarPos("Val Max", "TrackBars")


img = cv2.imread(dir)

white = np.full((img.shape[0], img.shape[1], 3),255, dtype = np.uint8)


img_blur = cv2.GaussianBlur(img, (17,17), 0)
# img_edged= cv2.Canny(img_blur,0,120)
# dilated_img = cv2.dilate(img_edged,(7,7),iterations = 7)
# dilated_inv_img = 255-dilated_img

hsv = cv2.cvtColor(img_blur, cv2.COLOR_BGR2HSV)


lower_black = np.array([0, 0, 0])
upper_black = np.array([180,55,100])

lower_brown = np.array([15,100,40])
upper_brown = np.array([21,255,255])

lower_blue = np.array([60,25,140])
upper_blue = np.array([180,255,255])

# lower_gold = np.array([20,100,100])
# upper_gold = np.array([21,255,255])


black_mask = cv2.inRange(hsv, lower_black, upper_black)
blue_mask = cv2.inRange(hsv, lower_blue, upper_blue)
# gold_mask = cv2.inRange(hsv, lower_gold, upper_gold)




res = cv2.bitwise_and(img, img, mask=black_mask) + cv2.bitwise_and(img, img, mask=blue_mask) + white

cv2.imshow("main",img)
# cv2.imshow("blur",img_blur)
# cv2.imshow("edged",img_edged)
# cv2.imshow("dilated",dilated_img)
# cv2.imshow("dilated inv",dilated_inv_img)
cv2.imshow("hsv",hsv)
cv2.imshow("res",res)

cv2.waitKey(0)
cv2.destroyAllWindows()