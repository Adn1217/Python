"""This module contains classes and functions to create a table in a Tkinter window
using Entries and pandas DataFrame with ttk.Treeview among others."""

from tkinter import END, NO, Entry, Scrollbar, ttk

import pandas as pd


class Table:
    """Class to create a table in a Tkinter window using Entries."""

    def __init__(self, window, dataList, width, color, font, fontSize):

        numRows = len(dataList)
        numCols = len(dataList[0])

        # code for creating table
        for i in range(numRows):
            for j in range(numCols):

                self.e = Entry(
                    window, width=width, fg=color, font=(font, fontSize, "bold")
                )
                self.e.grid(row=i, column=j)
                self.e.insert(END, dataList[i][j])

def formatList(dataList):

    DATESCOL = [
        "scheduledStartDate",
        "instructionTime",
        "occurrenceTime",
        "confirmationTime",
    ]

    # print('dataList: ', dataList);
    for item in dataList:  # Eliminando diccionarios internos y formateando campos de fecha.
        # print('item: ', item);
        for key in item.keys():
            if item[key] is None:
                item[key] = ""
            if isinstance(item[key], dict):
                item[key] = item[key]["value"]
            if key in DATESCOL and item[key] is not None and isinstance(item[key].strip(), str):
                item[key] = item[key].replace("T", " ")  # Replacing 'T' with space in date strings.
                # print(f"Formatted date for {key}: {item[key]}")
    return dataList

def dfTable(parent, dataList):
    """Create a DataFrame table in a Tkinter window using ttk.Treeview and pandas."""


    # print('dataList: ', dataList);
    dataList = formatList(dataList)  # Formateando lista de datos.
    df = pd.DataFrame(dataList)
    # print("DataFrame: ", df)
    # numElements = len(dataList)
    hScrollBar = Scrollbar(parent, orient="horizontal")
    # HScrollBar.grid(row=5, column=0, rowspan=1, columnspan=9, sticky='ew');
    vScrollBar = Scrollbar(parent, orient="vertical")

    tree = ttk.Treeview(
        parent,
        show=["headings"],
        xscrollcommand=hScrollBar.set,
        yscrollcommand=vScrollBar.set,
    )  ## "headings" to not show tree (additional column).
    # print('Columnas: ', list(df.columns));

    hScrollBar.config(command=tree.xview)
    vScrollBar.config(command=tree.yview)
    wantedCols = [
        "id",
        "actionType",
        "elementId",
        "elementName",
        "elementCompanyShortName",
        "instructionTime",
        "occurrenceTime",
        "confirmationTime",
        "causeStatus",
        "consignmentId",
        "causeChangeAvailability",
        "newAvailability",
        "elementCausingId",
        "causeOperational",
        "percentage",
        "withPriorAuthorization",
        "description",
        "verificationNote",
        "statusType",
        "system",
        "causeOrigin",
        "causeDetailCno",
        "additionalFieldsValue",
        "espName",
        "espElementId",
        "unavailableActionId",
        "subSystemUnavailableAction",
        "cneZone",
        "fuel",
        "fuelName",
        "fuelCEN",
        "plantCEN",
        "qualityScheme",
        "source",
        "dna",
        "userValidator",
        "configurationDesc",
        "thermalStateId",
        "descriptionAdditional",
    ]

    colsExisting = []
    for col in df.columns:
        if col in wantedCols:
            colsExisting.append(col)

    # print('Columnas rec: ', list(colsExisting))
    newDf = df[colsExisting].copy()

    tree["columns"] = list(newDf.columns)
    for col in newDf.columns:
        tree.column(col, anchor="center", minwidth=50, stretch=NO)
        tree.heading(col, text=col)

    maxHeight = 25
    tree.configure(height=maxHeight)
    # tree.column('#0', width=10) ## Auto additional column to show tree.
    for _, row in newDf.iterrows():
        # print('Fila: ', list(row));
        # print('newDf.iterrows: ', newDf.iterrows());
        tree.insert("", END, values=list(row))
        # tree.pack(expand=True, fill="both")

    return [tree, hScrollBar, vScrollBar]
