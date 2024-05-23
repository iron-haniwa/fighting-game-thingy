import pygame, sys, random, colour
pygame.init()
pygame.font.init()

le_font = pygame.font.SysFont('Arial', 64)

WIDTH, HEIGHT = 1280, 720
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
WIN = pygame.surface.Surface((WIDTH, HEIGHT))
FPS = 60
BLACK = (0,0,0)
YELLOW = (255, 255, 0)
GRAY = (255/2, 255/2, 255/2)
BLUE = (0, 0, 160)
DARKBLUE = (0,0,54.5)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
PURPLE = (125,0,225)
YELLOW = (255,255,0)

GRAVITY = 2
JUMP = 40



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

       
    def draw(self):
        
        pygame.draw.rect(WIN, RED, self.maximum_hp_1)
        pygame.draw.rect(WIN, RED, self.maximum_hp_2)
        length_1 = self.p1HP*self.health_ratio_1
        pygame.draw.rect(WIN, YELLOW,(self.maximum_hp_1.right - length_1,50, length_1, 50))
        length_2 = self.p2HP*self.health_ratio_2
        pygame.draw.rect(WIN, YELLOW,(self.maximum_hp_2.left,50, length_2, 50))



def main():
    bar = healthBar(1170, 1170)
    clock = pygame.time.Clock()
    while True:
        WIN.fill(BLACK)
        global keys
        keys = pygame.key.get_pressed()
        global events
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    bar.p1HP -= 100
                if event.key == pygame.K_w:
                    bar.p1HP += 100
        bar.draw()
        SCREEN.blit(WIN, (0,0))
        pygame.display.flip()
        clock.tick(FPS)

main()

