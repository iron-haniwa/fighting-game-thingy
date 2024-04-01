import pygame, sys, random, colour
pygame.init()
pygame.font.init()

le_font = pygame.font.SysFont('Arial', 64)

HITSTOP = pygame.USEREVENT + 1
hitstop_event = pygame.event.Event(HITSTOP)
hitboxes = []

WIDTH, HEIGHT = 1920, 1080
SCREEN = pygame.display.set_mode((WIDTH/1.5, HEIGHT/1.5))
WIN = pygame.surface.Surface((WIDTH, HEIGHT))
FPS = 60

SPEED = 30

BLACK = (0,0,0)
YELLOW = (255, 255, 0)
GRAY = (255/2, 255/2, 255/2)
BLUE = (0, 0, 160)
DARKBLUE = (0,0,54.5)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
PURPLE = (125,0,225)
GRAVITY = 2
JUMP = 40
red = colour.Color(rgb=(1,0,0))
blue = colour.Color(rgb=(1,0,1))
color = list(red.range_to(blue, 100))


class Circle:

    

    def __init__(self, xpos, ypos):
        self.height = 300
        self.width = 200

        self.rect = pygame.Rect(xpos,ypos, self.width, self.height)
        self.xvel = 0
        self.yvel = 0
        self.IsJump = False
        self.color = 0, 0, 0
        self.index = 0
        self.state = Idle()
        self.direction = 'right'

    def change_state(self):
        new_state = self.state.enter_state(self)
        if new_state: self.state = new_state
        else: self.state

    def movement(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy
        self.rect.clamp_ip(WIN.get_rect())
    def gravity(self):
        self.yvel += GRAVITY
    def move_left(self, vel):
        self.xvel = -vel
    def move_right(self, vel):
        self.xvel = vel
    def jump(self, jumpheight):
        self.yvel = -jumpheight
    def loop(self, thingy):
        if self.rect.y > HEIGHT - 300:
            self.IsJump = True
        else: self.IsJump = False
        if self.rect.centerx - thingy.rect.centerx > 0:
            self.direction = 'left'
        else:
            self.direction = 'right'
        
        self.movement(self.xvel,self.yvel)
        self.change_state()
        self.state.update(self)
        #print(self.direction)
    def draw(self):
        pygame.draw.rect(WIN, PURPLE, self.rect)


    
        
            
    def drawSelf(self):
        
        if self.index < len(color):
            self.color = pygame.Color(str(color[self.index].hex_l))
            self.index += 1
        else:
            self.index = 0
            color.reverse()
        pygame.draw.rect(WIN, self.color, self.rect)


class Idle:
    def enter_state(self, character):
        if keys[pygame.K_RIGHT]:
            return forwardWalk()
        if keys[pygame.K_LEFT]:
            return backWalk()
        if keys[pygame.K_SPACE] and not character.IsJump:
            character.jump(JUMP)
            return Jump()
    def update(self, character):
        character.xvel = 0
        character.gravity()
class forwardWalk:
    def enter_state(self, character):

        if not keys[pygame.K_RIGHT]:
            return Idle()
        elif keys[pygame.K_SPACE] and not character.IsJump:
            character.jump(JUMP)
            return Jump()
    def update(self, character):
        character.move_right(SPEED/2)
class backWalk:
    def enter_state(self, character):

        if not keys[pygame.K_LEFT]:
            return Idle()
        elif keys[pygame.K_SPACE] and not character.IsJump:
            character.jump(JUMP)
            return Jump()
    def update(self, character):
        character.move_left(SPEED/2)
class Jump:
    def enter_state(self, character):

        if character.rect.y == HEIGHT - character.height:
            return Idle()
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if keys[pygame.K_LEFT]:
                        character.move_left(SPEED/2)
                    elif keys[pygame.K_RIGHT]:
                        character.move_right(SPEED/2)
                    character.jump(JUMP/1.2)
                    return doubleJump()
    def update(self, character): 
        #print(character.yvel)
        character.gravity()
class doubleJump:
    def enter_state(self, character):
        
        if character.rect.y == HEIGHT - 300:
            return Idle()
        
    def update(self, character): 
        #print(character.yvel)
        character.gravity()

class Hitstun:
    def __init__(self,knockback,character):
        self.timer = 0
        character.xvel = -knockback
        character.yvel = 0
    def enter_state(self, character):
        if self.timer == 20:
            if character.rect.y == HEIGHT - 300:
                return Idle()
            else:
                return Jump()
    def update(self, character):
        if character.rect.y == HEIGHT - 300:
            if abs(character.xvel) != 0:
                if character.xvel > 0:
                    character.xvel -= 1
                elif character.xvel < 0:
                    character.xvel += 1
        else:
            if abs(character.xvel) != 0:
                if character.xvel > 0:
                    character.xvel -= 0.5
                elif character.xvel < 0:
                    character.xvel += 0.5
        character.gravity()
        character.yvel -= GRAVITY /2
        self.timer += 1 

class Hitbox:
    def __init__(self, knockback):
        self.rect = pygame.Rect(1300, (HEIGHT)-200, 100, 100)
        self.damage = None
        self.kb = knockback
        self.hasHit = False
        self.duration = 10
        self.time = 0
        self.hs_len = 5
    def timer(self):
        self.time += 1
    def draw(self):
        pygame.draw.rect(WIN,RED, self.rect)



        
class Thingy:
    def __init__(self):
        self.rect = pygame.Rect((WIDTH/2)+400, 700, 50, 100)
    def guh(self):
        pygame.draw.rect(WIN, WHITE, self.rect)

def collisionHandling(player, hitboxes):
    for hitboxes in hitboxes:
        if player.rect.colliderect(hitboxes) and hitboxes.hasHit == False:
            player.state = Hitstun(hitboxes.kb, player)
            hitboxes.hasHit = True
            pygame.event.post(hitstop_event)
            return hitboxes.hs_len
            

def draw(player, hitboxes, thingy):
    WIN.fill(BLACK)
    player.draw()
    for hitbox in hitboxes:
        hitbox.draw()
    text_surface = le_font.render(f'{player.state}', False, WHITE)
    text_surface2 = le_font.render(f'{player.direction}', False, WHITE)
    thingy.guh()
    WIN.blit(text_surface,(0,0))
    WIN.blit(text_surface2,(0,30))
    SCREEN.blit(pygame.transform.scale(WIN, SCREEN.get_rect().size), (0, 0))
    pygame.display.flip()

def main():
    hitstop = False
    clock = pygame.time.Clock()
    player = Circle((WIDTH/2)-600, WIDTH/2)
    thingy = Thingy()
    hitstopTimer = 0
    hitstop_len = 0
    while True:
        global keys
        keys = pygame.key.get_pressed()
        global events
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
                    hitboxes.append(Hitbox(20))
                    #print('sneed chungos')

        if hitstop == False:
            hitstop_len = collisionHandling(player, hitboxes)   
            player.loop(thingy)
            for hitbox in hitboxes:
                hitbox.timer()
                if hitbox.time >= hitbox.duration:
                    hitboxes.remove(hitbox)
        else:
            if hitstopTimer < hitstop_len:
                hitstopTimer += 1
            else:
                hitstopTimer = 0
                hitstop = False
            #print(hitstop)
        print(hitstop_len)
        draw(player, hitboxes, thingy)
 
        clock.tick(FPS)


main()