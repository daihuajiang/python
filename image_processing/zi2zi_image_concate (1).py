#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Improting Image class from PIL module 
from PIL import Image
  
#圖片路徑
path = "D:/dataset/zi2zi/1110_256_zi2zi/test/test1/infer/2/"
#path = 'D:/dataset/zi2zi/1110_256_zi2zi/test/hanwrite_test/infer/1/'
#圖片儲存路徑
#save_path = path+"poe.jpg"
save_path = path+'out.jpg'

#剪裁後的圖片list
jpg_list = []

# Setting the points for cropped image 
left1 = 0
top1 = 0
right1 = 256
bottom1 = 256

COL = 10 #拼接圖片的行數
ROW = 1 #拼接圖片的列數
UNIT_HEIGHT_SIZE = 256 #圖片高度
UNIT_WIDTH_SIZE = 256 #圖片寬度


# In[2]:


import os
"""
for root, dirs, files in os.walk(path):
    for file in files:
        n=int(os.path.basename(file).split('.')[0])
        os.rename(path+file, path+f'5_{n:04d}.png')
"""
#讀取圖片
for root, dirs, files in os.walk(path):
    for file in files:
        if file.endswith(".jpg") or file.endswith(".png"):
            filename = os.path.join(root, file)
            file_size = os.path.getsize(filename)
            category_name = os.path.basename(root)
            print(filename)
            im = Image.open(filename)
            im1 = im.crop((left1, top1, right1, bottom1))
            jpg_list.append(im)

target = Image.new('RGB', (UNIT_WIDTH_SIZE * COL, UNIT_HEIGHT_SIZE * ROW)) #创建成品图的画布
#第一个参数RGB表示创建RGB彩色图，第二个参数传入元组指定图片大小，第三个参数可指定颜色，默认为黑色
for row in range(ROW):
    for col in range(COL):
        #对图片进行逐行拼接
        #paste方法第一个参数指定需要拼接的图片，第二个参数为二元元组（指定复制位置的左上角坐标）
        #或四元元组（指定复制位置的左上角和右下角坐标）
        target.paste(jpg_list[row+(col*ROW)], (UNIT_WIDTH_SIZE*col, UNIT_HEIGHT_SIZE*row))
target.save(save_path)


# In[ ]:




