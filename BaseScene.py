import pygame, sys, random, colour, collections
import sneed2 as p
from backgroundClass import Background
import pygame.freetype
import testchar
pygame.init()
pygame.font.init()

le_font = pygame.font.SysFont('Arial', 64)

HITSTOP = pygame.USEREVENT + 1
hitstop_event = pygame.event.Event(HITSTOP)

p1hitboxes = []
p2hitboxes = []


WIDTH, HEIGHT = 1280, 720
SCREEN = pygame.display.set_mode((WIDTH/1,HEIGHT/1))
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
                    pygame.K_b,
                    pygame.K_n,
                    pygame.K_m]








FLOOR = HEIGHT - 50
 
SPEED = 15
FRICTION = 1

PURPLE = (125,0,225)
WHITE = (255, 255, 255)
BLACK = (0,0,0)

def draw(player1, player2):
    bg.draw(WIN)


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
    
    player1.draw(WIN)
    player2.draw(WIN)

    text_surface = le_font.render(f'{type(player1.state).__name__}', False, BLACK)
    text_surface2 = le_font.render(f'{player1.direction}', False, BLACK)
    WIN.blit(text_surface,(0,0))
    WIN.blit(text_surface2,(0,30))
    SCREEN.blit(pygame.transform.scale(WIN, SCREEN.get_rect().size), (0, 0))
    pygame.display.flip()

def collisionHandling(player1, player2):
    hs = 0
    for hitboxes in player2.hitboxes:
        for hb in player1.hurtboxes:
            if hb.rect.colliderect(hitboxes) and hitboxes.hasHit == False:
                hs = player1.get_hit(hitboxes)
                hitboxes.hasHit = True
                pygame.event.post(hitstop_event)
                if hs == None:
                    return 0
                return hs
    for hitboxes in player1.hitboxes:
        for hb in player2.hurtboxes:
            if hb.rect.colliderect(hitboxes) and hitboxes.hasHit == False:
                hs = player2.get_hit(hitboxes)
                hitboxes.hasHit = True
                pygame.event.post(hitstop_event)
                if hs == None:
                    return 0
                return hs
    
      
   
                
                
        
        



def main():
    hitstop = False
    clock = pygame.time.Clock()
    hitstopTimer = 0
    hitstop_len = 0

    player1 = testchar.testChar(WIN.get_rect().centerx-600,HEIGHT/2, player_1_controls)
    player2 = p.Player(WIN.get_rect().centerx+600,HEIGHT/2, player_2_controls, False)
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
            
            
            player1.loop(player2, keys)
            player2.loop(player1, keys)
            hitstop_len = collisionHandling(player1, player2)
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
        #print(player1.IsJump)
        clock.tick(FPS)
main()