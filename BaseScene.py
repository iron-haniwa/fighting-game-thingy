import pygame, sys, random, healthBarclass, cameracontrols, Sacchin
import characterselect
import sneed2 as p
from backgroundClass import Background
import pygame.freetype
import testchar
pygame.init()
pygame.font.init()

# Imports all the of the necessary modules and initializes pygame



# sets up the font to be used by the KO screen
le_font = pygame.font.SysFont('Futura', 140)


HITSTOP = pygame.USEREVENT + 1
hitstop_event = pygame.event.Event(HITSTOP)

# This code creates a custom pygame event that broadcasts a message to the entire file that lets the "hit pause" effect work later on
pygame.joystick.init()


p1hitboxes = []
p2hitboxes = []

# Sets up the empty lists to store the hitboxes



WIDTH, HEIGHT = 1280, 720
SCREEN = pygame.display.set_mode((WIDTH*1,HEIGHT*1))
WIN = pygame.surface.Surface((WIDTH, HEIGHT))
FPS = 60

# Sets up a few constants and then creates the window to be drawn to.
# SCREEN is the actual window, while WIN is a surface on which the entire game is drawn before being (potentially) resized to the size of the window.
# In our case, the window is the perfect size for our laptops, but if you want to increase the game size you can change the multiplied 1 into something larger






# These are dictionaries that control the controls of both players, by themselves they do nothing but they are passed into the input interface of
# the input later as the accepted controls. If you would like the change the control scheme, the order is as follows:

player_1_controls = [pygame.K_s,   # Down
                    pygame.K_w,     # Up
                    pygame.K_a,     # Left
                    pygame.K_d,     # Right
                    pygame.K_u,     # Light/A
                    pygame.K_i,     # Medium/B
                    pygame.K_o]     # Heavy/C
                                    # And the format is the same for the following dict.
player_2_controls = [-1,    # Down
                    1,     # Up
                    -1,     # Left
                    1,     # Right
                    2,     # Light/A
                    3,     # Medium/B
                    1]     # Heavy/C

# With this format, it is possible to remap the buttons to whatever you want. We did not implement controller support as we set out, but
# it would be very easy to do so with this setup. We did not follow through, because we kind of assumed you do not own an xbox controller







FLOOR = HEIGHT - 50

# Sets a floor constant so sprites know where to land






WHITE = (255, 255, 255)
BLACK = (0,0,0)

#Sets up 2 colours to be used by the text. As it turns out, we only needed black though.


#coin toss for which stage you play on. 
#Stages have no gameplay difference (as is the case with any fighting game that isn't called Super Smash Bros), it's just a different background
stage = random.randint(1,2)
if stage == 1:
    sky = pygame.image.load("./assets/stage/moonlitSky.png").convert_alpha()
    sky = pygame.transform.scale(sky, (1280,720))
    grass = pygame.image.load("./assets/stage/grass.png").convert_alpha()
    grass = pygame.transform.scale(grass, (1280,140))
    grass.set_colorkey((255,0,255))
    grass_rect = grass.get_rect()
    grass_rect.centerx = WIN.get_rect().centerx
    grass_rect.bottom = WIN.get_rect().bottom
if stage == 2:
    earth = pygame.image.load("./assets/stage/earth.png").convert_alpha()
    earth = pygame.transform.scale(earth, (1280,720))
    tile = pygame.image.load("./assets/stage/tilefloor.png").convert_alpha()
    tile = pygame.transform.scale(tile, (1280,140))
    tile_rect = tile.get_rect()
    tile_rect.centerx = WIN.get_rect().centerx
    tile_rect.bottom = WIN.get_rect().bottom

# This is a dictionary that maps strings to objects,
# This is used to allow the user to select their character, as the character select file passes in a string containing character names
# Which get converted to the actual character object
character_dict = {'Shiki':testchar.testChar,
                  'Sacchin':Sacchin.satsukichan}


# This is the draw function, which handles most aspects relating to drawing objects on the screen
# This also handles the draw order, so that objects are displayed correctly.

def draw(player1, player2, healthbars, bg):

    #Fills the screen with an initial black layer, which clears it of all previous drawn data and gives a blank canvas to work on
    WIN.fill(BLACK)
    
    #Handles drawing the various stage objects (Foreground and background) depending on what number was chosen

    if stage == 1:
        WIN.blit(sky, (0,0))  #Draws the sky in Crystal Tokyo

    if stage == 2: 
        WIN.blit(earth, (0,0)) #Draws the space background containing Earth on the Moon / Silver Millenium stage
    bg.draw(WIN, player1, player2) # This function draws the midground and handles the scrolling parallax effect. It already knows which Sailor Moon stage you are on

    if stage == 1:
        WIN.blit(grass, grass_rect) #Draws the grass foreground on which the players stand

    if stage == 2:
        WIN.blit(tile, tile_rect) #Draws the tile floor of the Silver Millenium


    # for hurtbox in player1.hurtboxes:
    #     hurtbox.draw(WIN)
    # for hurtbox in player2.hurtboxes:             #Somewhat important, this is debug code which draws the hurtboxes (as green boxes) which are points which can be damaged on a player
    #     hurtbox.draw(WIN)


    player1.draw(WIN) # Runs the player 1 draw function

    # for attack in player1.hitboxes: 
    #     for hitbox in player1.hitboxes[attack]:
    #         hitbox.draw(WIN)
    # for attack in player2.hitboxes:
    #     for hitbox in player2.hitboxes[attack]:      #Same as the last one, but this one draws in the hitboxes, so you can see what parts of the attack are damaging
    #         hitbox.draw(WIN)
    
    
    player2.draw(WIN)   # draws the 2nd player
    healthbars.draw(WIN, player1.current_health, player2.current_health)  # Draws the healthbars, reading the players health attributes.

 

    # If either player is dead, the K.O. text is displayed on center screen
    if not player1.alive or not player2.alive:
        
        text_surface3 = le_font.render('K.O.', False, WHITE)
       

        WIN.blit(text_surface3, ((WIN.get_rect().centerx) - (text_surface3.get_rect().w/2), (WIN.get_rect().centery) - (text_surface3.get_rect().h/2)))

    # Blits the entire WIN surface to the actual screen
    SCREEN.blit(pygame.transform.scale(WIN, SCREEN.get_rect().size), (0, 0))
    pygame.display.update() # Finally, the entire screen is updated, and is displayed to the user

def collisionHandling(player1, player2):
  

    # This is the function that handles collisions between hurtbox and hitbox


    for attack in player2.hitboxes: # Loops through player 2's hitboxes dictionary, going active attack by active attack
        for hitbox in player2.hitboxes[attack]: # Goes through every hitbox in the dictionary
            for hurtbox in player1.hurtboxes: # Proceeds to check if any of the other player's hurtboxes intersect a hitbox
                if hurtbox.rect.colliderect(hitbox.rect) and hitbox.hasHit == False: # Also checks if the hitbox has already collided with a hurtbox
                    hitstop = player1.get_hit(hitbox) # Runs the damage dealing routine on the other player, and simulatenously receives the hitstop length
                    for hitbox in player2.hitboxes[attack]: # If the attack hit, every other hitbox that makes up the attack is also set to haven hit, so no double collisions occur
                        hitbox.hasHit = True 
                    pygame.event.post(hitstop_event) # Posts the hitstop event
                    if hitstop == None: # So that 6the game does not crash, a zero is returned instead of None is there is no hitstop
                        return 0
                    return hitstop # Hitstop is returned

    for attack in player1.hitboxes: # not commenting this again, its the same
    
        for hitbox in player1.hitboxes[attack]:

            for hurtbox in player2.hurtboxes:
                if hurtbox.rect.colliderect(hitbox.rect) and hitbox.hasHit == False:
                    hitstop = player2.get_hit(hitbox)
                    for hitbox in player1.hitboxes[attack]:
                        hitbox.hasHit = True
                    pygame.event.post(hitstop_event)
                    if hitstop == None:
                        return 0
                    return hitstop               
        
        



def main(player1char, player2char): # Main loop, this is where the magic happens
    hitstop = False
    clock = pygame.time.Clock()
    hitstopTimer = 0
    hitstop_len = 0
    #Sets up a few variables with no values so that they can be used later, also sets up a clock which is required for the game to function properly
    #character positions are given an offset so that they spawn on opposite sides of the center
    #Characters are also created by taking in the passed character string, converting them to the appropriate object, and giving them the appropriate variables
    player1 = character_dict[player1char](WIN.get_rect().centerx-400,FLOOR, player_1_controls)
    player2 = character_dict[player2char](WIN.get_rect().centerx+400,FLOOR, player_2_controls)
    # Create the midground based on the stage roulette
    if stage == 1:
        bg = Background('assets\stage/tower.png', WIDTH, HEIGHT, WIN)
    if stage == 2:
        bg = Background('assets\stage\palace.png', WIDTH, HEIGHT, WIN)
    camera = cameracontrols.Camera(bg.bg_rect.w, bg.bg_rect.h) # Sets up the camera
    player1.rect.right = WIN.get_rect().centerx-400 # Repositions player 1 because rects are drawn from the left side, so this is just easier lol


    healthbars = healthBarclass.healthBar(player1.maximum_health, player2.maximum_health) # Creates the healthbars


    #RNG to decide which song plays during the fight
    battlesong = random.randint(1,7)
    if battlesong == 1:
        pygame.mixer.music.load("assets/music/Beat.mp3")  
        pygame.mixer.music.play(loops=-1)
        pygame.mixer.music.set_volume(0.5)
    elif battlesong == 2:
        pygame.mixer.music.load("assets/music/Mystic Eyes Awakening.mp3")  
        pygame.mixer.music.play(loops=-1)
        pygame.mixer.music.set_volume(0.5)
    elif battlesong == 3:
        pygame.mixer.music.load("assets/music/Light and Darkness.mp3")  
        pygame.mixer.music.play(loops=-1)
        pygame.mixer.music.set_volume(0.5)
    elif battlesong == 4:
        pygame.mixer.music.load("assets/music/Crimson Chapel.mp3")  
        pygame.mixer.music.play(loops=-1)
        pygame.mixer.music.set_volume(0.5)
    elif battlesong == 5:
        pygame.mixer.music.load("assets/music/Burly Heart.mp3")  
        pygame.mixer.music.play(loops=-1)
        pygame.mixer.music.set_volume(0.5)
    elif battlesong == 6:
        pygame.mixer.music.load("assets/music/Holy Orders.mp3")  
        pygame.mixer.music.play(loops=-1)
        pygame.mixer.music.set_volume(0.5)
    elif battlesong == 7:
        pygame.mixer.music.load("assets/music/Yu's Theme.mp3")  
        pygame.mixer.music.play(loops=-1)
        pygame.mixer.music.set_volume(0.5)

    endTimer = 0
    while True:      
        # Generic Pygame loop stuff, closes the game when you try to close it, also continously reads keyboard input and events
        keys = pygame.key.get_pressed()
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                break
            if event.type == HITSTOP: # If hitstop event is broadcasted, the hitstop variable is set to true and the game knows to pause logic
                hitstop = True

        # The hitstop system, if a hit occurs and there needs to be a dramatic pause, this freezes all game logic relating to the players
        if hitstop == False:
            
            # Main logic loop for the players is called, which handles and orders all actions they can take
            player1.loop(player2, keys, WIN) 
            player2.loop(player1, keys, WIN)
            #Calls collision handling, and gets the length of the hitstop if any
            hitstop_len = collisionHandling(player1, player2)
            
            # Cleanup duty, expired hitboxes are removed from existence

            for attack in list(player1.hitboxes.keys()):
                for hitbox in player1.hitboxes[attack]:
                    if hitbox.time >= hitbox.duration:
                        for hitbox in player1.hitboxes[attack]:
                            player1.hitboxes[attack].remove(hitbox)
            
            for attack in list(player2.hitboxes.keys()):
                for hitbox in player2.hitboxes[attack]:
                    if hitbox.time >= hitbox.duration:
                        for hitbox in player2.hitboxes[attack]:
                            player2.hitboxes[attack].remove(hitbox)

            # When the hitbox erasure is complete, it removes the empty attack keys from the dictionary

            for attack in list(player1.hitboxes.keys()):
                if any(player1.hitboxes[attack]) == False:
                    del player1.hitboxes[attack]
            for attack in list(player2.hitboxes.keys()):
                if any(player2.hitboxes[attack]) == False:
                    del player2.hitboxes[attack]
            
        else:
            
            #Timer system for the hitstop, the hitstop will continue until the counter (which counters down every frame) reaches zero from when it started, in which case
            #the hitstop variable is once again set to false

            if hitstopTimer < hitstop_len:
                hitstopTimer += 1
            else:
                hitstopTimer = 0
                hitstop = False
        # starts a timer to end the game if either player dies
        if not player1.alive or not player2.alive:
            endTimer += 1

        #Once the timer reaches the limit (400 frames), the game boots you back to the character select
        if endTimer >=200:
            characterselect.charselect()
        
        #Calls the draw function
        draw(player1,player2,healthbars,bg)
        #this calls the cameraupdate function to keep the boundaries
        camera.cameraupdate(player1, player2, WIN)
        

        #print(controls)

        # Ticks the clock, this forces the game to run 60fps, which is important as the game's internal logic is tied to framerate
        clock.tick(FPS)

if __name__ == '__main__':  # Incase this file is ran standalone, it calls the main function defaulting to Shiki and Akuma  
    main('Shiki', 'Sacchin')