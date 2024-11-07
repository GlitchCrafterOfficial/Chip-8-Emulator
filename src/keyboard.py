from src.singleton import SingletonMeta
import pygame

class Keyboard(metaclass=SingletonMeta):
    def __init__(self):
        self.keyboard = {
            pygame.K_KP_1: 0x1,
            pygame.K_KP_2: 0x2,
            pygame.K_KP_3: 0x3,
            pygame.K_KP_4: 0xC,
            pygame.K_KP_5: 0x4, 
            pygame.K_KP_6: 0x5, 
            pygame.K_KP_7: 0x6, 
            pygame.K_KP_8: 0xD,
            pygame.K_KP_9: 0x7, 
            pygame.K_KP_MULTIPLY: 0x8, 
            pygame.K_KP_DIVIDE: 0x9, 
            pygame.K_KP_PLUS: 0xE,
            pygame.K_KP_MINUS: 0xA, 
            pygame.K_KP_0: 0x0, 
            pygame.K_a: 0xB, 
            pygame.K_s: 0xF
        }
        self.pressed = -0xF
        self.last_press = -0xF
        self.__debug_font = pygame.font.Font(None, 16)

    def draw(self, screen):
        text_surface = self.__debug_font.render(f'Pressed: {self.pressed}',True,'white', None)
        screen.blit(text_surface, (0,0))

    def key_down(self, key):
        if self.keyboard.get(key):
            self.pressed = self.keyboard[key]
    
    def key_up(self):
        self.pressed = -0xF
    
    def is_pressed(self, key):
        return self.pressed == key