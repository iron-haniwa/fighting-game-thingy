import pygame, sys, random, colour
from inputreaderthing import inputReader, specialMove
import sneed2

pygame.init()
pygame.font.init()

YOFFSET = 55

FLOOR = 720 - 50

sacchinScale = 3.3 # This trio of variable exist because the Street Fighter III 3rd Strike sprites have a different scale 
sacchinOffset = 75 # And offset from the Melty Blood Type Lumina sprites used with Shiki, so I offset and scale everything by these values
sacchinOffset2 = - 30



# This is the character file for the game's second character Akuma, because I have 40 minutes to submit this, read testChar instead, it's pretty much the same thing




class satsukichan(sneed2.Player):
    def __init__(self, xpos, ypos, controls):
        super().__init__(xpos, ypos, controls)
        self.defaultHB = sneed2.Hurtbox(self,140, 390,0,80)
        self.crouchHB = sneed2.Hurtbox(self,140, 250,0,10)
        self.current_health = 11700 /1.5
        self.maximum_health = 11700 /1.5
        self.jumpLimit = 2
        self.image = pygame.image.load('assets\characters\Satsuki\SF3_3S_Gouki_21505.png')
        self.anims = {'Idle':[], 'fWalk':[], 'bWalk':[],'Crouch':[],'Jump':[], 'backDash':[], 'Dash':[], 'airDash':[], 'dashFall':[],'endDash':[], 'startCrouch':[],
                      'endCrouch':[],
                      'standHit':[], 'crouchHit':[],
                      'standBlock':[],'crouchBlock':[],
                      'kdTumble':[], 'getUp':[],'airStun':[], 'quickUp':[],
                      '2A':[], '5A':[], 'jA':[],
                      '2B':[],'5B':[], 'jB':[],
                      '2C':[], 'start5C':[], '5C':[], 'jC':[],
                      'sigmaSlide':[], '3C':[], 'lariat':[]}
        self.speed = 8
        self.dashFactor = 4
        for i in range(5):
            
            self.anims['Idle'].append(pygame.transform.scale_by(pygame.image.load(f'assets\characters\Satsuki\SF3_3S_Gouki_{i + 21505}.png'), sacchinScale).convert())
        self.anims['Idle'].extend(self.anims['Idle'][::-1])
        for i in range(10):
            self.anims['fWalk'].append(pygame.transform.scale_by(pygame.image.load(f'assets\characters\Satsuki\SF3_3S_Gouki_{i + 21520}.png'), sacchinScale).convert())
        for i in range(10):
            self.anims['bWalk'].append(pygame.transform.scale_by(pygame.image.load(f'assets\characters\Satsuki\SF3_3S_Gouki_{i + 21532}.png'), sacchinScale).convert())
        for i in range(4):
            self.anims['startCrouch'].append(pygame.transform.scale_by(pygame.image.load(f'assets\characters\Satsuki\SF3_3S_Gouki_{i + 21544}.png'), sacchinScale).convert())
        for i in range(4):
            self.anims['Crouch'].append(pygame.transform.scale_by(pygame.image.load(f'assets\characters\Satsuki\SF3_3S_Gouki_{i + 21552}.png'), sacchinScale).convert())
        for i in range(11):
            self.anims['Jump'].append(pygame.transform.scale_by(pygame.image.load(f'assets\characters\Satsuki\SF3_3S_Gouki_{i + 21568}.png'), sacchinScale).convert())
        for i in range(8):
            self.anims['backDash'].append(pygame.transform.scale_by(pygame.image.load(f'assets\characters\Satsuki\SF3_3S_Gouki_{i + 21632}.png'), sacchinScale).convert())
        self.anims['endCrouch'] = self.anims['startCrouch'][::-1]
        
        for i in range(2):
            self.anims['Dash'].append(pygame.transform.scale_by(pygame.image.load(f'assets\characters\Satsuki\SF3_3S_Gouki_{i + 22256}.png'), sacchinScale).convert())
        for i in range(2):
            self.anims['airDash'].append(pygame.transform.scale_by(pygame.image.load(f'assets\characters\Satsuki\SF3_3S_Gouki_{i + 22256}.png'), sacchinScale).convert())

        for i in range(5):
            self.anims['standHit'].append(pygame.transform.scale_by(pygame.image.load(f'assets\characters\Satsuki\SF3_3S_Gouki_{i + 21658}.png'), sacchinScale).convert())
        for i in range(4):
            self.anims['crouchHit'].append(pygame.transform.scale_by(pygame.image.load(f'assets\characters\Satsuki\SF3_3S_Gouki_{i + 21709}.png'), sacchinScale).convert())
        for i in range(4):
            self.anims['standBlock'].append(pygame.transform.scale_by(pygame.image.load(f'assets\characters\Satsuki\SF3_3S_Gouki_{i + 21599}.png'), sacchinScale).convert())
        for i in range(5):
            self.anims['crouchBlock'].append(pygame.transform.scale_by(pygame.image.load(f'assets\characters\Satsuki\SF3_3S_Gouki_{i + 21603}.png'), sacchinScale).convert())


        for i in range(6):
            self.anims['2A'].append(pygame.transform.scale_by(pygame.image.load(f'assets\characters\Satsuki\SF3_3S_Gouki_{i + 22032}.png'), sacchinScale).convert())
        for i in range(5):
            self.anims['5A'].append(pygame.transform.scale_by(pygame.image.load(f'assets\characters\Satsuki\SF3_3S_Gouki_{i + 21856}.png'), sacchinScale).convert())
        for i in range(6):
            self.anims['jA'].append(pygame.transform.scale_by(pygame.image.load(f'assets\characters\Satsuki\SF3_3S_Gouki_{i + 22064}.png'), sacchinScale).convert())

        for i in range(9):
            self.anims['2B'].append(pygame.transform.scale_by(pygame.image.load(f'assets\characters\Satsuki\SF3_3S_Gouki_{i + 22012}.png'), sacchinScale).convert())
        for i in range(6):
            self.anims['5B'].append(pygame.transform.scale_by(pygame.image.load(f'assets\characters\Satsuki\SF3_3S_Gouki_{i + 21895}.png'), sacchinScale).convert())  
        for i in range(8):
            self.anims['jB'].append(pygame.transform.scale_by(pygame.image.load(f'assets\characters\Satsuki\SF3_3S_Gouki_{i + 22094}.png'), sacchinScale).convert())
        for i in range(10):
            self.anims['2C'].append(pygame.transform.scale_by(pygame.image.load(f'assets\characters\Satsuki\SF3_3S_Gouki_{i + 22044}.png'), sacchinScale).convert())
        for i in range(4):
            self.anims['start5C'].append(pygame.image.load(f'assets\characters\Shiki\shiki_0-{i + 30}.png'))
        for i in range(13):
            self.anims['5C'].append(pygame.transform.scale_by(pygame.image.load(f'assets\characters\Satsuki\SF3_3S_Gouki_{i + 21936}.png'), sacchinScale).convert())
        for i in range(13):
            self.anims['jC'].append(pygame.transform.scale_by(pygame.image.load(f'assets\characters\Satsuki\SF3_3S_Gouki_{i + 22117}.png'), sacchinScale).convert())

            
        for i in range(5):
            self.anims['kdTumble'].append(pygame.transform.scale_by(pygame.image.load(f'assets\characters\Satsuki\SF3_3S_Gouki_{i + 21764}.png'), sacchinScale).convert())
        for i in range(3):
            self.anims['kdTumble'].append(pygame.transform.scale_by(pygame.image.load(f'assets\characters\Satsuki\SF3_3S_Gouki_{i + 21760}.png'), sacchinScale).convert())
        self.anims['kdTumble'].append(pygame.transform.scale_by(pygame.image.load(f'assets\characters\Satsuki\SF3_3S_Gouki_{i + 21750}.png'), sacchinScale).convert())
        self.anims['getUp'].append(pygame.transform.scale_by(pygame.image.load(f'assets\characters\Satsuki\SF3_3S_Gouki_{i + 21750}.png'), sacchinScale).convert())
        for i in range(11):
            self.anims['getUp'].append(pygame.transform.scale_by(pygame.image.load(f'assets\characters\Satsuki\SF3_3S_Gouki_{i + 21824}.png'), sacchinScale).convert())
        for i in range(16):
            self.anims['airStun'].append(pygame.transform.scale_by(pygame.image.load(f'assets\characters\Satsuki\SF3_3S_Gouki_{i + 21792}.png'), sacchinScale).convert())
        for i in range(11):
            self.anims['quickUp'].append(pygame.transform.scale_by(pygame.image.load(f'assets\characters\Satsuki\SF3_3S_Gouki_{i + 21824}.png'), sacchinScale).convert())


        self.animIndex = 0

        


    def process_inputs(self, player2):
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
        if self.move == '5A':
            if isinstance(self.state, (sneed2.Idle, sneed2.forwardWalk, sneed2.backWalk)):
                
                self.state = attack5A(self)

            elif isinstance(self.state, normals):
                if self.cancelNow:
                    if player2.currentCombo.count(self.move) <= 3:
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
                self.state = attack5C(self)
            elif isinstance(self.state, normals):
                if self.cancelNow:
                    if self.move not in player2.currentCombo:
                        self.state = attack5C(self)
            elif isinstance(self.state, aerialnormals):
                if self.cancelNow:
                    if self.move not in player2.currentCombo:
                        self.state = attackjC(self)
            elif isinstance(self.state, sneed2.Jump):
                self.state = attackjC(self)


    def animController(self, WIN):
        if self.direction == 'right':
            sacchinOffset2 = 30
        else:
            sacchinOffset2 = - 30
        
        if isinstance(self.state, sneed2.Idle):
            if self.state.endDash == True:
                
                self.animIndex = 1

                
                self.state.endDash = False
                    
                     
                
                self.image = self.anims['Dash'][int(self.animIndex)]
                self.imagenew = self.image.get_rect(centerx = self.rect.centerx + sacchinOffset2, bottom = self.rect.bottom + sacchinOffset)
                if self.animIndex >= len(self.anims['endDash']):
                    self.animIndex = 0
            elif self.state.endCrouch == True:
                self.animIndex += 0.25

                if self.animIndex >= len(self.anims['endCrouch']):
                    self.state.endCrouch = False
                    self.animIndex = len(self.anims['endCrouch']) -1 
                     
                
                self.image = self.anims['endCrouch'][int(self.animIndex)]
                self.imagenew = self.image.get_rect(centerx = self.rect.centerx + sacchinOffset2, bottom = self.rect.bottom + sacchinOffset)
                if self.animIndex >= len(self.anims['endCrouch']):
                    self.animIndex = 0
            else:
                self.animIndex += 0.12

                if self.animIndex >= len(self.anims['Idle']):
                    self.animIndex = 0 
                
                self.image = self.anims['Idle'][int(self.animIndex)]
                self.imagenew = self.image.get_rect(centerx = self.rect.centerx + sacchinOffset2, bottom = self.rect.bottom + sacchinOffset)

        elif isinstance(self.state, sneed2.Hitstun):
            step = len(self.anims['standHit']) / self.state.length
            self.animIndex += step / 2

            if self.animIndex >= len(self.anims['standHit']):
                self.animIndex = len(self.anims['standHit']) -1
            
            self.image = self.anims['standHit'][int(self.animIndex)]
            self.imagenew = self.image.get_rect(centerx = self.rect.centerx + sacchinOffset2, bottom = self.rect.bottom + sacchinOffset)
        elif isinstance(self.state, sneed2.cHitstun):
            step = len(self.anims['crouchHit']) / self.state.length
            self.animIndex += step / 2

            if self.animIndex >= len(self.anims['crouchHit']):
                self.animIndex = len(self.anims['crouchHit']) -1
            
            self.image = self.anims['crouchHit'][int(self.animIndex)]
            self.imagenew = self.image.get_rect(centerx = self.rect.centerx + sacchinOffset2, bottom = self.rect.bottom + sacchinOffset)
        elif isinstance(self.state, sneed2.Blockstun):
            step = len(self.anims['standBlock']) / self.state.length
            self.animIndex += step / 2

            if self.animIndex >= len(self.anims['standBlock']):
                self.animIndex = 1
            
            self.image = self.anims['standBlock'][int(self.animIndex)]
            self.imagenew = self.image.get_rect(centerx = self.rect.centerx + sacchinOffset2, bottom = self.rect.bottom + sacchinOffset)
        elif isinstance(self.state, sneed2.cBlockstun):
            step = len(self.anims['crouchBlock']) / self.state.length
            self.animIndex += step / 2

            if self.animIndex >= len(self.anims['crouchBlock']):
                self.animIndex = len(self.anims['crouchBlock']) -1
            
            self.image = self.anims['crouchBlock'][int(self.animIndex)]
            self.imagenew = self.image.get_rect(centerx = self.rect.centerx + sacchinOffset2, bottom = self.rect.bottom + sacchinOffset)

        elif isinstance(self.state, (sneed2.KDtumble, sneed2.deathFall)):
            if self.state.timer == 0:
                self.animIndex = 0
            else:
                self.animIndex += 0.25

            if self.animIndex >= len(self.anims['kdTumble']):
                self.animIndex = len(self.anims['kdTumble']) - 1
            
            self.image = self.anims['kdTumble'][int(self.animIndex)]
            self.imagenew = self.image.get_rect(centerx = self.rect.centerx + sacchinOffset2, bottom = self.rect.bottom + sacchinOffset)
        elif isinstance(self.state, sneed2.airStun):
            
            self.animIndex += 0.25

            if self.animIndex >= len(self.anims['airStun']):
                self.animIndex = len(self.anims['airStun']) - 1
            
            self.image = self.anims['airStun'][int(self.animIndex)]
            self.imagenew = self.image.get_rect(centerx = self.rect.centerx + sacchinOffset2, bottom = self.rect.bottom + sacchinOffset)

        elif isinstance(self.state, sneed2.hard_KD):
            if self.state.timer >= 30:
                self.animIndex += 0.25


            if self.animIndex >= len(self.anims['getUp']):
                self.animIndex = len(self.anims['getUp']) - 1
            
            self.image = self.anims['getUp'][int(self.animIndex)]
            self.imagenew = self.image.get_rect(centerx = self.rect.centerx + sacchinOffset2, bottom = self.rect.bottom + sacchinOffset)
        elif isinstance(self.state, sneed2.dead):
            self.animIndex = 0
            
            self.image = self.anims['getUp'][int(self.animIndex)]
            self.imagenew = self.image.get_rect(centerx = self.rect.centerx + sacchinOffset2, bottom = self.rect.bottom + sacchinOffset)    

        elif isinstance(self.state, sneed2.soft_KD):
            
            self.animIndex += 0.25


            if self.animIndex >= len(self.anims['quickUp']):
                self.animIndex = len(self.anims['quickUp']) - 1
            
            self.image = self.anims['quickUp'][int(self.animIndex)]
            self.imagenew = self.image.get_rect(centerx = self.rect.centerx + sacchinOffset2, bottom = self.rect.bottom + sacchinOffset)

        


        elif isinstance(self.state, sneed2.forwardWalk):
            self.animIndex += 0.15

            if self.animIndex >= len(self.anims['fWalk']):
                self.animIndex = 1
            
            self.image = self.anims['fWalk'][int(self.animIndex)]
            self.imagenew = self.image.get_rect(centerx = self.rect.centerx + sacchinOffset2, bottom = self.rect.bottom + sacchinOffset)

        elif isinstance(self.state, sneed2.backWalk):
            self.animIndex += 0.15

            if self.animIndex >= len(self.anims['bWalk']):
                self.animIndex = 1
            
            self.image = self.anims['bWalk'][int(self.animIndex)]
            self.imagenew = self.image.get_rect(centerx = self.rect.centerx + sacchinOffset2, bottom = self.rect.bottom + sacchinOffset)

        elif isinstance(self.state, sneed2.Crouch):

            if self.state.startCrouch == True:
                self.animIndex += 0.4
                if self.animIndex >= len(self.anims['startCrouch']):
                    self.state.startCrouch = False
                    self.animIndex = len(self.anims['startCrouch']) -1 
                     
                
                self.image = self.anims['startCrouch'][int(self.animIndex)]
                self.imagenew = self.image.get_rect(centerx = self.rect.centerx + sacchinOffset2, bottom = self.rect.bottom + sacchinOffset)
                if self.animIndex >= len(self.anims['startCrouch']):
                    self.animIndex = 0

            else:

                self.animIndex += 0.1

                if self.animIndex >= len(self.anims['Crouch']):
                    self.animIndex = 0
                
                self.image = self.anims['Crouch'][int(self.animIndex)]
                self.imagenew = self.image.get_rect(centerx = self.rect.centerx + sacchinOffset2, bottom = self.rect.bottom + sacchinOffset)
        elif isinstance(self.state, sneed2.Jump) or isinstance(self.state, sneed2.preJump) or isinstance(self.state, sneed2.airbDash):
            
            if self.yvel <= -35:
                self.animIndex = 0
            else:
                self.animIndex += 0.1
            
            if self.animIndex >= len(self.anims['Jump']):
                self.animIndex = 7
            
            self.image = self.anims['Jump'][int(self.animIndex)]
            self.imagenew = self.image.get_rect(centerx = self.rect.centerx + sacchinOffset2, bottom = self.rect.bottom + sacchinOffset)

        elif isinstance(self.state, sneed2.backDash):

            if self.state.timer <= 4:
                self.animIndex += 1

            if self.state.timer >= 15:
                self.animIndex += 0.25
            if self.animIndex >= len(self.anims['backDash']):
                self.animIndex = len(self.anims['backDash']) - 1
            
            self.image = self.anims['backDash'][int(self.animIndex)]
            self.imagenew = self.image.get_rect(centerx = self.rect.centerx + sacchinOffset2, bottom = self.rect.bottom + sacchinOffset)
        elif isinstance(self.state, sneed2.Dash):
            self.animIndex = 0
            
            self.image = self.anims['Dash'][int(self.animIndex)]
            self.imagenew = self.image.get_rect(centerx = self.rect.centerx + sacchinOffset2, bottom = self.rect.bottom + sacchinOffset)

        elif isinstance(self.state, sneed2.airDash):
            
            self.animIndex = 0
            self.image = self.anims['airDash'][int(self.animIndex)]
            self.imagenew = self.image.get_rect(centerx = self.rect.centerx + sacchinOffset2, bottom = self.rect.bottom + sacchinOffset)

        elif isinstance(self.state, attack2A):
            if self.state.timer < 5:
                self.animIndex += 0.25
            elif self.state.timer == 5 or self.state.timer == 6:
                self.animIndex = 3
            else:
                self.animIndex += 0.25

            if self.animIndex >= len(self.anims['2A']):
                self.animIndex = 1
            
            self.image = self.anims['2A'][int(self.animIndex)]
            self.imagenew = self.image.get_rect(centerx = self.rect.centerx + sacchinOffset2, bottom = self.rect.bottom + sacchinOffset)
        elif isinstance(self.state, attack5A):
            if self.state.timer < 4:
                self.animIndex = 0
            elif self.state.timer >= 4 and self.state.timer <= 7:
                self.animIndex = 1
            else:
                self.animIndex += 0.4

            if self.animIndex >= len(self.anims['5A']):
                self.animIndex = 1
            
            self.image = self.anims['5A'][int(self.animIndex)]
            self.imagenew = self.image.get_rect(centerx = self.rect.centerx + sacchinOffset2, bottom = self.rect.bottom + sacchinOffset)
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
            self.imagenew = self.image.get_rect(centerx = self.rect.centerx + sacchinOffset2, bottom = self.rect.bottom + sacchinOffset)

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
            self.imagenew = self.image.get_rect(centerx = self.rect.centerx + sacchinOffset2, bottom = self.rect.bottom + sacchinOffset)

        elif isinstance(self.state, attack5B):
            if self.state.timer < 6:
                self.animIndex += 0.25
            elif self.state.timer >= 6 and self.state.timer <= 10:
                self.animIndex = 4
            else:
                self.animIndex += 0.25

            if self.animIndex >= len(self.anims['5B']):
                self.animIndex = 1
            
            self.image = self.anims['5B'][int(self.animIndex)]
            self.imagenew = self.image.get_rect(centerx = self.rect.centerx + sacchinOffset2, bottom = self.rect.bottom + sacchinOffset)
        elif isinstance(self.state, attackjB):
            if self.state.timer < 7:
                self.animIndex += 0.25
            elif self.state.timer == 7:
                self.animIndex = 2
            elif self.state.timer > 9:
                self.animIndex += 0.25
        

            if self.animIndex >= len(self.anims['jB']):
                self.animIndex = len(self.anims['jB']) - 1
            
            self.image = self.anims['jB'][int(self.animIndex)]
            self.imagenew = self.image.get_rect(centerx = self.rect.centerx + sacchinOffset2, bottom = self.rect.bottom + sacchinOffset)
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
            self.imagenew = self.image.get_rect(centerx = self.rect.centerx + sacchinOffset2, bottom = self.rect.bottom + sacchinOffset)

        elif isinstance(self.state, attack5C):
           
            if self.state.timer < 9:
                self.animIndex += 0.25
            elif self.state.timer >= 9 and self.state.timer <= 14:
                self.animIndex = 7
            elif self.state.timer > 14:
                self.animIndex += 0.25
            if self.animIndex >= len(self.anims['5C']):
                self.animIndex = 0
            
            self.image = self.anims['5C'][int(self.animIndex)]
            self.imagenew = self.image.get_rect(centerx = self.rect.centerx + sacchinOffset2, bottom = self.rect.bottom + sacchinOffset)

        elif isinstance(self.state, attackjC):
            if self.state.timer < 5:
                self.animIndex += 0.25
            elif self.state.timer >= 5 and self.state.timer <= 11:
                self.animIndex = 2
            else:
                self.animIndex += 0.5

            if self.animIndex >= len(self.anims['jC']):
                
                self.animIndex = len(self.anims['jC']) - 1
            
            self.image = self.anims['jC'][int(self.animIndex)]
            self.imagenew = self.image.get_rect(centerx = self.rect.centerx + sacchinOffset2, bottom = self.rect.bottom + sacchinOffset)

    
    def animDraw(self, WIN):
        
        self.image.set_colorkey((248, 0, 248))
        if self.direction == 'left':
            
            
            WIN.blit(pygame.transform.flip(self.image, True, False), self.imagenew)
        else:
            WIN.blit(self.image, self.imagenew)
            


        



class attack2A:
    
    def __init__(self, character):
        self.timer = 0
        character.animIndex = 0
    def enter_state(self,character,inputs):
        if self.timer >= 10:
            if character.move == '2A':
              
                return attack2A(character)
        if self.timer == 15:
            return sneed2.Crouch()
        
    def update(self,character,inputs):
        character.hurtboxes = [sneed2.Hurtbox(character,140, 210,character.directionFlip(-10),-10),
                               sneed2.Hurtbox(character,110, 90,character.directionFlip(100),-70)]
        if self.timer == 6:
            
            character.place_hitbox('2A', 15, 0, 2, 100, 00, 100, 100, character, 'low', 1, 150)
            character.place_hitbox('2A', 15, 0, 2, 160, -70, 210, 100, character, 'low', 1, 150)
        self.timer += 1
class attack5A:
    
    def __init__(self, character):
        self.timer = 0
        character.animIndex = 0
    def enter_state(self,character,inputs):
        if self.timer >= 8:
            if character.move == '5A':
           
                return attack5A(character)
        if self.timer == 11:
            return sneed2.Idle()
        
    def update(self,character,inputs):
        character.hurtboxes = [sneed2.Hurtbox(character,140, 390,character.directionFlip(-10),80),
                               sneed2.Hurtbox(character,60, 110,character.directionFlip(70),50),
                               sneed2.Hurtbox(character,80, 110,character.directionFlip(90),10)]
        if self.timer == 5:
           
            character.place_hitbox('5A', 15, 0, 3, 190, 150, 150, 100, character, 'mid', 2, 200)
            character.place_hitbox('5A', 15, 0, 3, 120, 160, 110, 150, character, 'mid', 2, 200)
       

        self.timer += 1
        character.do_friction()
       
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
            character.place_hitbox('jA', 15, 0, 4, 140, 185, 120, 55, character, 'high', 1, 250)
            character.place_hitbox('jA', 15, 0, 4, 140,  120, 90, 90, character, 'high', 1, 250)
            character.place_hitbox('jA', 15, 0, 4, 55,  100, 80, 80, character, 'high', 1, 250)
        character.gravity()
        self.timer += 1

class attack2B:
    
    def __init__(self, character):
        self.timer = 0
        character.animIndex = 0
    def enter_state(self,character,inputs):

        if self.timer == 25:
            return sneed2.Crouch()
        
    def update(self,character,inputs):
        if self.timer == 6:
            character.place_hitbox('3C', 15, 40, 10, 10, 270, 50, 140, character, 'mid', 2, 300, 'L')
            character.place_hitbox('3C', 15, 40, 10, 60, 180, 110, 100, character, 'mid', 2, 400, 'L')
            character.place_hitbox('3C', 15, 40, 10, 120, 90, 110, 190, character, 'mid', 2, 400, 'L')
            character.place_hitbox('3C', 15, 40, 10, 170, 90, 110, 100, character, 'mid', 2, 400, 'L')
            character.place_hitbox('3C', 15, 40, 10, 110, -60, 100, 110, character, 'mid', 2, 400, 'L')

            
        
        character.hurtboxes = [sneed2.Hurtbox(character,100, 140,character.directionFlip(-90),-45),
                               sneed2.Hurtbox(character,110, 240,character.directionFlip(10),5),
                               sneed2.Hurtbox(character,120, 110,character.directionFlip(-10),150),
                               sneed2.Hurtbox(character,50, 150,character.directionFlip(0),270),
                        
                             ]
        self.timer += 1


class attack5B:
    
    def __init__(self, character):
        self.timer = 0
        character.animIndex = 0
    def enter_state(self,character,inputs):
        if self.timer == 19:
            return sneed2.Idle()
        
    def update(self,character,inputs):
        if self.timer == 0:
            
            character.move_forward(15)
        character.hurtboxes = [sneed2.Hurtbox(character,120, 180,character.directionFlip(50),100),
                               sneed2.Hurtbox(character,140, 240,character.directionFlip(-20),5),
                               sneed2.Hurtbox(character,100, 180,character.directionFlip(50),-20),
                               ]
        if self.timer == 8:
            character.place_hitbox('5B', 20, 0, 4, 120, 100, 100, 100, self, 'mid', 2, 480)
            character.place_hitbox('5B', 20, 0, 4, 100, 30, 80, 60, self, 'mid', 2, 480)
        self.timer += 1
        character.do_friction()
        

class attackjB:
    
    def __init__(self, character):
        self.timer = 0
        character.animIndex = 0
    def enter_state(self,character,inputs):
        if character.rect.bottom == sneed2.FLOOR:
            return sneed2.Idle()
        
    def update(self,character,inputs):
        character.hurtboxes = [sneed2.Hurtbox(character,140, 230,character.directionFlip(-10),140), 
                               sneed2.Hurtbox(character,110, 140,character.directionFlip(-100),100),
                               sneed2.Hurtbox(character,110, 50,character.directionFlip(100),50),]
        if self.timer == 6:
            character.place_hitbox('jB', 15, 0, 2, 130, 210, 180, 80, character, 'high', 2, 500)
            character.place_hitbox('jB', 15, 0, 2, 240,  200, 90, 90, character, 'high', 2, 500)
            character.place_hitbox('jB', 15, 0, 2, 90,  130, 170, 70, character, 'high', 2, 500)
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
            character.place_hitbox('2C', 15, 20, 3, 150, -30, 140, 100, character, 'low', 2, 620, 'HK')
                    
            character.place_hitbox('2C', 15, 20, 3, 270,  -40, 140, 90, character, 'low', 2, 620, 'HK')
        self.timer += 1




class attack5C:
    def __init__(self, character):
        self.timer = 0
        character.animIndex = 0
    def enter_state(self,character,inputs):

        if self.timer == 34:
            return sneed2.Idle()
        
    def update(self,character,inputs):
        if self.timer <= 10:
            character.move_forward(15)
        else:
            character.do_friction()
        character.hurtboxes = [sneed2.Hurtbox(character,140, 230,character.directionFlip(-10),0), 
                               sneed2.Hurtbox(character,110, 140,character.directionFlip(-100),-45),
                               sneed2.Hurtbox(character,110, 50,character.directionFlip(100),50),]
        if self.timer == 10:
            character.place_hitbox('5C', 15, 0, 5, 200, 200, 160, 140, character, 'mid', 3, 620)
            character.place_hitbox('5C', 15, 0, 5, 60, 180, 110, 100, character, 'mid', 3, 620)
            character.place_hitbox('5C', 15, 0, 5, 120, 90, 110, 190, character, 'mid', 3, 620)
        self.timer += 1

class attackjC:
    
    def __init__(self, character):
        self.timer = 0
        character.animIndex = 0
    def enter_state(self,character,inputs):
        if self.timer >= 20:
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




normals = (attack2A, attack5A,
           attack2B, attack5B,
           attack2C, attack5C,
           )

aerialnormals = (attackjA,
                 attackjB,
                 attackjC

)

