import cv2
import numpy as np
from PIL import Image
import os
import glob

#檔案路徑
filedir = 'D:/dataset/handwrite_sample/origin/test/'
savedir1 = 'D:/dataset/handwrite_sample/origin/test2/'
savedir2 = 'D:/dataset/handwrite_sample/origin/sample/'

if not os.path.isdir(savedir1):
    os.mkdir(savedir1)
    
if not os.path.isdir(savedir2):
    os.mkdir(savedir2)

img_size = 256
word_size = 240

#尋找contour列表中每一個元素的角落座標的函式
def find_contour_corner(contours):
    left = contours[0][0][0]
    right = contours[0][0][0]
    top = contours[0][0][1]
    bottom = contours[0][0][1]
    for j in range(len(contours)):
        if contours[j][0][0] < left:
            left = contours[j][0][0]
        if contours[j][0][0] > right:
            right = contours[j][0][0]
        if contours[j][0][1] < top:
            top = contours[j][0][1]
        if contours[j][0][1] > bottom:
            bottom = contours[j][0][1]
    
    return left, right, top, bottom

#將文字擷取出來並重塑圖片尺寸的函式
def img_word_crop(filename):
    img = cv2.imread(filename)
    img_width , img_height = img.shape[:2]
    #轉成灰階
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #cv2.imshow('gray', gray)
    
    #二值化
    ret,thresh = cv2.threshold(gray,100,255,cv2.THRESH_BINARY_INV)
    #cv2.imshow('bin', thresh)
    
    #找輪廓
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    #選出需要的輪廓
    contours_copy = list(contours)
    pop_count = 0
    
    for i in range(len(contours)):
        left, right, top, bottom = find_contour_corner(contours[i])
                
        #print(left,' ',right,' ',top,' ',bottom)
        """
        #如果長或寬太大則不是目標區域
        if right-left > img_size or bottom-top > img_size:
            contours_copy.pop(i-pop_count)
            pop_count += 1
        """
        #如果目標太小(可能為雜訊)則不是目標區域
        if (right-left)*(bottom-top)<100 :
            contours_copy.pop(i-pop_count)
            pop_count += 1
        
        #去除4邊的黑框
        pixcount = 0
        if left==0 or top==0 or right==img_width or bottom==img_height:
            for j in range(len(contours[i])):
                if contours[i][j][0][0] < 5:
                    pixcount += 1
                if contours[i][j][0][0] > img_width-5:
                    pixcount += 1
                if contours[i][j][0][1] < 5:
                    pixcount += 1
                if contours[i][j][0][1] > img_height-5:
                    pixcount += 1
            
        if pixcount > 15:
            contours_copy.pop(i-pop_count)
            pop_count += 1
        #print(pixcount)
           
          
    #print(pop_count)    
    
    #繪製輪廓
    blank_img = np.zeros((img_width,img_height,3), np.uint8)
    blank_img.fill(255)
    cv2.drawContours(blank_img, contours_copy, -1, (0,0,0),-1)
    #blank_img = cv2.resize(blank_img, (img_size, img_size))
    #顯示圖像
    #cv2.imshow('contour', blank_img)
    #儲存圖片
    filebasename = os.path.basename(filename)
    cv2.imwrite(savedir1+filebasename, blank_img)
    
    
    img = cv2.imread(savedir1+filebasename)
    #轉成灰階
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #cv2.imshow('gray', gray)
    
    #二值化
    ret,thresh = cv2.threshold(gray,100,255,cv2.THRESH_BINARY)
    #cv2.imshow('bin', thresh)
    
    #找輪廓
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    for i in range(len(contours)):
        left, right, top, bottom = find_contour_corner(contours[i])
        
    
    #計算重塑文字大小的比例
    max_left, max_right, max_top, max_bottom = find_contour_corner(contours[0])
    for i in range(len(contours)):
        left, right, top, bottom = find_contour_corner(contours[i])
        if left < max_left:
            max_left = left
        if right > max_right:
            max_right = right
        if top < max_top:
            max_top = top
        if bottom > max_bottom:
            max_bottom = bottom
             
    wordsize = 0
    if max_right-max_left > max_bottom-max_top:
        wordsize = max_right-max_left
    else:
        wordsize = max_bottom-max_top
    
    resize_rate = word_size/wordsize
    #print(resize_rate)
    
    #讀取圖片並重塑文字大小及圖片大小
    img = Image.open(savedir1+filebasename)
    img1 = img.crop((max_left, max_top, max_right, max_bottom))
    img1.resize((int((max_right-max_left)*resize_rate), int((max_bottom-max_top)*resize_rate)))
    blank_img = Image.new('RGB', (img_size, img_size), 'white')
    blank_img.paste(img1, (int((img_size-word_size)/2), int((img_size-word_size)/2)))
    blank_img.save(savedir2+filebasename)

for p in glob.glob(os.path.join(filedir, "*.jpg")):
    img_word_crop(p)
    print(p)

cv2.waitKey()
cv2.destroyAllWindows()
