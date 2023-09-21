import pygame
from sys import exit
import math
import Chess as c

screen = None

#
allGameObjects = [] # An list of layers, which in turn is a list of all objects in that list
    
# Renderer classes are used in order to store more information such as color, thickness etc.
class RectRenderer: 
    def __init__(self,rect,color,borderThickness):
        self.rect = rect
        self.color = color
        self.borderThickness = borderThickness
    
    # For retrieving information
    def get_size(self):
        return (self.rect.width, self.rect.height)
    
    def get_pos(self):
        return (self.rect.x, self.rect.y)

    # For using the renderer in some way
    def draw(self):
        pygame.draw.rect(screen,self.color,self.rect,0,self.borderThickness)

    # For modifying the renderer
    def move(self, x, y):
        self.rect.move(x, y)

    def setPos(self, pos):
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def setSize(self, size):
        x, y = size
        self.rect.width = x
        self.rect.height = y


class ImageRenderer(RectRenderer):
    def __init__(self,rect, image_path, image = None):
        self.rect = rect
        self.image_path = image_path
        if image is None:
            image = get_image(image_path)
        self.image = pygame.transform.smoothscale(image,(rect.width, rect.height))

    def draw(self):
        c.SCREEN.blit(self.image,self.rect)

    def setSize(self, size):
        #x, y = size
        self.rect.width = size[0]
        self.rect.height = size[1]

        image = get_image(self.image_path)
        self.image = pygame.transform.smoothscale(image,(self.rect.width, self.rect.height))


class GameObject:
    def __init__(self,renderer,collider,tag=None,layer=None,data=None):
        self.renderer = renderer
        self.collider = collider
        self.tag = tag
        if layer is None:
            layer = 0
        self.layer = layer
        self.data = data
        # Layer reservations
        # 0 = tiles
        # 1 = highlights 
        # 2 = pieces
        # >3 can be used for anything
        # Adds missing layers to "allGameObjects"
        if layer >= len(allGameObjects):
            missingLayers = (layer + 1) - len(allGameObjects)
            for i in range(missingLayers):
                allGameObjects.append([])

        # Adds GameObject to layer
        allGameObjects[layer].append(self)

    # Getting functions
    def get_center(self):
        width, height = self.renderer.get_size()
        x, y = self.renderer.get_pos()
        centered_x = x + (width / 2)
        centered_y = y + (height / 2)
        return centered_x, centered_y

    # Modifying Functions
    def move(self, x, y):
        self.collider.move_ip(x, y)
        self.renderer.move(x, y)

    def setPos_center(self, pos):
        x, y = pos
        width, height = self.renderer.get_size()
        centered_x = x - (width / 2)
        centered_y = y - (height / 2)
        self.renderer.setPos((centered_x, centered_y))
        if self.collider is not None:
            self.collider.x = centered_x
            self.collider.y = centered_y

    def setPos(self, pos):
        x, y = pos 
        self.renderer.setPos(pos)
        if self.collider is not None:
            self.collider.x = x
            self.collider.y = y

    def setSize(self, size):
        self.renderer.setSize(size)

    def destroy(self):
        allGameObjects[self.layer].remove(self)

    def move_layer(self,layer): # THIS IS BUGGY FOR SOME REASON
        allGameObjects[self.layer].remove(self)

        if layer >= len(allGameObjects):
            missingLayers = (layer + 1) - len(allGameObjects)
            for i in range(missingLayers):
                allGameObjects.append([])

        allGameObjects[layer].append(self)
#   

# Rendering Functions

def draw_objects():
    for layer in allGameObjects:
        for obj in layer:
            obj.renderer.draw()
            
def check_collision(mousePos, targetLayer = -1):
    if (targetLayer == -1): # -1 means to ignore this variable
        for layer in allGameObjects:
            for obj in layer:
                if obj.collider is not None and obj.collider.collidepoint(mousePos):
                    return obj
    else:
        for obj in allGameObjects[targetLayer]:
            if obj.collider is not None and obj.collider.collidepoint(mousePos):
                    return obj

# Graphical Functions

def get_image(imagePath):
    return pygame.image.load(imagePath).convert_alpha()