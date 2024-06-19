import pygame, sys, random, colour, math
from inputreaderthing import inputReader, specialMove
pygame.init()
pygame.font.init()



# Oh god, I didn't comment this as I wrote it, and I really don't want to comment it now....


# Random constants, some used throughout, and some not. This file used to be a standalone file (This was the first project file!) before being relegated to exclusively being
# a module for the player class
WIDTH, HEIGHT = 1280, 720
FLOOR = HEIGHT - 60
SPEED = 8
FRICTION = 2



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


# Attack levels dictionary, this dict stores a bunch of different possible values of different tiers of attack, making it easy to assign the more specific and annoying properities in broader strokes
# 1 is the weakest with the least impact, and 3 is the strongest with highest stun.

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
    






# Player class, this is not a class capable of being run on it's own, but it contains the base code common to both character,

# It is the engine of the vehicle


class Player:

    
        # Initializes the ridiculous amount of attributes the player has, many are self explantory controlling stuff such as initial position and such, but I will comment the more bizarre kinds
    def __init__(self, xpos, ypos, controls):
        self.height = 230
        self.width = 100
        self.controls = controls
        self.inputBuffer = inputReader(controls)
        #Sets up the height and width of the player, alongside setting up the local instance of the inputreader with you control scheme.

        self.absrect = pygame.Rect(xpos,ypos, self.width, self.height)
        self.rect = pygame.Rect(xpos,ypos, self.width, self.height)
        #While the rect is easy to understand (it is the actual "object" of the player), the abs rect is a version that
        #is never affected by the rect's changing shape, and since it is constant it is used to position the hurtboxes and hitboxes


        self.speed = SPEED
        self.dashFactor = 2.5 #Sets the amount SPEED is multiplied when you dash, so the players can run at different speeds
        self.xvel = 0
        self.yvel = 0 # creates the velocity attributes
        self.IsJump = False # Attribute that determines if you are jumping, I honestly don't know if I still use this, but I'm scared to get rid of it
        self.color = 0, 0, 0
        self.index = 0
        self.state = Idle() # Default state for the state machine (more later )
        self.direction = 'right' #default direct
        self.moveReader = specialMove # Initializes the move reader
        self.dashLimit = 2 # Sets a limit on air dashes
        self.amountDashed = 0 # Tracks amount of airdashes performed
        self.jumpLimit = 3 # Limits the amount of jumps
        self.jumpCount = 0 # Guess what this does
        self.hitboxes = {} 
        self.hurtboxes = []
        self.defaultHB = Hurtbox(self,160, 00,0,80) # Default HB size so i dont have to keep typing this in for every state
        self.crouchHB = Hurtbox(self,160, 390/2,0,-20) # Default crouching HB size so i dont have to keep typing this in for every state
        self.passthrough = False # This doesn't do anything anymore, but the program won't work without it and I'm too lazy to fix it
        self.pushbox = Pushbox(self, self.width, self.height) # Default PB size (Collision box) so i dont have to keep typing this in for every state
        self.animIndex = 0 #Animation index, this is used for the character and will be explained in test character
        self.currentCombo = [] #List of current attacks performed in a combo, used for the cancelling system
        self.cancelNow = False # Variable that says if current attack can be cancelled
        self.cancelwindow = 5 # The period you have to cancel moves
        
        self.alive = True
        

        self.floor = ypos
       
        self.isBlock = False
        self.blockLevel = 'LH' #Blocking related values
        

        self.current_health = 11700  #Sets default health values
        self.maximum_health = 11700
    
    # This is a function that mirrors x values depending on the direction the player is facing
    # It is used for placing hurtboxes and hitboxes, which must be the same on both sides
    def directionFlip(self, xvalue):
        if self.direction == 'left':
            return -xvalue
        else:
            return xvalue



    def get_hit(self, hitbox):
        #This entire function runs when you are hit by an attack, and decides how you react
        
        #First, the attack that hit you is added to your combo counter
        self.currentCombo.append(hitbox.name)
    

        #The game checks to see if you are blocking, and if you are blocking at the correct height for the attack
        #If you are, it puts you in a block state appropriate to how you are standing, if not, you are hit
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
        
        #Damage is processed
        self.get_damage(hitbox.damage)

        #The hitbox is checked for special properties (Hard Knockdown and Launch), and if none are found you are hit regularly
        for i in hitbox.properties:
            if 'HK' in i:
                self.state = KDtumble(0, self)
            elif 'L' in i:
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
        
    # You get damaged lol
    def get_damage(self, damage):
        self.current_health -= damage



            
    
    # This is the state machine's heart.
    # Every frame, the current state (Store as individual classes which dictate the current player behaviour) is read,
    # and if they meet the criteria to switch states, the state's own transition code it ran while the animation index is reset, and then the state changes
    # Otherwise, the state continues as usual
    def change_state(self):
        
        new_state = self.state.enter_state(self, self.inputBuffer)
        if new_state: 
            self.animIndex = 0
            self.state = new_state
            
            
        else: self.state
        

    def movement(self, dx, dy, player, WIN):
        # Movement function, the players X and Y are changed by the velocity every frame,
        # and the players are repelled if they enter eachother or the boundaries of the screen
        self.rect.x += dx
        
        self.absrect.centerx = self.rect.centerx
        
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
        # This seems like a non-sequitur, but this controls the displacement of the hitboxes
        for attack in list(self.hitboxes.keys()):
                for hitbox in self.hitboxes[attack]:
                    hitbox.timer(self)
        #moves the hurtboxes to match the players movement
        for hb in self.hurtboxes:
            hb.update_pos(self)
        
    # Gravity, you are able to pass it a factor to decrease or increase it
    def gravity(self, factor=1):
        self.yvel += GRAVITY * factor
        if self.rect.bottom == FLOOR:
            if self.yvel > 0:
                self.yvel = 0

    # Move back function, moves the character back in relation to their faced direction
    def move_back(self, vel):
        if self.direction == 'right':
            self.xvel = -vel
        else:
            self.xvel = vel

    # Same, but forward
    def move_forward(self, vel):
        if self.direction == 'right':
            self.xvel = vel
        else:
            self.xvel = -vel

    # Constant damper on velocity, slowing the character down when called
    def do_friction(self, factor=1):
        ##print(self.xvel)
        if self.xvel != 0:
            if self.xvel > 0:
                self.xvel -= FRICTION * factor
            elif self.xvel < 0:
                self.xvel += FRICTION * factor
        if abs(self.xvel) <= 1:
            self.xvel = 0
    
    #  makes the player jump    
    def jump(self, jumpheight):
        self.yvel = -jumpheight
    # Function defined to be further used by the subclasses
    def animController(self, WIN):
        pass
    # Defualt input processing, the subclasses expand this to include more inputs, but these are the basic ones
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
    # Function that automatically passes in the tangle of attributes a hitbox can have, and properly places it in the appropriate dict
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
    #Main logic loop of the character, ran every frame and dictates what happens when
    def loop(self, thingy, keys, WIN, joystick=None, controls=None):

        # If you are dead, you permanently enter a death state
        if self.alive and self.current_health <= 0:
            self.alive = False
            self.state = deathFall(20, self)
        # Reads if any of your attacks have hit your opp, and if they have you get a brief window to cancel into another attack   
        for attack in self.hitboxes:
    
            
            if any([x.hasHit for x in self.hitboxes[attack]]):
                self.cancelwindow = 10
                self.cancelNow = True
                
                
        if self.cancelwindow <= 0:
            self.cancelNow = False
        
        # Runs the input buffer functions, advancing and reading inputs every frame
        self.inputBuffer.handleInputs(self.direction, keys, joystick, controls)
        self.process_inputs(thingy)  
        
        # Determines the players direction
        if self.rect.centerx - thingy.rect.centerx > 0:
            self.direction = 'left'
        else:
            self.direction = 'right'
        
        

        

        
        
        #Runs the change state function
        self.change_state()

        #Reads the player's current state and executes whatever the player should be doing in their current state
        self.state.update(self, self.inputBuffer)
        
        #Does all movement
        self.movement(self.xvel,self.yvel, thingy, WIN)
        #Ticks the cancelWindow counter
        self.cancelwindow -= 1
        #Updates the animation controller
        self.animController(WIN)
        

        


        
        
    # Simple draw function, draws the sprite with the animDraw() method        
    def draw(self, WIN):
        self.animDraw(WIN)
        # guh = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        # pygame.draw.rect(guh, GRAY, guh.get_rect())           #Same as hit and hurt box draw functions, but for the gray pushbox that indicates player collision
        # WIN.blit(guh, self.rect)
        # pygame.draw.rect(WIN, GRAY, self.rect, 2)
        

    
        
# The following behemoth is the States section, and it would be pointless to comment every single one,

# In essence, every frame the current active frame class runs it's "update" method which tells the character what it should be currently doing, and also checks
# if it meets the conditions to switch states, and if it does it performs a transition before returning the new class

#Theres a whole lot of states, but most of them boil down to "How should the player move in this scenario"? "Are they actionable?" "How do they enter different states?", and "Does anything else need to happen right now?"

# This is mostly accomplished through the use of timers (usually created during init), and reading the current inputs. In some cases, like the jump class,
# We read whether or not the player has released the jump button before allowing another jump to be performed, so to avoid instant double jumps.



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
            if 'downleft'  in inputs.currentInput or 'down' in inputs.currentInput:
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
            if 'down' in inputs.currentInput or 'downleft' in inputs.currentInput:
                    character.rect.bottom = FLOOR
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

class deathFall(KDtumble):
    def __init__(self, xknockback, character):
        super().__init__(xknockback, character)
        character.hurtboxes = []
    def enter_state(self, character, *args):
        if character.rect.bottom == FLOOR and self.timer > 36:
            return dead(character)
    def update(self, character, inputs):

        character.gravity()
        character.do_friction(0.5)
        self.timer += 1 


class airStun:
    def __init__(self,xknockback,character, yknockback=False):
        self.timer = 0
        character.xvel -= xknockback
        character.animIndex = 0
        
        
        
        
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
class dead(hard_KD):
    
    def enter_state(self, character, *args):
        pass

    def update(self, character, inputs):
        character.animIndex = 0
        character.do_friction()
        character.gravity()




# Hitbox, Hurtbox, and Pushbox

# All fundamentally similar objects, they serve as "boxs" that are spawned in relation to the player so determine where attacks can and cannot hit, 
# To impose the properties of attack unto the opponents,
# And to avoid overlapping players.
# They all update themselves every frame to move to a certain distance away from the player as dictate by their offset, and other logic is handled in baseScene iwth collsion handling



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
       
    def draw(self, WIN):

        guh = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        pygame.draw.rect(guh, GRAY, guh.get_rect())
        WIN.blit(guh, self.rect)
        pygame.draw.rect(WIN, GRAY, self.rect, 5)
    






        

