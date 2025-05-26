from tkinter import *

class log_GUI():

    def tryLogin(self, window, log, updateIsGranted, userEntry, pswEntry, infoText):
        textInfo = log.logIn(userEntry, pswEntry);
        # textInfo ='';
        if(textInfo == ""):
            window.destroy();
            updateIsGranted(True);
        else:
            infoText.set(textInfo);
    
    def cancelLogin(self, window, updateGranted):
        updateGranted(False);
        window.quit();


    def __init__(self, log, updateIsGranted, userGranted):
        super().__init__();
        userGranted

        #print('Granted recibido de App: ', userGranted)
        window = Tk();
        window.title('Login');
        userLabel = Label(window, text= "Usuario:", padx = 10);
        userLabel.grid(row=0, column=0);

        userEntry = StringVar();
        userEntry.set("");
        entry = Entry(window, textvariable=userEntry);
        entry.grid(row=0, column=1, rowspan=1, columnspan=1, padx=10, pady=5);

        pswLabel = Label(window, text= "Contraseña:", padx = 10);
        pswLabel.grid(row=1, column=0);

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

        window.mainloop();