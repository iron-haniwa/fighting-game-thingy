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


class inputReader:
    def __init__(self):
        self.pressTime = 0
        self.inputBuffer = collections.deque([[1],[[None], None]],maxlen=7)
        self.inputsNow = [None]
        self.processedInput = [[None], [None]]
        self.currentInput = []


    def handleInputs(self, direction):
        keys = pygame.key.get_pressed()

        self.inputInterface = {'down':keys[pygame.K_s],
                               'up':keys[pygame.K_w],
                               'left':keys[pygame.K_a],
                               'right':keys[pygame.K_d],
                               'A':keys[pygame.K_u],
                               'B':keys[pygame.K_i],
                               'C':keys[pygame.K_o]}

        self.pressTime += 1
        self.inputsNow = [None]
        self.processedInput = [None, None]
        for input in self.inputInterface:
            if self.inputInterface[input] == True:
                if self.inputInterface['right'] and self.inputInterface['left']:
                    continue
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



def specialMovetest(buffer):
    specials = [
        {'name':"Hadouken",
         "sequences":{"seq1":[['down'], ['downright'],['right'],['A']],
                        "seq2":[['down'],['downright'],['right', 'A']],
                        "seq3":[['down'],['downright'],['right'],[None],['A']],
                        "seq4":[['down'], ['downright'],['right'],['A'],['A']],
                        "seq5":[['down'],['right'],['A']],
                        "seq6":[['down'],['downright'],['right'],['right','A']],
                        "seq7":[['down'],['right'],[None],['A']]},
        "leniency":12,
        "isCharge":False
                                          },
        {'name':"Hammerfall",
         'sequences':{"seq1":[['left'],['right'],['A']],
                      "seq2":[['left'],['right','A']],
                      "seq3":[['left'],['right'],[None],['A']],
                      "seq4":[['left'],[None],['right'],['right','A']],
                      "seq5":[['left'],['right'],['right','A']],
                      "seq6":[['left'],[None],['right','A']]
                      },
        "leniency":6,
        "isCharge":True,
        "chargeTime":30}
    ]
    for move in specials:
        for seq in move["sequences"]:
            if [i[0] for i in list(buffer)[-len(move['sequences'][seq]):]] == move["sequences"][seq]:
                print(move["name"])
                if move["isCharge"] == True:
                    #print(move['name'])
                    #print(buffer[-len(move['sequences'][seq])][1])
                    if buffer[-len(move['sequences'][seq])][1] > move['chargeTime']:
                        if max([i[-1] for i in list(buffer)[-len(move['sequences'][seq])+1:]]) <= move["leniency"]:

                            return move['name']

                if max([i[-1] for i in list(buffer)[-len(move['sequences'][seq]):]]) <= move["leniency"]:

                    return move['name']

            
            





def main():
    clock = pygame.time.Clock()
    buffer1 = inputReader()
    while True:
        WIN.fill(WHITE)
        buffer1.handleInputs('left')
        global keys
        keys = pygame.key.get_pressed()
        global events
        events = pygame.event.get()         
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                break
        text_str = str(specialMovetest(buffer1.inputBuffer))
        text_surface = le_font.get_rect(text_str)
        text_surface.center = WIN.get_rect().center
        le_font.render_to(WIN, text_surface.topleft, text_str, (100, 200, 255))
        SCREEN.blit(pygame.transform.scale(WIN, SCREEN.get_rect().size), (0, 0))
        clock.tick(FPS)
        pygame.display.flip()
if __name__ == '__main__':
    main()

