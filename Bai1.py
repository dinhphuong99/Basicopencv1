import cv2
img = cv2.imread("Lighthouse.jpg")

# img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

img2 = img[200:500,100:600]

cv2.imshow("Image",img)
cv2.imshow("Image2",img2)
cv2.waitKey()