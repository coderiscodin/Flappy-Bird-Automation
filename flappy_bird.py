import pygame
import random
import os
import time
import neat

# FPS = 32
# CAPITAL VARIABLES = CONSTATNS IN GENERAL CONVENTIONS
WIN_WIDTH = 600
WIN_HEIGHT = 800

#image of bird
bird_images = [pygame.transform.scale2x(pygame.image.load(os.path.join("images" , "bird1.png"))) , pygame.transform.scale2x(pygame.image.load(os.path.join("images" , "bird2.png"))) , pygame.transform.scale2x(pygame.image.load(os.path.join("images" , "bird3.png"))) ]
#scale2x makes image 2x bigger
#.convert_alpha() helps in faster rendering of image to provide real game experience

#image of pipe
pipe_images = pygame.transform.scale2x(pygame.image.load(os.path.join("images" , "pipe.png")).convert_alpha())

#image of base(bottom/floor)
base_images = pygame.transform.scale2x(pygame.image.load(os.path.join("images" , "base.png")).convert_alpha())

#image of back ground
bg_images = pygame.transform.scale2x(pygame.image.load(os.path.join("images" , "bg.png")).convert_alpha())

class Bird:
    IMGS = bird_images
    MAX_ROTATION = 25    # How much the bird will rotate while going up and down
    ROTATION_VELOCITY = 20    # Velocity(speed) at which rotation will take place
    ANIMATION_TIME = 5    # How fast will animation change((Here)How fast the bird will be flapping wings)

    def __init__(self, x, y):
        # position/(x and y co-ordinates) of the bird
        self.x = x
        self.y = y

        # degrees to tilt
        self.tilt = 0   
        # will take input(say for every touch/key input the count will inc. and dec. depeding on if the task is performed ot not)
        self.tick_count = 0
        # speed at which a bird will be moving  
        self.vel = 0
        #
        self.height = self.y
        #this will keep track of which image of bird we are showing currently
        self.img_count = 0
        # this will reference to the bird images to get the bird images
        self.img = self.IMGS[0]

    def jump(self):
        '''
        This function will get called with every tick count 
        as with every touch or key call bird will fly(jump(here)) 
        '''
        #in pygame due to co-ordinates system(4th-quadrent) , to move upwards(jump) we are actualy moving form a negative point towards zero
        self.vel = -10.5
        #this will keep track when we last jumped
        self.tick_count = 0
        # from which position jump is been made
        self.height = self.y
    
    def move(self):
        '''
        This function will move the bird after every single frame
        (If FPS = 30,this function will get called 30 times per second) 
        '''
        self.tick_count += 1
        
        # calculate displacement(distance) in pixels or say tiles we moved upward with every time we want to move upwards
        displacement = self.vel*(self.tick_count) + 0.5*(3)*(self.tick_count)**2  

        # terminal velocity
        if displacement >= 16:

        #ensures we going way downwards so we set a limit that we can not go downwards bellow a certain limit based on our max point upwards we reached 
            displacement = (displacement/abs(displacement)) * 16


        #set the upwards displacement limit as form equation in line 69 the more the tick count,more higher will be displacement 
        #lets say a bird is moving -1 upwards for tickcount 3 and <-2 for tickcount 4 and will go even higher with higher tick count so avoid exponential increase we set upper limit to it 
        if displacement < 0:
            displacement -= 2

        #adding the displacement to our actual psition
        self.y = self.y + displacement


        #by tilting (here) it means tilting actual image of the bird after a certain point
        if displacement < 0 or self.y < self.height + 50:  # tilt up
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:  # tilt down
            if self.tilt > -90:
                self.tilt -= self.ROT_VEL

    def draw(self, win):
        """
        animate the bird
        win represents pygame window or surface
        """
        #counting number of images shown
        self.img_count += 1

        # For animation of bird, loop through three images(Creating bird animation)
        if self.img_count <= self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_count <= self.ANIMATION_TIME*2:
            self.img = self.IMGS[1]
        elif self.img_count <= self.ANIMATION_TIME*3:
            self.img = self.IMGS[2]
        elif self.img_count <= self.ANIMATION_TIME*4:
            self.img = self.IMGS[1]
        elif self.img_count == self.ANIMATION_TIME*4 + 1:
            self.img = self.IMGS[0]
            self.img_count = 0

        #When bird is falling down instead of flapping wings,wings will remain stationary
        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME*2


        # tilt the bird
        rotated_image = pygame.transform.rotate(self.img , self.tilt)
        new_react = rotated_image.get_rect(centre = self.img.get_rect(topleft =  (self.x , self.y)).centre)
        win.blit(rotated_image , new_rect.topleft)

    def get_mask(self):
        """
        gets the mask for the current image of the bird for colisions between images
        """
        return pygame.mask.from_surface(self.img)

def draw_window(win,bird):
    win.blit(BG_IMG , (0,0))
    bird.draw(win)
    pygame.display.update()

def main():
    bird = Bird(200,200)
    win = pygame.display.set_mde((WIN_WIDTH,WIN_HEIGHT))

    run = True
    while(run):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        draw_window(win,bird)
    pygame.quit()
    quit()
main()

