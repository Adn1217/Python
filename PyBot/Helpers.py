from tkinter import *


class Table:
    
    def __init__(self, window, dataList):

        numRows = len(dataList);
        numCols = len(dataList[0]);
        
        # code for creating table
        for i in range(numRows):
            for j in range(numCols):
                
                self.e = Entry(window, width=20, fg='blue', font=('Arial',16,'bold'))
                self.e.grid(row=i, column=j)
                self.e.insert(END, dataList[i][j])