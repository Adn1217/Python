"""This module contains classes and functions to create a table in a Tkinter window
using Entries and pandas DataFrame with ttk.Treeview among others."""

from tkinter import END, NO, Entry, Scrollbar, ttk

import pandas as pd


class Table:
    """Class to create a table in a Tkinter window using Entries."""

    def get_table(self):
        """Return the table instance."""
        return self

    def set_table(self, parent):
        """Set the table instance."""
        numRows = len(self.data_list)
        numCols = len(self.data_list[0])

        # code for creating table
        for i in range(numRows):
            for j in range(numCols):

                self.e = Entry(
                    parent,
                    width=self.width,
                    fg=self.color,
                    font=(self.font, self.font_size, "bold"),
                )
                self.e.grid(row=i, column=j)
                self.e.insert(END, self.data_list[i][j])

    def __init__(self, parent, **kwargs):
        """Initialize the table with the given parameters."""
        self.data_list = kwargs["dataList"]
        self.width = kwargs["width"]
        self.color = kwargs["color"]
        self.font = kwargs["font"]
        self.font_size = kwargs["fontSize"]

        self.set_table(parent)


def formatList(dataList):
    """Format a list of dictionaries by replacing None with empty strings"""

    # pylint: disable=invalid-name
    DATESCOL = [
        "scheduledStartDate",
        "instructionTime",
        "occurrenceTime",
        "confirmationTime",
    ]
    for (
        item
    ) in dataList:  # Eliminando diccionarios internos y formateando campos de fecha.
        # print('item: ', item);
        for key in item.keys():
            if item[key] is None:
                item[key] = ""
            if isinstance(item[key], dict):
                item[key] = item[key]["value"]
            if (
                key in DATESCOL
                and item[key] is not None
                and isinstance(item[key].strip(), str)
            ):
                item[key] = item[key].replace(
                    "T", " "
                )  # Replacing 'T' with space in date strings.
                # print(f"Formatted date for {key}: {item[key]}")
    return dataList


def identifyColsToDisplay(dataList, layout, selectedCols) -> list:
    """Identify columns to display in the DataFrame based on layout, selected cols and dataList."""
    df = pd.DataFrame(dataList)
    # print("DataFrame: ", df)
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
        "validate",  # "validate" is used to highlight rows that are validated.
        "error",  # "error" is used to highlight rows that have errors.
    ]

    if layout == "compacta":
        if len(wantedCols) != len(selectedCols):
            if "source" not in selectedCols:
                selectedCols.append("source")
            if "validate" not in selectedCols:
                selectedCols.append("validate")
            if "error" not in selectedCols:
                selectedCols.append("error")

            wantedCols = selectedCols
        else:
            wantedCols = [
                "id",
                "actionType",
                "elementName",
                "elementCompanyShortName",
                "instructionTime",
                "occurrenceTime",
                "confirmationTime",
                "causeStatus",
                "consignmentId",
                "newAvailability",
                "elementCausingId",
                "causeOperational",
                "withPriorAuthorization",
                "statusType",
                "system",
                "causeOrigin",
                "unavailableActionId",
                "subSystemUnavailableAction",
                "cneZone",
                "fuel",
                "fuelName",
                "fuelCEN",
                "plantCEN",
                "qualityScheme",
                "source",
                "configurationDesc",
                "thermalStateId",
                "validate",  # "validate" is used to highlight rows that are validated.
                "error",  # "error" is used to highlight rows that have errors.
            ]

    colsExisting = []
    for col in df.columns:
        if col in wantedCols:
            colsExisting.append(col)

    sourceIndex = colsExisting.index("source")
    validateIndex = wantedCols.index("validate")
    errorIndex = wantedCols.index("error")

    if len(list(colsExisting)) == len(wantedCols):
        validateIndex = colsExisting.index("validate")
        errorIndex = colsExisting.index("error")

    # print('Columnas rec: ', list(colsExisting))
    newDf = df[colsExisting].copy()

    return [wantedCols, sourceIndex, validateIndex, errorIndex, newDf]


def dfTable(parent, dataList, selectedCols, layout="completa"):
    """Create a DataFrame table in a Tkinter window using ttk.Treeview and pandas."""

    # print('dataList: ', dataList);
    dataList = formatList(dataList)  # Formateando lista de datos.
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

    [wantedCols, sourceIndex, validateIndex, errorIndex, newDf] = identifyColsToDisplay(
        dataList, layout, selectedCols
    )

    tree["columns"] = list(newDf.columns)
    for col in newDf.columns:
        tree.column(col, anchor="center", minwidth=50, stretch=NO)
        tree.heading(col, text=col)

    maxHeight = 25
    tree.configure(height=maxHeight)
    # tree.column('#0', width=10) ## Auto additional column to show tree.
    tagName = ""
    for _, row in newDf.iterrows():

        # print('Fila: ', list(row));
        # print('Campo: ', list(row)[0]);
        # print('Campo: ', list(row)[sourceIndex]);

        if list(row)[0] == "":
            tagName = "Agent"
        elif list(row)[sourceIndex] == "Agente":
            tagName = "Agent"
        elif list(row)[sourceIndex] == "CND":
            tagName = "CND"
        else:
            tagName = "NoSource"

        if len(list(row)) == len(wantedCols):
            if list(row)[validateIndex]:
                tagName = "Validate"
            elif list(row)[errorIndex]:
                tagName = "error"

        tree.insert("", END, values=list(row), tags=tagName)
        tagName = ""
        tree.tag_configure("CND", background="#eeeeee")  # Light grey
        tree.tag_configure("NoSource", background="darkgrey")
        tree.tag_configure("Validate", background="lightgreen")
        tree.tag_configure("error", background="red")
        ##84de80
        # print('newDf.iterrows: ', newDf.iterrows());
        # tree.pack(expand=True, fill="both")

    return [tree, hScrollBar, vScrollBar]
