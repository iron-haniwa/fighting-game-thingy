import pygame


class Background:

    def __init__(self, bgname, WIDTH, HEIGHT, WIN):
        self.bg_image = pygame.transform.scale(pygame.image.load(bgname).convert_alpha(), (WIDTH,HEIGHT))
        self.bg_rect = self.bg_image.get_rect()
        self.bg_rect.centerx = WIN.get_rect().centerx
        self.bg_rect.bottom = WIN.get_rect().bottom
    def draw(self, WIN):
        WIN.blit(self.bg_image,self.bg_rect)