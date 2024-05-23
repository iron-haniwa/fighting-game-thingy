import pygame, sys, random, colour
from inputreaderthing import inputReader, specialMove
import sneed2
pygame.init()
pygame.font.init()



class testChar(sneed2.Player):
    def __init__(self, xpos, ypos, controls, stfu=True):
        super().__init__(xpos, ypos, controls, stfu)
        self.jumpLimit = 2
        self.image = pygame.image.load('assets\characters\Shiki\shiki_0-0.png')
        self.anims = {'Idle':[], 'fWalk':[], 'bWalk':[],'Crouch':[],'Jump':[], 'backDash':[], 'Dash':[], 'endDash':[]}
        self.speed = 8
        self.dashFactor = 3.5
        for i in range(15):
            self.anims['Idle'].append(pygame.image.load(f'assets\characters\Shiki\shiki_0-{i}.png'))
        for i in range(10):
            self.anims['fWalk'].append(pygame.image.load(f'assets\characters\Shiki\shiki_0-{i + 320}.png'))
        for i in range(12):
            self.anims['bWalk'].append(pygame.image.load(f'assets\characters\Shiki\shiki_0-{i + 332}.png'))
        self.anims['Crouch'].append(pygame.image.load(f'assets\characters\Shiki\shiki_0-{73}.png'))
        self.anims['Crouch'].append(pygame.image.load(f'assets\characters\Shiki\shiki_0-{74}.png'))
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
        self.animIndex = 0



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
            if self.animIndex < 3:
                self.animIndex += 0.25
            else:
                self.animIndex += 0.1

            if self.animIndex >= len(self.anims['Crouch']):
                self.animIndex = 2
            
            self.image = self.anims['Crouch'][int(self.animIndex)]
            self.imagenew = self.image.get_rect(centerx = self.rect.centerx, bottom = self.rect.bottom + 100)
        elif isinstance(self.state, sneed2.Jump) or isinstance(self.state, sneed2.preJump):
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
        
        if self.direction == 'left':
            
            WIN.blit(pygame.transform.flip(self.image, True, False), self.imagenew)
        else:
            WIN.blit(self.image, self.imagenew)