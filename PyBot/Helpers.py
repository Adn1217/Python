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



def dfTable(parent, dataList):

    # print('dataList: ', dataList);
    for item in dataList: #Eliminando diccionarios internos
        # print('item: ', item);
        for key in item.keys():
            if isinstance(item[key], dict):
               item[key] = item[key]["value"];
    
    df = pd.DataFrame(dataList);
    # print('DataFrame: ', df);
    tree = ttk.Treeview(parent, show=["headings"]) ## "headings" to not show tree (additional column).
    # print('Columnas: ', list(df.columns));
    
    wantedCols  = ['id', 'actionType', 'elementId', 'elementName', 'elementCompanyShortName', 'instructionTime', 'occurrenceTime',
                    'confirmationTime', 'causeStatus', 'consignmentId', 'causeChangeAvailability', 'newAvailability',
                    'elementCausingId', 'causeOperational', 'percentage','withPriorAuthorization', 'description',
                    'verificationNote', 'statusType', 'system', 'causeOrigin', 'causeDetailCno', 'additionalFieldsValue',
                    'espName', 'espElementId', 'unavailableActionId', 'subSystemUnavailableAction', 'cneZone', 'fuel',
                    'fuelName', 'fuelCEN', 'plantCEN', 'qualityScheme', 'source','dna', 'userValidator', 'configurationDesc',
                    'thermalStateId', 'descriptionAdditional'];
    colsExisting = [];
    for col in df.columns:
        if col in wantedCols:
            colsExisting.append(col);

    # print('Columnas rec: ', list(colsExisting))
    newDf = df[colsExisting].copy()
    
    tree["columns"] = list(newDf.columns)
    for col in newDf.columns:
        tree.column(col, anchor="center")
        tree.heading(col, text=col)
    # tree.column('#0', width=10) ## Auto additional column to show tree. 
    for _, row in newDf.iterrows():
        print('Fila: ', list(row));
        # print('newDf.iterrows: ', newDf.iterrows());
        tree.insert("", END, values=list(row))
        # tree.pack(expand=True, fill="both")

    # for cols in newDf.columns:
    #     celda = newDf[cols];
    #     print('Fila: ', )
    return tree;
