import cv2
import numpy as np
from PIL import Image
import os
import glob

"""
輸入圖片須為經過2值化且尺寸為2560*3840的圖片，檔名以數字命名(從1開始數)
"""
#檔案路徑
filedir = 'D:/dataset/handwrite_sample/origin/2_binary/'
savedir = 'D:/dataset/handwrite_sample/origin/test/'
savedir2 = 'D:/dataset/handwrite_sample/origin/sample/'

#如果資料夾不存在則創建資料夾
if not os.path.isdir(savedir):
    os.mkdir(savedir)
    
if not os.path.isdir(savedir2):
    os.mkdir(savedir2)

#圖片最終尺寸
img_size = 256

#最後擷取格子時圖片寬跟高減少多少像素(用於去除邊框)
mirgin_crop = 5

#文字大小
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

#將一張寫有150個文字的圖切割成150張圖片的函式
def split_img(filename, savedir):
    img_size = 256
    #讀取檔案
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
    
    """
    #選出需要的輪廓
    pop_count = 0
    for i in range(len(contours)):       
        left, right, top, bottom = find_contour_corner(contours[i])
        #print(left,' ',right,' ',top,' ',bottom)
        
        #如果長或寬太大則不是目標區域
        if right-left > img_size*0.8 or bottom-top > img_size*0.8:
            contours_copy.pop(i-pop_count)
            pop_count += 1
        
        #如果目標太小(可能為雜訊)則不是目標區域
        elif (right-left)*(bottom-top) < 100:
            contours_copy.pop(i-pop_count)
            pop_count += 1
          
    #print(pop_count)    
    """
    contours_copy = list(contours)
    #過濾出表格框線
    contours_copy = []
    pop_count = 0
    for i in range(len(contours)):
        left, right, top, bottom = find_contour_corner(contours[i])
        
        #有足夠長度線段為目標
        if right-left > img_size*0.8 or bottom-top > img_size*0.8:
            contours_copy.append(contours[i])
        
    
    contours_copy = tuple(contours_copy)
    
    #繪製輪廓
    blank_img = np.zeros((3840,2560,3), np.uint8)
    blank_img.fill(255)
    cv2.drawContours(blank_img, contours_copy, -1, (0,0,0),-1)
    #cv2.imwrite(savedir, blank_img)
    
    #顯示圖像
    #cv2.imshow('contour', blank_img)
    
    #將格線加粗之後再侵蝕回去
    kernel = np.ones((3,3), np.uint8)
    blank_img = cv2.erode(blank_img,kernel = kernel, iterations = 2)
    blank_img = cv2.dilate(blank_img,kernel = kernel, iterations = 2)
    
    #轉成灰階
    gray = cv2.cvtColor(blank_img, cv2.COLOR_BGR2GRAY)
    #cv2.imshow('gray', gray)
    
    #二值化
    ret,thresh = cv2.threshold(gray,50,255,cv2.THRESH_BINARY)
    
    #找出表格格子輪廓
    contours2, hierarchy2 = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    #print(contours2[150].shape)
    
    #找出目標格子
    contours_copy = list(contours2)
    pop_count = 0
    for i in range(len(contours2)):
        left, right, top, bottom = find_contour_corner(contours2[i])
            
        #如果長或寬太大則不是目標區域
        if right-left < img_size*0.9 or bottom-top < img_size*0.9:
            contours_copy.pop(i-pop_count)
            pop_count += 1
            
    contours_copy = tuple(contours_copy)
    print(os.path.basename(filename) + ' block number: ',len(contours_copy))
    #繪製輪廓
    #cv2.drawContours(blank_img, contours_copy, -1, (0,0,255),-1)
    #blank_img = cv2.resize(blank_img, (800, 1000))
    
    #顯示圖像
    #cv2.imshow('contour2', blank_img)
    
    #如果找到的區塊數量不是150則不分割圖片
    if len(contours_copy)!=150:
        print('in file '+os.path.basename(filename)+'. block number is not 150. block number: ',len(contours_copy))
        
    else:    
        #獲得格子座標
        block_position = []
        for i in range(len(contours_copy)):
            left, right, top, bottom = find_contour_corner(contours_copy[i])        
            block_position.append([left, right, top, bottom])
        #print(block_position[0][3])
        
        #將座標進行排序
        #先根據左上角x座標排序
        block_position_sortx = sorted(block_position, key= lambda s: s[0])
        
        #每15個座標形成新的列表，根據左上角y座標排序
        block_position_sorty = []
        for i in range(10):
            block_position_sorty.append([])
            
        for i in range(10):
            block_position_sorty[i] = sorted(block_position_sortx[15*i:15*i+15], key= lambda s: s[2])
        
        #依照座標順序填入列表
        block_position = []
        for i in range(15):
            for j in range(10):
                block_position.append(block_position_sorty[j][i])
        
        
        #儲存圖片
        img = Image.open(filename)
        filenum = int(os.path.basename(filename).split(".")[0])
        for i in range(len(block_position)): 
            save_img_name = savedir+str(150*(filenum-1)+i)+'.jpg'
            save_img = img.crop((block_position[i][0]+mirgin_crop, block_position[i][2]+mirgin_crop, block_position[i][1]-mirgin_crop, block_position[i][3]-mirgin_crop))
            save_img.save(save_img_name)

#將圖片調整為256*256的函式
def img_resize(filename, savedir):
    filebasename = os.path.basename(filename)
    #讀取圖片並重塑文字大小及圖片大小
    img = Image.open(filename)
    #計算圖片重塑比例
    width, height = img.size
    length = 0
    if width > height:
        length = width
    else:
        length = height
    
    resize_rate  = word_size/length
    #重塑圖片尺寸
    img.resize((int(width*resize_rate), int(height*resize_rate)))
    blank_img = Image.new('RGB', (img_size, img_size), 'white')
    blank_img.paste(img, (int((img_size-word_size)/2), int((img_size-word_size)/2)))
    blank_img.save(savedir+filebasename)

if __name__=='__main__':
    for p in glob.glob(os.path.join(filedir, "*.jpeg")):
        split_img(p, savedir)
    
    for p in glob.glob(os.path.join(savedir, "*.jpg")):
        img_resize(p, savedir2)
        #print('resize '+os.path.basename(p))
    
    print('finish')  
    #cv2.waitKey()
    #cv2.destroyAllWindows()
    