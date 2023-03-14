# -*- coding: utf-8 -*-
from PIL import Image
import os

img_path = 'D:/dataset/zi2zi/1110_256_zi2zi/compare/35.png'
img_basename = os.path.basename(img_path).split('.')[0]
savedir = 'D:/dataset/zi2zi/1110_256_zi2zi/compare/'


img = Image.open(img_path)

img1 = img.crop((0,0,256,256))
img2 = img.crop((256,0,512,256))

img1.save(savedir+img_basename+'_1.png')
img2.save(savedir+img_basename+'_2.png')