from tkinter import *


window = Tk();

'''Program must be between window and window.mainloop'''

def km_to_miles():
    entryText = entryVar.get();
    entryMiles = float(entryText)*1.6;
    #print("Entry: ", entryText);
    text1.insert(END, entryMiles);
    entryVar.set("");

entryVar = StringVar();
entry = Entry(window, textvariable=entryVar);
entry.grid(row=0, column=0,rowspan=1, columnspan=2);

button1 = Button(window, text="Execute", command=km_to_miles);
button1.grid(row=1, column=0, rowspan=1);

button2 = Button(window, text="Entry");
button2.grid(row=1, column=1, rowspan=1);
#button1.pack();

text1 = Text(window, height=1, width= 30);
text1.grid(row=2, column=0, rowspan=1, columnspan=2) 

window.mainloop();