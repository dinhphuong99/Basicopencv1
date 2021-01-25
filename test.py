import cv2
import time
cap = cv2.VideoCapture("videomau.mp4")
oimg = cv2.imread("adapth.jpg")


cap.grab()
pre_time = time.time()

ret,img = cap.retrieve(oimg)

print (ret)
cv2.imshow("s",img);
cv2.imshow("oimg",oimg);
print(time.time() - pre_time)
cv2.waitKey() 
cv2.destroyAllWindows()
