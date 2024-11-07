import pygame
import numpy as np
from src.singleton import SingletonMeta

class Screen(metaclass=SingletonMeta):
    def __init__(self):
        self.width = 64
        self.height = 32
        self.screen = np.zeros((self.width, self.height), dtype=int).tolist()

    def draw_screen(self, surface, size_factor):
        for x in range(len(self.screen)):
            for y in range(len(self.screen[x])):
                pygame.draw.rect(surface, 'white' if self.screen[x][y] == 1 else 'black', pygame.Rect(x*size_factor, y*size_factor,1*size_factor, 1*size_factor))
    
    def draw_pixel(self, x, y):
        if x > 64:
            x = x - 64
        elif x < 0:
            x = 64
        if y > 32:
            y = y - 32
        elif y < 0:
            y = 32
        self.screen[x][y] ^=1
        return not self.screen[x][y]
        

    
    def clear_display(self):
        self.screen[:, :] = 0 