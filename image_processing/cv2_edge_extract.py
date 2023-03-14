import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
img = cv.imread('C:/Users/David01/Desktop/t/test/0000.png')
edges = cv.Canny(img,100,200)
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
dst = 255 - edges

cv.imwrite('C:/Users/David01/Desktop/t/test/0000_edge.png', dst)
"""
plt.subplot(121),plt.imshow(img,cmap = 'gray')
plt.title('Original Image'), plt.xticks([]), plt.yticks([])
plt.subplot(122),plt.imshow(dst,cmap = 'gray')
plt.title('Edge Image'), plt.xticks([]), plt.yticks([])
plt.show()
"""