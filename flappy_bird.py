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
pipe_images = pygame.transform.scale2x(pygame.image.load(os.path.join("images" , "pipe.png")))

#image of base(bottom/floor)
base_images = pygame.transform.scale2x(pygame.image.load(os.path.join("images" , "base.png")))

#image of back ground
bg_images = pygame.transform.scale2x(pygame.image.load(os.path.join("images" , "bg.png")))

class Bird:
    """
    Bird class representing the flappy bird
    """
    IMGS = bird_images
    MAX_ROTATION = 25    # How much the bird will rotate while going up and down
    ROTATION_VELOCITY = 20    # Velocity(speed) at which rotation will take place
    ANIMATION_TIME = 5    # How fast will animation change((Here)How fast the bird will be flapping wings)

    def __init__(self, x, y):
        """
        Initialize the object
        :param x: starting x pos (int)
        :param y: starting y pos (int)
        :return: None
        """
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
        """
        This function will get called with every tick count 
        as with every touch or key call bird will fly(jump(here)) 
        :param : None
        :return: None
        """
        #in pygame due to co-ordinates system(4th-quadrent) , to move upwards(jump) we are actualy moving form a negative point towards zero
        self.vel = -10.5
        #this will keep track when we last jumped
        self.tick_count = 0
        # from which position jump is been made
        self.height = self.y
    
    def move(self):
        """
        This function will move the bird after every single frame
        (If FPS = 30,this function will get called 30 times per second) 
        :param : None
        :return: None
        """
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
        :param win: pygame window or surface
        :return: None
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
        new_rect = rotated_image.get_rect(center = self.img.get_rect(topleft =  (self.x , self.y)).center)
        win.blit(rotated_image , new_rect.topleft)

    def get_mask(self):
        """
        gets the mask for the current image of the bird for colisions between images
        :param : None
        :return : None
        """
        return pygame.mask.from_surface(self.img)

class Pipe:
    """
    represents a pipe object
    """
    GAP = 200
    #Space between pipes
    VEL = 5
    #Moving the pipes as we arent actually moving our bird instead we are moving pipes towards bird to vilualize bird to be moving

    def __init__(self, x):
        """
        initialize pipe object
        using x only because the height(y-parameter) of the pipe completely random
        :param x: int
        :return" None
        """
        self.x = x
        self.height = 0

        #keeping track of top and bottom positions of the pipe is
        self.top = 0
        self.bottom = 0

        #We aill use image that we had as it is for the bottom pipe
        self.PIPE_BOTTOM = pipe_img
        #We are flipping the pipe upside down to get the image for the top pipe
        self.PIPE_TOP = pygame.transform.flip(pipe_img, False, True)
        
        #Keeping track if bird has passed the pipe and to check for collisions
        self.passed = False
        #This method will define position of top and bottom pipes and the gap between them
        self.set_height()

    def set_height(self):
        """
        set the height of the pipe, from the top of the screen
        :return: None
        """
        #Using random function generating the position of the top of the pipe within range of our screen
        self.height = random.randrange(50, 450)
        #getting the bottom of the pipe but as this pipe will be filpped upside-down it will actually be top of the image(extreme y position towards top)
        self.top = self.height - self.PIPE_TOP.get_height()
        #getting the bottom of the pipe
        self.bottom = self.height + self.GAP

    def move(self):
        """
        # move pipe based on velcity
        :param: None
        :return: None
        """
        self.x -= self.VEL

    def draw(self, win):
        """
        draw both the top and bottom of the pipe
        :param win: pygame window/surface
        :return:None
        """
        # draw top of the pipe
        win.blit(self.PIPE_TOP, (self.x, self.top))
        # draw bottom of the pipe
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))
    
    def collide(self, bird, win):
        """
        returns if a point is colliding with the pipe or not using approach similar to a hitbox for an object
        :param bird: Bird object
        :return: Bool
        """
        #Getting the mask(hit box of the bird)
        bird_mask = bird.get_mask()
        #Getting mask for the pipe on top
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        #Getting mask for the pipe on bottom
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)
        #Distance between the mask of the bird and pipe at top
        #round() is used to
        top_offset = (self.x - bird.x, self.top - round(bird.y))
        #Distance between the mask of the bird and pipe at bottom
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))
        #If mask dont collide than we does not need to check if pixels overlap or not

        #Finding if point of collision or (say point where pixels overlap) between pipe at bottom and bird
        b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        #Finding if point of collision between pipe at top and bird
        t_point = bird_mask.overlap(top_mask,top_offset)

        #If pixels collision points exist than collision has occured so return True
        if b_point or t_point:
            return True
        #Else return false
        return False


def draw_window(win,bird):
    """
    specifying the window of the game
    :param win: pygame window/surface
    :return: None
    """
    win.blit(bg_images , (0,0))
    bird.draw(win)
    pygame.display.update()

def main():
    """
    main method to start the game
    :param: None
    :return: None
    """
    bird = Bird(200,200)
    win = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))

    run = True
    while(run):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        draw_window(win,bird)
    pygame.quit()
    quit()
main()
