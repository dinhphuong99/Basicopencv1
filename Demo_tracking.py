import cv2
import time
import numpy as np

def Mouse_event(event, x, y, f, img):

    if event == cv2.EVENT_LBUTTONDOWN:
        Mouse_event.x0 = x
        Mouse_event.y0 = y
        Mouse_event.draw = True
    if event == cv2.EVENT_LBUTTONUP:
        Mouse_event.x1 = x
        Mouse_event.y1 = y
        Mouse_event.draw = False
        miny = min(Mouse_event.y0,Mouse_event.y1)
        maxy = max(Mouse_event.y0, Mouse_event.y1)

        minx = min(Mouse_event.x0, Mouse_event.x1)
        maxx = max(Mouse_event.x0, Mouse_event.x1)
        Mouse_event.img = img[miny:maxy,minx:maxx]

        Mouse_event.track_window = minx, miny, maxx - minx, maxy - miny
    if event == cv2.EVENT_MOUSEMOVE:
        Mouse_event.x = x
        Mouse_event.y = y


Mouse_event.img = None
Mouse_event.x0 =0
Mouse_event.y0 =0
Mouse_event.x1 =0
Mouse_event.y1 =0
Mouse_event.x =0
Mouse_event.y =0
Mouse_event.draw = False
Mouse_event.track_window = None




cap = cv2.VideoCapture("tracking.mp4")
fps = cap.get(cv2.CAP_PROP_FPS)
wait_time = 1000/fps
print fps

play = True
term_crit = ( cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1 )
while True:
    pre_time = time.time()

    if play:
        ret, img = cap.read()
    if img is None:
        img = temp_img
    else:
        temp_img = img
    img_clone = img.copy()

    if Mouse_event.draw:
        img_clone = cv2.rectangle(img_clone,(Mouse_event.x0,Mouse_event.y0),(Mouse_event.x,Mouse_event.y),(0,0,255),2)
    if Mouse_event.img is not None:
        roi_img = Mouse_event.img
        roi_hsv = cv2.cvtColor(roi_img,cv2.COLOR_BGR2HSV)
        img_hsv =cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
        edge = cv2.Canny(roi_img,0,255)
        ret0 ,contours ,ret1 = cv2.findContours(edge,cv2.RETR_CCOMP,cv2.CHAIN_APPROX_NONE)
        mask = np.zeros((roi_img.shape), np.uint8)


        for e in contours:
            e = cv2.convexHull(e)
            mask = cv2.drawContours(mask,[e],0,(255,255,255),-1)




        mask = mask[:,:,0]
        mask = cv2.erode(mask,np.ones((1,1)))
        res = cv2.bitwise_and(roi_img,roi_img,mask=mask)
        roi_hist = cv2.calcHist([roi_hsv],[0],mask,[180],[0,180])
        cbp = cv2.calcBackProject([img_hsv],[0],roi_hist,[0,180],5)

        # apply meanshift to get the new location

        ret, Mouse_event.track_window = cv2.meanShift(cbp, Mouse_event.track_window, term_crit)
        # Draw it on image
        x, y, w, h = Mouse_event.track_window
        cv2.rectangle(img_clone, (x, y), (x + w, y + h), (255,255,0), 2)


        cv2.imshow("Sample", res)

        cv2.imshow("Compare",cbp )
    cv2.imshow("Video", img_clone)
    cv2.setMouseCallback("Video",Mouse_event,img)

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
