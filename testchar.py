import pygame, sys, random, colour
from inputreaderthing import inputReader, specialMove
import sneed2

pygame.init()
pygame.font.init()

YOFFSET = 55

FLOOR = 720 - 50

# The actual player, this is a subclass that takes all the basic functions of the Player class, and adds on what is needed to make an individual character uses its roots.

class testChar(sneed2.Player):
    def __init__(self, xpos, ypos, controls):
        #Calls Player's init from sneed2
        super().__init__(xpos, ypos, controls)
        #Overrides the default boxes to suit he character
        self.defaultHB = sneed2.Hurtbox(self,140, 390,0,80)
        self.crouchHB = sneed2.Hurtbox(self,140, 250,0,10)
        #Jumplimit override
        self.jumpLimit = 2
        self.speed = 8
        self.dashFactor = 3.5
        #More character specific overrides
        #creates a basic image var so things dont crash the first iteration
        self.image = pygame.image.load('assets\characters\Shiki\shiki_0-0.png').convert()


        #This is a dictionary holding all possible states for the character, which will correspond to lists of images containing all the graphics data for the character,
        #The state machine system machines animation supremely easy as I can simply read the current state of the player, and animate accordingly
        self.anims = {'Idle':[], 'fWalk':[], 'bWalk':[],'Crouch':[],'Jump':[], 'backDash':[], 'Dash':[], 'airDash':[], 'dashFall':[],'endDash':[], 'startCrouch':[],
                      'endCrouch':[],
                      'standHit':[], 'crouchHit':[],
                      'standBlock':[],'crouchBlock':[],
                      'kdTumble':[], 'getUp':[],'airStun':[], 'quickUp':[],
                      '2A':[], '5A':[], 'jA':[],
                      '2B':[],'5B':[], 'jB':[],
                      '2C':[], 'start5C':[], '5C':[], 'jC':[],
                      'sigmaSlide':[], '3C':[], 'lariat':[]}
        
        #This unholy wall of for loops reads every character sprite needed and stores it in the dictionary under the appropriate tags using nested lists that have the sprite codes

        for i in range(15):
            self.anims['Idle'].append(pygame.image.load(f'assets\characters\Shiki\shiki_0-{i}.png').convert())
        for i in range(10):
            self.anims['fWalk'].append(pygame.image.load(f'assets\characters\Shiki\shiki_0-{i + 320}.png').convert())
        for i in range(12):
            self.anims['bWalk'].append(pygame.image.load(f'assets\characters\Shiki\shiki_0-{i + 332}.png').convert())
        self.anims['startCrouch'].append(pygame.image.load(f'assets\characters\Shiki\shiki_0-{73}.png').convert())
        self.anims['startCrouch'].append(pygame.image.load(f'assets\characters\Shiki\shiki_0-{74}.png').convert())
        for i in range(15):
            self.anims['Crouch'].append(pygame.image.load(f'assets\characters\Shiki\shiki_0-{i + 105}.png').convert())
        for i in range(8):
            self.anims['Jump'].append(pygame.image.load(f'assets\characters\Shiki\shiki_0-{i + 120}.png').convert())
        for i in range(7):
            self.anims['backDash'].append(pygame.image.load(f'assets\characters\Shiki\shiki_0-{i + 357}.png').convert())
        self.anims['endCrouch'] = self.anims['startCrouch'][::-1]
        self.anims['backDash'].append(pygame.image.load(f'assets\characters\Shiki\shiki_0-362.png').convert())
        self.anims['backDash'].append(pygame.image.load(f'assets\characters\Shiki\shiki_0-362.png').convert())
        for i in range(9):
            self.anims['Dash'].append(pygame.image.load(f'assets\characters\Shiki\shiki_0-{i + 344}.png').convert())
        for i in range(4):
            self.anims['endDash'].append(pygame.image.load(f'assets\characters\Shiki\shiki_0-{i + 353}.png').convert())
        for i in range(8):
            self.anims['airDash'].append(pygame.image.load(f'assets\characters\Shiki\shiki_0-{i + 374}.png').convert())
        for i in range (2):
            self.anims['dashFall'].append(pygame.image.load(f'assets\characters\Shiki\shiki_0-{i + 381}.png').convert())

        for i in range(4):
            self.anims['standHit'].append(pygame.image.load(f'assets\characters\Shiki\shiki_0-{i + 410}.png').convert())
        for i in range(4):
            self.anims['crouchHit'].append(pygame.image.load(f'assets\characters\Shiki\shiki_0-{i + 415}.png').convert())
        for i in range(3):
            self.anims['standBlock'].append(pygame.image.load(f'assets\characters\Shiki\shiki_0-{i + 387}.png').convert())
        for i in range(3):
            self.anims['crouchBlock'].append(pygame.image.load(f'assets\characters\Shiki\shiki_0-{i + 390}.png').convert())


        for i in range(8):
            self.anims['2A'].append(pygame.image.load(f'assets\characters\Shiki\shiki_0-{i + 75}.png').convert())
        for i in range(7):
            self.anims['5A'].append(pygame.image.load(f'assets\characters\Shiki\shiki_0-{i + 16}.png').convert())
        for i in range(9):
            self.anims['jA'].append(pygame.image.load(f'assets\characters\Shiki\shiki_0-{i + 128}.png').convert())

        for i in range(12):
            self.anims['2B'].append(pygame.image.load(f'assets\characters\Shiki\shiki_0-{i + 83}.png').convert())
        for i in range(7):
            self.anims['5B'].append(pygame.image.load(f'assets\characters\Shiki\shiki_0-{i + 23}.png').convert())    
        for i in range(10):
            self.anims['jB'].append(pygame.image.load(f'assets\characters\Shiki\shiki_0-{i + 136}.png').convert())
        for i in range(10):
            self.anims['2C'].append(pygame.image.load(f'assets\characters\Shiki\shiki_0-{i + 95}.png').convert())
        for i in range(4):
            self.anims['start5C'].append(pygame.image.load(f'assets\characters\Shiki\shiki_0-{i + 30}.png').convert())
        for i in range(8):
            self.anims['5C'].append(pygame.image.load(f'assets\characters\Shiki\shiki_0-{i + 33}.png').convert())
        for i in range(11):
            self.anims['jC'].append(pygame.image.load(f'assets\characters\Shiki\shiki_0-{i + 146}.png').convert())
        for i in range(9):
            self.anims['kdTumble'].append(pygame.image.load(f'assets\characters\Shiki\shiki_0-{i + 433}.png').convert())
        for i in range(4):
            self.anims['getUp'].append(pygame.image.load(f'assets\characters\Shiki\shiki_0-{i + 454}.png').convert())
        for i in range(4):
            self.anims['airStun'].append(pygame.image.load(f'assets\characters\Shiki\shiki_0-{i + 425}.png').convert())
        for i in range(4):
            self.anims['quickUp'].append(pygame.image.load(f'assets\characters\Shiki\shiki_0-{i + 450}.png').convert())
        for i in range(10):
            self.anims['sigmaSlide'].append(pygame.image.load(f'assets\characters\Shiki\shiki_0-{i + 207}.png').convert())
        for i in range(12):
            self.anims['3C'].append(pygame.image.load(f'assets\characters\Shiki\shiki_0-{i + 166}.png').convert())
        for i in range(11):
            self.anims['lariat'].append(pygame.image.load(f'assets\characters\Shiki\shiki_0-{i + 178}.png').convert())
        #Defaults the anim index again
        self.animIndex = 0

        


    def process_inputs(self, player2):
        
        #This is the souped out input processor,
        #With every actual attacking state, this reads the special move list and interrupts the current state with an attack one is detected
        #while the player is in a valid state

        self.move = self.moveReader.commandReader(self, self.inputBuffer.inputBuffer)
       


        if self.move == 'Dash':
            
            if isinstance(self.state, sneed2.Jump):
                if self.amountDashed < self.dashLimit:
                    self.state = sneed2.airDash(self)
            elif isinstance(self.state, sneed2.Idle) or isinstance(self.state, sneed2.forwardWalk):
                self.state = sneed2.Dash()
        if self.move == 'bDash':
            
            if isinstance(self.state, sneed2.Idle) or isinstance(self.state, sneed2.backWalk):
                self.state = sneed2.backDash()
            elif isinstance(self.state, sneed2.Jump):
                if self.amountDashed < self.dashLimit:
                    self.state = sneed2.airbDash(self)
        if self.move == 'Tatsumaki':
            if isinstance(self.state, (sneed2.Idle, sneed2.forwardWalk, sneed2.backWalk)):
                self.state = sigmaSlide(self)
            elif isinstance(self.state, normals):
                if self.cancelNow:
                    if self.move not in player2.currentCombo:
                        self.state = sigmaSlide(self)
        if self.move == 'Hadouken':
            if isinstance(self.state, (sneed2.Idle, sneed2.forwardWalk, sneed2.backWalk)):
                self.state = lariatKojima(self)
            elif isinstance(self.state, normals):
                if self.cancelNow:
                    if self.move not in player2.currentCombo:
                        self.state = lariatKojima(self)

        # I will comment just 5A, as pretty much everything is copypasted anyway,


        if self.move == '5A':
            if isinstance(self.state, (sneed2.Idle, sneed2.forwardWalk, sneed2.backWalk)): # First, the input reader checks if the player is in a neutral state, 
                                                                                           # in which case the light attack routine is ran regularly
                
                self.state = attack5A(self)

            elif isinstance(self.state, normals):                   # Next comes Reverse Beat, if the player is currently in the middle of another normal attack.
                                                                    # and that move has both already hit the opponent and the current move has not been performed, you can cancel the recovery into the new attack
                if self.cancelNow:                                  # Anything can cancel into a command input, but they cannot cancel into anything
                    if player2.currentCombo.count(self.move) <= 3:  # A attacks are the exception, as they can be cancelled into themselves up to 3 times
                        self.state = attack5A(self)
            elif isinstance(self.state, aerialnormals):
                if self.cancelNow:
                    if player2.currentCombo.count(self.move) <= 3:
                        self.state = attackjA(self)
            elif isinstance(self.state, sneed2.Jump):
                self.state = attackjA(self)
        if self.move == '2A':
            if isinstance(self.state, sneed2.Crouch):
                self.state = attack2A(self)
            elif isinstance(self.state, normals):
                if self.cancelNow:
                    if player2.currentCombo.count(self.move) <= 3:
                        self.state = attack2A(self)
        if self.move == '5B':
            if isinstance(self.state, (sneed2.Idle, sneed2.forwardWalk, sneed2.backWalk)):
                self.state = attack5B(self)
            elif isinstance(self.state, normals):
                if self.cancelNow:
                    if self.move not in player2.currentCombo:
                        self.state = attack5B(self)
            elif isinstance(self.state, aerialnormals):
                if self.cancelNow:
                    if self.move not in player2.currentCombo:
                        self.state = attackjB(self)
            elif isinstance(self.state, sneed2.Jump):
                self.state = attackjB(self)
        if self.move == '2B':
            if isinstance(self.state, sneed2.Crouch):
                self.state = attack2B(self)
            elif self.cancelNow:
                    if self.move not in player2.currentCombo:
                        self.state = attack2B(self)
        if self.move == '2C':
            if isinstance(self.state, sneed2.Crouch):
                self.state = attack2C(self)
            elif self.cancelNow:
                    if self.move not in player2.currentCombo:
                        self.state = attack2C(self)
        if self.move == '5C':
            if isinstance(self.state, (sneed2.Idle, sneed2.forwardWalk, sneed2.backWalk)):
                self.state = startup5C(self)
            elif isinstance(self.state, normals):
                if self.cancelNow:
                    if self.move not in player2.currentCombo:
                        self.state = startup5C(self)
            elif isinstance(self.state, aerialnormals):
                if self.cancelNow:
                    if self.move not in player2.currentCombo:
                        self.state = attackjC(self)
            elif isinstance(self.state, sneed2.Jump):
                self.state = attackjC(self)


    def animController(self, WIN):
        
        #This is the animation controller. It reads the current state, chooses the appropriate list of 
        #sprites via the dictionary, and then displays them one typically while reading the players timer to know frame timing
        #The actual index of the list is controlled via the "animIndex" variable, which serves as the current reading point and is constantly updated by the various different types of animation.
        #In cases where I did not need to time specific frames of animation to specific frames of logic, I incremented the animIndex by decimal amounts to control the rate at which it increased,
        #And converted it to an integer at the point in which it was used as an index, which automatically rounds the number.
        
        
        if isinstance(self.state, sneed2.Idle):
            if self.state.endDash == True: # In some cases like the idle animation, I created special entry variables that play a different animation depending on the action you had just terminated,
                                           # such as a stopping animation in this case, and then it reverts to regular Idle when the animation completes.
                
                self.animIndex += 0.25

                if self.animIndex >= len(self.anims['endDash']): 
                    self.state.endDash = False
                    self.animIndex = len(self.anims['endDash']) -1 
                     
                
                self.image = self.anims['endDash'][int(self.animIndex)]
                self.imagenew = self.image.get_rect(centerx = self.rect.centerx, bottom = self.rect.bottom + 100)
                if self.animIndex >= len(self.anims['endDash']):
                    self.animIndex = 0
            elif self.state.endCrouch == True:
                self.animIndex += 0.25

                if self.animIndex >= len(self.anims['endCrouch']):
                    self.state.endCrouch = False
                    self.animIndex = len(self.anims['endCrouch']) -1 
                     
                
                self.image = self.anims['endCrouch'][int(self.animIndex)]
                self.imagenew = self.image.get_rect(centerx = self.rect.centerx, bottom = self.rect.bottom + 100)
                if self.animIndex >= len(self.anims['endCrouch']):
                    self.animIndex = 0
            else:
                self.animIndex += 0.12

                if self.animIndex >= len(self.anims['Idle']):
                    self.animIndex = 0 
                
                self.image = self.anims['Idle'][int(self.animIndex)]
                self.imagenew = self.image.get_rect(centerx = self.rect.centerx, bottom = self.rect.bottom + 100)

        elif isinstance(self.state, sneed2.Hitstun):
            step = len(self.anims['standHit']) / self.state.length
            self.animIndex += step / 2

            if self.animIndex >= len(self.anims['standHit']):
                self.animIndex = len(self.anims['standHit']) -1
            
            self.image = self.anims['standHit'][int(self.animIndex)]
            self.imagenew = self.image.get_rect(centerx = self.rect.centerx, bottom = self.rect.bottom + 100)
        elif isinstance(self.state, sneed2.cHitstun):
            step = len(self.anims['crouchHit']) / self.state.length
            self.animIndex += step / 2

            if self.animIndex >= len(self.anims['crouchHit']):
                self.animIndex = len(self.anims['crouchHit']) -1
            
            self.image = self.anims['crouchHit'][int(self.animIndex)]
            self.imagenew = self.image.get_rect(centerx = self.rect.centerx, bottom = self.rect.bottom + 100)
        elif isinstance(self.state, sneed2.Blockstun):
            step = len(self.anims['standBlock']) / self.state.length
            self.animIndex += step / 2

            if self.animIndex >= len(self.anims['standBlock']):
                self.animIndex = len(self.anims['standBlock']) -1
            
            self.image = self.anims['standBlock'][int(self.animIndex)]
            self.imagenew = self.image.get_rect(centerx = self.rect.centerx, bottom = self.rect.bottom + 100)
        elif isinstance(self.state, sneed2.cBlockstun):
            step = len(self.anims['crouchBlock']) / self.state.length
            self.animIndex += step / 2

            if self.animIndex >= len(self.anims['crouchBlock']):
                self.animIndex = len(self.anims['crouchBlock']) -1
            
            self.image = self.anims['crouchBlock'][int(self.animIndex)]
            self.imagenew = self.image.get_rect(centerx = self.rect.centerx, bottom = self.rect.bottom + 100)

        elif isinstance(self.state, (sneed2.KDtumble, sneed2.deathFall)):
            if self.state.timer == 0:
                self.animIndex = 0
            else:
                self.animIndex += 0.25

            if self.animIndex >= len(self.anims['kdTumble']):
                self.animIndex = len(self.anims['kdTumble']) - 1
            
            self.image = self.anims['kdTumble'][int(self.animIndex)]
            self.imagenew = self.image.get_rect(centerx = self.rect.centerx, bottom = self.rect.bottom + 100)
        elif isinstance(self.state, sneed2.airStun):
            if self.state.timer == 0:
                self.animIndex = 0
            else:
                self.animIndex += 0.25

            if self.animIndex >= len(self.anims['airStun']):
                self.animIndex = len(self.anims['airStun']) - 1
            
            self.image = self.anims['airStun'][int(self.animIndex)]
            self.imagenew = self.image.get_rect(centerx = self.rect.centerx, bottom = self.rect.bottom + 100)

        elif isinstance(self.state, sneed2.hard_KD):
            if self.state.timer >= 39:
                self.animIndex += 0.25


            if self.animIndex >= len(self.anims['getUp']):
                self.animIndex = len(self.anims['getUp']) - 1
            
            self.image = self.anims['getUp'][int(self.animIndex)]
            self.imagenew = self.image.get_rect(centerx = self.rect.centerx, bottom = self.rect.bottom + 100)
        elif isinstance(self.state, sneed2.dead):
            self.animIndex = 0
            
            self.image = self.anims['getUp'][int(self.animIndex)]
            self.imagenew = self.image.get_rect(centerx = self.rect.centerx, bottom = self.rect.bottom + 100)    

        elif isinstance(self.state, sneed2.soft_KD):
            
            self.animIndex += 0.25


            if self.animIndex >= len(self.anims['quickUp']):
                self.animIndex = len(self.anims['quickUp']) - 1
            
            self.image = self.anims['quickUp'][int(self.animIndex)]
            self.imagenew = self.image.get_rect(centerx = self.rect.centerx, bottom = self.rect.bottom + 100)

        


        elif isinstance(self.state, sneed2.forwardWalk):
            self.animIndex += 0.15

            if self.animIndex >= len(self.anims['fWalk']):
                self.animIndex = 1
            
            self.image = self.anims['fWalk'][int(self.animIndex)]
            self.imagenew = self.image.get_rect(centerx = self.rect.centerx, bottom = self.rect.bottom + 100)

        elif isinstance(self.state, sneed2.backWalk):
            self.animIndex += 0.15

            if self.animIndex >= len(self.anims['bWalk']):
                self.animIndex = 1
            
            self.image = self.anims['bWalk'][int(self.animIndex)]
            self.imagenew = self.image.get_rect(centerx = self.rect.centerx, bottom = self.rect.bottom + 100)

        elif isinstance(self.state, sneed2.Crouch):

            if self.state.startCrouch == True:
                self.animIndex += 0.4
                if self.animIndex >= len(self.anims['startCrouch']):
                    self.state.startCrouch = False
                    self.animIndex = len(self.anims['startCrouch']) -1 
                     
                
                self.image = self.anims['startCrouch'][int(self.animIndex)]
                self.imagenew = self.image.get_rect(centerx = self.rect.centerx, bottom = self.rect.bottom + 100)
                if self.animIndex >= len(self.anims['startCrouch']):
                    self.animIndex = 0

            else:

                self.animIndex += 0.1

                if self.animIndex >= len(self.anims['Crouch']):
                    self.animIndex = 0
                
                self.image = self.anims['Crouch'][int(self.animIndex)]
                self.imagenew = self.image.get_rect(centerx = self.rect.centerx, bottom = self.rect.bottom + 100)
        elif isinstance(self.state, sneed2.Jump) or isinstance(self.state, sneed2.preJump) or isinstance(self.state, sneed2.airbDash):
            if isinstance(self.state, sneed2.Jump) and self.state.postDash == True:
                self.animIndex += 0.25

                if self.animIndex >= len(self.anims['dashFall']):
                    self.animIndex = 0
            
                self.image = self.anims['dashFall'][int(self.animIndex)]
                self.imagenew = self.image.get_rect(centerx = self.rect.centerx, bottom = self.rect.bottom + 100)

            else:
                if self.yvel <= -35:
                    self.animIndex = 0
                else:
                    self.animIndex += 0.1
                
                if self.animIndex >= len(self.anims['Jump']):
                    self.animIndex = 7
                
                self.image = self.anims['Jump'][int(self.animIndex)]
                self.imagenew = self.image.get_rect(centerx = self.rect.centerx, bottom = self.rect.bottom + 100)

        elif isinstance(self.state, sneed2.backDash):

            if self.state.timer <= 4:
                self.animIndex += 1

            if self.state.timer >= 15:
                self.animIndex += 0.25
            if self.animIndex >= len(self.anims['backDash']):
                self.animIndex = len(self.anims['backDash']) - 1
            
            self.image = self.anims['backDash'][int(self.animIndex)]
            self.imagenew = self.image.get_rect(centerx = self.rect.centerx, bottom = self.rect.bottom + 100)
        elif isinstance(self.state, sneed2.Dash):
            self.animIndex += 0.25

            if self.animIndex >= len(self.anims['Dash']):
                self.animIndex = 1
            
            self.image = self.anims['Dash'][int(self.animIndex)]
            self.imagenew = self.image.get_rect(centerx = self.rect.centerx, bottom = self.rect.bottom + 100)

        elif isinstance(self.state, sneed2.airDash):
            
            if self.state.timer < 8:
                self.animIndex += 0.25
                if self.animIndex >= len(self.anims['airDash']) - 7:
                    self.animIndex = 1
            if self.state.timer == 14:
                self.animIndex = 0
            self.image = self.anims['airDash'][int(self.animIndex)]
            self.imagenew = self.image.get_rect(centerx = self.rect.centerx, bottom = self.rect.bottom + 100)

        elif isinstance(self.state, attack2A):
            if self.state.timer < 5:
                self.animIndex += 0.5
            elif self.state.timer == 5 or self.state.timer == 6:
                self.animIndex = 4
            else:
                self.animIndex += 0.25

            if self.animIndex >= len(self.anims['2A']):
                self.animIndex = 1
            
            self.image = self.anims['2A'][int(self.animIndex)]
            self.imagenew = self.image.get_rect(centerx = self.rect.centerx, bottom = self.rect.bottom + 100)
        elif isinstance(self.state, attack5A):
            if self.state.timer < 5:
                self.animIndex += 0.4
            elif self.state.timer == 5 or self.state.timer == 6:
                self.animIndex = 2
            else:
                self.animIndex += 0.4

            if self.animIndex >= len(self.anims['5A']):
                self.animIndex = 1
            
            self.image = self.anims['5A'][int(self.animIndex)]
            self.imagenew = self.image.get_rect(centerx = self.rect.centerx, bottom = self.rect.bottom + 100)
        elif isinstance(self.state, attackjA):
            if self.state.timer <= 2:
                self.animIndex = 0
            elif self.state.timer == 3 or self.state.timer == 4:
                self.animIndex += 1
            elif self.state.timer >= 5 and self.state.timer < 14:
                self.animIndex = 3
            elif self.state.timer >= 14:
                self.animIndex += 0.5

            if self.animIndex >= len(self.anims['jA']):
                self.animIndex = 1
            
            self.image = self.anims['jA'][int(self.animIndex)]
            self.imagenew = self.image.get_rect(centerx = self.rect.centerx, bottom = self.rect.bottom + 100)

        elif isinstance(self.state, attack2B):
            if self.state.timer <= 2:
                self.animIndex = 0
            elif self.state.timer < 8:
                self.animIndex = 3
            elif self.state.timer == 7:
                self.animIndex = 2
            elif self.state.timer == 12:
                self.animIndex += 0.5
            elif self.state.timer == 14:
                self.animIndex = 6
            else:
                self.animIndex += 0.25

            if self.animIndex >= len(self.anims['2B']):
                self.animIndex = 1
            
            self.image = self.anims['2B'][int(self.animIndex)]
            self.imagenew = self.image.get_rect(centerx = self.rect.centerx, bottom = self.rect.bottom + 100)

        elif isinstance(self.state, attack5B):
            if self.state.timer <= 2:
                self.animIndex = 0
            elif self.state.timer < 8:
                self.animIndex = 1
            elif self.state.timer >= 8 and self.state.timer <= 10:
                self.animIndex = 2
            else:
                self.animIndex += 0.25

            if self.animIndex >= len(self.anims['5B']):
                self.animIndex = 1
            
            self.image = self.anims['5B'][int(self.animIndex)]
            self.imagenew = self.image.get_rect(centerx = self.rect.centerx, bottom = self.rect.bottom + 100)
        elif isinstance(self.state, attackjB):
            if self.state.timer <= 2:
                self.animIndex = 0
            elif self.state.timer == 3 or self.state.timer == 4:
                self.animIndex += 1
            elif self.state.timer == 6 :
                self.animIndex = 3
            elif self.state.timer == 8:
                self.animIndex = 4
            elif self.state.timer >= 14:
                self.animIndex += 0.5

            if self.animIndex >= len(self.anims['jB']):
                self.animIndex = 9
            
            self.image = self.anims['jB'][int(self.animIndex)]
            self.imagenew = self.image.get_rect(centerx = self.rect.centerx, bottom = self.rect.bottom + 100)
        elif isinstance(self.state, attack2C):
            if self.state.timer < 2:
                self.animIndex = 0
            elif self.state.timer == 3:
                self.animIndex = 1
            elif self.state.timer == 5:
                self.animIndex = 2
            elif self.state.timer >= 7 and self.state.timer <= 12:

                self.animIndex = 4
            else:
                self.animIndex += 0.25

            if self.animIndex >= len(self.anims['2C']):
                self.animIndex = 9
            
            self.image = self.anims['2C'][int(self.animIndex)]
            self.imagenew = self.image.get_rect(centerx = self.rect.centerx, bottom = self.rect.bottom + 100)
        
        elif isinstance(self.state, startup5C):
            #print(len(self.anims['start5C']))
            if self.state.timer == 0:
                self.animIndex = 0
            elif self.state.timer == 4:
                self.animIndex = 1
            elif self.state.timer == 16:
                self.animIndex = 2
            if self.animIndex >= len(self.anims['start5C']):
                self.animIndex = 0
            
            self.image = self.anims['start5C'][int(self.animIndex)]
            self.imagenew = self.image.get_rect(centerx = self.rect.centerx, bottom = self.rect.bottom + 100)

        elif isinstance(self.state, attack5C):
            #print(len(self.anims['5C']))
            if self.state.timer == 0:
                self.animIndex = 0
            elif self.state.timer == 2:
                self.animIndex = 1
            elif self.state.timer > 10:
                self.animIndex += 0.3
            if self.animIndex >= len(self.anims['5C']):
                self.animIndex = 0
            
            self.image = self.anims['5C'][int(self.animIndex)]
            self.imagenew = self.image.get_rect(centerx = self.rect.centerx, bottom = self.rect.bottom + 100)

        elif isinstance(self.state, attackjC):
            if self.state.timer <= 4:
                self.animIndex += 1
            elif self.state.timer <= 7:
                self.animIndex = 4
            elif self.state.timer < 10:
                self.animIndex = 5
            elif self.state.timer >= 10 and self.state.timer < 17:
                self.animIndex = 6
            elif self.state.timer >= 17:
                self.animIndex += 0.5

            if self.animIndex >= len(self.anims['jC']):
                print(self.state.timer)
                self.animIndex = 10
            
            self.image = self.anims['jC'][int(self.animIndex)]
            self.imagenew = self.image.get_rect(centerx = self.rect.centerx, bottom = self.rect.bottom + 100)

        elif isinstance(self.state, sigmaSlide):
            #print(len(self.anims['5C']))
            if self.state.timer < 7:
                self.animIndex += 0.25
            if self.state.timer == 7:
                self.animIndex = 5
            elif self.state.timer > 7 and self.state.timer <= 20:
                #print(self.animIndex)
                self.animIndex += 0.3
                if self.animIndex > 7:
                 self.animIndex = 5
            else: 
                self.animIndex += 0.25
                if self.animIndex >= len(self.anims['sigmaSlide']):
                    
                    self.animIndex = len(self.anims['sigmaSlide']) - 1
            
            
            self.image = self.anims['sigmaSlide'][int(self.animIndex)]
            self.imagenew = self.image.get_rect(centerx = self.rect.centerx, bottom = self.rect.bottom + 100)
        elif isinstance(self.state, attack3C):
            #print(len(self.anims['5C']))
            if self.state.timer == 0:
                self.animIndex += 0.3
            elif self.state.timer == 10:
                self.animIndex = 5
            elif self.state.timer > 14:
                self.animIndex += 0.25
            if self.animIndex >= len(self.anims['3C']):
                self.animIndex = len(self.anims['3C']) - 1
            
            self.image = self.anims['3C'][int(self.animIndex)]
            self.imagenew = self.image.get_rect(centerx = self.rect.centerx, bottom = self.rect.bottom + 100)
        elif isinstance(self.state, lariatKojima):
            #print(len(self.anims['5C']))
            if self.state.timer < 12:
                self.animIndex += 0.3
            elif self.state.timer == 12:
                self.animIndex = 5
            elif self.state.timer > 14:
                self.animIndex += 0.3
            if self.animIndex >= len(self.anims['lariat']):
                self.animIndex = len(self.anims['lariat']) - 1
            
            self.image = self.anims['lariat'][int(self.animIndex)]
            self.imagenew = self.image.get_rect(centerx = self.rect.centerx, bottom = self.rect.bottom + 100)

    def animDraw(self, WIN):
        if self.direction == 'left':
            
            WIN.blit(pygame.transform.flip(self.image, True, False), self.imagenew)
        else:
            WIN.blit(self.image, self.imagenew)


        
# This section is much like the generic states section from Sneed2, as it is a field of the various attack states the player character can take

# This are slighly unique as they all have timers and an exact predetermined course of action, where they spawn hitboxes and shift hurtboxes at guaranteed times,

# Before returning you to normal or allowing special followups depending on the attack.


class attack2A:
    
    def __init__(self, character):
        self.timer = 0
        character.animIndex = 0
    def enter_state(self,character,inputs):
        if self.timer >= 10:
            if character.move == '2A':
                #print('cancel'+ str(self.timer))
                return attack2A(character)
        if self.timer == 18:
            return sneed2.Crouch()
        
    def update(self,character,inputs):
        character.hurtboxes = [sneed2.Hurtbox(character,140, 250,character.directionFlip(-10),10), sneed2.Hurtbox(character,110, 190,character.directionFlip(100),-20)]
        if self.timer == 5:
            #print('duh')
            character.place_hitbox('2A', 15, 0, 2, 100, 20, 100, 100, self, 'low', 1, 150)
            character.place_hitbox('2A', 15, 0, 2, 100, 90, 150, 80, self, 'low', 1, 150)
        self.timer += 1
class attack5A:
    
    def __init__(self, character):
        self.timer = 0
        character.animIndex = 0
    def enter_state(self,character,inputs):
        if self.timer >= 10:
            if character.move == '5A':
                print('cancel'+ str(self.timer))
                return attack5A(character)
        if self.timer == 18:
            return sneed2.Idle()
        
    def update(self,character,inputs):
        character.hurtboxes = [sneed2.Hurtbox(character,140, 390,character.directionFlip(-10),80),
                               sneed2.Hurtbox(character,60, 110,character.directionFlip(70),50),
                               sneed2.Hurtbox(character,80, 110,character.directionFlip(90),10)]
        if self.timer == 5:
            #print('duh')
            character.place_hitbox('5A', 15, 0, 2, 60, 30, 30, 90, self, 'low', 1, 150)
            character.place_hitbox('5A', 15, 0, 2, 90, 10, 80, 90, self, 'low', 1, 150)
       
            character.place_hitbox('5A', 15, 0, 2, 150, -20, 100, 80, self, 'low', 1, 150)
        self.timer += 1
        character.do_friction()
        #print(self.timer)
class attackjA:
    
    def __init__(self, character):
        self.timer = 0
        character.animIndex = 0
    def enter_state(self,character,inputs):
        if character.rect.bottom == sneed2.FLOOR:
            return sneed2.Idle()
        elif self.timer == 19:
            return sneed2.Jump(character)
        
    def update(self,character,inputs):
        character.hurtboxes = [sneed2.Hurtbox(character,120, 230,character.directionFlip(-20),120),
                               sneed2.Hurtbox(character,70, 140,character.directionFlip(70),150),
                               sneed2.Hurtbox(character,40, 100,character.directionFlip(120),160),
                        
                             ]
        if self.timer == 5:
            character.place_hitbox('jA', 15, 0, 4, 140, 185, 120, 55, character, 'high', 1, 150)
            character.place_hitbox('jA', 15, 0, 4, 80,  140, 90, 90, character, 'low', 1, 150)
            character.place_hitbox('jA', 15, 0, 4, 55,  100, 45, 80, character, 'low', 1, 150)
        character.gravity()
        self.timer += 1

class attack2B:
    
    def __init__(self, character):
        self.timer = 0
        character.animIndex = 0
    def enter_state(self,character,inputs):

        if self.timer == 30:
            return sneed2.Crouch()
        
    def update(self,character,inputs):
        if self.timer == 7:
            character.place_hitbox('2B', 5, 0, 4, 130, 60, 160, 100, character, 'low', 1, 260)
        if self.timer < 14:
            
            character.hurtboxes = [sneed2.Hurtbox(character,120, 230,character.directionFlip(-10),0),
                                sneed2.Hurtbox(character,70, 170,character.directionFlip(80),-30),
                                sneed2.Hurtbox(character,120, 80,character.directionFlip(90),60),
                                ]
        elif self.timer >= 14:
            character.hurtboxes = [sneed2.Hurtbox(character,200, 200,character.directionFlip(30),-15),
                             sneed2.Hurtbox(character,80, 90,character.directionFlip(-80),-70),
                             sneed2.Hurtbox(character,90, 110,character.directionFlip(150),-60),
                             ]
        if self.timer ==  14:
            character.place_hitbox('2B-2', 15, 0, 4, 150, -60, 210, 110, character, 'low', 2, 260)
            character.place_hitbox('2B-2', 15, 0, 4, 100,  0, 100, 100, character, 'low', 2, 260)
        self.timer += 1


class attack5B:
    
    def __init__(self, character):
        self.timer = 0
        character.animIndex = 0
    def enter_state(self,character,inputs):
        if self.timer == 26:
            return sneed2.Idle()
        
    def update(self,character,inputs):
        if self.timer == 0:
            
            character.move_forward(10)
        character.hurtboxes = [sneed2.Hurtbox(character,120, 180,character.directionFlip(50),100),
                               sneed2.Hurtbox(character,140, 240,character.directionFlip(-20),5),
                               sneed2.Hurtbox(character,100, 180,character.directionFlip(50),-20),
                               ]
        if self.timer == 8:
            character.place_hitbox('5B', 20, 0, 4, 120, 100, 100, 100, self, 'mid', 2, 480)
            character.place_hitbox('5B', 20, 0, 4, 100, 30, 80, 60, self, 'mid', 2, 480)
        self.timer += 1
        character.do_friction()
        #print(character.animIndex)

class attackjB:
    
    def __init__(self, character):
        self.timer = 0
        character.animIndex = 0
    def enter_state(self,character,inputs):
        if character.rect.bottom == sneed2.FLOOR:
            return sneed2.Idle()
        
    def update(self,character,inputs):
        character.hurtboxes = [sneed2.Hurtbox(character,140, 390,character.directionFlip(-10),80),
                               sneed2.Hurtbox(character,60, 110,character.directionFlip(70),50),
                               sneed2.Hurtbox(character,80, 110,character.directionFlip(90),10)]
        if self.timer == 5:
            character.place_hitbox('jB', 15, 0, 2, 130, 50, 180, 80, character, 'high', 2, 200)
            character.place_hitbox('jB', 15, 0, 2, 130,  100, 90, 90, character, 'high', 2, 200)
            character.place_hitbox('jB', 15, 0, 2, 90,  0, 170, 70, character, 'high', 2, 200)
            character.place_hitbox('jB', 15, 0, 2, 30,  10, 130, 50, character, 'high', 2, 20)
        if self.timer == 8:
            character.place_hitbox('jB-1', 15, 0, 4, 130, 50, 180, 80, character, 'high', 2, 200)
            character.place_hitbox('jB-1', 15, 0, 4, 160,  100, 90, 90, character, 'high', 2, 200)
            character.place_hitbox('jB-1', 15, 0, 4, 90,  0, 170, 70, character, 'high', 2, 200)
            character.place_hitbox('jB-1', 15, 0, 4, 30,  10, 130, 50, character, 'high', 2, 20)
        character.gravity()
        self.timer += 1


class attack2C:
    
    def __init__(self, character):
        self.timer = 0
        character.animIndex = 0
    def enter_state(self,character,inputs):

        if self.timer == 36:
            return sneed2.Crouch()
        
    def update(self,character,inputs):
        character.hurtboxes = [sneed2.Hurtbox(character,120, 230,character.directionFlip(-20),0),
                               sneed2.Hurtbox(character,70, 140,character.directionFlip(120),-45),
                               sneed2.Hurtbox(character,90, 210,character.directionFlip(70),-10),
                        
                             ]
        if self.timer == 7:
            character.place_hitbox('2C', 15, 20, 7, 150, -30, 140, 100, character, 'low', 2, 620, 'HK')
                    
            character.place_hitbox('2C', 15, 20, 7, 270,  -40, 140, 90, character, 'low', 2, 620, 'HK')
        self.timer += 1


class startup5C:

    def __init__(self, character):
        character.animIndex = 0
        self.timer = 0
        self.release_received = False
    def enter_state(self,character,inputs):
        if self.timer >= 7 and self.release_received == True:
            return attack5C(character)
        if self.timer == 19:
            return attack5C(character)
        
    def update(self,character,inputs):
        character.hurtboxes = [sneed2.Hurtbox(character,140, 250,character.directionFlip(-10),10)]
        if 'C' not in inputs.currentInput:
            self.release_received = True
        self.timer += 1


class attack5C:
    def __init__(self, character):
        self.timer = 0
        character.animIndex = 0
    def enter_state(self,character,inputs):

        if self.timer == 27:
            return sneed2.Idle()
        
    def update(self,character,inputs):
        if self.timer <= 10:
            character.move_forward(15)
        else:
            character.do_friction()
        character.hurtboxes = [sneed2.Hurtbox(character,140, 230,character.directionFlip(-10),0), 
                               sneed2.Hurtbox(character,110, 140,character.directionFlip(-100),-45),
                               sneed2.Hurtbox(character,110, 50,character.directionFlip(100),50),]
        if self.timer == 0:
            character.place_hitbox('5C', 15, 0, 8, 170, 50, 160, 80, self, 'mid', 3, 1000)
        self.timer += 1

class attackjC:
    
    def __init__(self, character):
        self.timer = 0
        character.animIndex = 0
    def enter_state(self,character,inputs):
        if self.timer >= 26:
            return sneed2.Jump(character)
        if character.rect.bottom == sneed2.FLOOR:
            return sneed2.Idle()
        
    def update(self,character,inputs):
        if self.timer == 0:
            character.animIndex = 0
        character.hurtboxes = [sneed2.Hurtbox(character,120, 230,character.directionFlip(-20),120),
                               sneed2.Hurtbox(character,70, 140,character.directionFlip(50),190),
                               sneed2.Hurtbox(character,90, 150,character.directionFlip(70),60),
                        
                             ]
        if self.timer == 10:
            character.place_hitbox('jC', 15, 0, 7, 150, 10, 140, 100, character, 'high', 2, 600)
            character.place_hitbox('jC', 15, 0, 7, 110,  100, 90, 90, character, 'high', 2, 600)
            character.place_hitbox('jC', 15, 0, 7, 110,  40, 170, 90, character, 'high', 2, 600)
            character.place_hitbox('jC', 15, 0, 7, 50,  130, 50, 100, character, 'high', 2, 600)

        
        character.gravity()
        self.timer += 1


class sigmaSlide:

    def __init__(self, character):
        character.animIndex = 0
        self.timer = 0
        self.release_received = False
        character.xvel = 0
    def enter_state(self,character,inputs):

        if self.timer >= 7 and self.timer <= 20:
            if character.move == '5A' or character.move == '5B' or character.move == '5C':
                return attack3C(character)
        if self.timer == 30:
            return sneed2.Crouch()
        
    def update(self,character,inputs):
        if self.timer >= 7 and self.timer <= 18:
            character.move_forward(20)
        if self.timer == 7:
            character.place_hitbox('sigmaSlide', 15, 0, 10, 110, -70, 200, 90, character, 'low', 2, 620, 'AK')
        character.hurtboxes = [sneed2.Hurtbox(character,140, 180,character.directionFlip(-120),-25),
                               sneed2.Hurtbox(character,120, 140,character.directionFlip(-30),-45),
                               sneed2.Hurtbox(character,200, 90,character.directionFlip(90),-70),
                        
                             ]
        character.do_friction()
        self.timer += 1

class lariatKojima:

    def __init__(self, character):
        character.animIndex = 0
        self.timer = 0
        self.release_received = False
        character.xvel = 0
    def enter_state(self,character,inputs):

        if self.timer == 34:
            return sneed2.Crouch()
        
    def update(self,character,inputs):
        if self.timer >= 7 and self.timer <= 18:
            character.move_forward(20)
        if self.timer == 12:
            character.place_hitbox('lariatA', 15, 0, 3, 150, 150, 110, 100, character, 'mid', 2, 1200)
            character.place_hitbox('lariatA', 15, 0, 3, 120, 90, 110, 190, character, 'mid', 2, 1200)
            character.place_hitbox('lariatA', 15, 0, 3, 240, 90, 130, 100, character, 'mid', 2, 1200)
            character.place_hitbox('lariatA', 15, 0, 3, 150, 10, 130, 70, character, 'mid', 2, 1200)
        character.hurtboxes = [sneed2.Hurtbox(character,100, 140,character.directionFlip(30),160),
                               sneed2.Hurtbox(character,240, 190,character.directionFlip(20),-20),
                               sneed2.Hurtbox(character,170, 100,character.directionFlip(40),120),
                              
                        
                             ]
        character.do_friction()
        self.timer += 1


class attack3C:
    def __init__(self, character):
        self.timer = 0
        character.animIndex = 0
    def enter_state(self,character,inputs):

        if self.timer == 39:
            return sneed2.Idle()
        
    def update(self,character,inputs):
        if self.timer == 15:
            character.place_hitbox('3C', 15, 40, 10, 10, 270, 50, 140, character, 'mid', 2, 620, 'L')
            character.place_hitbox('3C', 15, 40, 10, 60, 180, 110, 100, character, 'mid', 2, 620, 'L')
            character.place_hitbox('3C', 15, 40, 10, 120, 90, 110, 190, character, 'mid', 2, 620, 'L')
            character.place_hitbox('3C', 15, 40, 10, 170, 90, 110, 100, character, 'mid', 2, 620, 'L')
            character.place_hitbox('3C', 15, 40, 10, 110, -60, 100, 110, character, 'mid', 2, 620, 'L')
        character.do_friction()
        character.hurtboxes = [sneed2.Hurtbox(character,100, 140,character.directionFlip(-90),-45),
                               sneed2.Hurtbox(character,110, 240,character.directionFlip(10),5),
                               sneed2.Hurtbox(character,120, 110,character.directionFlip(-10),150),
                               sneed2.Hurtbox(character,50, 150,character.directionFlip(0),270),
                        
                             ]
        
        self.timer += 1

# Tuple with every kind of grounded normal, this exists for the isInstance logic of the Reverse Beat system to be able to detect whether or not you are performing an eligible move

normals = (attack2A, attack5A,
           attack2B, attack5B,
           attack2C, attack5C,
           )
# Same thing, but for aerials
aerialnormals = (attackjA,
                 attackjB,
                 attackjC

)


# For posterity, I keep this code, but this is the remnants of an unfortunately unimplemented system in Damage Proration,
# The idea is that every attack has a proration value which is a percentage that decreases the damage of following attacks in a combo
# Sadly, we ran out of time and were not able to fully implement it, so this stands as a final testament to what could have been.

proration_map = {'2A': 68, '5A': 70, 'jA': 75,
                 '2B': 85, '2B-2':100 ,'5B': 90, 'jB': 81, 'jB-1':79,
                 '2C': 55, '5C': 80, 'jC': 90}