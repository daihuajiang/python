#!/usr/bin/env python
# coding: utf-8

# In[1]:


#!/usr/bin/python
#coding=utf-8
#用於提取训练log，去除不可解析的log后使log文件格式化，生成新的log文件用以繪圖
#import inspect
#import os
#import random
#import sys
def extract_log(log_file, new_log_file, key_word):
    with open(log_file, 'r') as f:
        with open(new_log_file, 'w') as train_log:
            for line in f:
                #去除多GPU的同步log；去除除零错误的log
                if ('Syncing' in line) or ('nan' in line):
                    continue
                if key_word in line:
                    train_log.write(line)
    f.close()
    train_log.close()

#從訓練log生成log_loss.txt
#輸入訓練log路徑及log_loss.txt的儲存路徑
save_path = 'D:\\dataset\\zi2zi\\1013\\\loss\\'
extract_log(save_path + 'trainlog_1013.txt', save_path + 'log_loss.txt', 'Epoch:')


# In[2]:


#loss繪製
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#根據自己的log_loss.txt中的行數修改lines, 修改訓練時的起始回數(start_ite)和结束回數(end_ite)。
lines = 1621
start_ite =  0#log_loss.txt裡面的最小訓練回數
end_ite = 30 #log_loss.txt裡面的最大訓練回數
step = 10 #跳行數，决定畫圖的稠密程度
igore = 0 #當開始的loss較大時，你需要忽略前igore回，注意這裡是訓練回數
 

#y_ticks = [0, 50, 100, 150, 200, 250, 300, 350]#縱坐標的值，可以自己設置。
#設置橫坐標的刻度
x_tick = np.arange(0, end_ite+1, 2)
data_path =  save_path + 'log_loss.txt' #log_loss的路徑。
result_path = save_path + 'loss.png' #保存结果的路徑。
 
####-----------------只需要改上面的，下面的可以不改
names = ['epoch', 'time', 'd_loss', 'g_loss', 'category_loss', 'cheat_loss', 'const_loss', 'll_loss']
result = pd.read_csv(data_path, skiprows=[x for x in range(lines) if (x<lines*1.0/((end_ite - start_ite)*1.0)*igore or x%step!=step-1)], error_bad_lines=False, names=names)
#result.head()
for name in names:
    result[name] = result[name].str.split(', ').str.get(0).str.split(' ').str.get(2)
    #print(result[name])

#result.head()
#result.tail()

for name in names:
    result[name] = pd.to_numeric(result[name], errors='coerce')
result.dtypes
#print(result['g_loss'].values)

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)


###-----------設置橫坐標的值。
x_num = len(result['g_loss'].values)
tmp = (end_ite-start_ite - igore)/(x_num*1.0)
x = []
for i in range(x_num):
    x.append(i*tmp + start_ite + igore)
#print(x)
print('total = %d\n' %x_num)
print('start = %d, end = %d\n' %(x[0], x[-1]))
###----------

ax.plot(x, result['d_loss'].values, label='d_loss')
ax.plot(x, result['g_loss'].values, label='g_loss', linestyle = '--')
#ax.plot(result['loss'].values, label='loss')
#plt.yticks(y_ticks)#如果不想自己設置縱座標，可以註釋掉。
plt.xticks(x_tick)
plt.grid()
ax.legend(loc = 'best')
ax.set_title('The loss curves')
ax.set_xlabel('epoch')
fig.savefig(result_path)


# In[3]:


result_path = save_path + 'category_loss.png'
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.plot(x, result['category_loss'].values, label='category_loss')
plt.xticks(x_tick)
plt.grid()
ax.legend(loc = 'best')
ax.set_title('The loss curves')
ax.set_xlabel('epoch')
fig.savefig(result_path)


# In[4]:


result_path = save_path + 'category_loss.png'
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.plot(x, result['category_loss'].values, label='category_loss')
plt.xticks(x_tick)
plt.grid()
ax.legend(loc = 'best')
ax.set_title('The category loss curves')
ax.set_xlabel('epoch')
fig.savefig(result_path)


# In[5]:


result_path = save_path + 'cheat_loss.png'
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.plot(x, result['cheat_loss'].values, label='cheat_loss')
plt.xticks(x_tick)
plt.grid()
ax.legend(loc = 'best')
ax.set_title('The cheat loss curves')
ax.set_xlabel('epoch')
fig.savefig(result_path)


# In[6]:


result_path = save_path + 'const_loss.png'
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.plot(x, result['const_loss'].values, label='const_loss')
plt.xticks(x_tick)
plt.grid()
ax.legend(loc = 'best')
ax.set_title('The const loss curves')
ax.set_xlabel('epoch')
fig.savefig(result_path)


# In[7]:


result_path = save_path + 'll_loss.png'
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.plot(x, result['ll_loss'].values, label='ll_loss')
plt.xticks(x_tick)
plt.grid()
ax.legend(loc = 'best')
ax.set_title('The ll loss curves')
ax.set_xlabel('epoch')
fig.savefig(result_path)


# In[8]:

"""
result_path = save_path + 'tv_loss.png'
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.plot(x, result['tv_loss'].values, label='tv_loss')
plt.xticks(x_tick)
plt.grid()
ax.legend(loc = 'best')
ax.set_title('The tv loss curves')
ax.set_xlabel('epoch')
fig.savefig(result_path)

"""
# In[ ]:




