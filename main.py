"""
Este arquivo serve para abrir a tela de introdução do nome da pessoa que irá participar da pesquisa e da pessoa que está coordenando 
"""
from encodings.utf_8 import encode
from tkinter import *
import os, json


# definir a pasta base do programa
pastaApp = os.path.dirname(__file__)

# Função para importar dados
def impDados(event=None):
    # Abrir o arquivo JSON em modo de escrita
    with open("session_settings.json", "w", encoding="utf8") as e:
        # Escrever as informações do participante e do experimentador no arquivo JSON
        json.dump({"Participant": vParticipant.get(),
                   "Experimenter": vExperimenter.get()
                   }, e, ensure_ascii=False)
    # Importar o script principal
    import trial_vs9_02

def getDataSession():
    with open("configData.json", "r") as setting:
        blocks = json.load(setting)
    for item in blocks["blocks"]:
        listbox.insert(END, item)
    
def selectingBlock(event=None):
    selected_block = listbox.curselection()
    if selected_block:
        first_block = listbox.get(selected_block) 
        print("Selected block: ", first_block)
        changingConfigData(n=selected_block[0])
    else:
        print("No first block selected")

def changingConfigData(n):
    with open("configData.json", 'r', encoding='utf8') as file:
        data = json.load(file)
    data["start_block"] = n
    with open("configData.json", "w", encoding="utf8") as e:
        json.dump(data, e, ensure_ascii=False, indent=4, separators=(',', ': '))
    impDados()
    
# Criação da interface gráfica usando Tkinter
app = Tk()
app.title("Experiment Settings")    # Título da janela
app.geometry("250x250+750+200")     # Tamanho e posição da janela
app.configure(background="#dde")    # Cor de fundo da janela

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