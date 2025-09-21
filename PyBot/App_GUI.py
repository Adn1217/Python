"""This module handles the main application logic, including GUI initialization
and backend configuration."""

# import tkinter as tkinter
import time

from Consult_GUI import ConsultGUI
from Log_BackEnd import BackEnd
from Log_GUI import LogGUI


class App:
    """App class to manage the application state and GUI interactions."""

    # backend = backEnd('dev', 8000)
    def __init__(self, backend):
        self.grantedUser = ""
        self.isGranted = False
        # self._backend = backend
        self.backend = backend
        # print('Backend', self.backend)
        # super().__init__();
        # self.geometry("400x200");
        # self.title("Asistente de validación de Información Operativa AVIO")
        # print('Token :', self.backend.show_token() )

    @property
    def backend(self):
        """Property to get the backend instance."""
        return self._backend

    @backend.setter
    def backend(self, value):
        """Setter for the backend instance."""
        self._backend = value

    @property
    def grantedUser(self):
        """Property to get the granted user."""
        return self._grantedUser

    @grantedUser.setter
    def grantedUser(self, user):
        """Setter for the granted user."""
        self._grantedUser = user

    @property
    def isGranted(self):
        """Property to get the isGranted status."""
        return self._isGranted

    @isGranted.setter
    def isGranted(self, value):
        self._isGranted = value
        self.when_isgranted_is_changed(value)

    def login_gui(self):
        """Initialize the login GUI and set up the backend."""
        LogGUI(self.backend, self.update_granted_user, self.update_is_granted)

    def consult_gui(self):
        """Initialize the consult GUI with the backend."""
        ConsultGUI(self.backend, self.grantedUser)

    def update_granted_user(self, grantedUser):
        """Update the granted user and print the user for debug."""
        self.grantedUser = grantedUser
        print("Granted User: ", self.grantedUser)

    def update_is_granted(self, isGranted):
        """Update the isGranted status and print the status for debug."""
        self.isGranted = isGranted
        print("¿User Granted? ", self.isGranted)

    def when_isgranted_is_changed(self, isGranted):
        """Callback when isGranted status changes."""
        if isGranted:
            print("User Granted!")
            self.consult_gui()


def configureBackend(defaultEnv, defaultPort):
    """Configure the backend with the given environment and port."""
    env = defaultEnv
    intPort = defaultPort
    print("Enter environment ('env:port'/'prod'): ")
    envPort = input()
    _envPort = envPort.split(":")
    env = _envPort[0]

    if len(_envPort) == 1:
        if env == "env":
            print(f"Invalid port number. Using default port {defaultPort}.")
        elif env == "prod":
            print(f"Running App in {env}.")
        else:
            print("Invalid environment.")
            print(f"Using default environment '{defaultEnv}' and port {defaultPort}.")
            env = defaultEnv
    elif len(_envPort) == 2:
        if env == "env":
            try:
                port = _envPort[1]
                intPort = int(port)
                print(f"Running App {env}:{port}.")
            except (ValueError, IndexError):
                print(f"Invalid port number. Using default port {defaultPort}.")
                intPort = defaultPort
        elif env == "prod":
            print(f"Running '{env}'. Ignoring entered port.")
        else:
            print("Invalid environment.")
            print(f"Using default environment '{defaultEnv}' and port {defaultPort}.")

    else:
        print("Invalid environment.")
        print(f"Using default environment '{defaultEnv}' and port {defaultPort}.")
        env = defaultEnv
        intPort = defaultPort

    return BackEnd(env, intPort)


def main():
    """Main function to run the application."""

    # backend = BackEnd(env, intPort)
    backend = configureBackend(DEFAULTENV, DEFAULTPORT)
    # print(f"Backend instance Created in {backend.env}.")
    time.sleep(1)
    app = App(backend)
    app.login_gui()
    # app.mainloop();


DEFAULTPORT = 8000
DEFAULTENV = "env"

if __name__ == "__main__":
    main()
