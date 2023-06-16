# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as mp

#upload the data 
path= r"D:\Polimi\semester_4\geoiformatics project\X,Y Trajectory13.xlsx"
data= pd.read_excel(path)

data.dropna(inplace = True)
data=data.reset_index(drop=True)
        
data['epoch'] = range(0, len(data))

#compute diffrance in time 
data['&T']=data['epoch'].diff()
fin = data.loc[data['&T']>1] 
# delta_t is the time diffrance between one epoch and the following one 
delta_t= 1  #second
# VELOCITY ON X :-
X= data['LS Xreceiver']

n=len(X)

vt_x1=np.zeros((n,1), dtype=float)
vt_x2=np.zeros((n,1), dtype=float) 
vt=np.zeros((n,1), dtype=float)

#velocity (+)
for i in range(1,n-1):
      vt_x1[i] = abs(X[i+1]-X[i])/delta_t 

#velocity (-)
for i in range(1,n):     
      vt_x2[i] = abs(X[i]-X[i-1])/delta_t
      
#for i in range(1,n):
vt_x1=[float(i) for i in vt_x1]
vt_x2=[float(i) for i in vt_x2]

zipped_lists = zip(vt_x1,vt_x2)   
vt3 = [x + y for (x, y) in zipped_lists]
vt_x = [i * 0.5 for i in vt3]
#print(vt_x)
data['vt_x'] = vt_x
   
    

# VELOCITY ON Y :-
Y= data['LS Yreceiver']
n=len(Y)
vt_y1=np.zeros((n,1), dtype=float)
vt_y2=np.zeros((n,1), dtype=float) 

for i in range(1,n-1):
      vt_y1[i] = abs(Y[i+1]-Y[i])/delta_t 
      
for i in range(1,n):     
      vt_y2[i] = abs(Y[i]-Y[i-1])/delta_t      
      
vt_y1=[float(i) for i in vt_y1]
vt_y2=[float(i) for i in vt_y2]   

zipped_lists1 = zip(vt_y1,vt_y2)   
vt3_y = [x + y for (x, y) in zipped_lists1]
vt_y = [i * 0.5 for i in vt3_y]   

data['vt_y'] = vt_y
  

squared_vtx = [number ** 2 for number in vt_x]
squared_vty = [number ** 2 for number in vt_y]

zipped_lists2 = zip(squared_vtx,squared_vty) 
vts = [x + y for (x, y) in zipped_lists2] 
vt= np.sqrt(vts)
data['vt'] = vt




#Acceleration on X :-

vx=data['vt_x']
n=len(vx)

at_x1=np.zeros((n,1), dtype=float)
at_x2=np.zeros((n,1), dtype=float)

for i in range(1,n-1):
      at_x1[i] = abs(vx[i+1]-vx[i])/delta_t 
for i in range(1,n):     
      at_x2[i] = abs(vx[i]-vx[i-1])/delta_t
      
at_x1=[float(i) for i in at_x1]
at_x2=[float(i) for i in at_x2]     

zipped_lists3 = zip(at_x1,at_x2)   
at3 = [x + y for (x, y) in zipped_lists3]
at_x = [i * 0.5 for i in at3] 

data['at_x'] = at_x


#Acceleration on Y :-

vy=data['vt_y']
n=len(vy)

at_y1=np.zeros((n,1), dtype=float)
at_y2=np.zeros((n,1), dtype=float)

for i in range(1,n-1):
      at_y1[i] = abs(vy[i+1]-vy[i])/delta_t 
for i in range(1,n):     
      at_y2[i] = abs(vy[i]-vy[i-1])/delta_t 
      
at_y1=[float(i) for i in at_y1]
at_y2=[float(i) for i in at_y2]

zipped_lists4 = zip(at_y1,at_y2)   
at3 = [x + y for (x, y) in zipped_lists4]
at_y = [i * 0.5 for i in at3] 

data['at_y'] = at_y


squared_atx = [number ** 2 for number in at_x]
squared_aty = [number ** 2 for number in at_y]

zipped_lists5 = zip(squared_atx,squared_aty) 
ats = [x + y for (x, y) in zipped_lists5] 
at= np.sqrt(ats)
data['at'] = at




print(data)

#plots 
data.plot(x="epoch", y=["vt"],
        kind="line", figsize=(10, 10))
mp.show()

data.plot(x="epoch", y=["at"],
        kind="line", figsize=(10, 10))
mp.show()

data.to_csv(r'C:\Users\Ali\Desktop\my_data4.csv', index=False)
