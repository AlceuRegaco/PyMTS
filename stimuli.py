import pygame, time
import numpy as np

"""
This file contains the classes to add stimuli in the experiment according to the type of stimulus (create new classes for each new type of stimulus)
"""

pygame.init()

class Image:
    def __init__(self,screen,
                 stimulus_path:str,
                 stimulus_size:list,
                 stimulus_pos:list,
                ):
        
        self.stimulus_path = f'stimuli/{stimulus_path}'
        if stimulus_path == 'n':
            return None
        self.screen = screen
        self.screen_size = width, height = pygame.display.get_window_size()
        self.stimulus_pos = stimulus_pos
        self.stimulus_size = stimulus_size
        self.pos_center = np.array(self.screen_size) / 2 - np.array(self.stimulus_size) / 2
        self.pos_x, self.pos_y = self.pos_center + np.array([stimulus_pos[0], -stimulus_pos[1]])
        
        self.name = self.stimulus_path[8:]
        self.img = pygame.image.load(self.stimulus_path).convert()
        self.img = pygame.transform.scale(self.img, stimulus_size)
        self.start_time = time.time()
        self.rect = self.img.get_rect(center=(self.pos_x, self.pos_y))
    
    def update(self):
        if self.stimulus_path=="stimuli/n":
            return None
        self.screen_size = width, height = pygame.display.get_window_size()
        self.pos_x, self.pos_y = np.array(self.screen_size)/2 + np.array([self.stimulus_pos[0], -self.stimulus_pos[1]])
        self.rect = self.img.get_rect(center=(self.pos_x, self.pos_y))

       
        self.screen.blit(self.img, self.rect)
    
    def mouse_hover(self):
        mouse_pos = pygame.mouse.get_pos()
        if mouse_pos[0] in range(self.rect.left, self.rect.right)\
            and mouse_pos[1] in range(self.rect.top, self.rect.bottom):
            return True
            
    def mouse_click(self,e):
        return e.type == pygame.MOUSEBUTTONDOWN

class Sound:
    def __init__(self, stimulus_path:str, volume=0.5):
        self.stimulus_path = f'stimuli/{stimulus_path}'
        if stimulus_path == 'n':
            return None
        self.sound = pygame.mixer.Sound(self.stimulus_path)
        self.sound.set_volume(volume)
        #print(f'duração som:{self.sound.get_length()}')
        
    def stop(self):
        if self.stimulus_path == 'stimuli/n':
            return None
        self.sound.stop()

    def duration(self):
        return self.sound.get_length()
    
    def isPlaying(self):
        return self.sound.get_num_channels()
    
    def update(self, lops=0):
        if self.stimulus_path == 'stimuli/n':
            return None
        self.sound.play(loops=lops)

class Text:
    def __init__(self, screen, color, text, text_size=100, text_pos=list):
        main_font = pygame.font.SysFont("Calibri", text_size)
        self.screen_size = screen.get_size()
        self.text = main_font.render(text, True, color)
        self.text_pos = text_pos
        self.pos_center = np.array(self.screen_size) / 2 - np.array(self.text_pos) / 2
        self.pos_x, self.pos_y = self.pos_center + np.array([text_pos[0], -text_pos[1]])
        self.screen = screen

    def update(self):
        
        self.screen_size = width, height = pygame.display.get_window_size()
        self.pos_x, self.pos_y = np.array(self.screen_size)/2 + np.array([self.text_pos[0], -self.text_pos[1]])
        self.rect = self.text.get_rect(center=(self.pos_x, self.pos_y))
        self.screen.blit(self.text, self.rect)

