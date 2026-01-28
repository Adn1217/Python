"""This module handles GUI operations for consulting a database using Tkinter."""

import os
import threading
from datetime import date, datetime
from tkinter import (BooleanVar, Button, Checkbutton, Frame, Label,
                     Radiobutton, StringVar, Tk, Toplevel, filedialog,
                     messagebox, ttk)

from dotenv import load_dotenv
from Helpers import dfTable, formatList, identifyColsToDisplay
from pymongo.errors import PyMongoError
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from tkcalendar import Calendar


class ConsultGUI:
    """Class to manage the GUI for consulting database"""

    def update_infolabel(self, infoLabel, infoText, msg, color="black"):
        """Update the information label with a message and color."""
        ##TODO: Control of infoLabel and infoText types and erase controls implemented in other methods.
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
        disabledButtons = keywords["disabledButtons"]
        # selectedSource = "todos"
        selectedSource = keywords["selectedSource"]
        msg = f"Realizando consulta de {selectedSource} para el {selectedDate}..."
        self.update_infolabel(infoLabel, infoText, msg)
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
            #     disabledButtons,
            #     selectedSource,
            # ),
            kwargs={
                "backend": backend,
                "consultDate": consultDate,
                "infoLabel": infoLabel,
                "infoText": infoText,
                "numActionsText": numActionsText,
                "frame": frame,
                "disabledButtons": disabledButtons,
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
        disabledButtons = keywords["disabledButtons"]
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
            self.update_table(frame, data, self.selected_layout, disabledButtons)

    def update_table(self, parent, data, selectedLayout="completa", buttons=None):
        """Update the table with received data."""
        # print('Numero de elementos: ', len(data));
        # df = pd.DataFrame(self.dataList);
        [table, xscrollBar, yscrollBar] = dfTable(
            parent, data, self.selected_cols, selectedLayout
        )
        # print('Table list: ', self.dataList);
        table.grid(row=4, column=0, rowspan=1, padx=10, pady=10, sticky="EW")
        xscrollBar.grid(row=5, column=0, rowspan=1, sticky="EW")
        yscrollBar.grid(row=4, column=10, rowspan=1, sticky="NS")
        self.data_list = data
        if buttons is not None and len(buttons) > 0:
            self.update_buttons_state(buttons, self.data_list)
        return table

    def update_buttons_state(self, buttonSet: list[Button], dataList):
        """Update the state of the validate button based on the dataList number of elements."""

        state = "normal" if len(dataList) > 1 else "disabled"
        for button in buttonSet:
            button.configure(state=state)

    def select_date_and_exit(self, window, calendar, dateText):
        """Select the date from the calendar and close the window."""
        selectedDateStr = calendar.get_date()  # .strftime("%Y-%m-%D");
        selectedDateObj = datetime.strptime(selectedDateStr, "%m/%d/%y")
        fselectedDate = selectedDateObj.strftime("%Y-%m-%d")
        self.selected_date = selectedDateObj
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
        if self.selected_layout != selectedLayout:
            self.selected_layout = selectedLayout
            self.update_table(parent, self.data_list, self.selected_layout)
            # print("Radio button changed")

    def on_checkbox_click(self, recoverCheckbox):
        """Callback function for checkbox click."""
        # print("Checkbox clicked")
        self.selected_cols = [
            colVar.get()
            for _, colVar in self.col_var_dict.items()
            if colVar.get() != ""
        ]
        recoverCheckbox.configure(state="disabled")
        print("Selected columns: ", self.selected_cols)
        # self.update_table(frame, self.dataList, self.selectedLayout)

    def on_all_checkbox_click(self, allColVar, recoverCheckbox):
        """Select all columns in the checkbox list."""
        for key, colVar in self.col_var_dict.items():
            colVar.set(key)
        allColVar.set(False)
        recoverCheckbox.configure(state="normal")

    def on_none_checkbox_click(self, noneColVar, recoverCheckbox):
        """Deselect all columns in the checkbox list."""
        for _, colVar in self.col_var_dict.items():
            colVar.set("")
        noneColVar.set(False)
        recoverCheckbox.configure(state="normal")

    def on_recover_checkbox_click(self, recoverColVar):
        """Recover previously selected columns in the checkbox list."""

        for key, colVar in self.col_var_dict.items():
            if key in self.selected_cols:
                colVar.set(key)
            else:
                colVar.set("")

        recoverColVar.set(False)

    def validate(self, frame, infoText, infoLabel, dataList):
        """Validate operational records."""
        agentsDataList = []
        cndDataList = []
        idsToValidate = []
        idsWithError = []

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
            cndItemWitherror = False
            agentItemWitherror = False
            # if agentItem["statusType"] in ["Ejecutada", "Editada"]:
            for cndItem in cndDataList:
                if (
                    cndItem["instructionTime"] == ""
                    or cndItem["occurrenceTime"] == ""
                    or cndItem["confirmationTime"] == ""
                ) and (cndItem["statusType"] == "Validada"):
                    idsWithError.extend([cndItem["id"]])
                    cndItemWitherror = True
                if (
                    agentItem["instructionTime"] == ""
                    or agentItem["occurrenceTime"] == ""
                    or agentItem["confirmationTime"] == ""
                ) and (agentItem["statusType"] == "Validada"):
                    idsWithError.extend([agentItemId])
                    agentItemWitherror = True
                if (
                    not cndItemWitherror
                    and not agentItemWitherror
                    and cndItem["elementId"] == agentItem["elementId"]
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
            if item["id"] in idsWithError:
                item["error"] = True
            else:
                item["error"] = False

        if len(idsWithError) > 0:
            msg = "Existen registros validados con tiempos faltantes. Se resaltan en rojo. Revisar."
            color = "red"
            self.update_infolabel(infoLabel, infoText, msg, color)

        self.update_table(frame, itemsList, self.selected_layout)
        print("Se pulsó validar")

    def export(self, infoText, infoLabel, dataList):
        """Export operational records to a xlsx file."""
        outputFileName = "RegistrosSIO_" + str(self.selected_date) + ".xlsx"
        fdataList = formatList(dataList)
        [*_, df] = identifyColsToDisplay(
            fdataList, self.selected_layout, self.selected_cols
        )

        filePath = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("CSV files", "*.csv")],
            initialfile=outputFileName,
            title="Guardar como",
        )

        if filePath:
            print(f"Descargando registros a: {filePath}")
            try:
                if not filePath.lower().endswith(".csv"):
                    df.to_excel(
                        filePath, index=False, sheet_name=str(self.selected_date)
                    )
                else:
                    df.to_csv(filePath, index=False, sep=",")

                messagebox.showinfo(
                    "Descarga exitosa",
                    f"Registros guardados en {filePath}",
                )
                msg = f"Registros guardados en {outputFileName}"
                print(msg)
                self.update_infolabel(infoLabel, infoText, msg)

            except (ModuleNotFoundError, FileNotFoundError, PermissionError) as e:
                messagebox.showerror(
                    "Error",
                    f"Ha ocurrido un error al intentar descargar los registros: {e}",
                )
                msg = "Ha ocurrido un error en la descarga."
                color = "red"
                self.update_infolabel(infoLabel, infoText, msg, color)
                print(f"Error realizando la descarga: {e}")
        else:
            messagebox.showinfo("Info", "Descarga cancelada.")
            print("Descarga cancelada.")

    def try_save_custom_cols(self, **kwargs):
        """Controller of saving process of the selected custom columns."""
        # user = kwargs["user"]  # Unsecure way to get the user. Error if not provided.
        # customCols = kwargs["customCols"]
        # infoLabel = kwargs["infoLabel"]
        # infoText = kwargs["infoText"]
        user = kwargs.get("user", "")
        customColsDict = kwargs.get("customCols", [])
        infoLabel = kwargs.get("infoLabel", None)
        infoText = kwargs.get("infoText", None)
        selectedCols = [
            colVar.get() for _, colVar in customColsDict.items() if colVar.get() != ""
        ]
        # print("Selected columns: ", selectedCols)
        # with open("selected_columns.txt", "w") as f:
        #     for col in selectedCols:
        #         f.write(f"{col}\n")

        client = self.get_mongo_client(infoLabel, infoText)

        # Access a DB (creates it if it doesn't exist) and Collections
        doc = {"user": user, "columns": selectedCols}
        # wConcern = {"writeConcern": {"w": "majority", "j": True, "wtimeout": 2000}}
        if isinstance(client, MongoClient) and self.db_name and self.db_collection_name:
            db = client[self.db_name]
            collection = db[self.db_collection_name]
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
                        info = (
                            f"El usuario {user} ya tiene columnas personalizadas guardadas.\n"
                            "¿Desea sobrescribirlas?"
                        )
                        confirmationLabel = Label(window, text=info, padx=10)
                        confirmationLabel.grid(row=0, column=0, columnspan=2)
                        confirmButton = Button(
                            window,
                            text="Aceptar",
                            command=lambda: [
                                window.destroy(),
                                self.update_custom_cols(
                                    client, collection, doc, infoLabel, infoText
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
                        self.save_custom_cols(
                            client, collection, doc, infoLabel, infoText
                        )
                else:
                    self.update_infolabel(
                        infoLabel, infoText, "La BD de Mongo no responde", "red"
                    )
                    print("Mongo DB deployment is not reachable (ack = 0).")
            except PyMongoError as e:
                msg = "Error de Mongo al guardar las columnas seleccionadas."
                self.update_infolabel(infoLabel, infoText, msg, "red")
                print("Ha ocurrido error de Mongo: ", e)

    def update_custom_cols(self, client, collection, doc, infoLabel, infoText):
        """Save the custom columns document to the collection."""
        try:
            updateAck = collection.update_one(
                {"user": doc["user"]}, {"$set": {"columns": doc["columns"]}}
            )
            # print("updateAck: ", updateAck)
            if updateAck.acknowledged:
                print("Documents updated: ", updateAck.modified_count)
                if isinstance(infoLabel, Label) and isinstance(infoText, StringVar):
                    msg = "Columnas seleccionadas actualizadas correctamente."
                    self.update_infolabel(infoLabel, infoText, msg)
                print("Columnas seleccionadas actualizadas correctamente.")
        except PyMongoError as e:
            if isinstance(infoLabel, Label) and isinstance(infoText, StringVar):
                color = "red"
                msg = "Error de Mongo al guardar las columnas seleccionadas."
                self.update_infolabel(infoLabel, infoText, msg, color)
            print("Ha ocurrido error de Mongo: ", e)
        finally:
            client.close()

    def save_custom_cols(self, client, collection, doc, infoLabel, infoText):
        """Save the custom columns document to the collection."""
        try:
            insertAck = collection.insert_one(doc)
            print(insertAck)
            if insertAck.acknowledged:
                print("Document inserted with id: ", insertAck.inserted_id)
            if isinstance(infoLabel, Label) and isinstance(infoText, StringVar):
                msg = "Columnas seleccionadas guardadas correctamente."
                self.update_infolabel(infoLabel, infoText, msg)
            print("Columnas seleccionadas guardadas correctamente.")
        except PyMongoError as e:
            msg = "Error de Mongo al guardar las columnas seleccionadas."
            if isinstance(infoLabel, Label) and isinstance(infoText, StringVar):
                self.update_infolabel(infoLabel, infoText, msg, "red")
            print("Ha ocurrido error de Mongo: ", e)
        finally:
            client.close()

    def get_mongo_client(self, infoLabel, infoText) -> MongoClient | None:
        """Get a MongoDB client if the URI is configured."""
        client = None
        if self.mongo_db_uri:
            try:
                client = MongoClient(self.mongo_db_uri, server_api=ServerApi("1"))
            except PyMongoError as e:
                self.update_infolabel(
                    infoLabel, infoText, "Error de Mongo al crear el cliente.", "red"
                )
                print("Ha ocurrido error de Mongo al crear el cliente: ", e)
        else:
            self.update_infolabel(
                infoLabel, infoText, "MongoDB URI no está configurado.", "red"
            )
            print("MongoDB URI no está configurado.")
        return client

    def try_load_custom_cols(self, user, infoLabel, infoText):
        """Controller of loading process of the selected custom columns."""

        client = self.get_mongo_client(infoLabel, infoText)

        if isinstance(client, MongoClient) and self.db_name and self.db_collection_name:
            db = client[self.db_name]
            collection = db[self.db_collection_name]
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
                        info = (
                            f"El usuario {user} NO tiene columnas personalizadas guardadas.\n"
                            "¿Desea guardar las actualmente seleccionadas?"
                        )
                        confirmationLabel = Label(window, text=info, padx=10)
                        confirmationLabel.grid(row=0, column=0, columnspan=2)
                        confirmButton = Button(
                            window,
                            text="Aceptar",
                            command=lambda: [
                                self.save_custom_cols(
                                    client, collection, doc, infoLabel, infoText
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
                        self.load_custom_cols(
                            savedCols=savedCols, infoLabel=infoLabel, infoText=infoText
                        )
                else:
                    self.load_custom_cols(
                        infoLabel=infoLabel, infoText=infoText, connectionError=1
                    )
                    print("Mongo DB deployment is not reachable (ack = 0).")
            except PyMongoError as e:
                self.update_infolabel(
                    infoLabel,
                    infoText,
                    "Error de Mongo al cargar las columnas personalizadas.",
                    "red",
                )
                print("Ha ocurrido error de Mongo: ", e)
            finally:
                client.close()

    def load_custom_cols(self, **kwargs):
        """Load the custom columns from a file or database."""
        # colVarList = kwargs["colVarList"]
        # colVarList = self.col_var_dict
        colVarListDict = self.col_var_dict
        infoLabel = kwargs.get("infoLabel", None)
        infoText = kwargs.get("infoText", None)
        connectionError = kwargs.get("connectionError", 0)
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
            if connectionError == 0:
                msg = (
                    "Usuario sin columnas personalizadas guardadas."
                    "Se cargaron columnas por defecto."
                )
                if isinstance(infoLabel, Label) and isinstance(infoText, StringVar):
                    self.update_infolabel(infoLabel, infoText, msg)
                print(msg)
            else:
                msg = "No fue posible conectarse a Mongo. Se cargaron columnas por defecto."
                color = "red"
                if isinstance(infoLabel, Label) and isinstance(infoText, StringVar):
                    self.update_infolabel(infoLabel, infoText, msg, color)
                print(msg)
            self.selected_cols = savedCols
        else:
            msg = "Columnas personalizadas cargadas correctamente."
            if isinstance(infoLabel, Label) and isinstance(infoText, StringVar):
                self.update_infolabel(infoLabel, infoText, msg)
            self.selected_cols = savedCols

        # for colVar in colVarList:
        #     if colVar.get() in savedCols:
        #         colVar.set(colVar.get())
        #     else:
        #         colVar.set("")

        for col, colVar in colVarListDict.items():
            if col in savedCols:
                colVar.set(col)
            else:
                colVar.set("")

    def __init__(self, backend, grantedUser):

        # super().__init__();
        # self.withdraw(); #Hidden.
        load_dotenv()
        self.granted_user = grantedUser
        self.selected_date = date.today()
        self.col_var_dict = {}
        self.selected_layout = "completa"  # Default layout
        self.db_name = os.getenv("MONGODB_DB_NAME")
        self.db_collection_name = os.getenv("MONGODB_COL_COLLECTION_NAME")
        self.mongo_db_uri = os.getenv("MONGODB_URL")
        print("Mongo DB URI: ", self.mongo_db_uri)

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
        self.selected_cols = wantedCols.copy()
        dataListDict = {}
        for header in wantedCols:
            dataListDict[header] = ""
        self.data_list = [dataListDict]
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
        dateText.set(str(self.selected_date))
        dateTextLabel = Label(consultTab, textvariable=dateText, padx=10, fg="blue")
        dateTextLabel.grid(row=1, column=1, columnspan=1, sticky="W")

        selectDateButton = Button(
            consultTab,
            text="Seleccionar",
            command=lambda: self.select_date_window(dateText, self.selected_date),
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
        selectedLayout.set(self.selected_layout)  # Completa por defecto
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

        infoText = StringVar()
        infoText.set("")
        infoLabel = Label(consultTab, textvariable=infoText, padx=10)
        infoLabel.grid(row=3, column=0, columnspan=3, sticky="W")

        validateButton = Button(
            consultTab,
            text="Validar",
            state="disabled",
            command=lambda: self.validate(frame, infoText, infoLabel, self.data_list),
        )
        validateButton.grid(row=2, column=7, rowspan=1, padx=10, pady=10, sticky="W")

        exportButton = Button(
            consultTab,
            text="Exportar",
            state="disabled",
            command=lambda: self.export(infoText, infoLabel, self.data_list),
        )
        exportButton.grid(row=2, column=8, rowspan=1, padx=10, pady=10, sticky="W")

        frame = Frame(consultTab, width=1200, height=550)
        frame.grid(
            row=4, column=0, columnspan=10, rowspan=1, padx=10, pady=5, sticky="W"
        )

        frame.columnconfigure(
            list(range(gridNumCols)), weight=1
        )  # Configure all columns to expand
        frame.rowconfigure(
            list(range(gridNumCols)), weight=1
        )  # Configure all rows to expand
        frame.grid_propagate(False)  # Prevent frame from resizing to fit contents
        disabledButtons = [validateButton, exportButton]
        self.update_table(frame, self.data_list, self.selected_layout, disabledButtons)

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
                disabledButtons=[validateButton, exportButton],
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
            colVar = StringVar()  # Create a StringVar for each possible column
            # self.col_var_dict.append(colVar)
            self.col_var_dict[col] = (
                colVar  # Store StringVar in dictionary with column name as key
            )
            colVar.set(col)  # Default value for the checkbutton variable
            colCheckButton = Checkbutton(
                customFieldsTab,
                text=col,
                # variable=self.col_var_dict[-1],  # Last one = colVar
                variable=self.col_var_dict[col],  # Last one = colVar
                onvalue=col,
                offvalue="",
                command=lambda: self.on_checkbox_click(recoverColsCheckButton),
            )
            # colCheckButton.select()  # Select the checkbutton by default
            colCheckButton.grid(
                row=cont + 2, column=1 + numCol, columnspan=1, sticky="W"
            )

        allNoneCheckLabelText = StringVar()
        allNoneCheckLabelText.set("Seleccionar/Deseleccionar:")
        allNoneCheckLabel = Label(
            customFieldsTab,
            textvariable=allNoneCheckLabelText,
            padx=10,
            # pady=20,
            font=("Helvetica", 10, "bold"),
        )
        allNoneCheckLabel.grid(
            row=15,
            column=1,
            columnspan=2,
            sticky="NSEW",
        )
        allColVar = BooleanVar(
            value=False
        )  # Create a BooleanVar for all-cols checkbutton
        allColsCheckButton = Checkbutton(
            customFieldsTab,
            text="Todas",
            # variable=self.col_var_dict[-1],  # Last one = colVar
            variable=allColVar,
            # onvalue="",
            # offvalue="",
            command=lambda: self.on_all_checkbox_click(
                allColVar, recoverColsCheckButton
            ),
        )
        allColsCheckButton.grid(row=15, column=3, columnspan=1, sticky="W")

        noneColVar = BooleanVar(value=False)

        noneColsCheckButton = Checkbutton(
            customFieldsTab,
            text="Ninguna",
            # variable=self.col_var_dict[-1],  # Last one = colVar
            variable=noneColVar,
            command=lambda: self.on_none_checkbox_click(
                noneColVar, recoverColsCheckButton
            ),
        )
        noneColsCheckButton.grid(row=15, column=4, columnspan=1, sticky="W")

        recoverColVar = BooleanVar(
            value=False
        )  # Create a BooleanVar for all-cols checkbutton
        recoverColsCheckButton = Checkbutton(
            customFieldsTab,
            text="Recuperar",
            state="disabled",
            variable=recoverColVar,
            command=lambda: self.on_recover_checkbox_click(recoverColVar),
        )
        recoverColsCheckButton.grid(row=15, column=5, columnspan=1, sticky="W")

        saveCustomColsButton = Button(
            customFieldsTab,
            text="Guardar",
            command=lambda: self.try_save_custom_cols(
                user=self.granted_user,
                customCols=self.col_var_dict,
                infoLabel=infoLabelCustomCols,
                infoText=infoTextCustomCols,
            ),
        )
        saveCustomColsButton.grid(
            row=16, column=3, rowspan=1, padx=10, pady=10, sticky="WE"
        )

        loadCustomColsButton = Button(
            customFieldsTab,
            text="Cargar",
            command=lambda: self.try_load_custom_cols(
                user=self.granted_user,
                infoLabel=infoLabelCustomCols,
                infoText=infoTextCustomCols,
            ),
        )
        loadCustomColsButton.grid(
            row=16, column=4, rowspan=1, padx=10, pady=10, sticky="WE"
        )

        infoTextCustomCols = StringVar()
        infoTextCustomCols.set("")
        infoLabelCustomCols = Label(
            customFieldsTab, textvariable=infoTextCustomCols, padx=10, pady=10
        )
        infoLabelCustomCols.grid(row=14, column=1, columnspan=3, sticky="W")

        if (
            (self.mongo_db_uri is None)
            or (self.db_name is None)
            or (self.db_collection_name is None)
        ):
            print("Mongo DB environment variables not set.")
            infoTextCustomCols.set("Sin conexión a la base de datos.")

        self.try_load_custom_cols(
            user=self.granted_user,
            infoLabel=infoLabelCustomCols,
            infoText=infoTextCustomCols,
        )

        window.mainloop()

    @property
    def selected_layout(self):
        """Property to get the selectedLayout attribute."""
        return self._selected_layout

    @selected_layout.setter
    def selected_layout(self, value):
        """Setter for the selectedLayout attribute."""
        self._selected_layout = value

    @property
    def data_list(self):
        """Property to get the selectedDate attribute."""
        return self._data_list

    @data_list.setter
    def data_list(self, value):
        """Setter for the backend attribute."""
        self._data_list = value

    ##TODO: Remove grantedUser property and use directly self._grantedUser with inheritance in constructor.

    @property
    def granted_user(self):
        """Property to get the granted user."""
        return self._granted_user

    @granted_user.setter
    def granted_user(self, user):
        """Setter for the granted user."""
        self._granted_user = user

    @property
    def selected_date(self):
        """Property to get the selectedDate attribute."""
        return self._selected_date

    @selected_date.setter
    def selected_date(self, value):
        """Setter for the backend attribute."""
        self._selected_date = value
