import pygame, sys, random, colour, collections, healthBarclass, cameracontrols, Sacchin
import sneed2 as p
from backgroundClass import Background
import pygame.freetype
import testchar
pygame.init()
pygame.font.init()






le_font = pygame.font.SysFont('Futura', 140)


HITSTOP = pygame.USEREVENT + 1
hitstop_event = pygame.event.Event(HITSTOP)

p1hitboxes = []
p2hitboxes = []


WIDTH, HEIGHT = 1280, 720
SCREEN = pygame.display.set_mode((WIDTH/1,HEIGHT/1))
WIN = pygame.surface.Surface((WIDTH, HEIGHT))
FPS = 60




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


character_dict = {'Shiki':testchar.testChar,
                  'Sacchin':Sacchin.satsukichan}


def draw(player1, player2, healthbars, bg):
    WIN.fill(BLACK)
    bg.draw(WIN, player1, player2)

    #player1.draw(WIN)
    #player2.draw(WIN)

    for hurtbox in player1.hurtboxes:
        hurtbox.draw(WIN)
    for hurtbox in player2.hurtboxes:
        hurtbox.draw(WIN)
    player1.draw(WIN)
    for attack in player1.hitboxes:
        for hitbox in player1.hitboxes[attack]:
            hitbox.draw(WIN)
    for attack in player2.hitboxes:
        for hitbox in player2.hitboxes[attack]:
            hitbox.draw(WIN)
    
    
    player2.draw(WIN)
    healthbars.draw(WIN, player1.current_health, player2.current_health)


    if not player1.alive or not player2.alive:
        
        text_surface3 = le_font.render('K.O.', False, WHITE)
       

        WIN.blit(text_surface3, ((WIN.get_rect().centerx) - (text_surface3.get_rect().w/2), (WIN.get_rect().centery) - (text_surface3.get_rect().h/2)))

    
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
        
        



def main(player1char, player2char):
    hitstop = False
    clock = pygame.time.Clock()
    hitstopTimer = 0
    hitstop_len = 0

    player1 = character_dict[player1char](WIN.get_rect().centerx-400,FLOOR, player_1_controls)
    player2 = character_dict[player2char](WIN.get_rect().centerx+400,FLOOR, player_2_controls, False)
    bg = Background('wafflehousenight.webp', WIDTH, HEIGHT, WIN)
    camera = cameracontrols.Camera(bg.bg_rect.w, bg.bg_rect.h)
    player1.rect.right = WIN.get_rect().centerx-400


    healthbars = healthBarclass.healthBar(player1.maximum_health, player2.maximum_health)
    # pygame.mixer.music.load("C:/Users/bcarey65_s/Desktop/CompSci Grade 12/fighting-game-thingy-main/Beat.flac")  
    # pygame.mixer.music.play(loops=-1)
    endTimer = 0
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
            
            
            player1.loop(player2, keys, WIN)
            player2.loop(player1, keys, WIN)
            hitstop_len = collisionHandling(player1, player2)
            #print(player2.hitboxes)
            for attack in list(player1.hitboxes.keys()):
                for hitbox in player1.hitboxes[attack]:
                    if hitbox.time >= hitbox.duration:
                        for hitbox in player1.hitboxes[attack]:
                            player1.hitboxes[attack].remove(hitbox)
            #print(player2.hitboxes)
            for attack in list(player2.hitboxes.keys()):
                for hitbox in player2.hitboxes[attack]:
                    if hitbox.time >= hitbox.duration:
                        for hitbox in player2.hitboxes[attack]:
                            player2.hitboxes[attack].remove(hitbox)
            for attack in list(player1.hitboxes.keys()):
                if any(player1.hitboxes[attack]) == False:
                    del player1.hitboxes[attack]
            for attack in list(player2.hitboxes.keys()):
                if any(player2.hitboxes[attack]) == False:
                    del player2.hitboxes[attack]
            
        else:
            #print(hitstopTimer)
            #print(hitstop_len)
            if hitstopTimer < hitstop_len:
                hitstopTimer += 1
            else:
                hitstopTimer = 0
                hitstop = False

        if not player1.alive or not player2.alive:
            endTimer += 1

        if endTimer >=600:
            pygame.quit()
            sys.exit()
            break
        
        
        draw(player1,player2,healthbars,bg)
        camera.cameraupdate(player1, player2, WIN)
        
        clock.tick(FPS/1)

if __name__ == '__main__':    
    main('Shiki', 'Sacchin')