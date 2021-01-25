import cv2
import time
import numpy as np


def Min_H(pos):
    Min_H.value = pos
Min_H.value = 33

def Min_S(pos):
    Min_S.value = pos
Min_S.value = 50

def Min_V(pos):
    Min_V.value = pos
Min_V.value = 62

def Max_H(pos):
    Max_H.value = pos
Max_H.value = 102

def Max_S(pos):
    Max_S.value = pos
Max_S.value = 255

def Max_V(pos):
    Max_V.value = pos
Max_V.value = 248

def Zoom(pos):
    if pos < 1:
        pos =1
    Zoom.value = pos
Zoom.value = 1

cv2.namedWindow("Control")
cv2.createTrackbar("Min H", "Control", 33, 255, Min_H)
cv2.createTrackbar("Min S", "Control", 50, 255, Min_S)
cv2.createTrackbar("Min V", "Control", 62, 255, Min_V)

cv2.createTrackbar("Max H", "Control", 102, 255, Max_H)
cv2.createTrackbar("Max S", "Control", 255, 255, Max_S)
cv2.createTrackbar("Max V", "Control", 248, 255, Max_V)
cv2.createTrackbar("Zoom", "Control", 1, 10, Zoom)
trump = cv2.imread("trump.jpg")
cap = cv2.VideoCapture("tracking.mp4")
fps = cap.get(cv2.CAP_PROP_FPS)
wait_time = 1000 / fps

print fps
play = True
delta_time = 0
arr_point = np.array((),np.int32)
while True:
    pre_time = time.time()

    if play:
        ret, img = cap.read()
    if img is None:
        img = temp_img
    else:
        temp_img = img
    img_clone = img.copy()
    cv2.imshow("Control", cv2.putText(img_clone.copy(),"%.2f (ms)" %delta_time,(10,30),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2))
    img_hsv = cv2.cvtColor(img_clone, cv2.COLOR_BGR2HSV)
    lower = np.array([Min_H.value, Min_S.value, Min_V.value])
    upper = np.array([Max_H.value, Max_S.value, Max_V.value])
    mask = cv2.inRange(img_hsv, lower, upper)


    kernel = np.ones((5, 5))
    mask = cv2.erode(mask, kernel)
    mask = cv2.dilate(mask, kernel, iterations=2)

    image, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) > 0:
        tmp_c = contours [0]
        x,y,w,h = cv2.boundingRect(tmp_c)
        w = w*Zoom.value
        h = h*Zoom.value
        res = img_clone
        if (y+h >= res.shape[0]):
            h=res.shape[0] - y
        if (x+w >= res.shape[1]):
            w=res.shape[1] - x
        trump_clone = cv2.resize(trump.copy(),(w,h))


        res[y:y+h,x:x+w,:] = trump_clone




    else:
        res = img_clone



    cv2.imshow("Result", res)








    delta_time = (time.time() - pre_time) * 1000
    if delta_time > wait_time:
        delay_time = 1
    else:
        delay_time = wait_time - delta_time
    key = cv2.waitKey(int(delay_time))
    if key == ord('q'):
        break
    if key == ord(' '):
        play = not play
cv2.destroyAllWindows()
