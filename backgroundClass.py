import pygame


class Background:

    def __init__(self, bgname, WIDTH, HEIGHT, WIN):
        self.bg_image = pygame.transform.scale(pygame.image.load(bgname), (WIDTH * 2,HEIGHT * 1.5)).convert()
        self.bg_image.set_colorkey((255,0,255))
        self.bg_rect = self.bg_image.get_rect()
        self.bg_rect.centerx = WIN.get_rect().centerx + 300
        self.bg_rect.bottom = WIN.get_rect().bottom
    def draw(self, WIN, player1, player2):
        #taking the center between players in order to keep the camera centered. The divide is because the camera moves disorientingly fast if the value isn't reduced
        self.center_between_players = (player2.rect.centerx + player1.rect.centerx) / 18
        self.offset = pygame.math.Vector2(self.center_between_players,0)
        self.bg_offset = self.bg_rect.topleft - self.offset
        #as stated in the cameracontrols file, the "camera" effect involves panning the background and moving all other objects with it 
        WIN.blit(self.bg_image,self.bg_offset)