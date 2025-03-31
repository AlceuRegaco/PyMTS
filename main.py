"""
This file is used to open the introduction screen for the name of the person who will participate in the research and the person who is coordinating it.
"""

from encodings.utf_8 import encode
from tkinter import *
import os, json


# defining the path of the script
pastaApp = os.path.dirname(__file__)


def impDados(event=None):   # function to import data

    with open("session_settings.json", "w", encoding="utf8") as e:  # open the JSON file in write mode
        # writting the data to the JSON file
        json.dump({"Participant": vParticipant.get(),
                   "Experimenter": vExperimenter.get()
                   }, e, ensure_ascii=False)
    app.destroy()
    import trial_vs9_04     # import the trial file to start the experiment

def getDataSession():   # function to get the names of the blocks
    with open("configData.json", "r") as setting:
        blocks = json.load(setting)
    for item in blocks["blocks"]:
        listbox.insert(END, item)
    
def selectingBlock(event=None): # function to select the block
    selected_block = listbox.curselection()
    if selected_block:
        first_block = listbox.get(selected_block) 
        print("Selected block: ", first_block)
        changingConfigData(n=selected_block[0])
    else:
        print("No first block selected")

def changingConfigData(n):  # function to change the block in the configData.json file
    with open("configData.json", 'r', encoding='utf8') as file:
        data = json.load(file)
    data["start_block"] = n
    with open("configData.json", "w", encoding="utf8") as e:
        json.dump(data, e, ensure_ascii=False, indent=4, separators=(',', ': '))
    impDados()
    
# creating the window using tkinter
app = Tk()
app.title("Experiment Settings")    # title of the window
app.geometry("250x250+750+200")     # size and position of the window
app.configure(background="#dde")    # setting the background color of the window

Label(app, text="Participant: ",background="#dde", foreground="#000", anchor=W)\
.place(x=10, y=10, width=100, height=20)
vParticipant = Entry(app)
vParticipant.place(x=10, y=30, width=200, height=20)

Label(app, text="Experimenter: ",background="#dde", foreground="#000", anchor=W)\
.place(x=10, y=60, width=100, height=20)
vExperimenter = Entry(app)
vExperimenter.place(x=10, y=80, width=200, height=20)

listbox = Listbox(app)
listbox.place(x=10, y=110, width=200, height=80)

getDataSession()

btn = Button(app, text="enviar", command=selectingBlock)
btn.place(x=10, y=200, width=100, height=20)

app.bind('<Return>', impDados)

app.mainloop()