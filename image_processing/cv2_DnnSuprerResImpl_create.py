import cv2 
import matplotlib.pyplot as plt 
# 讀取圖片 
img = cv2.imread("metabolic_pathway.jpg") 
img = img[5:60,700:755] 
sr = cv2.dnn_superres.DnnSuperResImpl_create() 
path = "EDSR_x4.pb" 
sr.readModel(path) 
sr.setModel("edsr",4) 
result = sr.upsample(img) 

# 調整圖像大小 
resized = cv2.resize(img,dsize=None,fx=4,fy=4) 
plt.figure(figsize=(12,8)) 
plt.subplot(1,3,1) 

# 原始圖像 
plt.imshow(img[:,:,::-1]) 
plt.subplot(1,3,2) 

# SR上採樣圖像 
plt.imshow(result[:,:,::-1]) 
plt.subplot(1,3,3) 

# OpenCV 上採樣圖像 
plt.imshow(resized[:,:,::-1]) 
plt.show()
