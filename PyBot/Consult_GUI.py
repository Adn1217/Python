"""This module handles GUI operations for consulting a database using Tkinter."""

import os
import threading
from datetime import date, datetime
from tkinter import (Button, Checkbutton, Frame, Label, Radiobutton, StringVar,
                     Tk, Toplevel, ttk)

from dotenv import load_dotenv
from Helpers import dfTable
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from tkcalendar import Calendar


class ConsultGUI:
    """Class to manage the GUI for consulting database"""

    def update_infolabel(self, infoLabel, infoText, color, msg):
        """Update the information label with a message and color."""
        infoLabel.configure(fg=color)
        infoText.set(msg)

    def try_get(
        self,
        **keywords,  # selectedDate, infoLabel, infoText, numActionsText, frame, button, selectedSource="todos"
    ):
        """Try to get data from the backend and update the GUI."""
        backend = keywords["backend"]
        selectedDate = keywords["selectedDate"]
        infoLabel = keywords["infoLabel"]
        infoText = keywords["infoText"]
        numActionsText = keywords["numActionsText"]
        frame = keywords["frame"]
        button = keywords["button"]
        selectedSource = "todos"
        selectedSource = keywords["selectedSource"]
        msg = f"Realizando consulta de {selectedSource} para el {selectedDate}..."
        self.update_infolabel(infoLabel, infoText, "black", msg)
        print(f"Realizando consulta de {selectedSource} para el {selectedDate}...")
        consultDate = selectedDate
        threading.Thread(
            # TODO: Optimize threading to avoid passing too many arguments. Separate update table segment.
            target=self.execute_consult,
            # args=(
            #     backend,
            #     consultDate,
            #     infoLabel,
            #     infoText,
            #     numActionsText,
            #     frame,
            #     button,
            #     selectedSource,
            # ),
            kwargs={
                "backend": backend,
                "consultDate": consultDate,
                "infoLabel": infoLabel,
                "infoText": infoText,
                "numActionsText": numActionsText,
                "frame": frame,
                "button": button,
                "selectedSource": selectedSource,
            },
            daemon=True,
        ).start()
        # time.sleep(1)
        # infoLabel.update_idletasks()
        # table.update_idletasks()
        # numActionsTextLabel.update_idletasks()
        # print('Table list: ', self.dataList);
        # self.executeConsult(backend, consultDate, infoLabel, infoText);

    def execute_consult(
        self,
        **keywords,  # backend, consultDate, infoLabel, infoText, numActionsText, frame, button, selectedSource
    ):
        """Execute the consultation to the backend and update the GUI."""
        backend = keywords["backend"]
        consultDate = keywords["consultDate"]
        infoLabel = keywords["infoLabel"]
        infoText = keywords["infoText"]
        numActionsText = keywords["numActionsText"]
        frame = keywords["frame"]
        button = keywords["button"]
        selectedSource = keywords["selectedSource"]

        data = backend.get_data(consultDate, selectedSource)
        # data = []
        msg = f"Consulta del {consultDate}."
        infoText.set(msg)
        if len(data) == 1:
            msg2 = f"{len(data)} registro de {selectedSource}."
        else:
            msg2 = f"{len(data)} registros de {selectedSource}."
        numActionsText.set(msg2)
        print("Número de elementos: ", len(data))
        # print('First item of data: ', data[0]);
        if isinstance(data, dict) and "error" in data.keys():
            # self.dataList = {};
            error = data["error"]
            infoLabel.configure(fg="red")
            infoText.set(error)
            print(f"Info texto: {error}")
        else:
            # print('Numero de elementos: ', len(data));
            # table.destroy()
            self.update_table(frame, data, self.selectedLayout, button)

    def update_table(self, parent, data, selectedLayout="completa", button=None):
        """Update the table with received data."""
        # print('Numero de elementos: ', len(data));
        # df = pd.DataFrame(self.dataList);
        [table, xscrollBar, yscrollBar] = dfTable(
            parent, data, self.selectedCols, selectedLayout
        )
        # print('Table list: ', self.dataList);
        table.grid(row=4, column=0, rowspan=1, padx=10, pady=10, sticky="EW")
        xscrollBar.grid(row=5, column=0, rowspan=1, sticky="EW")
        yscrollBar.grid(row=4, column=10, rowspan=1, sticky="NS")
        self.dataList = data
        if button is not None:
            self.update_button_state(button, self.dataList)
        return table

    def update_button_state(self, validateButton: Button, dataList):
        """Update the state of the validate button based on the dataList number of elements."""
        state = "normal" if len(dataList) > 1 else "disabled"
        validateButton.configure(state=state)

    def select_date_and_exit(self, window, calendar, dateText):
        """Select the date from the calendar and close the window."""
        selectedDateStr = calendar.get_date()  # .strftime("%Y-%m-%D");
        selectedDateObj = datetime.strptime(selectedDateStr, "%m/%d/%y")
        fselectedDate = selectedDateObj.strftime("%Y-%m-%d")
        self.selectedDate = selectedDateObj
        print("Fecha seleccionada: ", fselectedDate)
        # selectedDate2= date.strptime(selectedDate, )
        dateText.set(fselectedDate)
        window.destroy()

    def select_date_window(self, dateText, selectedDate):
        """Open a new window to select a date."""
        window = Toplevel()
        # frm = Frame(window, padx=5);
        # frm.grid();
        window.title("Seleccione fecha")
        # window.geometry("600x400");
        dateLabel2 = Label(window, text="Seleccione la fecha de consulta: ", padx=10)
        dateLabel2.grid(row=0, column=0, columnspan=3)
        calendar = Calendar(
            window,
            selectmode="day",
            year=selectedDate.year,
            month=selectedDate.month,
            day=selectedDate.day,
        )
        calendar.grid(row=1, column=1, rowspan=3, padx=10, pady=10)
        selectDateButton2 = Button(
            window,
            text="Seleccionar",
            command=lambda: self.select_date_and_exit(window, calendar, dateText),
        )
        selectDateButton2.grid(row=4, column=1, rowspan=1, padx=10, pady=10)

    def on_radio_change(self, parent, selectedLayout):
        """Callback function for layout radio button change."""
        if self.selectedLayout != selectedLayout:
            self.selectedLayout = selectedLayout
            self.update_table(parent, self.dataList, self.selectedLayout)
            # print("Radio button changed")

    def on_checkBox_click(self):
        """Callback function for checkbox click."""
        # print("Checkbox clicked")
        self.selectedCols = [
            colVar.get() for colVar in self.colVarList if colVar.get() != ""
        ]
        print("Selected columns: ", self.selectedCols)
        # self.update_table(frame, self.dataList, self.selectedLayout)

    def validate(self, frame, dataList):
        """Validate operational records."""
        agentsDataList = []
        cndDataList = []
        idsToValidate = []

        for item in dataList:
            if item["source"] == "Agente":
                agentsDataList.append(item)
            else:
                cndDataList.append(item)

        for agentItem in agentsDataList:
            # TODO: Verify fields to compare and check comparing logic.
            # "consignmentId",
            # "causeChangeAvailability",
            # "elementCausingId",
            agentItemId = agentItem["id"]
            # if agentItem["statusType"] in ["Ejecutada", "Editada"]:
            for cndItem in cndDataList:
                if (
                    cndItem["elementId"] == agentItem["elementId"]
                    and cndItem["actionType"] == agentItem["actionType"]
                    and (cndItem["causeStatus"] == agentItem["causeStatus"])
                    and (cndItem["newAvailability"] == agentItem["newAvailability"])
                    and (cndItem["causeOperational"] == agentItem["causeOperational"])
                    and (
                        cndItem["withPriorAuthorization"]
                        == agentItem["withPriorAuthorization"]
                    )
                ):
                    cndItemInsTimeDate = datetime.strptime(
                        # cndItem["instructionTime"], "%Y-%m-%d %H:%M:%S.%f"
                        cndItem["instructionTime"],
                        "%Y-%m-%d %H:%M:%S",
                    )
                    cndItemOcurrTimeDate = datetime.strptime(
                        cndItem["occurrenceTime"], "%Y-%m-%d %H:%M:%S"
                    )
                    cndItemConfTimeDate = datetime.strptime(
                        cndItem["confirmationTime"], "%Y-%m-%d %H:%M:%S"
                    )
                    agentItemInsTimeDate = datetime.strptime(
                        agentItem["instructionTime"], "%Y-%m-%d %H:%M:%S"
                    )
                    agentItemOcurrTimeDate = datetime.strptime(
                        agentItem["occurrenceTime"], "%Y-%m-%d %H:%M:%S"
                    )
                    agentItemConfTimeDate = datetime.strptime(
                        agentItem["confirmationTime"], "%Y-%m-%d %H:%M:%S"
                    )

                    instMinsDiff = abs(
                        (cndItemInsTimeDate - agentItemInsTimeDate).total_seconds() / 60
                    )
                    ocurrMinsDiff = abs(
                        (cndItemOcurrTimeDate - agentItemOcurrTimeDate).total_seconds()
                        / 60
                    )
                    confMinsDiff = abs(
                        (cndItemConfTimeDate - agentItemConfTimeDate).total_seconds()
                        / 60
                    )
                    if not agentItem["withPriorAuthorization"]:
                        if (
                            instMinsDiff <= 2
                            and ocurrMinsDiff <= 2
                            and confMinsDiff <= 3
                        ):
                            cndItemId = cndItem["id"]
                            # print(f"Validar agentItem: {agentItemId}")
                            idsToValidate.extend([agentItemId, cndItemId])
                            break
                    else:
                        if ocurrMinsDiff <= 2 and confMinsDiff <= 3:
                            cndItemId = cndItem["id"]
                            # print(f"Validar agentItem: {agentItemId}")
                            idsToValidate.extend([agentItemId, cndItemId])
                            break

        itemsList = dataList

        for item in itemsList:
            if item["id"] in idsToValidate:
                item["validate"] = True
            else:
                item["validate"] = False

        self.update_table(frame, itemsList, self.selectedLayout)
        print("Se pulsó validar")

    def try_save_custom_cols(self, **kwargs):
        """Controller of saving process of the selected custom columns."""
        user = kwargs["user"]
        customCols = kwargs["customCols"]
        infoLabel = kwargs["infoLabel"]
        selectedCols = [col.get() for col in customCols if col.get() != ""]
        # print("Selected columns: ", selectedCols)
        # with open("selected_columns.txt", "w") as f:
        #     for col in selectedCols:
        #         f.write(f"{col}\n")

        # Create a new client and connect to the server
        client = MongoClient(self.mongDBUri, server_api=ServerApi("1"))

        # Access a DB (creates it if it doesn't exist) and Collections
        doc = {"user": user, "columns": selectedCols}
        # wConcern = {"writeConcern": {"w": "majority", "j": True, "wtimeout": 2000}}
        if self.dbName and self.dbCollectionName:
            db = client[self.dbName]
            collection = db[self.dbCollectionName]
            try:
                # Send a ping to confirm a successful connection
                ack = client.admin.command("ping")
                if ack["ok"] == 1:
                    print(
                        "Pinged your deployment. You successfully connected to MongoDB!"
                    )
                    query = {"user": user}  # Example query to find the user
                    numDocs = collection.count_documents(query)
                    if numDocs > 0:
                        window = Toplevel()
                        window.title("Confirmar")
                        # window.geometry("600x400");
                        info = f"El usuario {user} ya tiene columnas personalizadas guardadas.\n¿Desea sobrescribirlas?"
                        confirmationLabel = Label(window, text=info, padx=10)
                        confirmationLabel.grid(row=0, column=0, columnspan=2)
                        confirmButton = Button(
                            window,
                            text="Aceptar",
                            command=lambda: [
                                window.destroy(),
                                self.update_custom_cols(
                                    client, collection, doc, infoLabel
                                ),
                            ],
                        )
                        cancelButton = Button(
                            window,
                            text="Cancelar",
                            command=window.destroy,
                        )

                        confirmButton.grid(row=3, column=0, rowspan=1, padx=10, pady=10)
                        cancelButton.grid(row=3, column=1, rowspan=1, padx=10, pady=10)
                    else:
                        self.save_custom_cols(client, collection, doc, infoLabel)
                else:
                    print("Mongo DB deployment is not reachable (ack = 0).")
            except Exception as e:
                print(e)

    def update_custom_cols(self, client, collection, doc, infoLabel):
        """Save the custom columns document to the collection."""
        try:
            updateAck = collection.update_one(
                {"user": doc["user"]}, {"$set": {"columns": doc["columns"]}}
            )
            # print("updateAck: ", updateAck)
            if updateAck.acknowledged:
                print("Documents updated: ", updateAck.modified_count)
                infoLabel.set("Columnas seleccionadas guardadas correctamente.")
            client.close()
        except Exception as e:
            print(e)

    def save_custom_cols(self, client, collection, doc, infoLabel):
        """Save the custom columns document to the collection."""
        try:
            insertAck = collection.insert_one(doc)
            print(insertAck)
            if insertAck.acknowledged:
                print("Document inserted with id: ", insertAck.inserted_id)
            client.close()
            infoLabel.set("Columnas seleccionadas guardadas correctamente.")
        except Exception as e:
            print(e)

    def try_load_custom_cols(self, user, infoLabel):

        client = MongoClient(self.mongDBUri, server_api=ServerApi("1"))

        if self.dbName and self.dbCollectionName:
            db = client[self.dbName]
            collection = db[self.dbCollectionName]
            try:
                # Send a ping to confirm a successful connection
                ack = client.admin.command("ping")
                if ack["ok"] == 1:
                    print(
                        "Pinged your deployment. You successfully connected to MongoDB!"
                    )
                    query = {"user": user}  # Example query to find the user
                    doc = collection.find_one(query)
                    savedCols = doc["columns"] if doc and "columns" in doc else []
                    if doc is None:
                        window = Toplevel()
                        window.title("Usuario no encontrado")
                        # window.geometry("600x400");
                        info = f"El usuario {user} NO tiene columnas personalizadas guardadas.\n¿Desea guardar las actualmente seleccionadas?"
                        confirmationLabel = Label(window, text=info, padx=10)
                        confirmationLabel.grid(row=0, column=0, columnspan=2)
                        confirmButton = Button(
                            window,
                            text="Aceptar",
                            command=lambda: [
                                self.save_custom_cols(
                                    client, collection, doc, infoLabel
                                ),
                                window.destroy(),
                            ],
                        )
                        cancelButton = Button(
                            window,
                            text="Cancelar",
                            command=window.destroy,
                        )

                        confirmButton.grid(row=3, column=0, rowspan=1, padx=10, pady=10)
                        cancelButton.grid(row=3, column=1, rowspan=1, padx=10, pady=10)
                    else:
                        self.load_custom_cols(savedCols=savedCols, infoLabel=infoLabel)
                else:
                    self.load_custom_cols(infoLabel=infoLabel)
                    print("Mongo DB deployment is not reachable (ack = 0).")
            except Exception as e:
                print(e)

    def load_custom_cols(self, infoLabel, **kwargs):
        """Load the custom columns from a file or database."""
        # colVarList = kwargs["colVarList"]
        colVarList = self.colVarList
        # infoLabel = kwargs["infoLabel"]
        savedCols = kwargs.get("savedCols", [])
        if len(savedCols) == 0:
            # TODO: Change fixed defaultCols for the custom columns loaded from a file or database.
            defaultCols = [
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
                "validate",  # "validate" is used to highlight rows that are validated.
            ]
            savedCols = defaultCols
            infoLabel.set(
                "Usuario sin columnas personalizadas guardadas. Se cargaron columnas por defecto."
            )
            self.selectedCols = savedCols
        else:
            infoLabel.set("Columnas personalizadas cargadas correctamente.")
            self.selectedCols = savedCols

        # TODO: colVar is not saved. Is the current selection of columns, not the one saved.
        for colVar in colVarList:
            if colVar.get() in savedCols:
                colVar.set(colVar.get())
            else:
                colVar.set("")

    def __init__(self, backend, grantedUser):

        # super().__init__();
        # self.withdraw(); #Hidden.
        load_dotenv()
        self.grantedUser = grantedUser
        self.selectedDate = date.today()
        self.colVarList = []
        self.selectedLayout = "completa"  # Default layout
        self.dbName = os.getenv("MONGODB_DB_NAME")
        self.dbCollectionName = os.getenv("MONGODB_COL_COLLECTION_NAME")
        self.mongDBUri = os.getenv("MONGODB_URL")
        print("Mongo DB URI: ", self.mongDBUri)

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
        self.selectedCols = wantedCols.copy()
        dataListDict = {}
        for header in wantedCols:
            dataListDict[header] = ""
        self.dataList = [dataListDict]
        window = Tk()
        # frm = Frame(window, padx=5);
        # frm.grid();
        window.title("Consulta de registros operativos")
        window.geometry("1000x600")
        # window.attributes("-fullscreen", True)
        # window.state('zoomed');
        # window.iconbitmap('icono.ico');

        tabControl = ttk.Notebook(window)  # Create a notebook for tabs
        consultTab = Frame(tabControl)  # Create a tab for consultations
        customFieldsTab = Frame(tabControl)  # Create a tab for custom field's

        gridNumCols = 10

        # window.rowconfigure(0, weight=1); #Tamaño de la fila cero en relación con las demás.
        # today = date.today()

        tabControl.add(consultTab, text="Consulta")  # Add the consultation tabs
        tabControl.add(
            customFieldsTab, text="Campos personalizados"
        )  # Add the custom fields tabs
        tabControl.grid(row=0, column=0, rowspan=1, padx=10, pady=10, sticky="W")

        dateLabel = Label(consultTab, text="Fecha: ", padx=10)
        dateLabel.grid(row=1, column=0, sticky="W")

        dateText = StringVar()
        dateText.set(str(self.selectedDate))
        dateTextLabel = Label(consultTab, textvariable=dateText, padx=10, fg="blue")
        dateTextLabel.grid(row=1, column=1, columnspan=1, sticky="W")

        selectDateButton = Button(
            consultTab,
            text="Seleccionar",
            command=lambda: self.select_date_window(dateText, self.selectedDate),
        )
        selectDateButton.grid(row=1, column=2, rowspan=1, padx=10, pady=10, sticky="W")

        selectedSource = StringVar()  # Ambos por defecto
        selectedSource.set("todos")  # Set default value
        radioButtonAgents = Radiobutton(
            consultTab, text="Agents", variable=selectedSource, value="agentes"
        )
        radioButtonCND = Radiobutton(
            consultTab, text="CND", variable=selectedSource, value="CND"
        )
        radioButtonTodos = Radiobutton(
            consultTab, text="Todos", variable=selectedSource, value="todos"
        )

        radioButtonAgents.grid(
            row=2, column=1, columnspan=1, rowspan=1, padx=10, pady=10, sticky="W"
        )

        radioButtonCND.grid(
            row=2, column=2, columnspan=1, rowspan=1, padx=10, pady=10, sticky="W"
        )

        radioButtonTodos.grid(
            row=2, column=3, columnspan=1, rowspan=1, padx=10, pady=10, sticky="W"
        )

        vistaText = StringVar()
        vistaText.set("Vista: ")
        vistaLabel = Label(
            consultTab, textvariable=vistaText, padx=10, font=("Helvetica", 10, "bold")
        )
        vistaLabel.grid(row=2, column=4, columnspan=1, sticky="W")

        selectedLayout = StringVar()
        selectedLayout.set(self.selectedLayout)  # Completa por defecto
        radioButtonCompacta = Radiobutton(
            consultTab,
            text="Compacta",
            variable=selectedLayout,
            value="compacta",
            command=lambda: self.on_radio_change(frame, selectedLayout.get()),
        )

        radioButtonCompleta = Radiobutton(
            consultTab,
            text="Completa",
            variable=selectedLayout,
            value="completa",
            command=lambda: self.on_radio_change(frame, selectedLayout.get()),
        )

        radioButtonCompacta.grid(
            row=2, column=5, columnspan=1, rowspan=1, padx=10, pady=10, sticky="W"
        )

        radioButtonCompleta.grid(
            row=2, column=6, columnspan=1, rowspan=1, padx=10, pady=10, sticky="W"
        )

        validateButton = Button(
            consultTab,
            text="Validar",
            state="disabled",
            command=lambda: self.validate(frame, self.dataList),
        )
        validateButton.grid(row=2, column=7, rowspan=1, padx=10, pady=10, sticky="W")

        infoText = StringVar()
        infoText.set("")
        infoLabel = Label(consultTab, textvariable=infoText, padx=10, fg="red")
        infoLabel.grid(row=3, column=0, columnspan=3, sticky="W")

        frame = Frame(consultTab, width=1500, height=600)
        frame.grid(
            row=4, column=0, columnspan=9, rowspan=1, padx=10, pady=10, sticky="W"
        )

        frame.columnconfigure(
            list(range(gridNumCols)), weight=1
        )  # Configure all columns to expand
        frame.rowconfigure(
            list(range(gridNumCols)), weight=1
        )  # Configure all rows to expand
        frame.grid_propagate(False)  # Prevent frame from resizing to fit contents
        self.update_table(frame, self.dataList, self.selectedLayout, validateButton)

        numActionsText = StringVar()
        numActionsText.set("0 registros.")
        numActionsTextLabel = Label(consultTab, textvariable=numActionsText, padx=10)
        numActionsTextLabel.grid(row=10, column=0, columnspan=3, sticky="W")

        consultButton = Button(
            consultTab,
            text="Consultar",
            command=lambda: self.try_get(
                backend=backend,
                selectedDate=dateText.get(),
                infoLabel=infoLabel,
                infoText=infoText,
                numActionsText=numActionsText,
                frame=frame,
                button=validateButton,
                selectedSource=selectedSource.get(),
            ),
        )
        consultButton.grid(row=2, column=0, rowspan=1, padx=10, pady=10, sticky="W")

        # text1 = Text(window, height=1, width= 20);
        # text1.grid(row=2, column=0, rowspan=1, columnspan=1)
        # while True:

        #     window.update()
        #
        # ------------------------------------Configuration TAB-------------------------------------
        #
        # Custom fields tab for selecting columns to display
        # customFieldsTab.rowconfigure(1, weight=1)
        # customFieldsTab.columnconfigure(0, weight=1)
        colCheckLabelText = StringVar()
        colCheckLabelText.set("Columnas disponibles: ")
        colLabel = Label(
            customFieldsTab,
            textvariable=colCheckLabelText,
            padx=10,
            pady=20,
            font=("Helvetica", 10, "bold"),
        )
        colLabel.grid(
            row=1,
            column=0,
            columnspan=5,
            sticky="NSEW",
        )

        possibleCols = [
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
        ]

        cont = 0
        numCol = 0
        for col in possibleCols:

            if cont % 10 == 0:
                numCol = numCol + 1
                cont = 0

            cont = cont + 1
            colVar = StringVar()  # Create a StringVar for each column
            self.colVarList.append(colVar)
            colVar.set(col)  # Default value for the checkbutton variable
            colCheckButton = Checkbutton(
                customFieldsTab,
                text=col,
                variable=self.colVarList[-1],  # Last one = colVar
                onvalue=col,
                offvalue="",
                command=self.on_checkBox_click,
            )
            # colCheckButton.select()  # Select the checkbutton by default
            colCheckButton.grid(
                row=cont + 2, column=1 + numCol, columnspan=1, sticky="W"
            )

        saveCustomColsButton = Button(
            customFieldsTab,
            text="Guardar",
            command=lambda: self.try_save_custom_cols(
                user=self.grantedUser,
                customCols=self.colVarList,
                infoLabel=infoTextCustomCols,
            ),
        )
        saveCustomColsButton.grid(
            row=13, column=3, rowspan=1, padx=10, pady=10, sticky="WE"
        )

        loadCustomColsButton = Button(
            customFieldsTab,
            text="Cargar",
            command=lambda: self.try_load_custom_cols(
                user=self.grantedUser, infoLabel=infoTextCustomCols
            ),
        )
        loadCustomColsButton.grid(
            row=13, column=4, rowspan=1, padx=10, pady=10, sticky="WE"
        )

        infoTextCustomCols = StringVar()
        infoTextCustomCols.set("")
        infoLabelCustomCols = Label(
            customFieldsTab, textvariable=infoTextCustomCols, padx=10
        )
        infoLabelCustomCols.grid(row=14, column=1, columnspan=3, sticky="W")

        if (
            (self.mongDBUri is None)
            or (self.dbName is None)
            or (self.dbCollectionName is None)
        ):
            print("Mongo DB environment variables not set.")
            infoTextCustomCols.set("Sin conexión a la base de datos.")

        self.try_load_custom_cols(user=self.grantedUser, infoLabel=infoTextCustomCols)

        window.mainloop()

    @property
    def selectedLayout(self):
        """Property to get the selectedLayout attribute."""
        return self._selectedLayout

    @selectedLayout.setter
    def selectedLayout(self, value):
        """Setter for the selectedLayout attribute."""
        self._selectedLayout = value

    @property
    def dataList(self):
        """Property to get the selectedDate attribute."""
        return self._dataList

    @dataList.setter
    def dataList(self, value):
        """Setter for the backend attribute."""
        self._dataList = value

    @property
    def grantedUser(self):
        """Property to get the granted user."""
        return self._grantedUser

    @grantedUser.setter
    def grantedUser(self, user):
        """Setter for the granted user."""
        self._grantedUser = user

    @property
    def selectedDate(self):
        """Property to get the selectedDate attribute."""
        return self._selectedDate

    @selectedDate.setter
    def selectedDate(self, value):
        """Setter for the backend attribute."""
        self._selectedDate = value
