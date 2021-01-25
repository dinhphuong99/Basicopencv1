import cv2
import time

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




cap = cv2.VideoCapture(0)



while True:
    pre_time = time.time()
    ret,img = cap.read()
    img_lone = img.copy()

    if Mouse_event.draw:
        img_lone = cv2.rectangle(img_lone,(Mouse_event.x0,Mouse_event.y0),(Mouse_event.x,Mouse_event.y),(0,0,255),2)
    if Mouse_event.img is not None:
        cv2.imshow("Sample", Mouse_event.img)
    cv2.imshow("Video", img_lone)
    cv2.setMouseCallback("Video",Mouse_event,img)









    if cv2.waitKey(int (1)) == ord('q'):
        break
cv2.destroyAllWindows()
