import pygame, sys, random, colour
from inputreaderthing import inputReader, specialMove
pygame.init()
pygame.font.init()

le_font = pygame.font.SysFont('Arial', 64)

HITSTOP = pygame.USEREVENT + 1
hitstop_event = pygame.event.Event(HITSTOP)
hitboxes = []

WIDTH, HEIGHT = 1920, 1080
SCREEN = pygame.display.set_mode((WIDTH/1.5,HEIGHT/1.5))
WIN = pygame.surface.Surface((WIDTH, HEIGHT))
FPS = 60

bg_image = pygame.transform.scale(pygame.image.load("wafflehousenight.webp").convert_alpha(), (WIDTH*2,HEIGHT*2))
bg_rect = bg_image.get_rect()
bg_rect.centerx = WIN.get_rect().centerx
bg_rect.bottom = WIN.get_rect().bottom

FLOOR = HEIGHT - 100

SPEED = 15
FRICTION = 1

player_1_controls = [pygame.K_s,
                    pygame.K_w,
                    pygame.K_a,
                    pygame.K_d,
                    pygame.K_u,
                    pygame.K_i,
                    pygame.K_o]

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


class Player:

    

    def __init__(self, xpos, ypos, controls):
        self.height = 400
        self.width = 250
        self.controls = controls
        self.inputBuffer = inputReader(controls)
        self.rect = pygame.Rect(xpos,ypos, self.width, self.height)
        self.xvel = 0
        self.yvel = 0
        self.IsJump = False
        self.color = 0, 0, 0
        self.index = 0
        self.state = Idle()
        self.direction = 'right'
        self.moveReader = specialMove
        self.dashLimit = 2
        self.amountDashed = 0
        self.jumpLimit = 3
        self.jumpCount = 0
         
    

    def change_state(self):
        new_state = self.state.enter_state(self, self.inputBuffer)
        if new_state: self.state = new_state
        else: self.state

    def movement(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy
        if self.rect.bottom > FLOOR:
            #print('whar')
            self.rect.bottom = FLOOR
    def gravity(self):
        self.yvel += GRAVITY
    def move_back(self, vel):
        if self.direction == 'right':
            self.xvel = -vel
        else:
            self.xvel = vel
    def move_forward(self, vel):
        if self.direction == 'right':
            self.xvel = vel
        else:
            self.xvel = -vel
    def jump(self, jumpheight):
        self.yvel = -jumpheight

    def process_inputs(self):
        move = self.moveReader.commandReader(self, self.inputBuffer.inputBuffer)

        if move == 'Dash' and isinstance(self.state, Jump):
            #print('guh')
            if self.amountDashed < self.dashLimit:
                self.xvel += 10
                self.yvel -= GRAVITY*4

    def loop(self, thingy, keys):
        

        self.inputBuffer.handleInputs(self.direction, keys)
        self.process_inputs()  
        #print(self.state)
        #print(self.jumpCount)
        if self.rect.bottom > FLOOR:
            self.IsJump = True
        else: self.IsJump = False
        if self.rect.centerx - thingy.rect.centerx > 0:
            self.direction = 'left'
        else:
            self.direction = 'right'
        
        self.movement(self.xvel,self.yvel)
        self.change_state()
        self.state.update(self, self.inputBuffer)
        #print(self.direction)
    def draw(self, window):
        pygame.draw.rect(window, PURPLE, self.rect)


    
        
            
    def drawSelf(self):
        
        if self.index < len(color):
            self.color = pygame.Color(str(color[self.index].hex_l))
            self.index += 1
        else:
            self.index = 0
            color.reverse()
        pygame.draw.rect(WIN, self.color, self.rect)


class Idle:
    def enter_state(self, character, inputs):
        if 'right' in inputs.currentInput:
            return forwardWalk()
        if 'left' in inputs.currentInput:
            return backWalk()
        if 'up' in inputs.currentInput and not character.IsJump:
            inputs.inputBuffer[-1].append('jumped')
            return preJump()
    def update(self, character, inputs):
        character.amountDashed = 0
        character.jumpCount = 0
        #print('guh')
        if abs(character.xvel) > 0:
            if character.xvel > 0:
                character.xvel -= FRICTION
            elif character.xvel < 0:
                character.xvel += FRICTION
        character.gravity()
class forwardWalk:
    def enter_state(self, character, inputs):
        if 'up' in inputs.currentInput and not character.IsJump:
            return preJump()

        if inputs.currentInput != ['right']:
            if character.direction == 'right':
                character.xvel -= SPEED
            else:
                character.xvel += SPEED
            return Idle()
        
    def update(self, character, inputs):
        character.move_forward(SPEED)
class backWalk:
    def enter_state(self, character, inputs):

        if 'up' in inputs.currentInput and not character.IsJump:
            
            return preJump()

        if inputs.currentInput != ['left']:
            if character.direction == 'right':
                character.xvel += SPEED
            else:
                character.xvel -= SPEED
            return Idle()

    def update(self, character, inputs):
        character.move_back(SPEED)

class preJump:
    def __init__(self):
        self.prejump = 4
        self.timer = 0
    def enter_state(self, character, inputs):
        if self.timer >= self.prejump:
            character.jumpCount += 1
            character.jump(JUMP)
            return Jump()
    def update(self, character, inputs):
        self.timer += 1



class Jump:

    def __init__(self):
        self.release_received = False


    def enter_state(self, character, inputs):

        if character.rect.bottom == FLOOR:
            return Idle()
        if 'up' in inputs.currentInput and not character.IsJump and (self.release_received == True) and character.jumpCount < character.jumpLimit:

            if 'right' in inputs.currentInput:
                character.move_forward(SPEED)
            elif 'left' in inputs.currentInput:
                character.move_back(SPEED)

            character.jump(JUMP)
            character.jumpCount += 1
            return Jump()
        
    def update(self, character, inputs): 
        #print(character.yvel)
        character.gravity()
        #print(self.release_received)
        if '-up' in inputs.inputBuffer[-1][0]:
            #print('waaw')
            self.release_received = True


class doubleJump:
    def enter_state(self, character, inputs):
        
        if character.rect.bottom == FLOOR:
            return Idle()
        
    def update(self, character, inputs): 
        #print(character.yvel)
        character.gravity()

class Hitstun:
    def __init__(self,knockback,character):
        self.timer = 0
        character.xvel = -knockback
        character.yvel = 0
    def enter_state(self, character, *args):
        if self.timer == 20:
            if character.rect.y == HEIGHT - 300:
                return Idle()
            else:
                return Jump()
    def update(self, character, inputs):
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
    def __init__(self, knockback,):
        self.rect = pygame.Rect(1300, (HEIGHT)-200, 100, 100)
        self.damage = None
        self.kb = knockback
        self.hasHit = False
        self.duration = 10
        self.time = 0
        self.hs_len = 5
    def timer(self):
        self.time += 1
    def draw(self, WIN):
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
    WIN.blit(bg_image,bg_rect)
    #WIN.fill(WHITE)
    player.draw(WIN)
    for hitbox in hitboxes:
        hitbox.draw(WIN)
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
    player = Player((WIDTH/2)-600, WIDTH/2, player_1_controls)
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
            player.loop(thingy, keys)
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
        #sdprint(hitstop_len)
        draw(player, hitboxes, thingy)
 
        clock.tick(FPS)

if __name__ == '__main__':
    main()