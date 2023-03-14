f1 = open('D:/dataset/urban_scene/ImageSets/Main/trainval.txt','r')
f2 = open('D:/dataset/urban_scene/ImageSets/trainval.txt', 'a')

lines = f1.readlines()
for line in lines:
    new_line = 'D:/dataset/urban_scene/JPEGImages/'+str(line).split('\n')[0]+'.jpeg\n'
    f2.write(new_line)
    print(line)
    
f1.close()
f2.close()