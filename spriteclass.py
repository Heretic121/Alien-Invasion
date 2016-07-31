import pygame
import random

class Block(pygame.sprite.Sprite):
    """
    This class represents the ball
    It derives from the "Sprite" class in Pygame
    """
    def __init__(self, color, width, height):
        """ Constructor. Pass in the color of the block,
        and its x and y position. """
        # Call the parent class (Sprite) constructor
        super().__init__()
 
        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
 
        # Fetch the rectangle object that has the dimensions of the image
        # image.
        # Update the position of this object by setting the values
        # of rect.x and rect.y
        self.rect = self.image.get_rect()
        self.move_direction = 0
        self.offsetx = 0
        self.offsety = 0
 
    def update(self):
        """ Called each frame. """
        pass

class Player(Block):
    """ The player class derives from Block, but overrides the 'update'
    functionality with new a movement function that will move the block
    with the mouse. """
    def update(self,direction):
        if direction == 1: ## Move left
            if ( self.rect.x + 90 ) < 640:
                self.rect.x += 10
            else:
                self.rect.x = (640 - 81)
        elif direction == 0: ## Move right
            if ( self.rect.x - 10 ) > 0:
                self.rect.x -= 10
            else:
                self.rect.x = 1

class Alien(Block):
    def update(self):
        """ Called each frame. """
        if self.rect.x == ((639 - ((20*(15-self.offsetx))+(10*(15-self.offsetx)))) - 20):
            self.move_direction = 1
        elif self.rect.x == (1 + ((20*self.offsetx)+(10*self.offsetx))):
            self.move_direction = 0
        if self.move_direction == 0:
            self.rect.x += 1
        elif self.move_direction == 1:
            self.rect.x -= 1

class Bullet(pygame.sprite.Sprite):
    def __init__(self,color,width,height,whose):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.whose = whose
        
    def update(self):
        if self.whose == 0:
            self.rect.y -= 5
        elif self.whose == 1:
            self.rect.y += 5

def block_create(colour,pos,size):
    global Block
    block = Block(colour, size[0], size[1])
    block.rect.x = pos[0]
    block.rect.y = pos[1]
    return block
