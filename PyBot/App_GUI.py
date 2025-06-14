# import tkinter as tkinter
import time

from Consult_GUI import consult_GUI
from Log_BackeEnd import backEnd
from Log_GUI import log_GUI


class App:
    # backend = backEnd('dev', 8000)
    def __init__(self, backend):
        self._isGranted = False
        self.backend = backend
        # print('Backend', self.backend)
        # super().__init__();
        # self.geometry("400x200");
        # self.title("Asistente de validación de Información Operativa AVIO")
        # print('Token :', self.backend.showToken() )

    @property
    def isGranted(self):
        return self._isGranted

    @isGranted.setter
    def isGranted(self, value):
        self._isGranted = value
        self.whenIsGrantedIsChanged(value)

    def loginGUI(self):
        log_GUI(backend, self.updateIsGranted)

    def updateIsGranted(self, isGranted):
        self.isGranted = isGranted
        print("¿User Granted? ", self.isGranted)

    def whenIsGrantedIsChanged(self, isGranted):
        if isGranted:
            print("User Granted!")
            consult_GUI(self.backend)


if __name__ == "__main__":
    defaultPort = 8000
    defaultEnv = "env"
    env = defaultEnv
    intPort = defaultPort
    print("Enter environment ('env:port'/'prod'): ")
    envPort = input()
    env_port = envPort.split(":")
    env = env_port[0]

    if len(env_port) == 1:
        if env == "env":
            print(f"Invalid port number. Using default port {defaultPort}.")
        elif env == "prod":
            print(f"Running App in {env}.")
        else:
            print(
                f"Invalid environment. Using default environment '{defaultEnv}' with default port {defaultPort}."
            )
            env = defaultEnv
    elif len(env_port) == 2:
        if env == "env":
            try:
                port = env_port[1]
                intPort = int(port)
                print(f"Running App {env}:{port}.")
            except (ValueError, IndexError):
                print(f"Invalid port number. Using default port {defaultPort}.")
                intPort = defaultPort
        elif env == "prod":
            print(f"Running '{env}'. Ignoring entered port.")
        else:
            print(
                f"Invalid environment. Using default environment '{defaultEnv}' with default port {defaultPort}."
            )

    else:
        print(
            f"Invalid environment. Using default environment '{defaultEnv}' with default port {defaultPort}."
        )
        env = defaultEnv
        intPort = defaultPort

    backend = backEnd(env, intPort)
    # print(f"Backend instance Created in {backend.env}.")
    time.sleep(1)
    app = App(backend)
    app.loginGUI()
    # app.mainloop();
