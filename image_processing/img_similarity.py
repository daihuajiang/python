# -*- coding: utf-8 -*-
import numpy as np
from skimage.metrics import mean_squared_error, structural_similarity, peak_signal_noise_ratio
import imutils
import cv2

img1_path = 'D:/dataset/zi2zi/1110_256_zi2zi/compare/35_1.png'
img2_path = 'D:/dataset/zi2zi/1110_256_zi2zi/compare/35_2.png'

def MSE(img1_path, img2_path):
    image1 = cv2.imread(img1_path)
    image2 = cv2.imread(img2_path)
    
    gray1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
    
    #score = np.sum((gray1.astype("float") - gray2.astype("float")) ** 2)
    #score /= float(gray1.shape[0] * gray1.shape[1])
    score = mean_squared_error(gray1, gray2)
    
    return score

def SSIM(img1_path, img2_path):
    image1 = cv2.imread(img1_path)
    image2 = cv2.imread(img2_path)
    
    gray1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
    
    score = structural_similarity(gray1, gray2)
    
    return score

def PSNR(img1_path, img2_path):
    image1 = cv2.imread(img1_path)
    image2 = cv2.imread(img2_path)
    
    gray1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
    
    score = peak_signal_noise_ratio(gray1, gray2)
    
    return score
    
    

mse_score = MSE(img1_path, img2_path)
ssim_score = SSIM(img1_path, img2_path)
psnr_score = PSNR(img1_path, img2_path)

print(f'MSE:{mse_score}')
print(f'SSIM:{ssim_score}')
print(f'PSNR:{psnr_score}')
