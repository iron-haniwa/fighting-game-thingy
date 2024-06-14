import pygame, sys, random, colour, math
from inputreaderthing import inputReader, specialMove
pygame.init()
pygame.font.init()

le_font = pygame.font.SysFont('Arial', 64)

HITSTOP = pygame.USEREVENT + 1
hitstop_event = pygame.event.Event(HITSTOP)
hitboxes = []

WIDTH, HEIGHT = 1280, 720
SCREEN = pygame.display.set_mode((WIDTH/1.5,HEIGHT/1.5))
WIN = pygame.surface.Surface((WIDTH, HEIGHT))
FPS = 60

bg_image = pygame.transform.scale(pygame.image.load("wafflehousenight.webp").convert_alpha(), (WIDTH*2,HEIGHT*2))
bg_rect = bg_image.get_rect()
bg_rect.centerx = WIN.get_rect().centerx
bg_rect.bottom = WIN.get_rect().bottom

FLOOR = HEIGHT - 60

SPEED = 8
FRICTION = 2

player_1_controls = [pygame.K_s,
                    pygame.K_w,
                    pygame.K_a,
                    pygame.K_d,
                    pygame.K_u,
                    pygame.K_i,
                    pygame.K_o]

BLACK = (0,0,0)
YELLOW = (255, 255, 0)
GRAY = (255/2, 255/2, 255/2,100)
BLUE = (0, 0, 160)
DARKBLUE = (0,0,54.5)
WHITE = (255, 255, 255)
RED = (255, 0, 0, 100)
PURPLE = (125,0,225)
GREEN = (0,180,0,100)
GRAVITY = 2
JUMP = 40
red = colour.Color(rgb=(1,0,0))
blue = colour.Color(rgb=(1,0,1))
color = list(red.range_to(blue, 100))

attack_levels_dict = {

    1:{'hitstop':7,
       'blockstun':11,
       'hitstun':10
        },
    2:{'hitstop':9,
       'blockstun':14,
       'hitstun':16
        },
    3:{'hitstop':10,
       'blockstun':17,
       'hitstun':18
        }
}
    










class Player:

    

    def __init__(self, xpos, ypos, controls, stfu=True):
        self.height = 230
        self.width = 100
        self.controls = controls
        self.inputBuffer = inputReader(controls)
        self.absrect = pygame.Rect(xpos,ypos, self.width, self.height)
        self.rect = pygame.Rect(xpos,ypos, self.width, self.height)
        self.speed = SPEED
        self.dashFactor = 2.5
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
        self.hitboxes = {}
        self.hurtboxes = []
        self.defaultHB = Hurtbox(self,160, 00,0,80)
        self.crouchHB = Hurtbox(self,160, 390/2,0,-20)
        self.passthrough = False
        self.pushbox = Pushbox(self, self.width, self.height)
        self.animIndex = 0
        self.currentCombo = []
        self.cancelNow = False
        self.cancelwindow = 5
        self.prorationList = []
        
        

        self.floor = ypos
       
        self.isBlock = False
        self.blockLevel = 'LH'
        self.stfu = stfu

        self.current_health = 11700
        self.maximum_health = 11700
        self.health_bar_length = 440
        self.health_ratio = self.maximum_health / self.health_bar_length

    def directionFlip(self, xvalue):
        if self.direction == 'left':
            return -xvalue
        else:
            return xvalue



    def get_hit(self, hitbox):
        #print(hitbox.hitstop)

        self.currentCombo.append(hitbox.name)
        
        if self.isBlock:
            if hitbox.height == 'mid':
                if 'downleft' in self.inputBuffer.currentInput:
                    self.state = cBlockstun(hitbox.kb, self, hitbox.blockstun)
                    return
                else:
                    self.state = Blockstun(hitbox.kb, self, hitbox.blockstun)
                    return
                    
            elif hitbox.height == 'high':
                if self.blockLevel == 'H':
                    self.state = Blockstun(hitbox.kb, self, hitbox.blockstun)
                    return

            elif hitbox.height == 'low':
                if self.blockLevel == 'L':
                    if 'downleft' in self.inputBuffer.currentInput:
                        self.state = cBlockstun(hitbox.kb, self, hitbox.blockstun)
                        return
                    else:
                        self.state = Blockstun(hitbox.kb, self, hitbox.blockstun)
                        return
        
            
        self.get_damage(hitbox.damage)

        for i in hitbox.properties:
            if 'HK' in i:
                self.state = KDtumble(0, self)
            if 'L' in i:
                self.yvel -= hitbox.ykb
                self.state = airStun(hitbox.kb/3, self, True)


            elif self.rect.bottom < FLOOR or isinstance(self.state, KDtumble):
                self.state = airStun(hitbox.kb, self)
            
            else:
                if isinstance(self.state, Crouch):
                    self.state = cHitstun(hitbox.kb,self ,hitbox.hitstun)
                else:
                    self.state = Hitstun(hitbox.kb, hitbox.ykb,self, hitbox.hitstun)
            
            return hitbox.hitstop
    def get_damage(self, damage):
        self.current_health -= damage


    def get_health(self,amount):
        if self.current_health < self.maximum_health:
            self.current_health += amount
        if self.current_health >= self.maximum_health:
            self.current_health = self.maximum_health
            
    

    def change_state(self):
        
        new_state = self.state.enter_state(self, self.inputBuffer)
        if new_state: 
            self.animIndex = 0
            self.state = new_state
            
            
        else: self.state
        ##print(self.animIndex)

    def movement(self, dx, dy, player, WIN):
        
        self.rect.x += dx
        
        self.absrect.centerx = self.rect.centerx
        ##print(self.rect.bottom < FLOOR)
        if self.passthrough == False:
            if self.rect.colliderect(player.rect):
                player.rect.x += dx

                if self.rect.bottom < FLOOR:
                    
                    if self.rect.centerx - player.rect.centerx > 0:
                        self.rect.left = player.rect.right
                    else:
                        self.rect.right = player.rect.left
                if self.direction == 'right':
                    if self.rect.right >= player.rect.left:
                        self.rect.right = player.rect.left
                else:
                    if self.rect.left <= player.rect.right:
                        self.rect.left = player.rect.right
                        

        self.rect.y += dy
        
        
        if self.rect.bottom > FLOOR:
            ##print('whar')
            self.rect.bottom = FLOOR

        if self.rect.right > 1280:
            self.rect.right = 1280
        if self.rect.left < 0:
            self.rect.left = 0
        
        self.absrect.bottom = self.rect.bottom
        for attack in list(self.hitboxes.keys()):
                for hitbox in self.hitboxes[attack]:
                    hitbox.timer(self)
        for hb in self.hurtboxes:
            hb.update_pos(self)
        
        
    def gravity(self, factor=1):
        self.yvel += GRAVITY * factor
        if self.rect.bottom == FLOOR:
            if self.yvel > 0:
                self.yvel = 0
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
    def do_friction(self, factor=1):
        ##print(self.xvel)
        if self.xvel != 0:
            if self.xvel > 0:
                self.xvel -= FRICTION * factor
            elif self.xvel < 0:
                self.xvel += FRICTION * factor
        if abs(self.xvel) <= 1:
            self.xvel = 0
    #def do_pushback(self, player):
        
    def jump(self, jumpheight):
        self.yvel = -jumpheight

    def animController(self, WIN):
        pass

    def process_inputs(self):
        self.move = self.moveReader.commandReader(self, self.inputBuffer.inputBuffer)

        if self.move == 'Dash':
            ##print('guh')
            if isinstance(self.state, Jump):
                if self.amountDashed < self.dashLimit:
                    self.state = airDash(self)
            elif isinstance(self.state, Idle) or isinstance(self.state, forwardWalk):
                self.state = Dash()
        if self.move == 'bDash':
            ##print('guh')
            if isinstance(self.state, Idle) or isinstance(self.state, backWalk):
                self.state = backDash()
            elif isinstance(self.state, Jump):
                if self.amountDashed < self.dashLimit:
                    self.state = airbDash(self)
        if self.move == '5A':
            if isinstance(self.state, Idle):
                self.state = test_light_attack(self)
            if isinstance(self.state, airDash):
                if self.state.timer > 8:
                    self.state = test_light_attack(self)

    def place_hitbox(self, KEY, xkb, ykb, dur, xoff, yoff, w, h,player, height, level, damage, *properties):
        
        if self.direction == 'right':
            if KEY in self.hitboxes:
                self.hitboxes[KEY].append(Hitbox(-xkb,ykb,dur,xoff,yoff,w,h,self,height,level,damage, KEY,properties))
            else:
                self.hitboxes[KEY] = [Hitbox(-xkb,ykb,dur,xoff,yoff,w,h,self,height,level,damage, KEY,properties)]
                ##print('WHY WONT THIS WORK')
                ##print(self.hitboxes[KEY])
        else:
            if f'{KEY}' in self.hitboxes:
                self.hitboxes[KEY].append(Hitbox(xkb,ykb,dur,-xoff,yoff,w,h,self,height,level,damage, KEY,properties))
            else:
                self.hitboxes[KEY] = [Hitbox(xkb,ykb,dur,-xoff,yoff,w,h,self,height,level,damage, KEY,properties)]

    def loop(self, thingy, keys, WIN):
        
        for attack in self.hitboxes:
    
            
            if any([x.hasHit for x in self.hitboxes[attack]]):
                self.cancelwindow = 10
                self.cancelNow = True
                
                
        if self.cancelwindow <= 0:
            self.cancelNow = False
        
        self.inputBuffer.handleInputs(self.direction, keys)
        self.process_inputs(thingy)  
        ##print(self.state)
        ##print(self.jumpCount)
        if self.rect.centerx - thingy.rect.centerx > 0:
            self.direction = 'left'
        else:
            self.direction = 'right'
        
        

        

        
        
        
        self.change_state()
        self.state.update(self, self.inputBuffer)
        

        self.movement(self.xvel,self.yvel, thingy, WIN)
        self.cancelwindow -= 1
        self.animController(WIN)
        

        


        
        
            
    def draw(self, WIN):
        self.animDraw(WIN)
        guh = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        pygame.draw.rect(guh, GRAY, guh.get_rect())
        WIN.blit(guh, self.rect)
        pygame.draw.rect(WIN, GRAY, self.rect, 2)
        

    
        
            
    def drawSelf(self):
        
        if self.index < len(color):
            self.color = pygame.Color(str(color[self.index].hex_l))
            self.index += 1
        else:
            self.index = 0
            color.reverse()
        pygame.draw.rect(WIN, self.color, self.rect)


class Idle:
    def __init__(self, endDash=False, endCrouch=False):
        self.timer = 0
        self.endDash = endDash
        self.endCrouch = endCrouch

    def enter_state(self, character, inputs):
        if 'right' in inputs.currentInput:
            return forwardWalk()
        if 'left' in inputs.currentInput:
            return backWalk()
        if 'up' in inputs.currentInput and not character.IsJump:
            return preJump('Up')
        if 'upright' in inputs.currentInput and not character.IsJump:
            return preJump('Forward')
        if 'upleft' in inputs.currentInput and not character.IsJump:
            return preJump('Back')
        if any(x in ['down','downright','downleft'] for x in inputs.currentInput):
            return Crouch(True)
    
    def update(self, character, inputs):
        character.currentCombo = []
        character.rect.height = character.height
        character.hurtboxes = [character.defaultHB]
        character.amountDashed = 0
        character.jumpCount = 0
        ##print('guh')
        character.do_friction()
        character.gravity()
        self.timer += 1
        if self.timer >= 120:
            self.timer = 0

class Crouch:

    def __init__(self, startCrouch = False):
        self.startCrouch = startCrouch

    def enter_state(self,character,inputs):
        if not any(x in ['down','downright','downleft'] for x in inputs.currentInput):
            return Idle(endCrouch=True)
    def update(self,character,inputs):
        
        character.rect.height = character.height/2
        character.rect.bottom = FLOOR
        character.hurtboxes = [character.crouchHB]
        character.do_friction()
        if 'downleft' in inputs.currentInput:
            character.isBlock = True
            character.blockLevel = 'L'
        else:
            character.isBlock = False
            character.blockLevel = 'N'
class forwardWalk:
    def enter_state(self, character, inputs):
        if 'up' in inputs.currentInput and not character.IsJump:
            return preJump('Forward')

        if 'right' not in inputs.currentInput:
            #print(inputs.currentInput)
            if character.direction == 'right':
                character.xvel -= character.speed
            else:
                character.xvel += character.speed
            return Idle()
        
    def update(self, character, inputs):
        character.hurtboxes = [character.defaultHB]
        character.move_forward(character.speed)
class backWalk:
    def enter_state(self, character, inputs):

        if 'up' in inputs.currentInput and not character.IsJump:
            
            return preJump('Back')

        if 'left' not in inputs.currentInput:
            if character.direction == 'right':
                character.xvel += character.speed
            else:
                character.xvel -= character.speed
            character.isBlock = False
            return Idle()

    def update(self, character, inputs):
        character.isBlock = True
        character.blockLevel = 'H'
        character.hurtboxes = [character.defaultHB]
        character.move_back(character.speed)

class preJump:
    def __init__(self, dir):
        self.dir = dir
        self.prejump = 3
        self.timer = 0
    def enter_state(self, character, inputs):
        if self.timer >= self.prejump:
            character.jumpCount += 1
            character.jump(JUMP)
            if self.dir == 'Up':
                character.xvel = 0
                return Jump(character)
            else:
                return Jump(character, self.dir)
    def update(self, character, inputs):
        character.hurtboxes = [character.defaultHB]
        self.timer += 1
        



class Jump:

    def __init__(self, character,dir='',postDash=False):
        self.release_received = False
        self.postDash = postDash
        if abs(character.xvel) <= 8:
            if dir == 'Forward':
                character.move_forward(character.speed)
            if dir == 'Back':
                character.move_back(character.speed)
        
    def enter_state(self, character, inputs):

        if character.rect.bottom == FLOOR:
            character.amountDashed = 0
            character.isJump = False
            return Idle()
        if (self.release_received == True) and character.jumpCount < character.jumpLimit:

            if 'up' in inputs.currentInput:
                character.jump(JUMP)
                character.jumpCount += 1
                return Jump(character)

            elif 'upright' in inputs.currentInput:
                character.jump(JUMP)
                character.jumpCount += 1
                return Jump(character, 'Forward')
            elif 'upleft' in inputs.currentInput:
                character.jump(JUMP)
                character.jumpCount += 1
                return Jump(character, 'Back')

            
        
    def update(self, character, inputs):
        character.hurtboxes = [character.defaultHB]
        character.isJump = True
        character.gravity()
        ##print(self.release_received)
        if any(x in ['-up','-upright','-upleft'] for x in inputs.inputBuffer[-1]):
            #print('waaw')
            self.release_received = True

class Dash:
    def enter_state(self, character, inputs):
        if 'up' in inputs.currentInput:
                return preJump('What')
        elif inputs.currentInput != ['right']:
            
            
                return Idle(endDash=True)
    def update(self, character, inputs):
        character.hurtboxes = [character.defaultHB]
        character.move_forward(character.speed*character.dashFactor)

class backDash:
    def __init__(self):
        self.timer = 0
    def enter_state(self, character, inputs):
        if self.timer > 24:
            return Idle()
    def update(self, character, inputs):
        if self.timer == 1:
            character.jump(5)
        if self.timer < 3:
            character.hurtboxes = []
            character.move_back(character.speed*3)
            
        elif self.timer > 6:
            character.do_friction()
            character.hurtboxes = [character.defaultHB]
            
        elif self.timer < 15:
            character.isJump = True
        elif self.timer > 15:
            character.isJump = False
        character.gravity(0.5)
        self.timer += 1
class test_light_attack:
    def __init__(self, character):
        self.timer = 0
        character.hurtboxes = [character.defaultHB]
        #character.yvel = 50
    def enter_state(self, character, inputs):
        if character.move == '5A':
            return test_light_attack(character)
        if self.timer > 17:
            return Idle()
    def update(self, character, inputs):
        
        self.timer += 1
        if self.timer == 4:
            if character.direction == 'right':
                character.hurtboxes = [character.defaultHB, 
                                       Hurtbox(character,150,120,175,70)]
                character.hitboxes.append([Hitbox(-15, 0, 5, 175, 70, character, 'mid', 1,50)])
            else:
                character.hurtboxes = [character.defaultHB, 
                                       Hurtbox(character,150,120,-175,70)]
                character.hitboxes.append([Hitbox(15, 0, 5, -175, 70, character, 'mid', 1, 50)])


class airDash:
    def __init__(self,character):
        self.timer = 0
        character.yvel = 0
        self.direction = character.direction
        character.amountDashed += 1
        character.hurtboxes = [character.defaultHB]

    def enter_state(self, character, inputs):

        if self.timer == 20:
            return Jump(character, postDash=True)
        
        if character.rect.bottom == FLOOR:
            return Idle()
        
    def update(self, character, inputs): 
        character.direction = self.direction
        character.move_forward(character.speed*2.3)
        self.timer += 1
class airbDash:
    def __init__(self,character):
        self.timer = 0
        character.jump(10)
        
        self.direction = character.direction
        character.amountDashed += 1
        character.hurtboxes = [character.defaultHB]

    def enter_state(self, character, inputs):

        if self.timer == 5:
            return Jump(character)
        
        if character.rect.bottom == FLOOR:
            return Idle()
        
    def update(self, character, inputs): 
        character.direction = self.direction
        character.move_back(character.speed*1.2)
        self.timer += 1


class gotGrabbed:
    def enter_state(self, character, inputs):
        pass
    def update(self, character, inputs):
        pass 
    

class Hitstun:
    def __init__(self,xknockback, yknockback,character,length):
        character.hurtboxes = [character.defaultHB]
        self.timer = 0
        self.length = length
        character.xvel -= xknockback
        character.yvel -= yknockback
        character.animIndex = 0
    def enter_state(self, character, inputs):
        if self.timer == self.length:
            if 'down' in inputs.currentInput:
                return Crouch()
            else:
                return Idle()
    def update(self, character, inputs):
        character.do_friction()
        #print(character.yvel)
        self.timer += 1
class Blockstun:
    def __init__(self,xknockback,character,length):
        self.length = length
        self.timer = 0
        character.xvel -= xknockback
        character.animIndex = 0
    def enter_state(self, character, inputs):
        if self.timer == self.length:
            if 'downleft' or 'down' in inputs.currentInput:
                    return Crouch()
            else:
                return Idle()
    def update(self, character, inputs):
        if 'left' in inputs.currentInput:
            character.isBlock = True
            character.blockLevel = 'H'
        elif 'downleft' in inputs.currentInput:
            character.isBlock = True
            character.blockLevel = 'L'
        else:
            character.isBlock = False
        character.do_friction()
        character.gravity()
        character.yvel -= GRAVITY /2
        self.timer += 1



class cHitstun:
    def __init__(self,xknockback,character,length):
        character.hurtboxes = [character.crouchHB]
        self.timer = 0
        self.length = length
        character.xvel -= xknockback
        character.animIndex = 0
    def enter_state(self, character, inputs):
        if self.timer == self.length:
            if 'down' or 'downleft' in inputs.currentInput:
                    return Crouch()
            else:
                return Idle()
        
    def update(self, character, inputs):
        character.rect.height = character.height/2
        character.do_friction()
        character.gravity()
        character.yvel -= GRAVITY /2
        self.timer += 1
class cBlockstun:
    def __init__(self,xknockback,character,length):
        self.length = length
        self.timer = 0
        character.xvel -= xknockback * 1.1
        character.animIndex = 0
    def enter_state(self, character, inputs):
        if self.timer == self.length:
            if 'downleft' or 'down' in inputs.currentInput:
                    return Crouch()
            else:
                return Idle()

    def update(self, character, inputs):
        character.rect.height = character.height/2
        character.hurtboxes = [Hurtbox(character,250, 390/1.5,0,-70)]
        if 'left' in inputs.currentInput:
            character.isBlock = True
            character.blockLevel = 'H'
        elif 'downleft' in inputs.currentInput:
            character.isBlock = True
            character.blockLevel = 'L'
        else:
            character.isBlock = False
        character.do_friction()
        character.gravity()
        character.yvel -= GRAVITY /2
        self.timer += 1



class KDtumble:
    def __init__(self,xknockback,character):
        self.timer = 0
        character.animIndex = 0
        character.xvel -= xknockback
        character.jump(JUMP/2)
    def enter_state(self, character, *args):
        if character.rect.bottom == FLOOR and self.timer > 36:
            return hard_KD(character)
    def update(self, character, inputs):
        character.hurtboxes = [character.crouchHB]
        character.gravity()
        character.do_friction(0.5)
        self.timer += 1 


class airStun:
    def __init__(self,xknockback,character, yknockback=False):
        self.timer = 0
        character.xvel -= xknockback
        
        
        
        
        if not yknockback:
            character.jump(JUMP/3)
    def enter_state(self, character, *args):
        if character.rect.bottom == FLOOR:
            if self.timer > 3:
                return soft_KD(character)
    def update(self, character, inputs):
        character.gravity()
        self.timer += 1 

class soft_KD:
    def __init__(self,character):
        self.timer = 0
        character.jump(15)
        character.hurtboxes = []
        character.animIndex = 0
    def enter_state(self, character, *args):
        if self.timer == 16:
            return Idle()
    def update(self, character, inputs):
        character.do_friction()
        character.gravity()


        self.timer += 1
class hard_KD:
    def __init__(self,character):
        self.timer = 0
        character.hurtboxes = []
    def enter_state(self, character, *args):
        if self.timer == 55:
            return Idle()
    def update(self, character, inputs):
        character.do_friction()
        character.gravity()


        self.timer += 1 


class Hitbox:
    def __init__(self, xknockback, yknockback, duration, xoffset, yoffset, w, h, player, height, level, damage, name,*properties):
        self.player_rect = player.absrect
        self.width = w
        self.height = h
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.xoffset = xoffset
        self.yoffset = -yoffset
        self.rect.center = player.absrect.center
        self.rect.centerx += self.xoffset
        self.rect.centery += self.yoffset
        self.level_attributes = attack_levels_dict[level]
        self.damage = None
        self.kb = xknockback
        self.ykb = yknockback
        self.hasHit = False
        self.duration = duration
        self.time = 0
        self.hitstop = self.level_attributes['hitstop']
        self.hitstun = self.level_attributes['hitstun']
        self.blockstun = self.level_attributes['blockstun']
        self.height = height
        self.properties = properties
        self.damage = damage
        self.name = name
    def timer(self, player):
        self.time += 1
        
        self.rect.center = player.absrect.center
        self.rect.centerx += self.xoffset
        self.rect.centery += self.yoffset
    def draw(self, WIN):
        guh = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        pygame.draw.rect(guh, RED, guh.get_rect())
        WIN.blit(guh, self.rect)
        pygame.draw.rect(WIN, RED, self.rect, 2)


class Hurtbox:
    def __init__(self, player, width, height, x_off, y_off):
        self.player_rect = player.absrect
        self.rect = pygame.Rect(-1000, -1000, width, height)
        self.rect.center = player.absrect.center
        self.x_off = x_off
        self.y_off = -y_off
    def update_pos(self, player):
        self.rect.center = player.absrect.center
        self.rect.centerx += self.x_off
        self.rect.centery += self.y_off
        ##print(self.rect.x)
        
    def draw(self, WIN):
        guh = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        pygame.draw.rect(guh, GREEN, guh.get_rect())
        WIN.blit(guh, self.rect)
        pygame.draw.rect(WIN, GREEN, self.rect, 2)

class Pushbox:
    def __init__(self, player, width, height, x_off=0, y_off=0):
        self.player_rect = player.rect
        self.rect = pygame.Rect(0, 0, width, height)
        self.x_off = x_off
        self.y_off = y_off
    def update_pos(self, player):
        self.rect.center = player.rect.center
        self.rect.centerx += self.x_off
        self.rect.centery += self.y_off
        ##print(self.rect.x)
    def draw(self, WIN):

        guh = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        pygame.draw.rect(guh, GRAY, guh.get_rect())
        WIN.blit(guh, self.rect)
        pygame.draw.rect(WIN, GRAY, self.rect, 5)
    






        
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
                    #hitboxes.append(Hitbox(20, 10, 1300, (HEIGHT)-200))
                    ##print('sneed chungos')
                    pass

        if hitstop == False:
            hitstop_len = collisionHandling(player, hitboxes)   
            player.loop(thingy, keys, WIN)
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
            ##print(hitstop)
        #sd#print(hitstop_len)
        draw(player, hitboxes, thingy)
 
        clock.tick(FPS)

if __name__ == '__main__':
    main()