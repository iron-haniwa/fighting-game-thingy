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
    selectBackground = pygame.image.load("assets/backgrounds/charselect.png")
    shikibutton = pygame.image.load("assets/button icons/shikibutton.png")
    char2button = pygame.image.load("assets/button icons/char2button.png")
    buttons = [shikibutton,char2button]
    looping = True
    selected = [buttons[0]]
    brighten = 128
    shikibutton.fill((brighten, brighten, brighten), special_flags=pygame.BLEND_RGB_ADD)
    dim = 128
    playerchoosing = 1
    #pygame.mixer.music.load("fighting-game-thingy-main/assets/music/Actor's Anteroom.mp3")
    #pygame.mixer.music.play()
    while looping:
        #check the value of playerchoosing here. If it's 1, display text telling player1 to choose a character.
        #if the value is 2, display the text for player 2.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                looping = False
             
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if selected != buttons[0]:
                        #if you press up and aren't on shikibutton, that means you're on char2. This moves you back to shikibutton.
                        selected = buttons[0]
                        shikibutton.fill((brighten, brighten, brighten), special_flags=pygame.BLEND_RGB_ADD)
                        char2button.fill((dim, dim, dim), special_flags=pygame.BLEND_RGB_SUB)  
                    elif selected != buttons[1]:
                        #if you press up and aren't on char2button, that means you're on shikibutton. This moves you back to char2button.
                        selected = buttons[1]
                        char2button.fill((brighten, brighten, brighten), special_flags=pygame.BLEND_RGB_ADD) 
                        shikibutton.fill((dim, dim, dim), special_flags=pygame.BLEND_RGB_SUB) 
                if event.key == pygame.K_DOWN:
                    if selected != buttons[1]:
                        #if you press down and aren't on char2button, that means you're on shikibutton. This moves you back to char2button.
                        selected = buttons[1]
                        char2button.fill((brighten, brighten, brighten), special_flags=pygame.BLEND_RGB_ADD) 
                        shikibutton.fill((dim, dim, dim), special_flags=pygame.BLEND_RGB_SUB) 
                    elif selected != buttons[0]:
                        #if you press down and aren't on shikibutton, that means you're on char2button. This moves you back to shikibutton.
                        selected = buttons[0]
                        shikibutton.fill((brighten, brighten, brighten), special_flags=pygame.BLEND_RGB_ADD) 
                        char2button.fill((dim, dim, dim), special_flags=pygame.BLEND_RGB_SUB) 
                if event.key == pygame.K_z:
                        if selected == buttons[0]:
                            if playerchoosing == 1:
                                player1char = "Shiki"
                                playerchoosing +=1
                                #adds 1 to the playerchoosing variable and returns to the top so player 2 can choose a character
                            elif playerchoosing == 2:
                                player2char = "Shiki"
                                #implement the code here to run basescene with the player1char and player2char variables so that baseScene can read it      
                        elif selected == buttons[1]:
                            if playerchoosing == 1:
                                player1char = "char2"
                                playerchoosing+=1
                            elif playerchoosing == 2:
                                player2char = "char2"
                                #code here for running basescene like above
        WIN.blit(selectBackground, (0,0))
        WIN.blit(shikibutton, (WIDTH/2 - 130, HEIGHT/2 - 20))
        WIN.blit(char2button, (WIDTH/2 - 130, HEIGHT/2 + 270))
        SCREEN.blit(pygame.transform.scale(WIN, SCREEN.get_rect().size), (0, 0))
        pygame.display.flip()    
                                            

charselect()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
'''
def titleScreen(WIN):
    titleback = pygame.image.load("bullethell/images/BG+UI/title_background.png")
    logo = pygame.image.load("bullethell/images/BG+UI/logo.png")
    logo = pygame.transform.scale(logo, (664/2,776/2))
    newGame = pygame.image.load("bullethell/images/BG+UI/new_game_button.png")
    closeGame = pygame.image.load("bullethell/images/BG+UI/exit_button.png")
    buttons = [newGame,closeGame]
    loopContinues = True
    selected = buttons[0]
    brighten = 128
    newGame.fill((brighten, brighten, brighten), special_flags=pygame.BLEND_RGB_ADD)
    dim = 128
    paulRect = pygame.Rect(WIDTH/2 - 160, HEIGHT/2 - 400, (664/2), (776/2))
    while loopContinues:
        
        #we do a little event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loopContinues = False
                sys.exit()
             
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if selected != buttons[0]:
                        #if you press up and aren't on newGame, that means you're on closeGame. This moves you back to newGame.
                        selected = buttons[0]
                        newGame.fill((brighten, brighten, brighten), special_flags=pygame.BLEND_RGB_ADD)
                        closeGame.fill((dim, dim, dim), special_flags=pygame.BLEND_RGB_SUB)  
                    elif selected != buttons[1]:
                        #if you press up and aren't on closeGame, that means you're on newGame. This moves you back to closeGame.
                        selected = buttons[1]
                        closeGame.fill((brighten, brighten, brighten), special_flags=pygame.BLEND_RGB_ADD) 
                        newGame.fill((dim, dim, dim), special_flags=pygame.BLEND_RGB_SUB) 
                if event.key == pygame.K_DOWN:
                    if selected != buttons[1]:
                        #if you press down and aren't on closeGame, that means you're on newGame. This moves you back to closeGame.
                        selected = buttons[1]
                        closeGame.fill((brighten, brighten, brighten), special_flags=pygame.BLEND_RGB_ADD) 
                        newGame.fill((dim, dim, dim), special_flags=pygame.BLEND_RGB_SUB) 
                    elif selected != buttons[0]:
                        #if you press down and aren't on newGame, that means you're on closeGame. This moves you back to newGame.
                        selected = buttons[0]
                        newGame.fill((brighten, brighten, brighten), special_flags=pygame.BLEND_RGB_ADD) 
                        closeGame.fill((dim, dim, dim), special_flags=pygame.BLEND_RGB_SUB) 
                if event.key == pygame.K_z:
                        if selected == buttons[0]:
                            #play select sfx
                            loopContinues = False
                        elif selected == buttons[1]:
                            #play select sfx
                            time.sleep(1)
                            pygame.quit()
                            sys.exit()
                        #note to self: add a thing that makes the currently selected button light up (maybe by increasing contrast?)
        t = pygame.time.get_ticks()/500
        y = 20 * math.sin(t) + 50
        paulRect.y = y
        
        WIN.blit(titleback, (0,0))
        WIN.blit(newGame, (WIDTH/2 - 130, HEIGHT/2 - 20))
        WIN.blit(closeGame, (WIDTH/2 - 130, HEIGHT/2 + 270))
        WIN.blit(logo, paulRect)
        SCREEN.blit(pygame.transform.scale(WIN, SCREEN.get_rect().size), (0, 0))
        pygame.display.update()     
'''