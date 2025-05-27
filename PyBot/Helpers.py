from tkinter import *
import pandas as pd
from tkinter import ttk


class Table:
    
    def __init__(self, window, dataList, width, color, font, fontSize):

        numRows = len(dataList);
        numCols = len(dataList[0]);
        
        # code for creating table
        for i in range(numRows):
            for j in range(numCols):
                
                self.e = Entry(window, width=width, fg=color, font=(font,fontSize,'bold'))
                self.e.grid(row=i, column=j)
                self.e.insert(END, dataList[i][j])



def dfTable(parent, df):
    tree = ttk.Treeview(parent, show=["headings"]) ## "headings" to not show tree (additional column).
    tree["columns"] = list(df.columns)
    # print('Columnas: ', list(df.columns));
    for col in df.columns:
        tree.column(col, anchor="center")
        tree.heading(col, text=col)

    # tree.column('#0', width=10) ## Auto additional column to show tree. 
    for _, row in df.iterrows():
        # print('Fila: ', list(row));
        tree.insert("", END, values=list(row))
        # tree.pack(expand=True, fill="both")
    return tree;
