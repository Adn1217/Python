
from tkinter import *


class consult_GUI():

    def tryLogin(self, window, log, updateIsGranted, userEntry, pswEntry, infoText):
        textInfo = log.logIn(userEntry, pswEntry);
        if(textInfo == ""):
            window.destroy();
            updateIsGranted(True);
        else:
            # infoLabel.configure(text=infoText);
            infoText.set(textInfo);
            # print(f'Info texto: {textInfo}');
    
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
        print('Granted recibido de App: ', userGranted)
        window = Tk();
        # frm = Frame(window, padx=5);
        # frm.grid();
        window.title('Consulta de registros operativos');
        window.geometry("1000x600");
        # window.attributes("-fullscreen", True)
        window.state('zoomed');
        # window.iconbitmap('icono.ico');
        # window.columnconfigure(0, weight=1); #Tamaño de la columna cero en relación con las demás.
        # window.columnaconfigure(1, weight=1); 
        # window.rowconfigure(0, weight=1); #Tamaño de la fila cero en relación con las demás.
        label1 = Label(window, text= "Usuario:", padx = 10);
        label1.grid(row=0, column=0);

        userEntry = StringVar();
        userEntry.set("");
        entry = Entry(window, textvariable=userEntry);
        entry.grid(row=0, column=1, rowspan=1, columnspan=1, padx=10, pady=5);

        label2 = Label(window, text= "Contraseña:", padx = 10);
        label2.grid(row=1, column=0);

        pswEntry = StringVar();
        pswEntry.set("");
        entry = Entry(window, show="*", textvariable=pswEntry);
        entry.grid(row=1, column=1,rowspan=1, columnspan=1, padx=10, pady=5);

        infoText= StringVar();
        infoText.set("");
        infoLabel = Label(window, textvariable=infoText, padx = 10, fg='red');
        infoLabel.grid(row=2, column=0, columnspan=2, sticky="W");

        loginButton = Button(window, text="Ingresar", command=lambda: self.tryLogin(window, log, updateIsGranted, userEntry, pswEntry, infoText));
        loginButton.grid(row=3, column=0, rowspan=1, padx=10, pady=10);

        cancelButton = Button(window, text="Cancelar", command=lambda: self.cancelLogin(window,updateIsGranted));
        cancelButton.grid(row=3, column=1, rowspan=1, pady=10);
        #button1.pack();

        # text1 = Text(window, height=1, width= 20);
        # text1.grid(row=2, column=0, rowspan=1, columnspan=1) 

        window.mainloop();