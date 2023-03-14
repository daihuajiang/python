import os
import glob
import cv2
from skimage import morphology
import numpy as np

x=257 #圖像左上x座標
y=0 #圖像左上y座標
w=256 #圖像長度
h=256 #圖像寬度

def modify_contrast_and_brightness2(img, brightness=0 , contrast=100):
    # 上面做法的問題：有做到對比增強，白的的確更白了。
    # 但沒有實現「黑的更黑」的效果
    import math
    
    brightness = 0
    contrast = 250 # - 減少對比度/+ 增加對比度

    B = brightness / 255.0
    c = contrast / 255.0 
    k = math.tan((45 + 44 * c) / 180 * math.pi)

    img = (img - 127.5 * (1 - B)) * k + 127.5 * (1 + B)
      
    # 所有值必須介於 0~255 之間，超過255 = 255，小於 0 = 0
    img = np.clip(img, 0, 255).astype(np.uint8)
    
    return img

    #print("減少對比度 (白黑都接近灰，分不清楚): ")
    #show_img(img)
    
#圖片路徑
pic_dir = "D:\\dataset\\StyTR2\\dataset\\train\\content\\"
pic_dir_save = "D:\\dataset\\StyTR2\\dataset\\train\\content_sk\\"
#讀取資料夾內圖片
paths = glob.glob(os.path.join(pic_dir, "*.jpg"))

for p in paths:
    #cns_code = os.path.basename(p).split("_")[0]
    #label = int(os.path.basename(p).split("_")[1])
    filepath = os.path.basename(p)
    #filename = str(os.path.basename(p).split("_")[2])
    #print("img %s" % p, label)
    #讀取圖片
    image = cv2.imread(p, 0)
    
    # 裁切圖片
    #crop_img = image[y:y+h, x:x+w]
    
    #二值化
    _,binary = cv2.threshold(image,150,255,cv2.THRESH_BINARY_INV)
    
    #binary = modify_contrast_and_brightness2(image)
    #gray2rgb = cv2.cvtColor(binary, cv2.COLOR_GRAY2RGB)
    #cv2.imwrite(pic_dir_save+filepath, gray2rgb)
    
    binary[binary==255] = 1

    skeleton0 = morphology.skeletonize(binary)
    skeleton = skeleton0.astype(np.uint8)*255
    
    #轉成黑字白底
    skinverse = cv2.bitwise_not(skeleton,skeleton)
    gray2rgb = cv2.cvtColor(skinverse, cv2.COLOR_GRAY2RGB)
    
    #label+=6
    #將骨架化字體貼到圖片右邊及儲存
    #image[y:y+h, x:x+w] = skinverse
    #gray2rgb = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
    #cv2.imwrite(pic_dir+str(label)+"_"+filename, gray2rgb)
    #img_filename = pic_dir_save+cns_code+"_"+str(label)+"_"+filename
    img_filename = pic_dir_save+filepath
    
    cv2.imwrite(img_filename, gray2rgb)
    print(img_filename)
    
"""
pic_path = "C:\\Users\\tku-lifelab02\\Desktop\\ex\\sk\\6.jpg"
image = cv2.imread(pic_path, 0)
#二值化
_,binary = cv2.threshold(image,100,255,cv2.THRESH_BINARY_INV)
binary[binary==255] = 1
skeleton0 = morphology.skeletonize(binary)
skeleton = skeleton0.astype(np.uint8)*255
#轉成黑字白底
skinverse = cv2.bitwise_not(skeleton,skeleton)
gray2rgb = cv2.cvtColor(skinverse, cv2.COLOR_GRAY2RGB)
cv2.imwrite("C:\\Users\\tku-lifelab02\\Desktop\\ex\\sk\\7.jpg", gray2rgb)
"""