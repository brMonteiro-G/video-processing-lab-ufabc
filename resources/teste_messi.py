import numpy as np
import cv2 as cv

img = cv.imread('messi5.jpg')

cv.imshow('image',img)

k = cv.waitKey(0)

if k == 27:         # wait for ESC key to exit
    cv.destroyAllWindows()
