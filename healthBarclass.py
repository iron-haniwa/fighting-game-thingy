import pygame
class healthBar:

    def __init__(self, p1Max, p2Max):
        self.health_bar_length = 440
        self.health_ratio_1 = p1Max / self.health_bar_length
        self.health_ratio_2 = p2Max / self.health_bar_length
