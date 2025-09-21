"""This module handles login GUI operations for user authentication."""

from tkinter import Button, Entry, Label, StringVar, Tk


class LogGUI:
    """GUI for user login."""

    def try_login(
        self, window, **kwargs
    ):  # log, updateIsGranted, userEntry, pswEntry, infoText
        """Try to log in with the provided credentials."""
        log = kwargs["log"]
        updateGrantedUser = kwargs["updateGrantedUser"]
        updateIsGranted = kwargs["updateIsGranted"]
        userEntry = kwargs["userEntry"]
        pswEntry = kwargs["pswEntry"]
        infoText = kwargs["infoText"]
        enteredUser = userEntry.get()

        textInfo = log.log_in(userEntry, pswEntry)
        # textInfo ='';
        # print("updateGrantedUser: ", updateGrantedUser)
        # print("updateIsGranted: ", updateIsGranted)
        if textInfo == "":
            if enteredUser == "":
                updateGrantedUser("usuarioPrueba")
            else:
                updateGrantedUser(enteredUser)
            window.destroy()
            updateIsGranted(True)
        else:
            infoText.set(textInfo)

    def cancel_login(self, window, updateGranted):
        """Handle cancellation of the login."""
        updateGranted(False)
        window.quit()

    def __init__(self, log, updateGrantedUser, updateIsGranted):
        # super().__init__();

        window = Tk()
        window.title("Login")
        userLabel = Label(window, text="Usuario:", padx=10)
        userLabel.grid(row=0, column=0)

        userEntry = StringVar()
        userEntry.set("")
        entry = Entry(window, textvariable=userEntry)
        entry.grid(row=0, column=1, rowspan=1, columnspan=1, padx=10, pady=5)

        pswLabel = Label(window, text="Contraseña:", padx=10)
        pswLabel.grid(row=1, column=0)

        pswEntry = StringVar()
        pswEntry.set("")
        entry = Entry(window, show="*", textvariable=pswEntry)
        entry.grid(row=1, column=1, rowspan=1, columnspan=1, padx=10, pady=5)

        infoText = StringVar()
        infoText.set("")
        infoLabel = Label(window, textvariable=infoText, padx=10, fg="red")
        infoLabel.grid(row=2, column=0, columnspan=2, sticky="W")

        loginButton = Button(
            window,
            text="Ingresar",
            command=lambda: self.try_login(
                window,
                log=log,
                updateGrantedUser=updateGrantedUser,
                updateIsGranted=updateIsGranted,
                userEntry=userEntry,
                pswEntry=pswEntry,
                infoText=infoText,
            ),
        )
        loginButton.grid(row=3, column=0, rowspan=1, padx=10, pady=10)

        cancelButton = Button(
            window,
            text="Cancelar",
            command=lambda: self.cancel_login(window, updateIsGranted),
        )
        cancelButton.grid(row=3, column=1, rowspan=1, pady=10)

        window.mainloop()
