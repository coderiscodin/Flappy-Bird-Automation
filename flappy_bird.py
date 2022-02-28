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
        self.tick_count += 1

    
        displacement = self.vel*(self.tick_count) + 0.5*(3)*(self.tick_count)**2  
        # calculate displacement(distance) in pixels or say tiles we moved upward with every time we want to move upwards

        # terminal velocity
        if displacement >= 16:
            displacement = (displacement/abs(displacement)) * 16
        #ensures we going way downwards so we set a limit that we can not go downwards bellow a certain limit based on our max point upwards we reached 

        if displacement < 0:
            displacement -= 2
        #set the upwards displacement limit as form equation in line 69 the more the tick count,more higher will be displacement 
        #lets say a bird is moving -1 upwards for tickcount 3 and <-2 for tickcount 4 and will go even higher with higher tick count so avoid exponential increase we set upper limit to it 
  
        self.y = self.y + displacement
        #adding the displacement to our actual psition


        #by tilting (here) it means tilting actual image of the bird after a certain point
        if displacement < 0 or self.y < self.height + 50:  # tilt up
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:  # tilt down
            if self.tilt > -90:
                self.tilt -= self.ROT_VEL