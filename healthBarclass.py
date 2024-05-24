import pygame


RED = (255,0,0)
YELLOW = (255,255,0)

class healthBar:

    def __init__(self, p1Max, p2Max):
        self.health_bar_length = 570
        self.health_ratio_1 = self.health_bar_length / p1Max
        self.health_ratio_2 = self.health_bar_length / p2Max
        self.maximum_hp_1 = pygame.Rect(20,50, self.health_bar_length, 50)
        self.maximum_hp_2 = pygame.Rect(690,50, self.health_bar_length, 50)
        self.maximum_hp_2.right = 1280 - 20
        self.p1HP = p1Max
        self.p2HP = p2Max

       
    def draw(self, WIN, player1hp, player2hp):
        
        pygame.draw.rect(WIN, RED, self.maximum_hp_1)
        pygame.draw.rect(WIN, RED, self.maximum_hp_2)
        length_1 = player1hp*self.health_ratio_1
        pygame.draw.rect(WIN, YELLOW,(self.maximum_hp_1.right - length_1,50, length_1, 50))
        length_2 = player2hp*self.health_ratio_2
        pygame.draw.rect(WIN, YELLOW,(self.maximum_hp_2.left,50, length_2, 50))