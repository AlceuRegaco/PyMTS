#utf8
from random import shuffle
import pygame
import sys
import os
import time
from stimuli import Sound, Image, Text  # importing classes from stimuli.py
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

        self.trialCount = 0     # flag to control for the number of trials that were programmed for the block     
        self.totalTrials = 0    # total number of trials in the block
        self.isCorrect = 0      # flag to control for correct and incorrect responses
        self.accuracy = 0       # number of correct trials in the block
        self.expTrial = 0       # total number of trials in the experiment
        self.block_repetion = 0
        
        with open("configData.json") as setting:
            config = json.load(setting)
            setting.close()
        
        self.block_parameter = config["start_block"]    # defining first block
        # configuring variables
        self.update_values()        # updating data for the experiment

        # starting the trial
        self.load_experiment_data() # creating the file to save the data
        self.instruction()          # starting first instruction

    def load_experiment_data(self): # function to create the file to save the data
        with open("session_settings.json") as e:
            self.expData = json.load(e)
            e.close()
        with open(f'data\{self.expData["Participant"]}.csv', "w+") as file:
            file.write(f"sep=;\n")
            file.write(f"Participant;{self.expData['Participant']}\n")
            file.write(f"Experimenter;{self.expData['Experimenter']}\n")
            file.write(f"Date;{datetime.now()}\n\n")
            file.write(f"Total_Trial;Block;Block_Trial;Accuracy;Total_Correct;Sample;Sample_Sound;\
Comps;Selcted_Comp;Time_Click_Sample;Time_Click_Comp;Time_Trial\n")
               
    def update_values(self):    # function to update the values for the experiment

        config = self.config_experiment()
        self.criterias = config[1]['criteria'] # list of block criteria (number of correct trials to pass the block)
        self.repetitions = config[1]['repetitions'] # list of the maximmum number of repetitions for each block
        self.screen_color = config[1]['screen_color'] # screen colour
        self.time_ITI = config[1]['ITI']  # inter-trial interval   
        self.blocks_number = len(config[1]['blocks']) # number of blocks
        self.samples = [i.split(':') for i in config[0]['sample'].values] # list of the sample stimuli (in the same order of presentation)
        self.sample_sound = config[0]['sample_sound'].values # list of the auditive sample stimuli (in the same order of presentation)
        self.comps = [i.split(':') for i in config[0]['comp'].values]   # list of the comparison stimuli (in the same order of presentation)  
        self.correct_comps = [i.split(':') for i in config[0]['correct_comp'].values]   # list of the correct comparison stimuli (in the same order of presentation)
        self.volume = config[1]['volume']   # sound volume

        self.img_right = config[0]['img_right'].values  # list of the images for correct response consequence
        self.img_wrong = config[0]['img_wrong'].values  # list of the images for the incorrect response consequence
        self.sound_right = config[0]['sound_right'].values  # list of the sounds for the correct response consequence
        self.sound_wrong = config[0]['sound_wrong'].values  # list of the sounds for the incorrect response consequence
        self.time_right = config[0]['time_right'].values    # list of the time for the correct response consequence
        self.time_wrong = config[0]['time_wrong'].values    # list of the time for the incorrect response consequence
       
        self.pos_sample = config[1]['pos_sample']               # list with sample stimuli position
        self.pos_comps = config[1]['pos_comps']                 # list with comparison stimuli position
        self.stimulus_size = config[1]['stimulus_size']         # list with stimulus size (all stimuli have the same size/proportion)
        self.instruction_size = config[1]['instructions_size']  # list with instruction size (all instructions have the same size/proportion)
        self.consequence_size = config[1]["consequence_size"]   # list with consequence size (all consequences have the same size/proportion)
        self.instructions = config[1]['instructions']           # list with instructions (in the same order of block presentation)
        self.protocol = config[1]['comp display']               # list defining the protocol for the comparison display (in the same order of block presentation)
        self.end_text = config[1]['end_text']                   # text to be displayed at the end of the experiment

    def config_experiment(self):    # function to open  the configuration file and get the data for the experiment
        with open("configData.json") as setting:
            config = json.load(setting) # defining the configuration file 'configData.json'
            setting.close()

        self.blocks = config["blocks"]           
        self.block_name = self.blocks[self.block_parameter] # getting the name of the current block

        current_block = pd.read_csv(f"config/{self.block_name}.csv", sep=r'[;,]+', engine='python')   # getting the data from the current block
        current_block = current_block.sample(current_block.shape[0])            # randomizing the order of the trials in the block
        
        return [current_block, config]     # returning the data from the current block and the configuration data

    def instruction(self):     # function to present the instructions for the block
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

    def getTime(self, timeI): # function to get the time
        return time.time() - timeI

    def sample(self):   # function to present the sample stimuli
        self.timeI = time.time()
        screen.fill(self.screen_color)
        timeI = time.time() # defining the time for the sample stimulus
        sample = self.samples[self.trialCount]  # sample stimuli
        sample_sound = self.sample_sound[self.trialCount]   # auditive sample stimulus
        self.save_sample = sample
        self.save_sample_sound = sample_sound     
        self.sample_stimulus = [Image(screen,sample[i],
                       self.stimulus_size,
                       self.pos_sample[i]) for i in range(len(sample))]  # defining the visual sample stimuli
        self.sample_sound_stimulus = Sound(sample_sound, volume=self.volume)   # defining the auditive sample stimulus

        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                for stimulus in self.sample_stimulus[0:1]:  # only the first stimulus is clickable
                    if stimulus.mouse_click(event) and stimulus.mouse_hover():
                        if sample_sound == 'n':                        
                            self.save_time_sample = self.getTime(timeI)
                            self.comparison()
                        else:
                            self.save_time_sample = self.getTime(timeI)
                            self.sample_sound_stimulus.update(lops=0)   # plays the sample sound stimulus
                            self.comparison()

            for stimulus in self.sample_stimulus:  
                stimulus.update()      
            pygame.display.update()

    def comparison(self):   # function to present the comparison stimuli
        sample_sound = self.sample_sound[self.trialCount]   # sample sound stimulus
        comps = self.comps[self.trialCount]  # defining the comparison stimuli
        shuffle(comps)  # randomizing the order of the comparison stimuli
        stimuli = [Image(screen, comps[i], self.stimulus_size, self.pos_comps[i]) for i in range(len(comps))]   # defining the visual comparison stimuli
        self.save_comps = comps
        timeI = time.time() # starting the time for the comparison stimuli
        
        while 1:
            for event in pygame.event.get():    # checking for events
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if self.protocol[self.block_parameter] == "SMTS":   
                    if sample_sound == 'n':
                        ...
                    else:
                        for stimulus in self.sample_stimulus[0:1]:  # only the first stimulus is clickable
                            if stimulus.mouse_click(event) and stimulus.mouse_hover():
                                if self.sample_sound_stimulus.isPlaying():
                                    ...
                                else:
                                    self.sample_sound_stimulus.stop()
                                    self.sample_sound_stimulus.update(lops=0)   # plays the sample sound stimulus

                for stimulus in stimuli:
                    if stimulus.mouse_click(event) and stimulus.mouse_hover():
                        if sample_sound == 'n': # if there is no sample sound stimulus
                            if stimulus.name in self.correct_comps[self.trialCount]:    # defining consequences for correct responses
                                self.save_time_comp = self.getTime(timeI)
                                self.isCorrect = 1
                                self.accuracy += 1
                                self.save_select = stimulus.name
                                self.consequences(self.time_right[self.trialCount],
                                                self.img_right[self.trialCount],
                                                self.sound_right[self.trialCount])   
                            else:   # defining consequences for incorrect responses
                                self.save_time_comp = self.getTime(timeI)
                                self.isCorrect = 0
                                self.save_select = stimulus.name
                                self.consequences(self.time_wrong[self.trialCount],
                                                self.img_wrong[self.trialCount],
                                                self.sound_wrong[self.trialCount])      

                        else:   # if there is a sample sound stimulus
                            if self.sample_sound_stimulus.isPlaying():  # if the sample sound stimulus is playing nothing happens
                                ...
                            else:
                                self.sample_sound_stimulus.stop()
                                if stimulus.name in self.correct_comps[self.trialCount]:    # defining consequences for correct responses
                                    self.save_time_comp = self.getTime(timeI)
                                    self.isCorrect = 1
                                    self.accuracy += 1
                                    self.save_select = stimulus.name
                                    self.consequences(self.time_right[self.trialCount],
                                                    self.img_right[self.trialCount],
                                                    self.sound_right[self.trialCount])   
                                else:   # defining consequences for incorrect responses
                                    self.save_time_comp = self.getTime(timeI)
                                    self.isCorrect = 0
                                    self.save_select = stimulus.name
                                    self.consequences(self.time_wrong[self.trialCount],
                                                    self.img_wrong[self.trialCount],
                                                    self.sound_wrong[self.trialCount])      

            if self.protocol[self.block_parameter] == "SMTS":
                for stimulus in stimuli:
                    stimulus.update()   # presenting the comparisson stimuli
            else:
                if self.getTime(timeI) <= self.protocol[self.block_parameter]:
                    screen.fill(self.screen_color)   # filling the screen with the background color             
                else:
                    for stimulus in stimuli:
                        stimulus.update()   # presenting only the comparisson stimuli
                     
            pygame.display.update()

    def consequences(self, time_consequence, img_cons, sound_cons): # function to present the consequences for the responses
        
        screen.fill(self.screen_color)
        consequence_img = Image(screen, img_cons, self.consequence_size, (0, 0)) # defining the consequence image
        consequence_sound = Sound(sound_cons, volume=self.volume)   # defining the consequence sound stimulus
        timeI = time.time()
        self.trialCount += 1        # updating the trial count for the block
        self.totalTrials += 1       # incrementing the number of trials in the block
        self.expTrial += 1          # incrementing the total number of trials in the experiment
        self.save_trial_time = self.getTime(self.timeI)
        self.save_data()  # saving the data for the trial
        
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            if self.getTime(timeI) <= time_consequence: # defining the time limit for consequence presentation
                consequence_img.update()
                consequence_sound.update()

            else:  # finishing the consequence presentation      
                screen.fill(self.screen_color)
                if self.getTime(timeI) >  self.time_ITI + time_consequence:
                    self.ITI()  # starting the inter-trial interval

            pygame.display.update()

    def ITI(self): # function to verify if the experiment is finished or if it should continue
        
        if self.trialCount > len(self.samples)-1:   # verifying if the block is finished (if the csv file is finished)
                        
            if self.accuracy >= self.criterias[self.block_parameter]:       # verifying if the block was passed (if the number of correct trials is greater than the criteria)
                                    
                if self.block_parameter + 1 >= self.blocks_number:          # veryfying if the block is the last one
                    self.end_experiment()

                else:    
                    self.block_parameter += 1  # increasing the block parameter to the next block
                    self.block_repetion = 0   # zeroing the block repetition counter
                    self.accuracy = 0       # zeroing the number of correct responses in the block
                    self.trialCount = 0     # zeroing the trial count for the block
                    self.totalTrials = 0    # zeroing the total number of trials in the block
                    self.update_values()    # updating the values for the next block
                    self.instruction()      # checking if the next block has instructions to be presented
        
            else:  # if the block was not passed, it is necessary to repeat the block
                            
                if self.block_repetion >= self.repetitions[self.block_parameter]: # verifying if the number of repetitions is greater than the maximum number of repetitions
                    self.end_experiment()   # ending the experiment
                    
                else:   # if the block was not passed, it is necessary to repeat the block                        
                    self.block_repetion += 1    # increasing the block repetition counter
                    self.trialCount = 0         # zeroing the trial count for the block
                    self.accuracy = 0           # zeroing the number of correct responses in the block
                    self.update_values()        # updating the values for the next block
                    self.sample()               # starting the next trial in the block
        else:
            self.sample()   # starting the next trial in the block       
         
    def end_experiment(self):   # function to end the experiment
        os.remove("session_settings.json")
        timeI = time.time()
        screen.fill(self.screen_color)
        end_text = Image(screen, self.end_text, self.instruction_size, (0, 0)) # defining the end text
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            end_text.update()                   # presenting the end text
            #self.format_data() # TODO          # formatting the data for the experiment (future implementation)
            if self.getTime(timeI) > 5:         # time limit for the end text presentation
                pygame.quit()
                sys.exit()
            pygame.display.update()
        
    def save_data(self): # function to save the data for the trial (all variables named 'save_' are used ONLY to save the data)
        text = f"{self.expTrial};{self.block_name};{self.totalTrials};{self.isCorrect};{self.accuracy};\
{self.save_sample};{self.save_sample_sound};{self.save_comps};{self.save_select};\
{round(self.save_time_sample,2)};{round(self.save_time_comp,2)};{round(self.save_trial_time,2)}\n"
        with open(f'data\{self.expData["Participant"]}.csv', "a+") as file:
            file.write(text)
        
Trial()
