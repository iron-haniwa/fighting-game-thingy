import pygame, sys, random, colour, collections
import sneed2 as p
from backgroundClass import Background
import pygame.freetype
pygame.init()
pygame.font.init()

le_font = pygame.font.SysFont('Arial', 64)

HITSTOP = pygame.USEREVENT + 1
hitstop_event = pygame.event.Event(HITSTOP)

p1hitboxes = []
p2hitboxes = []


WIDTH, HEIGHT = 1920, 1080
SCREEN = pygame.display.set_mode((WIDTH/1.5,HEIGHT/1.5))
WIN = pygame.surface.Surface((WIDTH, HEIGHT))
FPS = 60

bg = Background('wafflehousenight.webp', WIDTH, HEIGHT, WIN)





player_1_controls = [pygame.K_s,
                    pygame.K_w,
                    pygame.K_a,
                    pygame.K_d,
                    pygame.K_u,
                    pygame.K_i,
                    pygame.K_o]
player_2_controls = [pygame.K_DOWN,
                    pygame.K_UP,
                    pygame.K_LEFT,
                    pygame.K_RIGHT,
                    pygame.K_1,
                    pygame.K_2,
                    pygame.K_3]








FLOOR = HEIGHT - 100

SPEED = 15
FRICTION = 1

PURPLE = (125,0,225)
WHITE = (255, 255, 255)

def draw(player1, player2, hitbox1, hitbox2):
    bg.draw(WIN)

    player1.draw(WIN)
    player2.draw(WIN)


    for hitbox in hitbox1:
        hitbox.draw(WIN)
    for hitbox in hitbox2:
        hitbox.draw(WIN)
    text_surface = le_font.render(f'{player1.state}', False, WHITE)
    text_surface2 = le_font.render(f'{player1.direction}', False, WHITE)
    WIN.blit(text_surface,(0,0))
    WIN.blit(text_surface2,(0,30))
    SCREEN.blit(pygame.transform.scale(WIN, SCREEN.get_rect().size), (0, 0))
    pygame.display.flip()

def collisionHandling(player, hitboxes):
    for hitboxes in hitboxes:
        if player.rect.colliderect(hitboxes) and hitboxes.hasHit == False:
            player.state = p.Hitstun(hitboxes.kb, player)
            hitboxes.hasHit = True
            pygame.event.post(hitstop_event)
            return hitboxes.hs_len
        



def main():
    hitstop = False
    clock = pygame.time.Clock()
    hitstopTimer = 0
    hitstop_len = 0

    player1 = p.Player(WIN.get_rect().centerx-600,WIDTH/2, player_1_controls)
    player2 = p.Player(WIN.get_rect().centerx+600,WIDTH/2, player_2_controls)
    player1.rect.right = WIN.get_rect().centerx-600
    while True:

        

        keys = pygame.key.get_pressed()
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                break
            if event.type == HITSTOP:
                hitstop = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    p2hitboxes.append(p.Hitbox(20))
                    print('sneed chungos')


        if hitstop == False:
            hitstop_len = collisionHandling(player1, p2hitboxes)   
            player1.loop(player2, keys)
            player2.loop(player1, keys)
            for hitbox in p1hitboxes:
                hitbox.timer()
                if hitbox.time >= hitbox.duration:
                    p1hitboxes.remove(hitbox)
            for hitbox in p2hitboxes:
                hitbox.timer()
                if hitbox.time >= hitbox.duration:
                    p2hitboxes.remove(hitbox)
        else:
            if hitstopTimer < hitstop_len:
                hitstopTimer += 1
            else:
                hitstopTimer = 0
                hitstop = False




        
        

        draw(player1,player2,p1hitboxes, p2hitboxes)
 
        clock.tick(FPS)
main()