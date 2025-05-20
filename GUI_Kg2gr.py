from tkinter import *


window = Tk();

'''Program must be between window and window.mainloop'''

def kg_to_rest():
    entryText = entryVar.get();
    entryG = float(entryText)*1000;
    entryP = float(entryText)*2.20462;
    entryO = float(entryText)*35.274;
    #print("Entry: ", entryText);
    text1.delete("1.0", END);
    text1.insert(END, entryG);
    text2.delete("1.0", END);
    text2.insert(END, entryP);
    text3.delete("1.0", END);
    text3.insert(END, entryO);
    entryVar.set("");


# frm = Frame(window, padx=5);
# frm.grid();

label1 = Label(window, text= "Kg.", padx = 10);
label1.grid(row=0, column=0);


entryVar = StringVar();
entry = Entry(window, textvariable=entryVar);
entry.grid(row=0, column=1,rowspan=1, columnspan=1, padx=10);

button1 = Button(window, text="Convert", command=kg_to_rest);
button1.grid(row=0, column=2, rowspan=1, padx=10);

# button2 = Button(window, text="Entry");
# button2.grid(row=1, column=1, rowspan=1);
#button1.pack();

label1 = Label(window, text= "Grams", padx = 10);
label1.grid(row=1, column=0);

label2 = Label(window, text= "Pounds", padx = 10);
label2.grid(row=1, column=1);

label3 = Label(window, text= "Ounces", padx = 10);
label3.grid(row=1, column=2);

text1 = Text(window, height=1, width= 20);
text1.grid(row=2, column=0, rowspan=1, columnspan=1) 

text2 = Text(window, height=1, width= 20)
text2.grid(row=2, column=1, rowspan=1, columnspan=1) 

text3 = Text(window, height=1, width= 20)
text3.grid(row=2, column=2, rowspan=1, columnspan=1) 


window.mainloop();