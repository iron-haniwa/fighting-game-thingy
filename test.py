import pygame

pygame.joystick.init()
while True:
    joysticks = pygame.joystick.Joystick(0)
    print(joysticks.get_button(0))
