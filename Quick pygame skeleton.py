import pygame, sys, random, colour, sneed2, testchar, Sacchin
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

YOFFSET = 0

GRAVITY = 2
JUMP = 40
FLOOR = HEIGHT - 50
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



# This file will be uncommented, as it does not do anything by itself,

# This program existed only as a shell of a program with the bare necessities to draw stuff on the screen so that I could quickly test code

# In it's final form, I gutted it to display certain frames of certain states of the player so that I could program in the hitboxes easier

# Please ignore





def main():
    character = Sacchin.satsukichan(WIN.get_rect().centerx-400,400, player_1_controls)
   
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
                    

                    character.place_hitbox('jB', 15, 0, 2, 130, 210, 180, 80, character, 'high', 2, 500)
                    character.place_hitbox('jB', 15, 0, 2, 240,  200, 90, 90, character, 'high', 2, 500)
                    character.place_hitbox('jB', 15, 0, 2, 90,  130, 170, 70, character, 'high', 2, 500)
                    
                    
                    

                    
                    
        character.animController(WIN)
        character.draw(WIN)
        for hurtbox in character.hurtboxes:
            hurtbox.draw(WIN)
        for attack in list(character.hitboxes.keys()):
                for hitbox in character.hitboxes[attack]:
                    hitbox.timer(character)
                    if hitbox.time >= hitbox.duration:
                        character.hitboxes[attack].remove(hitbox)
        for attack in character.hitboxes:
            for hitbox in character.hitboxes[attack]:
                hitbox.draw(WIN)
        
        character.state = Sacchin.attackjB(character)
        character.state.timer = 7
        #print(character.state.timer)
        character.hurtboxes = [sneed2.Hurtbox(character,140, 230,character.directionFlip(-10),140), 
                               sneed2.Hurtbox(character,110, 140,character.directionFlip(-100),100),
                               sneed2.Hurtbox(character,110, 50,character.directionFlip(100),50),]

        for hb in character.hurtboxes:
            hb.update_pos(character)
        
        SCREEN.blit(WIN, (0,0))
        pygame.display.flip()
        clock.tick(FPS)

main()