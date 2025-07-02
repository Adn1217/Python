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
        backend,
        selectedDate,
        infoLabel,
        infoText,
        numActionsTextLabel,
        numActionsText,
        frame,
        table,
        selectedSource="todos",
    ):
        """Try to get data from the backend and update the GUI."""
        msg = f"Realizando consulta de {selectedSource} para el {selectedDate}..."
        self.update_infolabel(infoLabel, infoText, "black", msg)
        print(f"Realizando consulta de {selectedSource} para el {selectedDate}...")
        consultDate = selectedDate
        threading.Thread(
            target=self.execute_consult,
            args=(
                backend,
                consultDate,
                infoLabel,
                infoText,
                numActionsText,
                frame,
                table,
                selectedSource,
            ),
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
        backend,
        consultDate,
        infoLabel,
        infoText,
        numActionsText,
        frame,
        table,
        selectedSource,
    ):
        """Execute the consultation to the backend and update the GUI."""
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
            self.update_table(frame, data)

    def update_table(self, parent, data):
        """Update the table with received data."""
        # print('Numero de elementos: ', len(data));
        # df = pd.DataFrame(self.dataList);
        [table, xscrollBar, yscrollBar] = dfTable(parent, data)
        # print('Table list: ', self.dataList);
        table.grid(row=4, column=0, rowspan=1, padx=10, pady=10, sticky="EW")
        xscrollBar.grid(row=5, column=0, rowspan=1, sticky="EW")
        yscrollBar.grid(row=4, column=10, rowspan=1, sticky="NS")
        self.dataList = data
        return table

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

    def validate(self):
        """Validate operational records."""
        print("Se pulso validar")

    def __init__(self, backend):
        # super().__init__();
        # self.withdraw(); #Hidden.
        self._selectedDate = date.today()
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
        radioButton1 = Radiobutton(
            window, text="Agents", variable=selectedSource, value="agentes"
        )
        radioButton2 = Radiobutton(
            window, text="CND", variable=selectedSource, value="CND"
        )
        radioButton3 = Radiobutton(
            window, text="Todos", variable=selectedSource, value="todos"
        )

        radioButton1.grid(
            row=2, column=1, columnspan=1, rowspan=1, padx=10, pady=10, sticky="W"
        )

        radioButton2.grid(
            row=2, column=2, columnspan=1, rowspan=1, padx=10, pady=10, sticky="W"
        )

        radioButton3.grid(
            row=2, column=3, columnspan=1, rowspan=1, padx=10, pady=10, sticky="W"
        )

        validateButton = Button(
            window,
            text="Validar",
            command=lambda: self.validate(),
        )
        validateButton.grid(row=2, column=4, rowspan=1, padx=10, pady=10, sticky="W")

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

        table = self.update_table(frame, self.dataList)

        numActionsText = StringVar()
        numActionsText.set("0 registros.")
        numActionsTextLabel = Label(window, textvariable=numActionsText, padx=10)
        numActionsTextLabel.grid(row=10, column=0, columnspan=3, sticky="W")

        consultButton = Button(
            window,
            text="Consultar",
            command=lambda: self.try_get(
                backend,
                dateText.get(),
                infoLabel,
                infoText,
                numActionsTextLabel,
                numActionsText,
                frame,
                table,
                selectedSource.get(),
            ),
        )
        consultButton.grid(row=2, column=0, rowspan=1, padx=10, pady=10, sticky="W")

        # text1 = Text(window, height=1, width= 20);
        # text1.grid(row=2, column=0, rowspan=1, columnspan=1)
        # while True:

        #     window.update()
        window.mainloop()

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
