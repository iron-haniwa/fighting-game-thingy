import pygame, characterselect, os

def titlescreen():
    WIDTH, HEIGHT = 1280, 720
    SCREEN = pygame.display.set_mode((WIDTH/1,HEIGHT/1))
    WIN = pygame.surface.Surface((WIDTH, HEIGHT))
    FPS = 60
    titleBackground = pygame.image.load("assets/titlescreen/titletest.png")
    startbutton = pygame.image.load("assets/titlescreen/startbutton.png")
    exitbutton = pygame.image.load("assets/titlescreen/exitbutton.png")
    buttons = [startbutton, exitbutton]
    looping = True
    brighten = 128
    dim = 128
    selected = buttons[0]
    #defaults position to startgame
    exitbutton.fill((dim, dim, dim), special_flags=pygame.BLEND_RGB_SUB)
    pygame.mixer.init()
    #initializes the mixer to use music
    pygame.mixer.music.load("assets/music/This Illusion.mp3")
    pygame.mixer.music.play()
    while looping:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                looping = False
             
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    #the brighten and dim lines are to give the effect of "highlighting" the option you are currently targeting.
                    if selected != buttons[0]:
                        #if you press left and you aren't currently on exitbutton, then that means you're trying to reach the startbutton. So this moves you there.
                        selected = buttons[0]
                        startbutton.fill((brighten, brighten, brighten), special_flags=pygame.BLEND_RGB_ADD)
                        exitbutton.fill((dim, dim, dim), special_flags=pygame.BLEND_RGB_SUB)  
                    elif selected != buttons[1]:
                        #if you press left and you aren't currently on startbutton, then that means you're trying to reach the exitbutton. So this moves you there.
                        selected = buttons[1]
                        exitbutton.fill((brighten, brighten, brighten), special_flags=pygame.BLEND_RGB_ADD) 
                        startbutton.fill((dim, dim, dim), special_flags=pygame.BLEND_RGB_SUB) 
                if event.key == pygame.K_RIGHT:
                    #if you press right and you aren't currently on exitbutton, then that means you're trying to reach the exitbutton. So this moves you there.
                    if selected != buttons[1]:
                        selected = buttons[1]
                        exitbutton.fill((brighten, brighten, brighten), special_flags=pygame.BLEND_RGB_ADD) 
                        startbutton.fill((dim, dim, dim), special_flags=pygame.BLEND_RGB_SUB) 
                    elif selected != buttons[0]:
                        #if you press right and you aren't currently on startbutton, then that means you're trying to reach the startbutton. So this moves you there.
                        selected = buttons[0]
                        startbutton.fill((brighten, brighten, brighten), special_flags=pygame.BLEND_RGB_ADD) 
                        exitbutton.fill((dim, dim, dim), special_flags=pygame.BLEND_RGB_SUB) 
                if event.key == pygame.K_z:
                        #this handles confirmation. If you're on the startbutton, it calls characterselect.py, and if you're on the exitbutton it closes the game
                        if selected == buttons[0]:
                            characterselect.charselect()   
                        elif selected == buttons[1]:
                            os.abort()
        WIN.blit(titleBackground, (0,0))
        WIN.blit(startbutton, (WIDTH/2 - 300, HEIGHT/2 + 90))
        WIN.blit(exitbutton, (WIDTH/2 + 100, HEIGHT/2 + 90))
        SCREEN.blit(pygame.transform.scale(WIN, SCREEN.get_rect().size), (0, 0))
        pygame.display.flip() 
                                            
titlescreen()