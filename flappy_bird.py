import pygame
import random
import os
import time
import neat

# FPS = 32
# CAPITAL VARIABLES = CONSTATNS IN GENERAL CONVENTIONS
WIN_WIDTH = 600
WIN_HEIGHT = 800

bird_images = [pygame.transform.scale2x(pygame.image.load(os.path.join("images" , "bird1.png"))) , pygame.transform.scale2x(pygame.image.load(os.path.join("images" , "bird2.png"))) , pygame.transform.scale2x(pygame.image.load(os.path.join("images" , "bird3.png"))) ]
#image of bird
#scale2x makes image 2x bigger
#.convert_alpha() helps in faster rendering of image to provide real game experience

pipe_images = pygame.transform.scale2x(pygame.image.load(os.path.join("images" , "pipe.png")).convert_alpha())
#image of pipe

base_images = pygame.transform.scale2x(pygame.image.load(os.path.join("images" , "base.png")).convert_alpha())
#image of base(bottom/floor)

bg_images = pygame.transform.scale2x(pygame.image.load(os.path.join("images" , "bg.png")).convert_alpha())
#image of back ground

class Bird:
    IMGS = bird_images
    MAX_ROTATION = 25    # How much the bird will rotate while going up and down
    ROTATION_VELOCITY = 20    # Velocity(speed) at which rotation will take place
    ANIMATION_TIME = 5    # How fast will animation change((Here)How fast the bird will be flapping wings)

    def __init__(self, x, y):
        self.x = x
        self.y = y
        # position/(x and y co-ordinates) of the bird
        self.tilt = 0   
        # degrees to tilt
        self.tick_count = 0  
        # will take input(say for every touch/key input the count will inc. and dec. depeding on if the task is performed ot not)
        self.vel = 0
        # speed at which a bird will be moving
        self.height = self.y
        #
        self.img_count = 0
        #this will keep track of which image of bird we are showing currently
        self.img = self.IMGS[0]
        # this will reference to the bird images to get the bird images

    def jump(self):
        '''
        This function will get called with every tick count 
        as with every touch or key call bird will fly(jump(here)) 
        '''   
        self.vel = -10.5
        #in pygame due to co-ordinates system(4th-quadrent) , to move upwards(jump) we are actualy moving form a negative point towards zero
        self.tick_count = 0
        #this will keep track when we last jumped
        self.height = self.y
        # from which position jump is been made
    
    def move(self):
        '''
        This function will move the bird after every single frame
        (If FPS = 30,this function will get called 30 times per second) 
        '''