
from tkinter import *
from Helpers import Table, dfTable
from tkcalendar import Calendar
import threading
from datetime import date, datetime

class consult_GUI():

    def updateInfoLabel(self, infoLabel, infoText, color, msg):
        infoLabel.configure(fg=color);
        infoText.set(msg);

    def tryGet(self, backend, selectedDate, infoLabel, infoText, numActionsTextLabel, numActionsText, frame, table):
        msg = f"Realizando consulta para el {selectedDate}...";
        self.updateInfoLabel(infoLabel, infoText, "black", msg);
        print(f'Realizando consulta para el {selectedDate}...');
        consultDate = selectedDate;
        threading.Thread(target=self.executeConsult, args=(backend, consultDate, infoLabel, infoText,numActionsText, frame, table), daemon=True).start()
        infoLabel.update_idletasks();
        table.update_idletasks();
        numActionsTextLabel.update_idletasks();
        # print('Table list: ', self.dataList);
        # self.executeConsult(backend, consultDate, infoLabel, infoText);
        
    def executeConsult(self, backend, consultDate, infoLabel, infoText, numActionsText, frame, table):
        data = backend.getData(consultDate);
        # data = []
        msg = f"Consulta del {consultDate}."
        infoText.set(msg);
        if(len(data) == 1):
            msg2 = f"{len(data)} registro."
        else:
            msg2 = f"{len(data)} registros."
        numActionsText.set(msg2);
        print('Número de elementos: ', len(data));
        # print('First item of data: ', data[0]);
        if(isinstance(data, dict) and 'error' in data.keys()):
            # self.dataList = {};
            error = data['error'];
            infoLabel.configure(fg='red');
            infoText.set(error);
            print(f'Info texto: {error}');
        else:
            # print('Numero de elementos: ', len(data));
            table.destroy();
            self.updateTable(frame, data);
    
    def updateTable(self, parent, data):
        # print('Numero de elementos: ', len(data));
        self.dataList = data;
        # df = pd.DataFrame(self.dataList);    
        [table, xscrollBar, yscrollBar] = dfTable(parent, self.dataList);
        # print('Table list: ', self.dataList);
        table.grid(row=4, column=0, rowspan=1, padx=10, pady=10, sticky='EW');
        xscrollBar.grid(row=5, column=0, rowspan=1, sticky='EW');
        yscrollBar.grid(row=4, column=10, rowspan=1, sticky='NS');
        return table;
            

    @property
    def dataList(self):
        return self._dataList

    @dataList.setter
    def dataList(self, value):
        self._dataList = value

    def selectDateAndExit(self, window, calendar, dateText):
        selectedDateStr=calendar.get_date() #.strftime("%Y-%m-%D");
        selectedDateObj = datetime.strptime(selectedDateStr, "%m/%d/%y")
        fselectedDate = selectedDateObj.strftime("%Y-%m-%d")
        print('Fecha seleccionada: ', fselectedDate)
        # selectedDate2= date.strptime(selectedDate, )
        dateText.set(fselectedDate);
        window.destroy();
    
    def selectDateWindow(self, dateText, today):
        window = Tk();
        # frm = Frame(window, padx=5);
        # frm.grid();
        window.title('Seleccione fecha');
        # window.geometry("600x400");
        dateLabel2 = Label(window, text= "Seleccione la fecha de consulta: ", padx = 10);
        dateLabel2.grid(row=0, column=0, columnspan=3);
        calendar = Calendar(window, selectmode = 'day', year = today.year, month = today.month, day = today.day);
        calendar.grid(row=1, column=1, rowspan=3, padx=10, pady=10);
        selectDateButton2 = Button(window, text="Seleccionar", command=lambda: self.selectDateAndExit(window, calendar, dateText));
        selectDateButton2.grid(row=4, column=1, rowspan=1, padx=10, pady=10);

    

    def __init__(self, backend):
        # super().__init__();
        # self.withdraw(); #Hidden.
        # self._dataList = {'id': [], 'nombre': [], 'edad': []};
        wantedCols  = ['id', 'actionType', 'elementId', 'elementName', 'elementCompanyShortName', 'instructionTime', 'occurrenceTime',
                       'confirmationTime', 'causeStatus', 'consignmentId', 'causeChangeAvailability', 'newAvailability',
                       'elementCausingId', 'causeOperational', 'percentage','withPriorAuthorization', 'description',
                       'verificationNote', 'statusType', 'system', 'causeOrigin', 'causeDetailCno', 'additionalFieldsValue',
                       'espName', 'espElementId', 'unavailableActionId', 'subSystemUnavailableAction', 'cneZone', 'fuel',
                       'fuelName', 'fuelCEN', 'plantCEN', 'qualityScheme', 'source','dna', 'userValidator', 'configurationDesc',
                       'thermalStateId', 'descriptionAdditional'];
        dataListDict =  {}
        for header in wantedCols:
            dataListDict[header] = [];
        self._dataList = [dataListDict];
        window = Tk();
        # frm = Frame(window, padx=5);
        # frm.grid();
        window.title('Consulta de registros operativos');
        window.geometry("1000x600");
        # window.attributes("-fullscreen", True)
        # window.state('zoomed');
        # window.iconbitmap('icono.ico');

        gridNumCols = 10
        for i in range(gridNumCols):
            window.columnconfigure(i, weight=1); #Tamaño de la columna i en relación con las demás.

        # window.rowconfigure(0, weight=1); #Tamaño de la fila cero en relación con las demás.
        today = date.today();

        dateLabel = Label(window, text= "Fecha: ", padx = 10);
        dateLabel.grid(row=0, column=0, sticky ="W");

        dateText= StringVar();
        dateText.set(today);
        dateTextLabel = Label(window, textvariable=dateText, padx = 10, fg='blue');
        dateTextLabel.grid(row=0, column=1, columnspan=1, sticky="W");

        selectDateButton = Button(window, text="Seleccionar", command=lambda: self.selectDateWindow(dateText, today));
        selectDateButton.grid(row=0, column=2, rowspan=1, padx=10, pady=10, sticky='W');
        
        infoText= StringVar();
        infoText.set("");
        infoLabel = Label(window, textvariable=infoText, padx = 10, fg='red');
        infoLabel.grid(row=3, column=0, columnspan=3, sticky="W");
        
        frame = Frame(window);
        frame.grid(row=4, column=0, columnspan=9, rowspan=1, padx=10, pady=10, sticky='W');

        for i in range(10):
            frame.columnconfigure(index=i, weight=1)
            frame.rowconfigure(index=i, weight=1)

        table = self.updateTable(frame, self.dataList);

        numActionsText= StringVar();
        numActionsText.set("0 registros.");
        numActionsTextLabel = Label(window, textvariable=numActionsText, padx = 10);
        numActionsTextLabel.grid(row=10, column=0, columnspan=1, sticky="W");
        
        consultButton = Button(window, text="Consultar", command=lambda: self.tryGet(backend, dateText.get(), infoLabel, infoText, numActionsTextLabel, numActionsText, frame, table));
        consultButton.grid(row=2, column=0, rowspan=1, padx=10, pady=10, sticky='W');
        
        
        # text1 = Text(window, height=1, width= 20);
        # text1.grid(row=2, column=0, rowspan=1, columnspan=1) 

        window.mainloop();