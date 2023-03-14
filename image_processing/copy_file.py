import os
import glob
import shutil

#source_path = 'D:/dataset/handwrite_sample/1/sample_256/'
#source_path = 'D:/dataset/zi2zi/1110_256_zi2zi/test/testchar/char/'
source_path = 'D:/dataset/zi2zi/1110_256_zi2zi/test/poe_test/2/poe2/char/'
#target_path = 'C:/Users/David01/DGfont/DG-Font-main/data/1110_256/id_4/'
#target_path = 'D:/dataset/zi2zi/1023_256_zi2zi/test/testchar/infer/lisu/'
target_path = source_path

for p in glob.glob(os.path.join(source_path, "*.jpg")):
    filepath = p
    
    file_num = os.path.basename(p).split("_")[1]
    #手寫字測試檔案複製
    for i in range(1,12):
        new_label = int(os.path.basename(p).split("_")[0])+i
        new_filename = str(new_label)+"_"+file_num
        shutil.copyfile(p, target_path+new_filename)
    
    #手寫字測試檔案生成結果重新命名
    """
    label = int(os.path.basename(p).split("_")[0])
    if label==0:
        new_label = 1
    elif label==5:
        new_label = 4
    """
    
    #複製檔案並重新命名
    """
    #new_label = 5
    file_num=int(os.path.basename(p).split('.')[0])
    #new_filename = str(new_label)+"_"+file_num
    #new_filename = str(new_label)+"_"+f'{file_num:04d}.png'
    new_filename = f'{file_num:04d}.png'
    shutil.copyfile(p, target_path+new_filename)
    """