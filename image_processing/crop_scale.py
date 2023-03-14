# Improting Image class from PIL module 
import glob
import os
from PIL import Image

#file_path = "D:/dataset/StyTR2/dataset/char/val/"
#save_path1 = "D:/dataset/StyTR2/dataset/val/content/"
#save_path2 = "D:/dataset/StyTR2/dataset/val/style/"
file_path = "C:/Users/David01/DGfont/DG-Font-main/data/dgfonttest/"
save_path1 = "C:/Users/David01/DGfont/DG-Font-main/data/0907/test_handwrite/id_2/"
#save_path2 = "D:/dataset/StyTR2/dataset/val/style/"


for p in glob.glob(os.path.join(file_path, "*.jpg")):
    #cns=os.path.basename(p).split("_")[0]
    #label=int(os.path.basename(p).split("_")[0])
    #filenum=os.path.basename(p).split("_")[1]
    #label+=12
    #filename=str(label)+"_"+filenum
    filename=os.path.basename(p).split(".")[0]
    filename=filename+".png"
    #創建符合模型格式的空白圖片
    #target = Image.new('RGB', (512, 256), 'white')
    img = Image.open(p)
    #img1 = img.crop((0,0,256,256))
    #img2 = img.crop((257,0,512,256))
    img1=img.resize((80,80))
    #img2=img2.resize((250,250))
    #target.paste(img1, (0, 0))
    #target.paste(img2, (257, 0))
    #target.save(save_path+filename)
    img1.save(save_path1+filename)
    #img2.save(save_path1+filename)
    print(p)
    