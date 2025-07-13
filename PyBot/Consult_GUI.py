"""This module handles GUI operations for consulting a database using Tkinter."""

import threading
from datetime import date, datetime
from tkinter import Button, Frame, Label, Radiobutton, StringVar, Tk, Toplevel

from Helpers import dfTable
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
        [table, xscrollBar, yscrollBar] = dfTable(parent, data, selectedLayout)
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

    def __init__(self, backend):
        # super().__init__();
        # self.withdraw(); #Hidden.
        self.selectedDate = date.today()
        self.selectedLayout = "completa"  # Default layout

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

        gridNumCols = 10
        for i in range(gridNumCols):
            window.columnconfigure(
                i, weight=1
            )  # Tamaño de la columna i en relación con las demás.

        # window.rowconfigure(0, weight=1); #Tamaño de la fila cero en relación con las demás.
        # today = date.today()

        dateLabel = Label(window, text="Fecha: ", padx=10)
        dateLabel.grid(row=0, column=0, sticky="W")

        dateText = StringVar()
        dateText.set(str(self.selectedDate))
        dateTextLabel = Label(window, textvariable=dateText, padx=10, fg="blue")
        dateTextLabel.grid(row=0, column=1, columnspan=1, sticky="W")

        selectDateButton = Button(
            window,
            text="Seleccionar",
            command=lambda: self.select_date_window(dateText, self.selectedDate),
        )
        selectDateButton.grid(row=0, column=2, rowspan=1, padx=10, pady=10, sticky="W")

        selectedSource = StringVar(window, "todos")  # Ambos por defecto
        radioButtonAgents = Radiobutton(
            window, text="Agents", variable=selectedSource, value="agentes"
        )
        radioButtonCND = Radiobutton(
            window, text="CND", variable=selectedSource, value="CND"
        )
        radioButtonTodos = Radiobutton(
            window, text="Todos", variable=selectedSource, value="todos"
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
            window, textvariable=vistaText, padx=10, font=("Helvetica", 10, "bold")
        )
        vistaLabel.grid(row=2, column=4, columnspan=1, sticky="W")

        selectedLayout = StringVar(window, self.selectedLayout)  # Completa por defecto
        radioButtonCompacta = Radiobutton(
            window,
            text="Compacta",
            variable=selectedLayout,
            value="compacta",
            command=lambda: self.on_radio_change(frame, selectedLayout.get()),
        )

        radioButtonCompleta = Radiobutton(
            window,
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
            window,
            text="Validar",
            state="disabled",
            command=lambda: self.validate(frame, self.dataList),
        )
        validateButton.grid(row=2, column=7, rowspan=1, padx=10, pady=10, sticky="W")

        infoText = StringVar()
        infoText.set("")
        infoLabel = Label(window, textvariable=infoText, padx=10, fg="red")
        infoLabel.grid(row=3, column=0, columnspan=3, sticky="W")

        frame = Frame(window)
        frame.grid(
            row=4, column=0, columnspan=9, rowspan=1, padx=10, pady=10, sticky="W"
        )

        for i in range(10):
            frame.columnconfigure(index=i, weight=1)
            frame.rowconfigure(index=i, weight=1)

        self.update_table(frame, self.dataList, self.selectedLayout, validateButton)

        numActionsText = StringVar()
        numActionsText.set("0 registros.")
        numActionsTextLabel = Label(window, textvariable=numActionsText, padx=10)
        numActionsTextLabel.grid(row=10, column=0, columnspan=3, sticky="W")

        consultButton = Button(
            window,
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
    def selectedDate(self):
        """Property to get the selectedDate attribute."""
        return self._selectedDate

    @selectedDate.setter
    def selectedDate(self, value):
        """Setter for the backend attribute."""
        self._selectedDate = value
