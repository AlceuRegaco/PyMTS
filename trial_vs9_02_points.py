#utf8
from random import shuffle
import pygame
import sys
import os
import time
from stimuli import Sound, Image, Text       #chamando as classes dentro do arquivo 'stimuli.py'
import json
import pandas as pd
from datetime import datetime
import numpy as np

pygame.init()

screen = pygame.display.set_mode()

x, y = screen.get_size()
pygame.display.quit()
size =  width, height = np.array([(x-100), (y-100)])
screen = pygame.display.set_mode(size, pygame.RESIZABLE)


pygame.display.set_caption("PyMTS")

class Trial:
    
    def __init__(self):
        self.clock = pygame.time.Clock()

        self.trialCount = 0         # flag para contar quantas tentativas já foram (daquelas que foram programadas)
        self.totalTrials = 0        # número total de tentativas de cada bloco
        self.isCorrect = 0          # flag para saber se a pessoa acertou ou errou
        self.accuracy = 0           # quantas tentativas corretas
        self.expTrial = 0           # número total de tentativas do experimento
        self.block_repetion = 0
        
        with open("configData.json") as setting:
            config = json.load(setting)
            setting.close()
        
        self.block_parameter = config["start_block"]    # parâmetro do bloco para saber qual arquivo 'csv' buscar para organizar as tentativas
        # configurando variáveis
        self.update_values()        # função para atualizar quais serão os dados utilizados nas tentativas
        
        self.point_name = config["points_name"]     #função para pegar o nome dos pontos
        self.points = config["points"]      # função para pegar o número de pontos inicial
        self.pos_points = config["pos_points"]      # função para pegar a posição dos pontos
        self.text_size = config["text_size"]        #função para pegar o tamanho do texto dos pontos

        # inicia a tentativa
        self.load_experiment_data() # função para criar o arquivo no qual os dados serão salvos
        self.instruction()          # função para chamar a instrução inicial

    def load_experiment_data(self): # função para criar o arquivo no qual os dados serão salvos
        with open("session_settings.json") as e:
            self.expData = json.load(e)
            e.close()
        with open(f'data\{self.expData["Participant"]}.csv', "w+") as file:
            file.write(f"Participant;{self.expData['Participant']}\n")
            file.write(f"Experimenter;{self.expData['Experimenter']}\n")
            file.write(f'Date;{datetime.now()}\n\n')
            file.write(f"Total_Trial;Block;Block_Trial;Accuracy;Total_Correct;Points;Contextual_Stimulus;\
Sample;Sample_Sound;Comps;Selected_Comp;Time_Click_Sample;Time_Click_Comp;Time_Trial\n")
               
    def update_values(self):
        
        # função para atualizar quais serão os dados utilizados nas tentativas
        config = self.config_experiment()
        self.criterias = config[1]['criteria'] # lista de critérios dos blocos
        self.repetitions = config[1]['repetitions'] # lista do número de repetições máximas do bloco
        self.screen_color = config[1]['screen_color'] # cor da tela 
        self.time_ITI = config[1]['ITI']  # intervalo entre tentativas   
        self.blocks_number = len(config[1]['blocks']) # quantidade de blocos
        self.samples = config[0]['sample'].values # lista com os estímulos modelos (na ordem de apresentação)
        self.sample_sound = config[0]['sample_sound'].values # lista com os estímulos modelos auditivos (na ordem de apresentação)
        self.comps = [i.split(',') for i in config[0]['comp'].values]  # lista com os estímulos comparação (só a primeira letra e na mesma ordem dos modelos)
        self.correct_comps = [i.split(',') for i in config[0]['correct_comp'].values]

        self.cont_stim = config[0]['cont_stim'].values
        self.pos_cont_stim = config[1]['pos_stim_cont']
        self.points_right = config[0]['points_right'].values
        self.points_wrong = config[0]['points_wrong'].values

        self.img_right = config[0]['img_right'].values
        self.img_wrong = config[0]['img_wrong'].values
        self.sound_right = config[0]['sound_right'].values
        self.sound_wrong = config[0]['sound_wrong'].values
        self.time_right = config[0]['time_right'].values
        self.time_wrong = config[0]['time_wrong'].values
       
        self.pos_sample = config[1]['pos_sample']               # lista com os valores da posição do modelo
        self.pos_comps = config[1]['pos_comps']                 # lista com os valores da posição dos estímulos comparação 
        self.stimulus_size = config[1]['stimulus_size']         # lista com os valores do tamanho dos estímulos (todos devem ter a mesma proporção para não distorcer)
        self.instruction_size = config[1]['instructions_size']
        self.consequence_size = config[1]["consequence_size"]
        self.instructions = config[1]['instructions']           # lista com as instruções do experimento
        self.protocol = config[1]['protocol']                   # lista definido se é SMTS ou DMTS
        self.end_text = config[1]['end_text']

    def config_experiment(self):    # função para abrir as confiugurações opcionais do experimento (no arquivo 'myConfig.json')
        with open("configData.json") as setting:
            config = json.load(setting)
            setting.close()

        self.blocks = config["blocks"]           
        self.block_name = self.blocks[self.block_parameter] # pega o nome do bloco para usar durante o procedimento (caso precise)

        current_block = pd.read_csv(f"config/{self.block_name}.csv", sep=';')   # pega o bloco atual
        current_block = current_block.sample(current_block.shape[0])            # randomiza as tentativas dentro do próprio bloco
        
        return [current_block, config]      # ver informações do 'config' no arquivo 'config.json'

    def instruction(self):     # função para chamar as instruções (tanto a primeira quanto outras que você queira apresentar)
        screen.fill(self.screen_color)

        if self.instructions[self.block_parameter] == "n":
            self.sample()
        
        else:
            inst_text = Image(screen, self.instructions[self.block_parameter], self.instruction_size, (0, 0))
            timeI = time.time()
            while 1:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                    if event.type == pygame.MOUSEBUTTONDOWN and self.getTime(timeI) > 4: # tempo mínimo para a pessoa ler as instruções
                        self.sample()

                inst_text.update()
                pygame.display.update()

    def getTime(self, timeI): # função para retornar o tempo desde algum registro (que deverá ser passado ao se chamar a função)
        return time.time() - timeI

    def gui(self):
        text = Text(screen, 'white', f'{self.point_name}', text_size=self.text_size, text_pos=(self.pos_points[0], (self.pos_points[1]+60)))
        self.text_points = Text(screen, 'white', f'{self.points}', text_size=self.text_size+20, text_pos=(self.pos_points[0], self.pos_points[1]))
        return text.update(), self.text_points.update()

    def sample(self):
        self.timeI = time.time()
        screen.fill(self.screen_color)
        # define o tempo inical da apresentação do modelo
        timeI = time.time()
        sample = self.samples[self.trialCount]  # estímulo modelo visual
        sample_sound = self.sample_sound[self.trialCount]   # estímulo modelo auditivo
        cont_stim = self.cont_stim[self.trialCount]         # estímulo contextual
        self.save_cont_stim = cont_stim
        self.save_sample = sample
        self.save_sample_sound = sample_sound     
        self.sample_stimulus = Image(screen,sample,
                       self.stimulus_size,
                       self.pos_sample
                       )    # definindo o estímulo modelo
        self.cont_stim_stimulus = Image(screen,cont_stim,
                       self.stimulus_size,
                       self.pos_cont_stim
                       )    # definindo o estímulo contextual
        self.sample_sound_stimulus = Sound(sample_sound)   # definindo o estímulo modelo auditivo

        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if self.sample_stimulus.mouse_click(event) and self.sample_stimulus.mouse_hover():
                    if sample_sound == 'n':                        
                        self.save_time_sample = self.getTime(timeI)
                        self.comparison()
                    else:
                        self.save_time_sample = self.getTime(timeI)
                        self.sample_sound_stimulus.update(lops=0)   # toca o estímulo modelo auditivo
                        self.comparison()

            self.gui()
            self.sample_stimulus.update()  # apresentando o modelo
            self.cont_stim_stimulus.update()    # apresentando o estímulo contextual
            pygame.display.update()

    def comparison(self):
        sample_sound = self.sample_sound[self.trialCount]   # estímulo modelo auditivo
        comps = self.comps[self.trialCount]  # definindo a lista dos estímulos comparação
        shuffle(comps)  # randomizando a lista para randomizar a ordem dos estímulos
        # definindo os estímulos para serem apresentados
        stimuli = [Image(screen, comps[i], self.stimulus_size, self.pos_comps[i]) for i in range(len(comps))]
        self.save_comps = comps
        timeI = time.time() #resetando o tempo para apresentação dos estímulos comparação
        
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if self.protocol[self.block_parameter] == "SMTS":
                    if sample_sound == 'n':
                        ...
                    else:
                        if self.sample_stimulus.mouse_click(event) and self.sample_stimulus.mouse_hover():
                            if self.sample_sound_stimulus.isPlaying():
                                ...
                            else:
                                self.sample_sound_stimulus.stop()
                                self.sample_sound_stimulus.update(lops=0)   # toca o estímulo modelo auditivo

                for stimulus in stimuli:
                    if stimulus.mouse_click(event) and stimulus.mouse_hover():
                        if sample_sound == 'n':
                            if stimulus.name in self.correct_comps[self.trialCount]:
                                self.save_time_comp = self.getTime(timeI)
                                self.isCorrect = 1
                                self.accuracy += 1
                                self.points += self.points_right[self.trialCount]
                                self.save_select = stimulus.name
                                self.consequences(self.time_right[self.trialCount],
                                                self.img_right[self.trialCount],
                                                self.sound_right[self.trialCount])   # chamando as consequências a partir do acerto
                            else:
                                self.save_time_comp = self.getTime(timeI)
                                self.isCorrect = 0
                                self.points -= self.points_right[self.trialCount]
                                self.save_select = stimulus.name
                                self.consequences(self.time_wrong[self.trialCount],
                                                self.img_wrong[self.trialCount],
                                                self.sound_wrong[self.trialCount])      # chamando as consequências a partir do erro 

                        else:
                            if self.sample_sound_stimulus.isPlaying():
                                ...
                            else:
                                self.sample_sound_stimulus.stop()
                                # definindo acerto e erro

                                if stimulus.name in self.correct_comps[self.trialCount]:
                                    self.save_time_comp = self.getTime(timeI)
                                    self.isCorrect = 1
                                    self.accuracy += 1
                                    self.points += self.points_right[self.trialCount]
                                    self.save_select = stimulus.name
                                    self.consequences(self.time_right[self.trialCount],
                                                    self.img_right[self.trialCount],
                                                    self.sound_right[self.trialCount])   # chamando as consequências a partir do acerto
                                else:
                                    self.save_time_comp = self.getTime(timeI)
                                    self.isCorrect = 0
                                    self.points -= self.points_right[self.trialCount]
                                    self.save_select = stimulus.name
                                    self.consequences(self.time_wrong[self.trialCount],
                                                    self.img_wrong[self.trialCount],
                                                    self.sound_wrong[self.trialCount])      # chamando as consequências a partir do erro

            if self.protocol[self.block_parameter] == "SMTS":
                for stimulus in stimuli:
                    stimulus.update()   # apresentando os estímulos   
            else:
                if self.getTime(timeI) <= self.protocol[self.block_parameter]:
                    screen.fill(self.screen_color)   # preenchendo a tela                
                else:
                    for stimulus in stimuli:
                        stimulus.update()   # apresentando os estímulos
                     
            self.gui()
            pygame.display.update()

    def consequences(self, time_consequence, img_cons, sound_cons):
        
        screen.fill(self.screen_color)
        # definindo o texto da consequência
        consequence_img = Image(screen, img_cons, self.consequence_size, (0, 0)) # definindo a apresentação da consequência
        consequence_sound = Sound(sound_cons)
        timeI = time.time()
        self.trialCount += 1
        self.totalTrials += 1
        self.expTrial += 1          # aumenta o número total de tentativas
        self.save_trial_time = self.getTime(self.timeI)
        self.save_data()  # chamando a função para salvar os dados
        
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # condição para só apresentar a consequência caso seja um bloco de treino
            if self.getTime(timeI) <= time_consequence:
                consequence_img.update()
                consequence_sound.update()

            else:  # terminou a apresentação da consequência         
                screen.fill(self.screen_color)
                if self.getTime(timeI) >  self.time_ITI + time_consequence:
                    self.ITI()  # inicia o intervalo entre tentativas

            self.gui()
            pygame.display.update()

    def ITI(self): # função para verificar como o experimento vai continuar
        
        if self.trialCount > len(self.samples)-1:   # verificando se não tem mais dados para continuar as tentativas (se já finalizou o bloco 'csv')
                        
            if self.accuracy >= self.criterias[self.block_parameter]:       # verificando se atingiu o critério do bloco
                                    
                if self.block_parameter + 1 >= self.blocks_number:          # verificando se era o último bloco
                    self.end_experiment()

                else:    
                    self.block_parameter += 1  # aumenta o parâmetro do bloco (para chamar o bloco seguinte na próxima tentativa)
                    self.block_repetion = 0   # reseta a contagem das repetições
                    self.accuracy = 0       # zera o número de tentativas corretas
                    self.trialCount = 0     # zera a contagem de tentativas do bloco
                    self.totalTrials = 0    # zera o número total de tentativas do bloco
                    self.update_values()    # chama a função para atualizar as características das tentativas
                    self.instruction()      # se mudou de bloco, verificar se deve apresentar instrução
        
            else:  # se não atingiu o critério
                            
                if self.block_repetion >= self.repetitions[self.block_parameter]: # verificando se atingiu o critério de repetições
                    self.end_experiment()   # finaliza o experimento
                    
                else:                        
                    self.block_repetion += 1
                    self.trialCount = 0
                    self.accuracy = 0
                    self.update_values()
                    self.sample()
        else:
            self.sample()       
         
    def end_experiment(self):
        os.remove("session_settings.json")
        timeI = time.time()
        screen.fill(self.screen_color)
        end_text = Image(screen, self.end_text, self.instruction_size, (0, 0)) # definindo texto do fim do experimento
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            end_text.update()                   # se o bloco era o último teste, ele apresenta uma mensagem final e fecha o programa
            #self.format_data() # TODO
            if self.getTime(timeI) > 5:         # tempo para fechar o programa
                pygame.quit()
                sys.exit()
            pygame.display.update()
        
    def save_data(self): # todas as variáveis globais nomeadas 'save_' servem APENAS para salvar os dados
        """está função salva os dados do experimento: """
        
        text = f"{self.expTrial};{self.block_name};{self.totalTrials};{self.isCorrect};{self.accuracy};{self.points};\
{self.save_cont_stim};{self.save_sample};{self.save_sample_sound};{self.save_comps};{self.save_select};\
{round(self.save_time_sample,2)};{round(self.save_time_comp,2)};{round(self.save_trial_time,2)}\n"
        with open(f'data\{self.expData["Participant"]}.csv', "a+") as file:
            file.write(text)
        
Trial()
