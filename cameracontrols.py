from typing import Any
import pygame
from abc import ABC
import backgroundClass

'''
The way this was originally supposed to work is that the background would move based on a value inbetween the players' X positions, but I accidentally created a parallax effect
and Caleb thought it looked better than my original setup, so I used 3 different images (ripped from a game that is much older than the other art assets we used, hence the 
weird style clash) to make a "stage". Most of that is in backgroundClass.py and BaseScene.py though, this module is pretty much just for the code that keeps the characters onscreen.

I apologize in advance for my inability to stick to a consistent naming case for variables, I just use whichever case I think "feels" natural-sounding for that particular variable in my head. 
In other words, it's completely arbitrary.
'''
class Camera():
    def __init__(self, bg_width, bg_height):
        self.stage_width, self.stage_height = bg_width, bg_height
        

    def cameraupdate(self,player1,player2,WIN):
        self.p1posx = player1.rect.centerx
        self.p2posx = player2.rect.centerx
        self.window = WIN

        if self.p1posx >= 1280/2:
        #this if statement sets up a "boundary" on the right side of the screen so that
            if self.p1posx >= 1280:
                player1.rect.centerx = 1260
        elif self.p2posx >= 1280:
            player2.rect.centerx = 1260
            #else:
                #this is a remnant from some testing I did that didn't work. 
                #print("movement here")

        if self.p1posx <= 0:
        #this if statement is for setting up a boundary on the left side of the screen, so that players can't go offscreen.
            print("zero")
            player1.rect.centerx = 5
        elif self.p2posx <= 0:
            print("zero")
            player2.rect.centerx = 5