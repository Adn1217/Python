
from tkinter import *
from Helpers import Table
from tkcalendar import Calendar
import threading
from datetime import date, datetime

class consult_GUI():

    def updateInfoLabel(self, infoLabel, infoText, color, msg):
        infoLabel.configure(fg=color);
        infoText.set(msg);

    def tryGet(self, log, selectedDate, infoLabel, infoText):
        msg = f"Realizando consulta para el {selectedDate}";
        self.updateInfoLabel(infoLabel, infoText, "black", msg);
        print('Realizando consulta para el ', selectedDate);
        consultDate = selectedDate;
        threading.Thread(target=self.executeConsult, args=(log, consultDate, infoLabel, infoText), daemon=True).start()
        infoLabel.update_idletasks()
        self.executeConsult(log, consultDate, infoLabel, infoText);
        
    def executeConsult(self, log, consultDate, infoLabel, infoText):
        data = log.getData(consultDate);
        # data = []
        infoText.set(f"Consulta del {consultDate}");
        print('Data: ', data);
        # window.destroy();
        if(isinstance(data, dict) and 'error' in data.keys()):
            error = data['error'];
            infoLabel.configure(fg='red');
            infoText.set(error);
            print(f'Info texto: {error}');
    
    def cancelLogin(self, window, updateGranted):
        updateGranted(False);
        window.quit();
        # self.deiconify();
        # self.destroy();

    def selectDateAndExit(self, window, calendar, dateText):
        selectedDateStr=calendar.get_date() #.strftime("%Y-%m-%D");
        # date_string = "12/25/24"
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

    

    def __init__(self, log, updateIsGranted, userGranted):
        super().__init__();
        # self.withdraw(); #Hidden.
        userGranted

        '''Program must be between window and window.mainloop'''
        # print('Granted recibido de App: ', userGranted)
        window = Tk();
        # frm = Frame(window, padx=5);
        # frm.grid();
        window.title('Consulta de registros operativos');
        window.geometry("1000x600");
        # window.attributes("-fullscreen", True)
        # window.state('zoomed');
        # window.iconbitmap('icono.ico');
        # window.columnconfigure(0, weight=1); #Tamaño de la columna cero en relación con las demás.
        # window.columnconfigure(1, weight=1); 
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

        consultButton = Button(window, text="Consultar", command=lambda: self.tryGet(log, dateText.get(), infoLabel, infoText));
        consultButton.grid(row=2, column=0, rowspan=1, padx=10, pady=10, sticky='W');
        
        infoText= StringVar();
        infoText.set("");
        infoLabel = Label(window, textvariable=infoText, padx = 10, fg='red');
        infoLabel.grid(row=3, column=0, columnspan=3, sticky="W");
        
        # frame = Frame(window);
        # frame.grid(row=1, column=0, rowspan=1, padx=10, pady=10);
        data = [(1,'Raj','Mumbai',19), (2,'Aaryan','Pune',18),(3,'Vaishnavi','Mumbai',20),(4,'Rachna','Mumbai',21),(5,'Shubham','Delhi',21)]
        # print('Num columnas: ', len(data[0]));
        # t = Table(frame, data),
        # t.grid(row=2, column=0, rowspan=1, padx=10, pady=10);


        # text1 = Text(window, height=1, width= 20);
        # text1.grid(row=2, column=0, rowspan=1, columnspan=1) 

        window.mainloop();