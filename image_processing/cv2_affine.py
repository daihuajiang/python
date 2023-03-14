import cv2 as cv
import numpy as np
from PIL import Image
import os

#圖片檔案路徑
filename = 'D:/dataset/handwrite_sample/origin/2/20.jpeg'

#要進行投影轉換的4個角點
#左上角
corner_topleft = [186,203]
#右上角
corner_topright = [1439,204]
#左下角
corner_bottomleft= [185,2049]
#右下角
corner_bottomright = [1446,2052]

#儲存路徑
filebasename = os.path.basename(filename)
savedir1 = 'D:/dataset/handwrite_sample/origin/2_perspective/'
savefile = savedir1+filebasename
savedir2 = 'D:/dataset/handwrite_sample/origin/2_crop/'
savecrop = savedir2+filebasename

#如果資料夾不存在則創建資料夾
if not os.path.isdir(savedir1):
    os.mkdir(savedir1)

if not os.path.isdir(savedir2):
    os.mkdir(savedir2)

#讀取檔案
img = cv.imread(filename)
rows, cols = img.shape[:2]

#投影轉換後的4個角點
if corner_topleft[0] < corner_bottomleft[0]:
    left = corner_topleft[0]
else:
    left =corner_bottomleft[0]

if corner_topright[0] < corner_bottomright[0]:
    right = corner_bottomright[0]
else:
    right = corner_topright[0]
    
if corner_topleft[1] < corner_topright[1]:
    top = corner_topleft[1]
else:
    top = corner_topright[1]
    
if corner_bottomleft[1] < corner_bottomright[1]:
    bottom = corner_bottomright[1]
else:
    bottom = corner_bottomleft[1]

#投影轉換並儲存
pts1 = np.float32([corner_topleft, corner_topright, corner_bottomleft,corner_bottomright])
pts2 = np.float32([[left,top], [right,top], [left,bottom],[right,bottom]])

M = cv.getPerspectiveTransform(pts1, pts2)

dst = cv.warpPerspective(img, M, (cols, rows))

cv.imwrite(savefile, dst)

#擷取被投影區域圖像並儲存
im = Image.open(savefile)
im = im.crop((left, top, right, bottom))
im.save(savecrop)