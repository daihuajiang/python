import cv2
import numpy as np

#讀取圖片
filename = 'D:\\dataset\\handwrite_sample\\origin\\test\\1.jpg'

#四個外邊裁切範圍大小設定
left_width=140
right_width=300
top_height=200
bottom_height=300

#讀取檔案
img = cv2.imread(filename)
img_width=img.shape[0]
img_height=img.shape[1]
#img=img[left_width:img_width-right_width,top_height:img_height-bottom_height]
cv2.imshow('img', img)

#轉成灰階
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#cv2.imshow('gray', gray)

#二值化
_,binary = cv2.threshold(gray,200,255,cv2.THRESH_BINARY)
#cv2.imshow('bin',binary)

#影像侵蝕
kernel = np.ones((2,2), np.uint8)
centerradius = 1
kernel = cv2.circle(kernel, (centerradius,centerradius), centerradius, (1,1,1),-1, cv2.LINE_4)

erode = cv2.erode(binary,kernel = kernel, iterations = 1)
cv2.imshow('ero',erode)

#尋找角點
erode = np.float32(erode)
dst = cv2.cornerHarris(erode, 2 , 5 , 0.01)

img[dst > 0.01*dst.max()] - [0, 0, 255]
cv2.imshow('dst',dst)


#_,binary_dst = cv2.threshold(dst,100,255,cv2.THRESH_BINARY)
#cv2.imshow('dst2',binary_dst)
#print(binary_dst.shape)

#4個角落的座標初始設定
corner_topleft = ( img_width,img_height)
corner_topright = (0, img_height)
corner_bottomleft= (img_width, 0)
corner_bottomright = (0, 0)

#print(binary_dst)

#找出4個角的座標
for i in range(dst.shape[0]):
    for j in range(dst.shape[1]):
        
        #print(" -- Refined Corner [", i, "]  (", dst[i,0], ",", dst[i,0], ")")
        if dst[i][j] != 0:
            if i < corner_topleft[0] and j < corner_topleft[1]:
                corner_topleft = (i, j)
                
            if i > corner_topright[0] and j < corner_topright[1]:
                corner_topright = (i , j)
                
            if i < corner_bottomleft[0] and j > corner_bottomleft[1]:
                corner_bottomleft = (i , j)
                
            if i > corner_bottomright[0] and j > corner_bottomright[1]:
                corner_bottomright = (i , j)

print('corner_topleft', corner_topleft)
print('corner_topright', corner_topright)  
print('corner_bottomleft', corner_bottomleft)
print('corner_bottomright', corner_bottomright)    
  
#print(len(dst))

#dst = cv2.resize(dst, (600, 860))
#img = cv2.resize(img, (600, 860))

#cv2.imshow('dst',dst)


cv2.waitKey(0)
cv2.destroyAllWindows()
