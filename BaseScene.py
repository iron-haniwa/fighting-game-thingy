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

def draw(player1, player2):
    bg.draw(WIN)

    for hurtbox in player1.hurtboxes:
        hurtbox.draw(WIN)
    for hurtbox in player2.hurtboxes:
        hurtbox.draw(WIN)
    #player1.draw(WIN)
    #player2.draw(WIN)

    for hurtbox in player1.hurtboxes:
        hurtbox.draw(WIN)
    for hurtbox in player2.hurtboxes:
        hurtbox.draw(WIN)
    for hitbox in player1.hitboxes:
        hitbox.draw(WIN)
    for hitbox in player2.hitboxes:
        hitbox.draw(WIN)
    text_surface = le_font.render(f'{player1.state}', False, WHITE)
    text_surface2 = le_font.render(f'{player1.direction}', False, WHITE)
    WIN.blit(text_surface,(0,0))
    WIN.blit(text_surface2,(0,30))
    SCREEN.blit(pygame.transform.scale(WIN, SCREEN.get_rect().size), (0, 0))
    pygame.display.flip()

def collisionHandling(player1, player2):
    for hitboxes in player2.hitboxes:
        for hb in player1.hurtboxes:
            if hb.rect.colliderect(hitboxes) and hitboxes.hasHit == False:
                player1.state = p.Hitstun(hitboxes.kb, player1)
                hitboxes.hasHit = True
                pygame.event.post(hitstop_event)
                print(hitboxes.hs_len)
                return hitboxes.hs_len
    for hitboxes in player1.hitboxes:
        for hb in player2.hurtboxes:
            if hb.rect.colliderect(hitboxes) and hitboxes.hasHit == False:
                player2.state = p.Hitstun(hitboxes.kb, player2)
                hitboxes.hasHit = True
                pygame.event.post(hitstop_event)
                print(hitboxes.hs_len)
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
                    player2.hitboxes.append(p.Hitbox(20, 10, 1300, (HEIGHT)-200))
                    print('sneed chungos')


        if hitstop == False:
            hitstop_len = collisionHandling(player1, player2)
       
            player1.loop(player2, keys)
            player2.loop(player1, keys)
            for hitbox in player1.hitboxes:
                hitbox.timer(player1)
                if hitbox.time >= hitbox.duration:
                    player1.hitboxes.remove(hitbox)
            for hitbox in player2.hitboxes:
                hitbox.timer(player2)
                if hitbox.time >= hitbox.duration:
                    player2.hitboxes.remove(hitbox)
        else:
            print(hitstopTimer)
            print(hitstop_len)
            if hitstopTimer < hitstop_len:
                hitstopTimer += 1
            else:
                hitstopTimer = 0
                hitstop = False




        
        

        draw(player1,player2)
 
        clock.tick(FPS)
main()