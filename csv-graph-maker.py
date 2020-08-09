# -*- coding: utf-8 -*-
"""
Created on Sat Jul 25 14:36:10 2020

@author: Windows 10
"""
## -- APPLICATION FUNCTION -- ## 
# open csv files and save into pd dataframe
# --> "browse" widget need
# plot the requested data
# --> Label: Show imported files/ data
# --> Entry: Tick the desired plot
# --> Plot the graph and display it 


# TODO
# ADD FUNCTIONALITY TO BETTER ALLOW USERS TO CUSTOMISE/ CHOOSE WHICH DATA HEADING
# THEY WANT TO USE
# -------> Popup window with checkboxes showing all availables headings
# -------> .columns <---------


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import csv
import math

from tkinter import *
from tkinter import filedialog
import os
os.system('clear')


# =============================================================================
# ## -- GUI -- ##
# =============================================================================

root = Tk()
root.title('CSV Graph Maker')
root.geometry('500x500')

# CANVAS - stackoverflow
def onFrameConfigure(canvas):
    #Reset the scroll region to encompass the inner frame
    canvas.configure(scrollregion=canvas.bbox("all"))

canvas = Canvas(root, borderwidth=0, background="#ffffff")
frame = Frame(canvas, background="#ffffff")
vsb = Scrollbar(root, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=vsb.set)

vsb.pack(side="right", fill="y")
canvas.pack(side="left", fill="both", expand=True)
canvas.create_window((4,4), window=frame, anchor="nw")

frame.bind("<Configure>", lambda event, canvas=canvas: onFrameConfigure(canvas))



# -- VARIABLES -- ##
all_files = {}
graph_files = {}
r = {}
checks = {}
short_filename = {}
flux_dict = {}
toggler = 2

# =============================================================================
# # -- FUNCTIONS -- #
# =============================================================================
# read csv files into pandas

#
def prepare_graph(filename):
    next_data = pd.read_csv(filename)
    graph_files[filename] = next_data
    

# select a file and create a check button for it
def open_excel():
    filenames = filedialog.askopenfilenames(initialdir="/User/Windows 10/Desktop", title="select csv")
    
    for filename in filenames:
        
        if filename not in all_files:
            current_data = pd.read_csv(filename)
            all_files[filename] = current_data
            
            
            # create the filename for the checkbutton
            last_i = len(filename) - 1
            last = filename[last_i]
            true_filename_length = 0
            
            while last != "/":
                true_filename_length += 1
                last_i -= 1
                last = filename[last_i]
            
            short_filename[filename] = filename[-true_filename_length:][:-4]
            
            # send file name into the dictionary for all files
            prepare_graph(filename)
            
            r[filename] = IntVar()
            # create a checkbutton
            checks[filename] = Checkbutton(frame, text = short_filename[filename], variable=r[filename], onvalue=1, 
                        offvalue=0)
            checks[filename].deselect()
            checks[filename].pack()
            
        else:
            messagebox.showerror("e","You alreay picked that file")


#for debugging
def show_all_files():
    a = Label(frame, text=short_filename.values())
    a.pack()


# plotting the selected data
def make_graph():
    
    if graph_name.get():
        g_name = graph_name.get()
    else:
        g_name = 'Water Flux Comparisons'
    graph_name.delete(0, END)
    
    plt.figure()
    for i in all_files.keys():
        
        if r[i].get() == 1:
        
            k = graph_files[i].keys()
            
            #x = k[0]
            #y = k[1]
            
            m = np.array(graph_files[i]['Weight'])
            m_0 = m[0]
            m_f = m - m_0
            
            plt.scatter(np.array(range(len(graph_files[i]['Time'])))*10, m_f, 
                        label=short_filename[i])
    
    # add 20LMH line
    #lmh_x = np.array(range(121)) * 10
    #lmh_y = np.array(range(121)) * 0.346989     #41.6/120
    #plt.scatter(lmh_x, lmh_y, label = '20LMH LINE')
    
    
    plt.ylabel('Weight (g)')
    plt.xlabel('Time (s)')
    plt.title(g_name)
    plt.legend(loc='upper right')
    plt.show()
    

# show flux of selected - uses label
def show_flux():
    
    if csv_name.get():
        f_name = csv_name.get()
    else:
        f_name = 'flux'
    csv_name.delete(0,END)
    
    
    # reset all vars
    flux = {}
    flux_dict = {}
    area = (math.pi * (0.047**2)) / 4
    dt = {}
    q = {}
    
    #make a new window pop up each time
    top = Toplevel()
    
    for i in all_files.keys():
        
        if r[i].get() == 1:
            
            # calculate flux
            time = np.array(range(len(graph_files[i]['Time'])))*10
            weight = graph_files[i]['Weight']
            
            
            dt[i] = time[len(time) - 1]# - time[0]
            q[i] = weight[len(weight) - 1] - weight[0]
            
            # J = Q/A * 1/dt =  Q/dt * 1/A
            flux[i] = (q[i]*0.001 / (dt[i]/3600)) / area
            stringflux = str(flux[i])
            
            # print
            print_string = short_filename[i] + "'s FLUX is   =   " + stringflux + "LMH"
            flux_dict[i] = Label(top, text=print_string).pack()
    
    # write to csv
    file_name_for_csv = f_name + ".csv"
    with open(file_name_for_csv, 'w', newline='') as f:
        
        csvwriter = csv.writer(f)
        csvwriter.writerow(['Membrane', 'dt (s)', 'Q (mL)', 'Area (m)', 'Flux - J (LMH)'])
        
        for i in all_files.keys():
            if r[i].get() == 1:
                csvwriter.writerow([short_filename[i], dt[i], q[i], area, flux[i]])
        

# toggle selection of all
def toggle_selection():
    
    global toggler
    
    for i in all_files.keys():
        if toggler % 2 == 0:
            checks[i].select()
        else:
            checks[i].deselect()
            
    toggler += 1


# =============================================================================
# ## -- WIDGETS -- ##
# =============================================================================
# add scroll...-- Need a Canvas??????????????????
#sb = Scrollbar(root)
#sb.pack(side=RIGHT, fill=Y) 
#sb.config()# command = mylist.yview )  

# add bubble-point conversion feature -
# - input ?
# ---- interactive input? --> BOX: (name, pressure) ... "add another"? 
# - output --> max d of each 



# create button that allows user to select file
get_button = Button(frame, text="Select CSV's", command=open_excel)
get_button.pack()

# used for debugging
show_all = Button(frame, text="Show all_files", command=show_all_files).pack()

#graph name -- .get() to retrieve
graph_name = Entry(frame, width=80)
graph_name.pack()
graph_name.insert(0, 'Enter graph\'s name')

# create button to graph
make_graph_button = Button(frame, text="Make Graph", command=make_graph).pack()

#csv name -- .get() to retrieve
csv_name = Entry(frame, width=60)
csv_name.pack()
csv_name.insert(0, 'Enter filename (without .csv)')

# create button that shows flux of selected
make_flux_button = Button(frame, text="Calculate J, Water Flux", command=show_flux).pack()

# make toggle button
make_toggle_button= Button(frame, text="Select all", command=toggle_selection).pack()


root.mainloop()




