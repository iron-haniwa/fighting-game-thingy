from typing import Any
import pygame
import sneed2
import inputreaderthing
vec = pygame.math.Vector2
from abc import ABC, abstractmethod

class Camera:
    def __init__(self, player, FLOOR):
        self.player = player
        self.width, self.height = 1920, 1080
        self.constant = vec(-self.width/2 + self.player.rect.w, -FLOOR + 20)
        
        
        
    def setmethod(self, method):
        self.method = method
        
    def scroll(self):
        self.method.scroll()
        

class CameraMovement:
    def __init__(self, camera, object):
        self.camera = camera
        self.object = object
        
    @abstractmethod    
    def scroll(self):
        pass
    
class Follow(CameraMovement):
    def __init__(self, camera, player):
        CameraMovement.__init__(self,camera, object)
        
    def scroll(self):
        self.camera.offset.float.x += (self.player.rect.x - self.camera.offset.float.x + self.camera.constant.x)
        self.camera.offset.float.y += (self.player.rect.y - self.camera.offset.float.y + self.camera.constant.y)
        
        
class Border(CameraMovement):
    def __init__(self, camera, player):
        CameraMovement.__init__(self,camera, object)
        
    def scroll(self):
        self.camera.offset.float.x += (self.player.rect.x - self.camera.offset.float.x + self.camera.constant.x)
        self.camera.offset.float.y += (self.player.rect.y - self.camera.offset.float.y + self.camera.constant.y)
        self.camera.offset.x = max(self.player.left_border, self.camera.offset.x)
        self.camera.offset.x = min(self.camera.offset.x, self.player.right_border - self.camera.width)
        
class Auto(CameraMovement):
    def __init__(self, camera, player):
        CameraMovement.__init__(self,camera, object)
        
    def scroll(self):
        self.camera.offset.x += 1