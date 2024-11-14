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


#This stuff is pretty much just another pygame skeleton, just random stuff I used to get this program up and running standalone, copied from an ancient version of sneed2









# Quick function that takes in a nested list and flattens it, returning a single unnested list

def flatten_list(x):

    flattenedlist = []

    stack = [x]

    # Basically, the last entry of the original list is removed from it and if it is a list, it is readded to the end of the stack to be continously processed until no more nesting remains
    while stack:
        current = stack.pop(-1)

        if isinstance(current, (list, dict)):
            stack.extend(current)
        else:
            flattenedlist.append(current)

    # Since this method flips the order of the list, I then reverse the list to have a new, properly order flat list
    flattenedlist.reverse()
    return flattenedlist


# My magnus opus, an input interpreter that reads inputs whatever you told it corresponded to the inputs in BaseScene's control dictionary, runs it through an interface,
# and saves a short input history to a rolling buffer so that I can read the last few frames of input to determine whether or not a special move has been inputted

class inputReader:
    def __init__(self, controls):
        self.pressTime = 0
        self.inputBuffer = collections.deque([{'None':0}],maxlen=7)
        self.inputsNow = [None]
        self.processedInput = {'None':0}
        self.currentInput = []
        self.controls = controls
        # Sets up a few attributes, such as creating a Deque (A FIFO queue that deletes the oldest entries when it gets too long), and creating the skeletons of lists that will be needed later

    def handleInputs(self, direction, keys, joystick=None, joycontrols=None):
        keys = keys
        # The interface, reads the actual input data, and converts it to inputs that are actually usable by game logic
        if joystick == None:
            self.inputInterface = {'down':keys[self.controls[0]],
                                'up':keys[self.controls[1]],
                                'left':keys[self.controls[2]],
                                'right':keys[self.controls[3]],
                                'A':keys[self.controls[4]],
                                'B':keys[self.controls[5]],
                                'C':keys[self.controls[6]]}
        else:
            self.inputInterface = {'down':joycontrols[1] == self.controls[0],
                                'up':joycontrols[1] == self.controls[1],
                                'left':joycontrols[0] == self.controls[2],
                                'right':joycontrols[0] == self.controls[3],
                                'A':joystick.get_button(self.controls[4]),
                                'B':joystick.get_button(self.controls[5]),
                                'C':joystick.get_button(self.controls[6])}
            #print(self.inputInterface)

        self.inputsNow = [None] # Wipes the inputs now list clear every iteration
        self.processedInput = {'None':0} # Ditto, for processed inputs


        for input in self.inputInterface:
            #If left and right are both held, both inputs are thrown out
            if self.inputInterface['right'] and self.inputInterface['left']:
                    self.inputInterface['right'] = False
                    self.inputInterface['left'] = False
            # Otherwise, the current input is added to a list of what is currently being held, and then removes the None that it defaults to
            if self.inputInterface[input] == True:
                
                if self.inputsNow[0] is None:
                    self.inputsNow.remove(None)
                self.inputsNow.append(input)
        # If the player is facing the other way, directions are mirrored for consistent input
        if direction == 'left':
            for i in range(len(self.inputsNow)):
                if self.inputsNow[i] == 'right':
                    self.inputsNow[i] = 'left'
                elif self.inputsNow[i] == 'left':
                    self.inputsNow[i] = 'right'

        # This code block checks for diagonals, and replaces the corresponding inputs as needed
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
        

        # If the current inputs are identical to the last frame, the rest is skipped and a frame is added to the timer each active input possesses.
        if self.inputsNow == list(self.inputBuffer[-1].keys()):
            
            for input in self.inputBuffer[-1]:
                self.inputBuffer[-1][input] += 1
                


        else:  
            
            # The following few lines check for button *depresses*, and add their unpressing to the input history, this is needed for smooth jumping and Negative Edge
            if 'A' in self.inputBuffer[-1] and 'A' not in self.inputsNow:
                self.inputsNow.append('-A')
            
            if 'up' in self.inputBuffer[-1] and not any(x in ['up','upright','upleft'] for x in self.inputsNow):
                self.inputsNow.append('-up')
            
            #Iterates through inputsNow, and formats it to be added to the buffer
            for input in self.inputsNow:
                
                #If the input was already in the last frame, instead of being added again a frame is added to the timer. This is used for input leniency and making sure you time your presses correctly
                if str(input) in self.inputBuffer[-1]:
                    self.processedInput[str(input)] = self.inputBuffer[-1][str(input)] + 1
                else:
                    self.processedInput.update({input:0})
            if len(self.processedInput) > 1:
                # If literally anything was inputted, the None is eradicated from processedInput
                del self.processedInput['None']
            #Finally, the current input is appended to the buffer as a dict in format 'KeyPressed':'LengthCurrentlyPressed'
            self.inputBuffer.append(self.processedInput)

        # This is just a quick variable that lets the player easily access the most recently pressed keys   
        self.currentInput = list(self.inputBuffer[-1].keys())
        


# This is the class that reads the input history, compares it to it's own internal list of possible moves
class specialMove:

    def commandReader(self, buffer):

        # Each move is given multiple ways to input it, to account for player error and make it easier to input

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
                          "seq3":[['A','downright']],
                          "seq4":[['downleft', 'A']]
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
                          "seq3":[['B','downright']],
                          "seq4":[['downleft', 'B']]
                          },
             'leniency': 2,
             "isCharge": False

            },
            {'name': '2C',
             "sequences":{"seq1":[['down','C']],
                          "seq2":[['downright','C']],
                          "seq3":[['C','downright']],
                          "seq4":[['downleft', 'C']]
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

        # The nightmare code, I do not believe list comprehension is a real thing. There is simply no way...

        # Instead of commenting line by line, what this broadly does is iterate over every sequence in the special move dictionary, 

        # Compares the last (length of sequence) amount of inputs in the buffer, and then if they match and the individual keys have not been

        # pressed for too long, the move is returned. Notably, the length of the first directional is ignored, for a better input experience

        # It's not even that long, but this nightmarish block has gone through an ungodly amount of revisions, and is actually much simply than when
        
        # I stored the inputs as multiple nested lists, and there was some triple list comprehension nonsense going on.

        for move in specials:
            for seq in move["sequences"]:
                
                flat_buffer = [list(i.keys()) for i in list(buffer)[-len(move['sequences'][seq]):]]
                
                value_buffer = flatten_list([list(i.values()) for i in list(buffer)[-len(move['sequences'][seq]):]])
                if len(value_buffer) > 1:
                    del value_buffer[0]
                
                
                
                if flat_buffer == move["sequences"][seq]:
                    
                    if move["isCharge"] == True:
                        
                        if buffer[-len(move['sequences'][seq])][1] > move['chargeTime']:
                            if max([i[-1] for i in list(buffer)[-len(move['sequences'][seq])+1:]]) <= move["leniency"]:

                                return move['name']

                    if max(flatten_list(value_buffer)) <= move["leniency"]:
                        
                        return move['name']
                    
                    
                        

 # The following doesnt actually matter, it is once again dummy code that lets me debug the input reader
 # In it's current state, it currently shows you on screen the moment a special move is return by the function,
 # But in the past it has served a variety of functions, such as helping me understand how my own nested list hell was structured,
 # to displaying the entire input buffer.           
            

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
if __name__ == '__main__': # The debug stuff is only run if I run this file directly, of course
    main()

