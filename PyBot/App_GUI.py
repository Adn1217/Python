# import tkinter as tkinter
from Log_GUI import log_GUI
from Consult_GUI import consult_GUI
from Log_BackeEnd import logging


class App():
    
    log = logging();

    def __init__(self):
        isGranted = False;
        super().__init__();
        # self.geometry("400x200");
        # self.title("Asistente de validación de Información Operativa AVIO")
        self.loginGUI(self.log, self.updateIsGranted, isGranted);
        print('¿User granted?: ', isGranted);
        print('Token :', self.log.showToken() )
    
    def loginGUI(self, log, updateIsGranted, isGranted):
        log_GUI(log, updateIsGranted, isGranted);

    def updateIsGranted(self, isGranted):
        self.isGranted = isGranted;
    
    def whenIsGrantedIsChanged(self, updateIsGranted, isGranted):
        if(isGranted):
            print('User Granted!');
            consult_GUI(self.log, updateIsGranted, isGranted);

    def __setattr__(self, key, value):
        # self.key = value
        # print('keyChanged: ', key)
        if(key=='isGranted'):
            self.whenIsGrantedIsChanged(self.updateIsGranted, value)  # <-- Your function
        # super().__setattr__(key, value)

if __name__ == '__main__':
    app = App();
    # app.loginGUI();
    # app.mainloop(); 