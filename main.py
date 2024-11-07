import pygame
from src.screen import Screen
from src.ram import RAM
from src.keyboard import Keyboard
from src.cpu import CPU
import time 
import sys

ram = RAM()
ram.load_program(sys.argv[1])

pygame.init()

screen_factor_size = 18
screen_size = (64*screen_factor_size, 32*screen_factor_size)
screen = pygame.display.set_mode(screen_size)

clock = pygame.time.Clock()
running = True
chip_8_screen = Screen()
options = False
menu_height = 400
menu_width = 200
chip_8_keyboard = Keyboard()
prev_time = time.time()
cpu = CPU(chip_8_screen)
paused = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False 
        if event.type == pygame.KEYUP:
            chip_8_keyboard.key_up()
            if event.key == pygame.K_ESCAPE:
                paused = not paused
        if event.type == pygame.KEYDOWN:
            chip_8_keyboard.key_down(event.key)

    screen.fill("black")

    if not paused:
        # Game render
        chip_8_screen.draw_screen(screen, screen_factor_size)

        chip_8_keyboard.draw(screen)
        
        pygame.display.set_caption(f'FPS: {clock.get_fps()}')
        pygame.display.flip()
        clock.tick(60)
        cpu.update_timer()
        cpu.cycle()
    if paused:
        time.sleep(.1)
pygame.quit()