
from tkinter import *
from Helpers import Table
import threading

class consult_GUI():

    def updateInfoLabel(self, infoLabel, infoText, color, msg):
        infoLabel.configure(fg=color);
        infoText.set(msg);

    def tryGet(self, window, log, infoLabel, infoText):
        self.updateInfoLabel(infoLabel, infoText, "black", "Realizando consulta...");
        print('Realizando consulta...');
        consultDate = "2025-05-23"
        threading.Thread(target=self.executeConsult, args=(log, consultDate, infoLabel, infoText), daemon=True).start()
        infoLabel.update_idletasks()
        self.executeConsult(log, consultDate, infoLabel, infoText);
        
    def executeConsult(self, log, consultDate, infoLabel, infoText):
        data = log.getData(consultDate);
        # data = []
        infoText.set("");
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

        consultButton = Button(window, text="Consultar", command=lambda: self.tryGet(window, log, infoLabel, infoText));
        consultButton.grid(row=1, column=0, rowspan=1, padx=10, pady=10, sticky='W');
        
        frame = Frame(window);
        frame.grid(row=1, column=0, rowspan=1, padx=10, pady=10);
        data = [(1,'Raj','Mumbai',19), (2,'Aaryan','Pune',18),(3,'Vaishnavi','Mumbai',20),(4,'Rachna','Mumbai',21),(5,'Shubham','Delhi',21)]
        # print('Num columnas: ', len(data[0]));
        # t = Table(frame, data),
        # t.grid(row=2, column=0, rowspan=1, padx=10, pady=10);
        # window.iconbitmap('icono.ico');
        # window.columnconfigure(0, weight=1); #Tamaño de la columna cero en relación con las demás.
        # window.columnaconfigure(1, weight=1); 
        # window.rowconfigure(0, weight=1); #Tamaño de la fila cero en relación con las demás.

        # userEntry = StringVar();
        # userEntry.set("");
        # entry = Entry(window, textvariable=userEntry);
        # entry.grid(row=0, column=1, rowspan=1, columnspan=1, padx=10, pady=5);

        # label2 = Label(window, text= "Contraseña:", padx = 10);
        # label2.grid(row=1, column=0);

        # pswEntry = StringVar();
        # pswEntry.set("");
        # entry = Entry(window, show="*", textvariable=pswEntry);
        # entry.grid(row=1, column=1,rowspan=1, columnspan=1, padx=10, pady=5);

        infoText= StringVar();
        infoText.set("");
        infoLabel = Label(window, textvariable=infoText, padx = 10, fg='red');
        infoLabel.grid(row=2, column=0, columnspan=2, sticky="W");


        # text1 = Text(window, height=1, width= 20);
        # text1.grid(row=2, column=0, rowspan=1, columnspan=1) 

        window.mainloop();