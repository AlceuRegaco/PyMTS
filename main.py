"""
Este arquivo serve para abrir a tela de introdução do nome da pessoa que irá participar da pesquisa e da pessoa que está coordenando 
"""
from encodings.utf_8 import encode
from tkinter import *
import os, json


# definir a pasta base do programa
pastaApp = os.path.dirname(__file__)

def impDados():
    with open("session_settings.json", "w", encoding="utf8") as e:
        json.dump({"Participant": vParticipant.get(),
                   "Experimenter": vExperimenter.get()
                   }, e, ensure_ascii=False)
        e.close()
    import trial_vs9_02
app = Tk()
app.title("Experiment Settings")    # nome da aba
app.geometry("300x150+750+200")     # tamanho da aba 
app.configure(background="#dde")    

Label(app, text="Participant: ",background="#dde", foreground="#000", anchor=W)\
.place(x=10, y=10, width=100, height=20)
vParticipant = Entry(app)
vParticipant.place(x=10, y=30, width=200, height=20)

Label(app, text="Experimenter: ",background="#dde", foreground="#000", anchor=W)\
.place(x=10, y=60, width=100, height=20)
vExperimenter = Entry(app)
vExperimenter.place(x=10, y=80, width=200, height=20)

btn = Button(app, text="enviar", command=impDados)
btn.place(x=10, y=110, width=100, height=20)


app.mainloop()