import pygame, sys, random, colour, collections
import pygame.freetype
pygame.init()
pygame.font.init()

le_font = pygame.freetype.SysFont('Arial', 52)

WIDTH, HEIGHT = 1920, 1080
SCREEN = pygame.display.set_mode((WIDTH/2, HEIGHT/2))
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
GRAVITY = 2
JUMP = 40
keys = pygame.key.get_pressed()

inputBuffer = collections.deque([[None],[None, None]],maxlen=7)

pressTime = 0

bg_image = pygame.transform.scale(pygame.image.load("wafflehousenight.webp").convert_alpha(), (WIDTH*2,HEIGHT*2))
bg_rect = bg_image.get_rect()
bg_rect.centerx = WIN.get_rect().centerx
bg_rect.bottom = WIN.get_rect().bottom

class inputReader:
    def __init__(self, controls):
        self.pressTime = 0
        self.inputBuffer = collections.deque([[1],[[None], None]],maxlen=7)
        self.inputsNow = [None]
        self.processedInput = [[None], [None]]
        self.currentInput = []
        self.controls = controls


    def handleInputs(self, direction, keys):
        keys = keys

        self.inputInterface = {'down':keys[self.controls[0]],
                               'up':keys[self.controls[1]],
                               'left':keys[self.controls[2]],
                               'right':keys[self.controls[3]],
                               'A':keys[self.controls[4]],
                               'B':keys[self.controls[5]],
                               'C':keys[self.controls[6]]}

        self.pressTime += 1
        self.inputsNow = [None]
        self.processedInput = [None, None]
        for input in self.inputInterface:
            if self.inputInterface['right'] and self.inputInterface['left']:
                    self.inputInterface['right'] = False
                    self.inputInterface['left'] = False

            if self.inputInterface[input] == True:
                
                if self.inputsNow[0] is None:
                    self.inputsNow.remove(None)
                self.inputsNow.append(input)

        if direction == 'left':
            for i in range(len(self.inputsNow)):
                if self.inputsNow[i] == 'right':
                    self.inputsNow[i] = 'left'
                elif self.inputsNow[i] == 'left':
                    self.inputsNow[i] = 'right'


        if 'down' in self.inputsNow and 'right' in self.inputsNow:
            self.inputsNow.remove('down')
            self.inputsNow.remove('right')
            self.inputsNow.append('downright')
        if self.inputsNow == ['down','left'] or self.inputsNow == ['left','down']:
            self.inputsNow.remove('down')
            self.inputsNow.remove('left')
            self.inputsNow.append('downleft')
        if self.inputsNow == self.inputBuffer[-1][0]:
            pass
        else:
            
            #print('change')uuuuuuu
            
            
            #print(f'last input: {self.inputBuffer[-1][0]}')
            #print(f'current input: {self.inputsNow}')
            if 'A' in self.inputBuffer[-1][0] and 'A' not in self.inputsNow:
                self.inputsNow.append('-A')
            #if 'B' in self.inputBuffer[-1][0] and 'B' not in self.inputsNow:
                #print('released B')
            #if 'C' in self.inputBuffer[-1][0] and 'C' not in self.inputsNow:
                #print('released C')
            if 'up' in self.inputBuffer[-1][0] and 'up' not in self.inputsNow:
                self.inputsNow.append('-up')
            self.processedInput[0] = self.inputsNow
            self.inputBuffer.append(self.processedInput)
            self.pressTime = 1
        self.inputBuffer[-1][1] = self.pressTime
        templist = [i[0] for i in list(self.inputBuffer)]
        self.currentInput = [i for i in templist][-1]
        #print(self.inputBuffer[-1])



class specialMove:

    def commandReader(self, buffer):
        specials = [
            
            {'name': 'Dash',
             "sequences":{"seq1":[['right'],['right']],
                          "seq2":[['right'],[None],['right']]},
             'leniency': 8,
             "isCharge": False

            },
            {'name': 'bDash',
             "sequences":{"seq1":[['left'],['left']],
                          "seq2":[['left'],[None],['left']]},
             'leniency': 8,
             "isCharge": False

            },
            {'name': '5A',
             "sequences":{"seq1":[['A']],
                          "seq2":[['right','A']]
                          },
             'leniency': 2,
             "isCharge": False

            },
            {'name': '2A',
             "sequences":{"seq1":[['down','A']],
                          "seq2":[['downright','A']],
                          "seq3":[['A','downright']]
                          },
             'leniency': 2,
             "isCharge": False

            }
        ]
        for move in specials:
            for seq in move["sequences"]:
                if [i[0] for i in list(buffer)[-len(move['sequences'][seq]):]] == move["sequences"][seq]:
                    #print(move["name"])
                    if move["isCharge"] == True:
                        #print(move['name'])
                        #print(buffer[-len(move['sequences'][seq])][1])
                        if buffer[-len(move['sequences'][seq])][1] > move['chargeTime']:
                            if max([i[-1] for i in list(buffer)[-len(move['sequences'][seq])+1:]]) <= move["leniency"]:

                                return move['name']

                    if max([i[-1] for i in list(buffer)[-len(move['sequences'][seq]):]]) <= move["leniency"]:
                        #print(move["name"])
                        return move['name']
                        

            
            

player_1_controls = [pygame.K_s,
                    pygame.K_w,
                    pygame.K_a,
                    pygame.K_d,
                    pygame.K_u,
                    pygame.K_i,
                    pygame.K_o]



def main():
    clock = pygame.time.Clock()
    buffer1 = inputReader(player_1_controls)
    movereader = specialMove()
    while True:
        WIN.fill(WHITE)
        keys = pygame.key.get_pressed()
        buffer1.handleInputs('right', keys)
        global events
        events = pygame.event.get()         
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                break
        text_str = str(movereader.commandReader(buffer1.inputBuffer))
        text_surface = le_font.get_rect(text_str)
        text_surface.center = WIN.get_rect().center
        le_font.render_to(WIN, text_surface.topleft, text_str, (100, 200, 255))
        SCREEN.blit(pygame.transform.scale(WIN, SCREEN.get_rect().size), (0, 0))
        clock.tick(FPS)
        pygame.display.flip()
if __name__ == '__main__':
    main()

