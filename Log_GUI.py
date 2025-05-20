from tkinter import *
from Log_BackeEnd import logging

log = logging();

window = Tk();

'''Program must be between window and window.mainloop'''

# frm = Frame(window, padx=5);
# frm.grid();

label1 = Label(window, text= "Usuario:", padx = 10);
label1.grid(row=0, column=0);

userEntry = StringVar();
entry = Entry(window, textvariable=userEntry);
entry.grid(row=0, column=1, rowspan=1, columnspan=1, padx=10, pady=5);

label2 = Label(window, text= "Contraseña:", padx = 10);
label2.grid(row=1, column=0);

pswEntry = StringVar();
entry = Entry(window, show="*", textvariable=pswEntry);
entry.grid(row=1, column=1,rowspan=1, columnspan=1, padx=10, pady=5);

button1 = Button(window, text="Aceptar", command=lambda: log.logIn(userEntry, pswEntry));
button1.grid(row=2, column=0, rowspan=1, padx=10, pady=10);

button2 = Button(window, text="Cancelar");
button2.grid(row=2, column=1, rowspan=1, pady=10);
#button1.pack();

# text1 = Text(window, height=1, width= 20);
# text1.grid(row=2, column=0, rowspan=1, columnspan=1) 

# text2 = Text(window, height=1, width= 20)
# text2.grid(row=2, column=1, rowspan=1, columnspan=1) 

# text3 = Text(window, height=1, width= 20)
# text3.grid(row=2, column=2, rowspan=1, columnspan=1) 


window.mainloop();