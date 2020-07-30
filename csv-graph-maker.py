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

from tkinter import *
from tkinter import filedialog
import os
os.system('clear')


## -- GUI -- ##

root = Tk()
root.title('CSV Graph Maker')
root.geometry('500x500')


# -- VARIABLES -- ##
all_files = {}
graph_files = {}
r = {}
checks = {}
short_filename = {}
flux_dict = {}
toggler = 2

# -- FUNCTIONS -- #
# read csv files into pandas

#
def prepare_graph(filename):
    next_data = pd.read_csv(filename)
    graph_files[filename] = next_data

    #data_keys = graph_files.keys()

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
            checks[filename] = Checkbutton(root, text = short_filename[filename], variable=r[filename], onvalue=1, 
                        offvalue=0)
            checks[filename].deselect()
            checks[filename].pack()
            
        else:
            messagebox.showerror("e","You alreay picked that file")
        

#for debugging
def show_all_files():
    a = Label(root, text=all_files.keys())
    a.pack()


# plotting the selected data
def make_graph():
        
    plt.figure()
    for i in all_files.keys():
        
        if r[i].get() == 1:
        
            k = graph_files[i].keys()
            
            #x = k[0]
            #y = k[1]
            
            plt.scatter(np.array(range(len(graph_files[i]['Time'])))*10, graph_files[i]['Weight'], 
                        label=short_filename[i])
            
    plt.ylabel('Weight (g)')
    plt.xlabel('Time (s)')
    plt.title('Water Flux Comparisons')
    plt.legend(loc='upper left')
    plt.show()
    

# show flux of selected - uses label
def show_flux():
    
    # reset all vars
    flux_dict = {}
    area = 0.047
    
    #make a new window pop up each time
    top = Toplevel()
    
    for i in all_files.keys():
        
        if r[i].get() == 1:
            
            # calculate flux
            time = np.array(range(len(graph_files[i]['Time'])))*10
            weight = graph_files[i]['Weight']
            
            
            dt = time[len(time) - 1]# - time[0]
            dm = weight[len(weight) - 1] - weight[0]
            
            flux= (dm*0.001 / (dt/3600)) / area
            flux = str(flux)
            
            # print
            print_string = short_filename[i] + "'s FLUX is   =   " + flux + "LMH"
            flux_dict[i] = Label(top, text=print_string).pack()
    

# toggle selection of all
def toggle_selection():
    
    global toggler
    
    for i in all_files.keys():
        if toggler % 2 == 0:
            checks[i].select()
        else:
            checks[i].deselect()
            
    toggler += 1



## -- WIDGETS -- ##
# add scroll...-- Need a Canvas??????????????????
#sb = Scrollbar(root)
#sb.pack(side=RIGHT, fill=Y) 
#sb.config()# command = mylist.yview )  


# create button that allows user to select file
get_button = Button(root, text="Select Excel", command=open_excel)
get_button.pack()

# used for debugging
show_all = Button(root, text="Show all_files", command=show_all_files).pack()

# create button to graph
make_graph_button = Button(root, text="Make Graph", command=make_graph).pack()

# create button that shows flux of selected
make_flux_button = Button(root, text="Calculate J, Water Flux", command=show_flux).pack()

# make toggle button
make_toggle_button= Button(root, text="Select all", command=toggle_selection).pack()


root.mainloop()










