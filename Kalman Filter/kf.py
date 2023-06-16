# -*- coding: utf-8 -*-
"""
Created on Wed Oct 26 19:17:43 2022

@author: Ali
"""

import numpy as np

class KF:
    def __init__(self, initial_x:float, initial_y:float, 
                 initial_vx:float , initial_vy:float 
                 , std_x: float , std_y: float  ) -> None:
        #state matrix
        self._x = np.array([[initial_x], [initial_y], [initial_vx],[initial_vy]])
        
        
        #initial process covariance matrix 
        self._P = np.array([[std_x, 0, 0, 0], [0, std_x, 0, 0], [0, 0, std_y, 0],
                            [0, 0, 0, std_y]])    
    def predict(self, dt: float , std_x: float , std_y: float) -> None:
           
          T =np.array([[1, 0, dt, 0], [0, 1, 0, dt], [0, 0, 1, 0], [0, 0, 0, 1]])
          C_epslon= np.array([[std_x, 0, 0, 0], [0, std_x, 0, 0], [0, 0, std_y, 0],
                            [0, 0, 0, std_y]], dtype=float)
          
           
          new_x=T @ (self._x)
         
          
          #predicted process covariance matrix
          new_P = T @ (self._P) @ (T.T) + C_epslon
        
          self._P = new_P
          self._x = new_x
        
    def update(self, meas_x: float, meas_y: float, meas_vx: float, 
               meas_vy: float, dt: float):

       
       T =np.array([[1, 0, dt, 0], [0, 1, 0, dt], [0, 0, 1, 0], [0, 0, 0, 1]])
       y = np.array([[meas_x],[meas_y]])
       
       Cv = np.array([[0.01, 0], [0, 0.01]])   #observation error matrix
       
       A = np.array([[1 ,0 ,0 ,0],[0, 1, 0, 0]])  
       # A is design matrix
       

       S = A @ (self._P) @ (A.T) + Cv
       G = self._P @ (A.T) @ (np.linalg.inv(S))
       
       

       new_x = G @ y + (np.eye(4)-G @ A) @ (T @ self._x)
       new_P = (np.eye(4) - G @ (A)) @ (self._P)
       
       self._P = new_P 
       self._x = new_x

       initial_x=self._x[0]
       initial_y=self._x[1]
       initial_vx=self._x[2]
       initial_vy=self._x[3]
       
#property method make tge access as an attribute       
    @property
    def pos_x(self)-> float:   #return float
        return self._x[0]
    
    @property
    def pos_y(self)-> float:   #return float
        return self._x[1]
    
    @property
    def vel_x(self)-> float:   #return float
        return self._x[3]
    @property
    def vel_y(self)-> float:   #return float
        return self._x[4] 
    @property
    def cov(self) -> np.array:
        return self._P
    @property
    def state(self) -> np.array:
        return self._x

