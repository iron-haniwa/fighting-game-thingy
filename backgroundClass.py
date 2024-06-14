import pygame


class Background:

    def __init__(self, bgname, WIDTH, HEIGHT, WIN):
        self.bg_image = pygame.transform.scale(pygame.image.load(bgname).convert_alpha(), (WIDTH*2.6,HEIGHT*2.6))
        self.bg_rect = self.bg_image.get_rect()
        self.bg_rect.centerx = WIN.get_rect().centerx
        self.bg_rect.bottom = WIN.get_rect().bottom
    def draw(self, WIN, player1, player2):
        #taking the center between players in order to keep the camera centered. The divide by 1.5 is because the camera movement is disorientingly fast if the value isn't cut down a bit
        self.center_between_players = (player2.rect.centerx + player1.rect.centerx) / 2.5
        self.offset = pygame.math.Vector2(self.center_between_players,0)
        self.bg_offset = self.bg_rect.topleft - self.offset
        #as stated in the cameracontrols file, the "camera" effect involves panning the background and moving all other objects with it 
        WIN.blit(self.bg_image,self.bg_offset)