import pygame, sys, random, colour, collections, healthBarclass
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

def draw(player1, player2, healthbars):
    bg.draw(WIN)


    #player1.draw(WIN)
    #player2.draw(WIN)

    for hurtbox in player1.hurtboxes:
        hurtbox.draw(WIN)
    for hurtbox in player2.hurtboxes:
        hurtbox.draw(WIN)
    for attack in player1.hitboxes:
        for hitbox in player1.hitboxes[attack]:
            hitbox.draw(WIN)
    for attack in player2.hitboxes:
        for hitbox in player1.hitboxes[attack]:
            hitbox.draw(WIN)
    
    player1.draw(WIN)
    player2.draw(WIN)
    healthbars.draw(WIN, player1.current_health, player2.current_health)

    text_surface = le_font.render(f'{type(player1.state).__name__}', False, BLACK)
    text_surface2 = le_font.render(f'{player1.direction}', False, BLACK)
    WIN.blit(text_surface,(0,0))
    WIN.blit(text_surface2,(0,30))
    SCREEN.blit(pygame.transform.scale(WIN, SCREEN.get_rect().size), (0, 0))
    pygame.display.flip()

def collisionHandling(player1, player2):
    hs = 0
    for attack in player2.hitboxes:
        for hitbox in player2.hitboxes[attack]:
            for hurtbox in player1.hurtboxes:
                if hurtbox.rect.colliderect(hitbox.rect) and hitbox.hasHit == False:
                    hitstop = player1.get_hit(hitbox)
                    for hitbox in player2.hitboxes[attack]:
                        hitbox.hasHit = True
                    pygame.event.post(hitstop_event)
                    if hitstop == None:
                        return 0
                    return hitstop

    for attack in player1.hitboxes:
    
        for hitbox in player1.hitboxes[attack]:

            for hurtbox in player2.hurtboxes:
                if hurtbox.rect.colliderect(hitbox.rect) and hitbox.hasHit == False:
                    hitstop = player2.get_hit(hitbox)
                    for hitbox in player1.hitboxes[attack]:
                        hitbox.hasHit = True
                    pygame.event.post(hitstop_event)
                    if hitstop == None:
                        return 0
                    return hitstop
        
      
   
                
                
        
        



def main():
    hitstop = False
    clock = pygame.time.Clock()
    hitstopTimer = 0
    hitstop_len = 0

    player1 = testchar.testChar(WIN.get_rect().centerx-400,HEIGHT/2, player_1_controls)
    player2 = p.Player(WIN.get_rect().centerx+400,HEIGHT/2, player_2_controls, False)
    player1.rect.right = WIN.get_rect().centerx-400

    healthbars = healthBarclass.healthBar(player1.maximum_health, player2.maximum_health)

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
            
            for attack in list(player1.hitboxes.keys()):
                for hitbox in player1.hitboxes[attack]:
                    hitbox.timer(player1)
                    if hitbox.time >= hitbox.duration:
                        player1.hitboxes[attack].remove(hitbox)
            print(player2.hitboxes)
            for attack in list(player2.hitboxes.keys()):
                for hitbox in player1.hitboxes[attack]:
                    hitbox.timer(player2)
                    if hitbox.time >= hitbox.duration:
                        player2.hitboxes[attack].remove(hitbox)
            for attack in list(player1.hitboxes.keys()):
                if any(player1.hitboxes[attack]) == False:
                    del player1.hitboxes[attack]
            for attack in list(player2.hitboxes.keys()):
                if any(player2.hitboxes[attack]) == False:
                    del player2.hitboxes[attack]
            
        else:
            print(hitstopTimer)
            print(hitstop_len)
            if hitstopTimer < hitstop_len:
                hitstopTimer += 1
            else:
                hitstopTimer = 0
                hitstop = False




        
        

        draw(player1,player2,healthbars)
        #print(player1.IsJump)
        clock.tick(FPS)
main()