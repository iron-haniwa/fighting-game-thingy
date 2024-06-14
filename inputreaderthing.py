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



def flatten_list(x):

    flattenedlist = []

    stack = [x]

    while stack:
        current = stack.pop(-1)

        if isinstance(current, (list, dict)):
            stack.extend(current)
        else:
            flattenedlist.append(current)
    flattenedlist.reverse()
    return flattenedlist


class inputReader:
    def __init__(self, controls):
        self.pressTime = 0
        self.inputBuffer = collections.deque([{'None':0}],maxlen=7)
        self.inputsNow = [None]
        self.processedInput = {'None':0}
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

        self.inputsNow = [None]
        self.processedInput = {'None':0}
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
            self.inputsNow.insert(0, 'downright')
        if 'down' in self.inputsNow and 'left' in self.inputsNow:
            self.inputsNow.remove('down')
            self.inputsNow.remove('left')
            self.inputsNow.insert(0, 'downleft')
        if 'right' in self.inputsNow and 'up' in self.inputsNow:
            self.inputsNow.remove('right')
            self.inputsNow.remove('up')
            self.inputsNow.insert(0, 'upright')
        if 'left' in self.inputsNow and 'up' in self.inputsNow:
            self.inputsNow.remove('left')
            self.inputsNow.remove('up')
            self.inputsNow.insert(0, 'upleft')
        

        #print(self.inputsNow)
        #print(list(self.inputBuffer[-1].keys()))
        if self.inputsNow == list(self.inputBuffer[-1].keys()):
            
            for input in self.inputBuffer[-1]:
                self.inputBuffer[-1][input] += 1
                #print(self.inputBuffer[-1])


        else:  
            #print('change')uuuuuuu
            
            
            #print(f'last input: {self.inputBuffer[-1][0]}')
            #print(f'current input: {self.inputsNow}')
            if 'A' in self.inputBuffer[-1] and 'A' not in self.inputsNow:
                self.inputsNow.append('-A')
            #if 'B' in self.inputBuffer[-1][0] and 'B' not in self.inputsNow:
                #print('released B')
            #if 'C' in self.inputBuffer[-1][0] and 'C' not in self.inputsNow:
                #print('released C')
            if 'up' in self.inputBuffer[-1] and not any(x in ['up','upright','upleft'] for x in self.inputsNow):
                self.inputsNow.append('-up')
            

            for input in self.inputsNow:
                #print(input)
                
                if str(input) in self.inputBuffer[-1]:
                    self.processedInput[str(input)] = self.inputBuffer[-1][str(input)] + 1
                else:
                    self.processedInput.update({input:0})
            if len(self.processedInput) > 1:
                del self.processedInput['None']
        
            self.inputBuffer.append(self.processedInput)
        self.currentInput = list(self.inputBuffer[-1].keys())
        #print(self.currentInput)

        #templist = [i[0] for i in list(self.inputBuffer)]
        #self.currentInput = [i for i in templist][-1]
        #print(self.inputBuffer[-1])



class specialMove:

    def commandReader(self, buffer):
        specials = [
            
            {'name': 'Dash',
             "sequences":{"seq1":[['right'],['right']],
                          "seq2":[['right'],[None],['right']]},
             'leniency': 4,
             "isCharge": False,
             'Type':'Special'

            },
            {'name': 'bDash',
             "sequences":{"seq1":[['left'],['left']],
                          "seq2":[['left'],[None],['left']]},
             'leniency': 8,
             "isCharge": False,
             'Type':'Special'

            },
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
            {'name':"Tatsumaki",
            "sequences":{"seq1":[['down'], ['downleft'],['left'],['A']],
                            "seq2":[['down'],['downleft'],['left', 'A']],
                            "seq3":[['down'],['downleft'],['left'],[None],['A']],
                            "seq4":[['down'], ['downleft'],['left'],['A'],['A']],
                            "seq5":[['down'],['left'],['A']],
                            "seq6":[['down'],['downleft'],['left'],['le ft','A']],
                            "seq7":[['down'],['left'],[None],['A']]},
            "leniency":12,
            "isCharge":False
                                            },
            {'name': '5A',
             "sequences":{"seq1":[['A']],
                          "seq2":[['right', 'A']],
                          "seq3":[['left', 'A']],
                          "seq4":[['upright','A']],
                          "seq5":[['upleft', 'A']],
                          "seq6":[['up', 'A']]
                          
                          },
             'leniency': 2,
             "isCharge": False,
             'Type': 'Normal'

            },
            {'name': '2A',
             "sequences":{"seq1":[['down','A']],
                          "seq2":[['downright','A']],
                          "seq3":[['A','downright']]
                          },
             'leniency': 2,
             "isCharge": False

            },
            {'name': '5B',
             "sequences":{"seq1":[['B']],
                          "seq2":[['right','B']],
                          "seq3":[['left', 'B']],
                          "seq4":[['upright','B']],
                          "seq5":[['upleft', 'B']],
                          "seq6":[['up', 'B']]
                          },
             'leniency': 2,
             "isCharge": False

            },
            {'name': '2B',
             "sequences":{"seq1":[['down','B']],
                          "seq2":[['downright','B']],
                          "seq3":[['B','downright']]
                          },
             'leniency': 2,
             "isCharge": False

            },
            {'name': '2C',
             "sequences":{"seq1":[['down','C']],
                          "seq2":[['downright','C']],
                          "seq3":[['C','downright']]
                          },
             'leniency': 2,
             "isCharge": False

            },
            {'name': '5C',
             "sequences":{"seq1":[['C']],
                          "seq2":[['right','C']],
                          "seq3":[['left', 'C']],
                          "seq4":[['upright','C']],
                          "seq5":[['upleft', 'C']],
                          "seq6":[['up', 'C']]
                          },
             'leniency': 2,
             "isCharge": False

            }
            
        ]
        for move in specials:
            for seq in move["sequences"]:
                #print(move['sequences'][seq], 'this is it')
                flat_buffer = [list(i.keys()) for i in list(buffer)[-len(move['sequences'][seq]):]]
                #flat_buffer = [list(i.keys()) for i in list(buffer)[-4:]]
                #print(flat_buffer)
                value_buffer = flatten_list([list(i.values()) for i in list(buffer)[-len(move['sequences'][seq]):]])
                if len(value_buffer) > 1:
                    del value_buffer[0]
                #print([list(i.keys()) for i in list(buffer)[-4:]])
                
                
                
                if flat_buffer == move["sequences"][seq]:
                    #print(move["name"])
                    if move["isCharge"] == True:
                        #print(move['name'])
                        #print(buffer[-len(move['sequences'][seq])][1])
                        if buffer[-len(move['sequences'][seq])][1] > move['chargeTime']:
                            if max([i[-1] for i in list(buffer)[-len(move['sequences'][seq])+1:]]) <= move["leniency"]:

                                return move['name']

                    if max(flatten_list(value_buffer)) <= move["leniency"]:
                        #print(value_buffer)
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

