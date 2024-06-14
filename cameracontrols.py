from typing import Any
import pygame
from abc import ABC
import backgroundClass

'''
width/height of the BG and the stage are 2 different things. Stage refers to the space the player(s) can move around in, which extends beyond the 
boundary of the screen. The idea is that the background image (BG) will move with the player(s) to give the illusion of moving further. 
When the player reaches the a certain point (likely the center of the stage), the BG stops moving, indicating that the side of the screen (on one side) is 
the boundary (which cannot be moved past)

I apologize in advance for my inability to stick to a consistent naming case for variables, I just use whichever case I think "feels" natural-sounding in my head. 
In other words, it's completely arbitrary
'''
class Camera():
    def __init__(self, bg_width, bg_height):
        self.stage_width, self.stage_height = bg_width, bg_height
        

    def cameraupdate(self,player1,player2,WIN):
        self.p1posx = player1.rect.centerx
        self.p2posx = player2.rect.centerx
        self.p1posy = player1.rect.bottom 
        self.p2posy = player2.rect.bottom
        
        self.window = WIN
        #this if statement tests the player's position on the screen. At halfway, the background will start moving to simulate the movement of the "camera".
        if self.p1posx >= 1280/2:
            #the background shouldn't move if the player(s) isn't moving, hence this if statement. Could've been better implemented but I have genuinely 0 clue what I am doing
            if player1.xvel == 0:
                pass
            if self.p1posx >= 1280:
                player1.rect.centerx = 1260
        if self.p2posx >= 1280/2:
            if player2.xvel == 0:
                pass
            elif self.p2posx >= 1280:
                player2.rect.centerx = 1260
            #else:
                #this is a remnant from some testing I did that didn't work. 
                #print("movement here")
            
        
        if self.p1posx <= 0:
            #this if statement is for setting up a boundary on the screen, so that players can't go offscreen.
            print("zero")
            player1.rect.centerx = 5
            
        if self.p2posx <= 0:
            print("zero")
            player2.rect.centerx = 5
'''
to do:
- set up height boundary
- change the x-boundary code and make the entire BG a rectangle so that characters simply can't move outside it, removing the need for the awkward "manually move them back on screen" code
'''