import pygame, sys, random, colour, sneed2, testchar
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





def main():
    character = testchar.testChar(WIN.get_rect().centerx-400,400, player_1_controls)
   
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
                    
                    character.place_hitbox('lariatA', 15, 30, 10, 150, 150, 110, 100, character, 'mid', 2, 1200)
                    character.place_hitbox('lariatA', 15, 30, 10, 120, 90, 110, 190, character, 'mid', 2, 1200)
                    character.place_hitbox('lariatA', 15, 30, 10, 240, 90, 130, 100, character, 'mid', 2, 1200)
                    character.place_hitbox('lariatA', 15, 30, 10, 150, 10, 130, 70, character, 'mid', 2, 1200)

                    
                    
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
        
        character.state = testchar.lariatKojima(character)
        character.state.timer = 12
        #print(character.state.timer)
        character.hurtboxes = [sneed2.Hurtbox(character,100, 140,character.directionFlip(30),160),
                               sneed2.Hurtbox(character,240, 190,character.directionFlip(20),-20),
                               sneed2.Hurtbox(character,170, 100,character.directionFlip(40),120),
                              
                        
                             ]

        for hb in character.hurtboxes:
            hb.update_pos(character)
        
        SCREEN.blit(WIN, (0,0))
        pygame.display.flip()
        clock.tick(FPS)

main()

