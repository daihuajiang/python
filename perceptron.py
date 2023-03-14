"""
algorithm:
for t <- 1 to T do //T iterations
    for d <- 1 to D do //D input samples
        read data(x1,...,xn;T1,...,Tp)
        //forward
        //compute output layer
        for k <- 1 to p do
            net_k <- -theta_k
            for j <- 1 to n do
                net_k <- neth_k + wjk * xj
            Yk <- 1/(1 + exp^-net_k) //activation function: sigmoid
        //backward
        //compute delta for output layer
        for k <- 1 to p do
            delta_k <-  (Tk - Yk)
        //adjust parameters
        for k <- 1 to p do
            theta_k <- theta_k - eta * delta_k
            for j <- 1 to n do
                wjk <- wjk + eta * delta_k * xj
"""

import numpy as np

d_ = 100 #樣本數
t_ = 50 #訓練回數
n = 2 #輸入的資料維度  
p = 1 #輸出層的神經元數量

#資料特徵有2維，共100筆
X = np.random.rand(d_, n)
X_count = 0 #計算有多少筆資料欄位1的值大於等於欄位2

#資料類別: 如果欄位1的值大於等於欄位2類別為1，否則為0
X_label = np.zeros((d_, p))

for d in range(d_):
    if X[d][0] >= X[d][1]:
        X_label[d] = 1
        X_count += 1


#定義參數
#input layer到output layer的weight
weight_w = np.random.rand(n, p) 
#output layer的bias
theta_k = np.random.rand(p, 1)
#output layer的輸出
net_k =  np.random.rand(p, 1)
#output layer的輸出經過activtion function後的輸出
Yk = np.zeros((d_, p), dtype = 'float64')
#調整output layer的weight的偏差
delta_k = np.zeros_like(net_k)
#學習率
eta = 10

for t in range(t_): #T iterations
    for d in range(d_): #D input samples
        xi = X[d]
        Tk = X_label[d]
        
        #forward
        #compute output layer
        for k in range(p):
            #net_k <- -theta_k
            net_k[k] = 0 - theta_k[k]
            for j in range(n):
                #net_k <- net_k + wjk * xj
                net_k[k] = net_k[k] + (weight_w[j][k] * xi[j])
            
            #activation function: sigmoid
            #Yk <- 1/(1 + exp^-net_k)
            Yk[d] = 1.0 / (1.0 + np.exp(-net_k[k]))
            
            """
            #activation function: relu
            if net_k[k] <=0:
                Yk[d] = 0
            else:
                Yk[d] = net_k[k]
            """
        
        #backward
        #compute delta for output layer
        for k in range(p):
            #delta_k <- Yk * (1 - Yk) * (Tk - Yk)
            delta_k[k] = (Tk - Yk[d])
           
        #adjust parameters
        for k in range(p):
            #theta_k <- theta_k - eta * delta_k
            theta_k[k] = theta_k[k] - (eta * delta_k[k])
            for j in range(n):
                #wjk <- wjk + eta * delta_k * xj
                weight_w[j][k] = weight_w[j][k] + (eta * delta_k[k] * xi[j])
    print(weight_w)
    
    print('epoch: %d'%(t))    
    #print('Yk =')
    #print(Yk) 

#recall
for d in range(d_): #D input samples
        xi = X[d]
        Tk = X_label[d]
        #forward
        #compute output layer
        for k in range(p):
            #neth_k <- -theta_hk
            net_k[k] = 0 - theta_k[k]
            for j in range(n):
                #neth_k = neth_k + wjk * Hj
                net_k[k] += (weight_w[j][k] * xi[j])
            
            #Yk = 1/(1 + exp^-net_k)
            Yk[d] = 1/(1.0 + np.exp(-net_k[k]))
            
            """
            #activation function: relu
            if net_k[k] <=0:
                Yk[d] = 0
            else:
                Yk[d] = net_k[k]
            """
            #輸出值大於0.5則歸類為1，否則為0
            if Yk[d] >= 0.5:
                Yk[d] = 1
            else:
                Yk[d] = 0

#印出網路預測的結果
print("predict:")
print("欄位1, 欄位2, 類別")
for d in range(d_):
    print("%f %f %d"%(X[d][0], X[d][1], Yk[d]))
          
print("\n訓練回數: %d, 學習率: %f"%(t_, eta))
print("\n資料筆數共%d筆，其中有%d筆資料欄位1的值大於等於欄位2的值"%(d_, X_count))
print("欄位1的值大於等於欄位2的值歸類為1，否則為0\n")

#印出正確率
acc_count = 0
for d in range(d_):
    if Yk[d] == X_label[d]:
        acc_count += 1

accuracy = float(acc_count / d_)
print("正確率: %f"%accuracy)
