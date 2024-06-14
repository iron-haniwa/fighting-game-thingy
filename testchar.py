import pygame, sys, random, colour
from inputreaderthing import inputReader, specialMove
import sneed2

pygame.init()
pygame.font.init()



class testChar(sneed2.Player):
    def __init__(self, xpos, ypos, controls, stfu=True):
        super().__init__(xpos, ypos, controls, stfu)
        self.defaultHB = sneed2.Hurtbox(self,140, 390,0,80)
        self.crouchHB = sneed2.Hurtbox(self,140, 250,0,10)
        self.jumpLimit = 2
        self.image = pygame.image.load('assets\characters\Shiki\shiki_0-0.png')
        self.anims = {'Idle':[], 'fWalk':[], 'bWalk':[],'Crouch':[],'Jump':[], 'backDash':[], 'Dash':[], 'airDash':[], 'dashFall':[],'endDash':[], 'startCrouch':[], 
                      '2A':[], '5A':[], 'jA':[]}
        self.speed = 8
        self.dashFactor = 3.5
        for i in range(15):
            self.anims['Idle'].append(pygame.image.load(f'assets\characters\Shiki\shiki_0-{i}.png'))
        for i in range(10):
            self.anims['fWalk'].append(pygame.image.load(f'assets\characters\Shiki\shiki_0-{i + 320}.png'))
        for i in range(12):
            self.anims['bWalk'].append(pygame.image.load(f'assets\characters\Shiki\shiki_0-{i + 332}.png'))
        self.anims['startCrouch'].append(pygame.image.load(f'assets\characters\Shiki\shiki_0-{73}.png'))
        self.anims['startCrouch'].append(pygame.image.load(f'assets\characters\Shiki\shiki_0-{74}.png'))
        for i in range(15):
            self.anims['Crouch'].append(pygame.image.load(f'assets\characters\Shiki\shiki_0-{i + 105}.png'))
        for i in range(8):
            self.anims['Jump'].append(pygame.image.load(f'assets\characters\Shiki\shiki_0-{i + 120}.png'))
        for i in range(7):
            self.anims['backDash'].append(pygame.image.load(f'assets\characters\Shiki\shiki_0-{i + 357}.png'))
        
        self.anims['backDash'].append(pygame.image.load(f'assets\characters\Shiki\shiki_0-362.png'))
        self.anims['backDash'].append(pygame.image.load(f'assets\characters\Shiki\shiki_0-362.png'))
        for i in range(9):
            self.anims['Dash'].append(pygame.image.load(f'assets\characters\Shiki\shiki_0-{i + 344}.png'))
        for i in range(4):
            self.anims['endDash'].append(pygame.image.load(f'assets\characters\Shiki\shiki_0-{i + 353}.png'))
        for i in range(8):
            self.anims['airDash'].append(pygame.image.load(f'assets\characters\Shiki\shiki_0-{i + 374}.png'))
        for i in range (2):
            self.anims['dashFall'].append(pygame.image.load(f'assets\characters\Shiki\shiki_0-{i + 381}.png'))
        for i in range(8):
            self.anims['2A'].append(pygame.image.load(f'assets\characters\Shiki\shiki_0-{i + 75}.png'))
        for i in range(7):
            self.anims['5A'].append(pygame.image.load(f'assets\characters\Shiki\shiki_0-{i + 16}.png'))
        for i in range(9):
            self.anims['jA'].append(pygame.image.load(f'assets\characters\Shiki\shiki_0-{i + 128}.png'))
        self.animIndex = 0

    def process_inputs(self):
        self.move = self.moveReader.commandReader(self, self.inputBuffer.inputBuffer)
        #print(self.inputBuffer.currentInput)
        if self.move == 'Dash':
            #print('guh')
            if isinstance(self.state, sneed2.Jump):
                if self.amountDashed < self.dashLimit:
                    self.state = sneed2.airDash(self)
            elif isinstance(self.state, sneed2.Idle) or isinstance(self.state, sneed2.forwardWalk):
                self.state = sneed2.Dash()
        if self.move == 'bDash':
            #print('guh')
            if isinstance(self.state, sneed2.Idle) or isinstance(self.state, sneed2.backWalk):
                self.state = sneed2.backDash()
            elif isinstance(self.state, sneed2.Jump):
                if self.amountDashed < self.dashLimit:
                    self.state = sneed2.airbDash(self)
        if self.move == '5A':
            if isinstance(self.state, sneed2.Idle):
                self.state = attack5A()
            elif isinstance(self.state, sneed2.Jump):
                self.state = attackjA()
        if self.move == '2A':
            if isinstance(self.state, sneed2.Crouch):
                self.state = attack2A()


    def animController(self, WIN):
        
        
        if isinstance(self.state, sneed2.Idle):
            if self.state.endDash == True:
                self.animIndex += 0.25

                if self.animIndex >= len(self.anims['endDash']):
                    self.state.endDash = False
                    self.animIndex = len(self.anims['endDash']) -1 
                     
                
                self.image = self.anims['endDash'][int(self.animIndex)]
                self.imagenew = self.image.get_rect(centerx = self.rect.centerx, bottom = self.rect.bottom + 100)
                if self.animIndex >= len(self.anims['endDash']):
                    self.animIndex = 0

            else:
                self.animIndex += 0.12

                if self.animIndex >= len(self.anims['Idle']):
                    self.animIndex = 0 
                
                self.image = self.anims['Idle'][int(self.animIndex)]
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
        
        if self.direction == 'left':
            
            WIN.blit(pygame.transform.flip(self.image, True, False), self.imagenew)
        else:
            WIN.blit(self.image, self.imagenew)


        



class attack2A:
    
    def __init__(self):
        self.timer = 0
    def enter_state(self,character,inputs):
        if self.timer >= 10:
            if character.move == '2A':
                print('cancel'+ str(self.timer))
                return attack2A()
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
    
    def __init__(self):
        self.timer = 0
    def enter_state(self,character,inputs):
        if self.timer >= 10:
            if character.move == '5A':
                print('cancel'+ str(self.timer))
                return attack5A()
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
        #print(self.timer)
class attackjA:
    
    def __init__(self):
        self.timer = 0
    def enter_state(self,character,inputs):
        if character.rect.bottom == sneed2.FLOOR:
            return sneed2.Idle()
        elif self.timer == 19:
            return sneed2.Jump()
        
    def update(self,character,inputs):
        character.hurtboxes = [sneed2.Hurtbox(character,140, 390,character.directionFlip(-10),80),
                               sneed2.Hurtbox(character,60, 110,character.directionFlip(70),50),
                               sneed2.Hurtbox(character,80, 110,character.directionFlip(90),10)]
        if self.timer == 5:
            #print('duh')
            character.place_hitbox('5A', 15, 0, 2, 60, 30, 30, 90, self, 'low', 1, 150)
            character.place_hitbox('5A', 15, 0, 2, 90, 10, 80, 90, self, 'low', 1, 150)
       
            character.place_hitbox('5A', 15, 0, 2, 150, -20, 100, 80, self, 'low', 1, 150)
        character.gravity()
        self.timer += 1
