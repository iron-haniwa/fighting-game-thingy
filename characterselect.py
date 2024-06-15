import pygame, BaseScene
        
def charselect():
    WIDTH, HEIGHT = 1280, 720
    SCREEN = pygame.display.set_mode((WIDTH/1,HEIGHT/1))
    WIN = pygame.surface.Surface((WIDTH, HEIGHT))
    FPS = 60
    selectBackground = pygame.image.load("assets/backgrounds/charselect.png")
    shikibutton = pygame.image.load("assets/button icons/shikibutton.png")
    char2button = pygame.image.load("assets/button icons/satsukibutton.png")
    player1text = pygame.image.load("assets/button icons/player1select.png")
    player2text = pygame.image.load("assets/button icons/player2select.png")
    buttons = [shikibutton,char2button]
    looping = True
    selected = buttons[0]
    brighten = 128
    dim = 128
    char2button.fill((dim, dim, dim), special_flags=pygame.BLEND_RGB_SUB)
    playerchoosing = 1
    pygame.mixer.music.load("assets/music/Actor's Anteroom.mp3")
    pygame.mixer.music.play()
    while looping:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                looping = False
             
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    #the brighten and dim lines are to give the effect of "highlighting" the option you are currently targeting.
                    #the character select code is identical to the titlescreen code so I won't bother explaining it again
                    if selected != buttons[0]:
                        selected = buttons[0]
                        shikibutton.fill((brighten, brighten, brighten), special_flags=pygame.BLEND_RGB_ADD)
                        char2button.fill((dim, dim, dim), special_flags=pygame.BLEND_RGB_SUB)  
                    elif selected != buttons[1]:
                        selected = buttons[1]
                        char2button.fill((brighten, brighten, brighten), special_flags=pygame.BLEND_RGB_ADD) 
                        shikibutton.fill((dim, dim, dim), special_flags=pygame.BLEND_RGB_SUB) 
                if event.key == pygame.K_RIGHT:
                    if selected != buttons[1]:
                        selected = buttons[1]
                        char2button.fill((brighten, brighten, brighten), special_flags=pygame.BLEND_RGB_ADD) 
                        shikibutton.fill((dim, dim, dim), special_flags=pygame.BLEND_RGB_SUB) 
                    elif selected != buttons[0]:
                        selected = buttons[0]
                        shikibutton.fill((brighten, brighten, brighten), special_flags=pygame.BLEND_RGB_ADD) 
                        char2button.fill((dim, dim, dim), special_flags=pygame.BLEND_RGB_SUB) 
                if event.key == pygame.K_z:
                        if selected == buttons[0]:
                            if playerchoosing == 1:
                                player1char = "Shiki"
                                #the player1char/player2char variables are later called in BaseScene and compared against a dictionary in order to assign the right character class to the right player
                                playerchoosing +=1
                                #adds 1 to the playerchoosing variable and returns to the top so player 2 can choose a character
                            elif playerchoosing == 2:
                                player2char = "Shiki"
                                BaseScene.main(player1char, player2char)     
                        elif selected == buttons[1]:
                            if playerchoosing == 1:
                                player1char = "Satsuki"
                                playerchoosing+=1
                            elif playerchoosing == 2:
                                player2char = "Satsuki"
                                BaseScene.main(player1char, player2char)

        WIN.blit(selectBackground, (0,0))
        WIN.blit(shikibutton, (WIDTH/2 - 450, HEIGHT/2 - 63))
        WIN.blit(char2button, (WIDTH/2 +130, HEIGHT/2 - 50))
        if playerchoosing == 1:
            WIN.blit(player1text, (175,0))
        elif playerchoosing == 2:
            #it would've been easier to just print text to the screen rather than make it an image, but it doesn't really matter and I like how this turned out anyway
            WIN.blit(player2text, (175,0))
        SCREEN.blit(pygame.transform.scale(WIN, SCREEN.get_rect().size), (0, 0))
        pygame.display.flip()    

if __name__ == "main":
    charselect()