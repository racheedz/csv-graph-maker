# -*- coding: utf-8 -*-
"""
Created on Sat Jul 25 14:36:10 2020

@author: Windows 10
"""
## -- APPLICATION FUNCTION -- ## 
# open excel files and save into pd dataframe
# --> "browse" widget need
# plot the requested data
# --> Label: Show imported files/ data
# --> Entry: Tick the desired plot
# --> Plot the graph and display it (in a seperate window?)



import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from tkinter import *
from tkinter import filedialog
import os
os.system('clear')


## -- GUI -- ##

root = Tk()
root.title('Excel Graph Maker')
root.geometry('500x500')


# select file
all_files = {}
graph_files = {}
r = {}
data_keys = []
checks = {}


# -- functions -- #
# read excel files into pandas

def prepare_graph(filename):
    next_data = pd.read_csv(filename)
    graph_files[filename] = next_data
    
    data_keys = graph_files.keys()


def open_excel():
    filename = filedialog.askopenfilename(initialdir="/User/Windows 10/Desktop", title="select csv")
    
    if filename not in all_files:
        current_data = pd.read_csv(filename)
        all_files[filename] = current_data
        
        #temp_title = Label(root, text=filename)
        #temp_title.pack_forget()
        #temp_title.pack()
        
        #temp_table = Label(root, text = current_data.head())
        #temp_table.pack_forget()
        #temp_table.pack()
        
        # create the filename for the checkbutton
        last_i = len(filename) - 1
        last = filename[last_i]
        true_filename_length = 0
        
        while last != "/":
            true_filename_length += 1
            last_i -= 1
            last = filename[last_i]
        
        new_filename = filename[-true_filename_length:]
        
        # send file name into the dictionary for all files
        prepare_graph(filename)
        
        r[filename] = IntVar()
        # create a checkbutton
        checks[filename] = Checkbutton(root, text = new_filename, variable=r[filename], onvalue=1, 
                    offvalue=0)
        checks[filename].deselect()
        checks[filename].pack()
        
    else:
        messagebox.showerror("e","You alreay picked that file")
        

def show_all_files():
    a = Label(root, text=all_files.keys())
    a.pack()


def make_graph():
    
    # NEED TO ACTUALLY EXTRACT THE DATA
    
    plt.figure()
    for i in all_files.keys():
        
        if r[i].get() == 1:
        
            k = graph_files[i].keys()
            
            #x = k[0]
            #y = k[1]
            
            plt.scatter(np.array(range(len(graph_files[i]['Time'])))*10, graph_files[i]['Weight'])
    
    plt.show()
    

## -- Widgets -- ##
get_button = Button(root, text="Select Excel", command=open_excel)
get_button.pack()

show_all = Button(root, text="Show all_files", command=show_all_files).pack()

# THE r THING


make_graph_button = Button(root, text="Make Graph", command=make_graph).pack()

#sliderV = Scale(root, from_0=0, to=1000)
#sliderH = Scale(root, from_0=0, to=1000, orient=HORIZONTAL)

root.mainloop()










