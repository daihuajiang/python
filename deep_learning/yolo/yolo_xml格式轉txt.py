#!/usr/bin/env python
# coding: utf-8

# In[10]:


import xml.etree.ElementTree as ET
import pickle
import os
from os import listdir, getcwd
from os.path import join

#classes = ["aeroplane", "bicycle", "bird", "boat", "bottle"]
classes = ["blue", "green", "red", "yellow"]#（改！）自己要測的目標類別


def convert(size, box):
    dw = 1./(size[0])
    dh = 1./(size[1])
    x = (box[0] + box[1])/2.0 - 1
    y = (box[2] + box[3])/2.0 - 1
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)

def convert_annotation(image_id):
    in_file = open('D:/test/blockcolor/Annotations/yellow/%s.xml'%(image_id))#（改！）自己的圖像標籤xml文件的路徑
    out_file = open('D:/test/blockcolor/txt/yellow/%s.txt'%(image_id), 'w')#（改！）自己的圖像標籤txt文件要保存的路徑
    tree=ET.parse(in_file)#直接解析xml文件
    root = tree.getroot()#獲取xml文件的根節點
    size = root.find('size')#獲取指定節點“圖像尺寸”
    w = int(size.find('width').text)#獲取圖像寬
    h = int(size.find('height').text)#圖像高

    for obj in root.iter('object'):
        difficult = obj.find('difficult').text#xml裏的difficult參數
        cls = obj.find('name').text#要檢測的類別名稱name
        if cls not in classes or int(difficult)==1:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
        bb = convert((w,h), b)
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')


#用VOC數據集的話，是將VOCdevkit/VOC2007/ImageSets/Main/文件夾下的所有txt都循環讀入了
#這裏我只讀入所有待訓練圖像的路徑list.txt
image_paths = open('D:/test/blockcolor/ImageSets/Main/train.txt').read().strip().split()#（改！）
#list_file = open('train.txt', 'w')
for image_path in image_paths:
    #list_file.write('/root/darknet-master/data/obj/%s.jpg\n'%(image_id))
    image_id=os.path.split(image_path)[1]#image_id內容類似'0001.jpg'
    image_id2=os.path.splitext(image_id)[0]#image_id2內容類似'0001'
    convert_annotation(image_id2)


# In[ ]:




