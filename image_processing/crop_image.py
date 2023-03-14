# Improting Image class from PIL module 
from PIL import Image
import os
import glob

#file_path = "C:\\Users\\David01\\Downloads\\0\\infer\\infer\\cns_testchar\\id2\\frame_00_01_step_00.jpg"
#save_path = "C:\\Users\\David01\\Downloads\\0\\infer\\infer\\cns_testchar\\id2\\00_01_00\\"
filedir = 'D:/dataset/handwrite_sample/origin/2r/'
savedir = 'D:/dataset/handwrite_sample/origin/2_data/'

row = 10
column = 15
crop_width = 256
crop_height = 256

for p in glob.glob(os.path.join(filedir, "*.jpeg")):
    filenumber = int(os.path.basename(p).split('.')[0])
    
    img = Image.open(p)
    img_width, img_height = img.size
    """
    #旋轉+水平翻轉
    target = Image.new('RGB', (img_height, img_height), 'white')
    target.paste(img)
    target = target.rotate(-90)
    target = target.crop((0, 0, img_height, img_width))
    target = target.transpose(Image.FLIP_LEFT_RIGHT)
    target.save(savedir+os.path.basename(p))
    """
    #crop_width = img_width/column
    #crop_height = img_height/row
    """
    #如果為從左寫到右的需要改成從寫右到左
    #創建符合模型格式的空白圖片
    target = Image.new('RGB', (img_width, img_height), 'white')
    for i in range(column):
        img_crop = img.crop((crop_width*i, 0, crop_width*(i+1), img_height))
        target.paste(img_crop, (int(crop_width*(column-i-1)), 0))
    
    target.save(save_path+"do_poetest1.jpg")    
    
    """
    #創建符合模型格式的空白圖片
    #target = Image.new('RGB', (256, 256), 'white')
    #擷取圖片
    count=0
    for j in range(column):
        for i in range(row):
            filename = 150*(filenumber-1)+count
            #擷取圖片
            img1 = img.crop((crop_width*j, crop_height*i, crop_width*(j+1), crop_height*(i+1)))
            #img1 = img1.crop((10, 10, crop_width-10, crop_height-10))
            img1.resize((int(crop_width), int(crop_height)))
            img1 = img1.transpose(Image.FLIP_LEFT_RIGHT)
            img1 = img1.rotate(90)
            img1.save(savedir+str(filename).zfill(4)+".jpg")
            count+=1
            """
            target.paste(img1, (257, 0))
            if count<10:
                target.save(save_path+"0_"+str(count)+".jpg")
            else:
                target.save(save_path+"0_9"+str(count)+".jpg")
            """
            