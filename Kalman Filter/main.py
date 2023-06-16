

# -*- coding: utf-8 -*-
"""
Created on Mon Mar  6 18:08:46 2023

@author: Ali
"""


#import the required libraries 
import os
import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from kf import KF
from tkinter import filedialog
from bokeh.plotting import figure, output_file, save , show
from bokeh.io import output_notebook


def open_csv_file():
    global data
    file_path = filedialog.askopenfilename()
    if file_path:
        data = pd.read_csv(file_path)
        print(file_path)
def main_code():
    global df
    global save_path2
    global save_path5
    global save_path6



    # Get values from GUI entry boxes
    initial_x = float(initial_x_entry.get())
    initial_y = float(initial_y_entry.get())
    initial_vx = float(initial_vx_entry.get())
    initial_vy = float(initial_vy_entry.get())
    std_x = float(std_x_entry.get())
    std_y = float(std_y_entry.get())

    plt.ion()
    plt.figure()

    kf = KF(initial_x=initial_x, initial_y=initial_y,
            initial_vx=initial_vx, initial_vy=initial_vy
            ,std_x=std_x, std_y=std_y)
            

    DT = 1 #sec
    num = 13587
# Assigning the columns from the 'data' DataFrame to the variables
    Meas_x_column = data['LS Xreceiver']
    Meas_y_column = data['LS Yreceiver']
    Meas_vx_column = data['vt_x']
    Meas_vy_column = data['vt_y']

# Initializing an empty lists
    current_state = [] 
    current_cov = []
    position_x = []
    velocity_x = []
    measure=[]


    

    for i in range(num):
        # Extracting the measurement values
        meas_x = Meas_x_column.iloc[i]
        meas_y = Meas_y_column.iloc[i]
        meas_vx = Meas_vx_column.iloc[i]
        meas_vy = Meas_vy_column.iloc[i]
        
        n_x = kf.predict(dt=DT, std_x=std_x, std_y=std_y)
        u_x = kf.update(meas_x, meas_y, meas_vx, meas_vy, dt=DT)
        y = np.array([[meas_x],[meas_y]])
        
        # Appending to the lists
        current_state.append(kf.state)
        current_cov.append(kf.cov)
        position_x.append(kf.pos_x)
        velocity_x.append(kf.vel_x)
        measure.append(y)


    # Creating a subplot and save it    
    plt.subplot(2, 1, 1)    
    plt.title('position')
    plot=plt.plot([mu[0] for mu in current_state],[mu[1] for mu in current_state], 'r')


    plt.plot(Meas_x_column, Meas_y_column, 'b')

    plt.savefig(save_path5)
    # create the dataframe
    df = pd.concat([pd.DataFrame(np.array(i).reshape(1, -1)) for i in current_state], ignore_index=True)
    df = df.iloc[:, :-2]
    # You can add column names if you like
    df.columns = ['x', 'y']


    extracted_data = []
    for arr in current_cov:
            extracted_data.append([arr[0, 0],arr[1, 1]])

     # convert list to dataframe
    df1 = pd.DataFrame(extracted_data, columns=['std_X', 'std_Y'])
    combined_df = pd.concat([df, df1], axis=1)
    #save the dataframe as CSV
    combined_df.to_csv(save_path6, index=False)



    #create the second plots
    plt.figure()
    plt.plot([mu[0,0] for mu in current_cov], 'r--')
    plt.title(' Standard deviation on X over time')
    plt.xlabel('epoch')
    plt.ylabel('std on Y')
    plt.savefig(save_path2)
    plt.show()
    
    
    plt.savefig(save_path2)

    # Show the plot

    plt.show()
    #create the third plots
    plt.figure()
    plt.plot([mu[1,1] for mu in current_cov], 'r--')
    plt.title(' Standard deviation on Y over time')
    plt.xlabel('epoch')
    plt.ylabel('std on Y')
    plt.savefig(save_path7)
    plt.show()
    
    
    # Create a figure by Bokeh
    p = figure(title='Coordinate Plot')

    # Extract x and y coordinates from the 'current_state' list
    x1 = [point[0][0] for point in current_state]
    y1 = [point[1][0] for point in current_state]

    # Extract x and y coordinates from the 'measure' list
    x2 = [point[0][0] for point in measure]
    y2 = [point[1][0] for point in measure]

    # Plot the lines
    p.line(x1, y1, line_color='red', legend_label='filtered')
    p.line(x2, y2, line_color='blue', legend_label='observed')

    # Set the legend location
    p.legend.location = 'top_left'

    # Show the plot
    output_file('coordinate_plot.html')  # Specify the output file name
    show(p)
    output_file(save_path2)
    save(p)
    
    
    
    
    print(file_path1)
    print(initial_x)
    print(initial_y)
    print(initial_vx)
    print(initial_vy)

    print(std_x)
    print(std_y)
    
        
    
#save_plots()
    
def save_plots():
    global file_path1
    global save_path2
    global save_path5
    global save_path6
    global save_path7

# Get the file path to save the plots
    file_path1 = filedialog.askdirectory()
    if file_path1:
        # Save the plots to the selected directory

        file_name1= "Standard deviation on X over time.png"
        save_path2 = os.path.join(file_path1,file_name1)
        file_name2= "position.png"
        save_path5 = os.path.join(file_path1,file_name2)
        file_name3= "position.csv"
        save_path6 = os.path.join(file_path1,file_name3)
        file_name4= "Standard deviation on Y over time.png"
        save_path7 = os.path.join(file_path1,file_name4)

        plt.savefig(save_path2) 
        print(save_path2)

      
      
    
def run_kalman_filter():
    main_code()

root = tk.Tk()
root.title("Kalman Filter")
root.geometry("500x500")
#create RUN buttom
run_button = tk.Button(root, text="Run", command=run_kalman_filter)
run_button.grid(row=10, column=1, padx=5, pady=5)

# Add labels and entry boxes for initial state 
tk.Label(root, text="Enter The Initial Postion X").grid(row=3, column=0, padx=5, pady=5)
initial_x_entry = tk.Entry(root)
initial_x_entry.grid(row=3, column=1, padx=5, pady=5)

tk.Label(root, text="Enter The Initial Postion Y").grid(row=4, column=0, padx=5, pady=5)
initial_y_entry = tk.Entry(root)
initial_y_entry.grid(row=4, column=1, padx=5, pady=5)

tk.Label(root, text="Enter The Initial Velocity VX").grid(row=5, column=0, padx=5, pady=5)
initial_vx_entry = tk.Entry(root)
initial_vx_entry.grid(row=5, column=1, padx=5, pady=5)

tk.Label(root, text="Enter The Initial Velocity VY").grid(row=6, column=0, padx=5, pady=5)
initial_vy_entry = tk.Entry(root)
initial_vy_entry.grid(row=6, column=1, padx=5, pady=5)


tk.Label(root, text="Enter The Standard devition For Position").grid(row=7, column=0, padx=5, pady=5)
std_x_entry = tk.Entry(root)
std_x_entry.grid(row=7, column=1, padx=5, pady=5)   

tk.Label(root, text="Select  CSV File").grid(row=0, column=0, padx=5, pady=5)
csv_file_button = tk.Button(root, text="Select File", command=open_csv_file)
csv_file_button.grid(row=0, column=1, padx=5, pady=5)


tk.Label(root, text="Enter The Standard devition For velocity").grid(row=8, column=0, padx=5, pady=5)
std_y_entry = tk.Entry(root)
std_y_entry.grid(row=8, column=1, padx=5, pady=5)  

tk.Label(root, text="Select Output Folder ").grid(row=1, column=0, padx=5, pady=5)
save_button= tk.Button(root, text="Select Folder", command=save_plots)
save_button.grid(row=1, column=1, padx=5, pady=5)


root.mainloop()