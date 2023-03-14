import cv2
import numpy as np
from PIL import Image
import os
import glob

#檔案路徑
filedir = 'D:/dataset/zi2zi/20221209test/calligan_rgb/'
savedir = 'D:/dataset/zi2zi/20221209test/calligan/'

#如果資料夾不存在則創建資料夾
if not os.path.isdir(savedir):
    os.mkdir(savedir)

#將圖片二值化
def binary_img(filename):
    filebasename = os.path.basename(filename)
    #讀取檔案
    img = cv2.imread(filename)
    #img = cv2.resize(img, (2560,3840), interpolation=cv2.INTER_AREA)
    #img=img[left_width:img_width-right_width,top_height:img_height-bottom_height]
    #cv2.imshow('img', img)
    
    #轉成灰階
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(savedir+filebasename, gray)
    #cv2.imshow('gray', gray)
    """
    #二值化
    _,binary = cv2.threshold(gray,180,255,cv2.THRESH_BINARY)
    #cv2.imshow('bin',binary)
    
    #模糊(減少圖像中的鋸齒)
    binary = cv2.medianBlur(binary, 3)
    #binary = cv2.equalizeHist(binary)
    
    #影像侵蝕
    kernel = np.ones((2,2), np.uint8)
    centerradius = 1
    kernel = cv2.circle(kernel, (centerradius,centerradius), centerradius, (1,1,1),-1, cv2.LINE_4)
    
    erode = cv2.erode(binary,kernel = kernel, iterations = 1)
    
    #cv2.imshow('ero',erode)
    
    cv2.imwrite(savedir+filebasename, erode)
    """
for p in glob.glob(os.path.join(filedir, "*.jpg")):
    binary_img(p)