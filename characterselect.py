import pygame, math, random


class Button(pygame.sprite.Sprite):
    #Button class, used in menus and stuff
    
    def __init__(self,xy_pos,message):
        pygame.sprite.Sprite.__init__(self)
        
        self.__message = message
        #self.__font = pygame.font(assets/comicsans.ttf, 30)
        
def charselect():
    WIDTH, HEIGHT = 1280, 720
    SCREEN = pygame.display.set_mode((WIDTH/1,HEIGHT/1))
    WIN = pygame.surface.Surface((WIDTH, HEIGHT))
    FPS = 60
    pygame.image.load("assets/backgrounds/charselect.png")
    
    char1 = Button((120, 100), "Shiki Tohno")
    char2 = Button((80,60), "Character 2") 
    closeGame = Button((50,70), "Close Game")  
    buttons = [char1,char2,closeGame]
    
    
charselect()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
'''
def titleScreen(screen):
    #this function contains all the code for the main menu. Once a new game is started, main() will automatically continue.
    background = #load title screen BG
    newGame = game_sprites.button #load image that will be used as new game button, make sure it has the right X/Y coords
    closeGame = game_sprites.button #load image that will be used as exit button, make sure it has the right X/Y coords
    #list of buttons to make event handling easier
    buttons = [newGame,closeGame]
    #we should add a clock variable that's tied to the internal clock so that enemy spawns can be predetermined based on time, I'll add this later.
    #sfx and bgm that are used on the title screen should be loaded in this function too, make a variable that equals the sound. then just type "[sfx var. name].play()" when it needs to play
    loopContinues = True
    selected = [buttons[0]]
    while loopContinues:
        clock.tick(FPS)
        #Clock's ticking is now tied to the FPS
        
        #we do a little event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loopContinues = False
                return 0
             
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if selected != [start_button]:
                        #select sfx should play here
                        selected = [buttons[(buttons.index(selected[0])-1)]]
                if event.key == pygame.K_DOWN:
                    if selected != [quit_button]:
                        #select sfx should play here
                        selected = [buttons[(buttons.index(selected[0])+1)]]
                if event.key == pygame.K_z:
                        if selected == [newGame]:
                            #stop the music here as well since the 1st stage music will be loaded alongside stage 1
                            #Return start game loop value.
                            return 1
                        elif selected == [closeGame]:
                            #Return exit game value. 
                            return 0                       
                                    
        #this should make the button you're hovering over light up a bit
        for select in selected:
            select.set_select()
     
        # clears the screen so that the level assets can be loaded
        all_sprites.clear(screen, background)
        all_sprites.update()
        all_sprites.draw(screen)     
'''