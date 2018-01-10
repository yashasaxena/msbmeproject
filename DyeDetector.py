
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun September 03, 2017
@author: yashasaxena
"""


#ANN for deciphering between two different dyes using absorption spectrum data 

import numpy as np
import matplotlib.pyplot as plt
import csv

def nonlin(x,deriv=False):
    if(deriv==True):
        return x*(1-x)

    return 1/(1+np.exp(-x))
    
#starting threshold
threshold = 0.002
alpha = 10
ss2 = 0

#Input array    


training_data = [0,0] #initialize a matrix to store training data
y_d = [0] #desired output vector 

##Opening CSV containing training data elements
with open('/Users/yashasaxena/Google Drive/Duke University MS BME/Vo-Dinh Lab/Detection System/ANN Practice/Raman bone analysis/TrainingDataSet.csv') as td:
    csv_td = csv.reader(td)
    next(csv_td)

    for row in csv_td:
        #converting column elements to float from string
        wave_n = float(row[0])
        I_cy5_1 = float(row[1])
        I_cy5_2 = float(row[2])
        I_dtt_1 = float(row[3])
        I_dtt_2 = float(row[4])
        
        #use append method to add I/lambda for each respective dye to training data
        training_data = np.vstack([training_data,[I_cy5_1/wave_n,-1]])
        training_data = np.vstack([training_data,[I_cy5_2/wave_n,-1]])
        y_d = np.vstack([y_d,1])
        y_d = np.vstack([y_d,1])
        training_data = np.vstack([training_data,[I_dtt_1/wave_n,-1]])
        training_data = np.vstack([training_data,[I_dtt_2/wave_n,-1]])
        y_d = np.vstack([y_d,0])
        y_d = np.vstack([y_d,0])
td.close()


training_data = np.delete(training_data,(0),axis=0)
y_d = np.delete(y_d,(0),axis=0)

# Weight arrays (1 input neuron to 2 hidden layer neurons)
#w11 w12  
#th1 th2 
syn0 = np.matrix('0.5 0.9; 0.8 -0.1')

#w1o th_o
syn1=np.matrix('-1.2,0.3')      


l2_error = []

while(threshold>0.001):
    
    # Feed forward through layers 0, 1, and 2
    for i in range(len(training_data)):
        l0 = training_data[i]
        y_i = y[i]        
        l1 = nonlin(l0*syn0)
        a=np.matrix([-1])
        l1=np.matrix(l1)
        l1=np.column_stack((l1[0],a))
        l2 = nonlin(np.dot(l1,syn1.T))
    
        #error from target value
        e = y_i - l2
        se = e**2
        ss2 += se
        eg5 = nonlin(l2,True)*e   #error gradient for neuron 5

        w5_u = []
        for x in l1[0]: #updates for weights going to neuron 5
            w5_u.append(x*alpha*eg5[0,0])
            
        
        eg3 = nonlin(l1[0,0],True)*eg5[0,0]*syn1[0,0] #error gradient for neuron 3
        eg4 = nonlin(l1[0,1],True)*eg5[0,0]*syn1[0,1] #error gradient for neuron 4

        #update weights from input layer
        w3_u = []
        w4_u = []
        
        for x in l0[0]:
            w3_u.append(x*alpha*eg3)
            w4_u.append(x*alpha*eg4)
        
        #weird indices as a result of matrix manipulations
        for x in range(3):
            syn1[0,x] = syn1[0,x] + w5_u[0][0,x]
            syn0[:,0][x,0] = syn0[:,0][x,0] + w3_u[0][0,x]
            syn0[:,1][x,0] = syn0[:,1][x,0] + w4_u[0][0,x] 
     
        
    
    threshold = ss2
    l2_error.append(ss2[0][0,0])
    print(threshold)
    ss2=0


plt.plot(l2_error)