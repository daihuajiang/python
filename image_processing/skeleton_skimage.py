# -*- coding: utf-8 -*-
import numpy as np
from skimage import morphology
from PIL import Image
import cv2 as cv
import os
import glob

def skeleton_demo(image):
    #gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    gray = image
    ret, binary = cv.threshold(gray, 0, 255, cv.THRESH_BINARY | cv.THRESH_OTSU)
    binary[binary == 255] = 1
    skeleton0 = morphology.skeletonize(binary)
    skeleton = skeleton0.astype(np.uint8) * 255
    """
    cv.imshow("skeleton", skeleton)
    cv.waitKey(0)
    cv.destroyAllWindows()
    """
    return skeleton
    
def medial_axis_demo(image):
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    ret, binary = cv.threshold(gray, 0, 255, cv.THRESH_BINARY | cv.THRESH_OTSU)
    binary[binary == 255] = 1
    skel, distance = morphology.medial_axis(binary, return_distance=True)
    dist_on_skel = distance * skel
    skel_img = dist_on_skel.astype(np.uint8)*255
    contours, hireachy = cv.findContours(skel_img, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    img_contour = cv.drawContours(image, contours, -1, (0, 0, 255), 1, 8)
    """
    cv.imshow("result", image)
    cv.waitKey(0)
    cv.destroyAllWindows()
    """
    return img_contour

def morph_find(image):
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    ret, binary = cv.threshold(gray, 0, 255, cv.THRESH_BINARY | cv.THRESH_OTSU)
    kernel = cv.getStructuringElement(cv.MORPH_CROSS, (3, 3))
    finished = False
    size = np.size(binary)
    skeleton = np.zeros(binary.shape, np.uint8)
    while (not finished):
        eroded = cv.erode(binary, kernel)
        temp = cv.dilate(eroded, kernel)
        temp = cv.subtract(binary, temp)
        skeleton = cv.bitwise_or(skeleton, temp)
        binary = eroded.copy()

        zeros = size - cv.countNonZero(binary)
        if zeros == size:
            finished = True

    contours, hireachy = cv.findContours(skeleton, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    img_contour = cv.drawContours(image, contours, -1, (0, 0, 255), 1, 8)
    """
    cv.imshow("skeleton", image)
    cv.waitKey(0)
    cv.destroyAllWindows()
    """
    return img_contour

def thin_demo(image):
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    ret, binary = cv.threshold(gray, 0, 255, cv.THRESH_BINARY | cv.THRESH_OTSU)
    thinned = cv.ximgproc.thinning(binary)
    contours, hireachy = cv.findContours(thinned, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    cv.drawContours(image, contours, -1, (0, 0, 255), 1, 8)
    cv.imshow("thin", image)
    cv.waitKey(0)
    cv.destroyAllWindows()

def revers_color(image):
    #cv.imshow('img', image)
    img_shape = image.shape
    #print(img_shape)
    h = img_shape[0]
    w = img_shape[1]
    # 彩色图像转换为灰度图像（3通道变为1通道）
    #gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    gray = image
    #print(gray.shape)
    # 最大图像灰度值减去原图像，即可得到反转的图像
    dst = 255 - gray
    #cv.imshow('dst', dst)
    #cv.waitKey(0)    
    return dst

#尋找contour列表中每一個元素的角落座標的函式
def find_contour_corner(contours):
    left = contours[0][0][0][0]
    right = contours[0][0][0][0]
    top = contours[0][0][0][1]
    bottom = contours[0][0][0][1]
    
    for i in range(len(contours)):
        for j in range(len(contours[i])):
            if contours[i][j][0][0] < left:
                left = contours[i][j][0][0]
            if contours[i][j][0][0] > right:
                right = contours[i][j][0][0]
            if contours[i][j][0][1] < top:
                top = contours[i][j][0][1]
            if contours[i][j][0][1] > bottom:
                bottom = contours[i][j][0][1]
    
    return left, right, top, bottom

def img_resize(filename, savedir):
    #圖片最終尺寸
    img_size = 256
    #文字大小
    word_size = 240
    
    filebasename = os.path.basename(filename)
    #讀取圖片並重塑文字大小及圖片大小
    img = Image.open(filename)
    #計算圖片重塑比例
    width, height = img.size
    print(img.size)
    length = 0
    if width > height:
        length = width
    else:
        length = height
    
    resize_rate  = word_size/length
    print(resize_rate)
    #重塑圖片尺寸
    img.resize((int(width*resize_rate), int(height*resize_rate)))
        
    blank_img = Image.new('RGB', (img_size, img_size), 'white')
    blank_img.paste(img, (int((img_size-word_size)/2), int((img_size-word_size)/2)))
    blank_img.save(savedir+filebasename)

#image_path = "C:/Users/David01/DGfont/DG-Font-main/data/0106_256/fu_test/fu"
#image_savepath = "C:/Users/David01/DGfont/DG-Font-main/data/0106_256/fu_test/test"
image_path = 'C:/Users/David01/Desktop/t/test/'
image_savepath = 'C:/Users/David01/Desktop/t/test/sk/'
for p in glob.glob(os.path.join(image_path, "*.png")):
    img_basename = os.path.basename(p)
    print(img_basename)
    img = cv.imread(p)
    img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    
    dst = revers_color(img)
    """
    #二值化
    ret,thresh = cv.threshold(img,100,255,cv.THRESH_BINARY_INV)
    
    contours, hireachy = cv.findContours(thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    for i in range(len(contours)):
        left, right, top, bottom = find_contour_corner(contours)
    """
    
    #image_path = "C:/Users/tku-lifelab02/dgfont/dgfont/traindata/1110_256/reverse/id_0/"
    #cv.imwrite(image_path, dst)
    #img = cv.imread(image_path)
    skeleton_img = skeleton_demo(dst)
    #medial_axis_demo(img)
    #morph_find(img)
    #thin_demo(img)
    kernel = np.ones((3,3), np.uint8)
    centerradius = 1
    kernel = cv.circle(kernel, (centerradius,centerradius), centerradius, (3,3,3),-1, cv.LINE_4)
    dilate = cv.dilate(skeleton_img, kernel = kernel, iterations = 1)
    """
    cv.imshow('dilate', dilate)
    cv.waitKey(0)
    cv.destroyAllWindows()
    """
    skeleton_img_reverse = revers_color(dilate)
    img_save_path = image_savepath+img_basename
    cv.imwrite(img_save_path, skeleton_img_reverse)
    #img = Image.open(img_save_path)
    #cropped = img.crop((left-5, top-5, right+5, bottom+5))
    #img_save_path = image_savepath0+img_basename
    #cropped.save(img_save_path)
    
    #img_resize(img_save_path, image_savepath)
