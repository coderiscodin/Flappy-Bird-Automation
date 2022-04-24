import pygame
import random
import os
import time
import neat
import pickle
pygame.font.init()  #INIT FONT

#GLOBAL VARIABLES

#FRAMES PER SECOND
FPS = 25

#WINDOW WIDTH
WIN_WIDTH = 600

#WINDOW HEIGHT
WIN_HEIGHT = 700  

#HEIGHT OF BASE(FLOOR)
FLOOR = 630  

#STYLE AND SIZE OF FONT TO BE RENDERED
STAT_FONT = pygame.font.SysFont("comicsans", 50) 
END_FONT = pygame.font.SysFont("comicsans", 70)
DRAW_LINES = False

#INITIALIZING WINDOW
WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Flappy Bird")

#IMAGE OF PIPE
pipe_img = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","pipe.png")).convert_alpha())

#BACKGROUND IMAGE
bg_img = pygame.transform.scale(pygame.image.load(os.path.join("imgs","bg.png")).convert_alpha(), (600, 800))

#IMAGE OF BIRD
bird_images = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird" + str(x) + ".png"))) for x in range(1,4)]

#IMAGE OF BASE(BOTTOM/FLOOR)
base_img = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","base.png")).convert_alpha())

#SCALE2X MAKES IMAGE 2 TIMES BIGGER

#INITIALIZING GENERATION FOR NEURAL NETWORK
gen = 0

class Bird:
    """
    REPRESEND THE BIRD
    """
    IMGS = bird_images

    #HOW MUCH THE BIRD WILL ROTATE WHILE GOING UP AND DOWN
    MAX_ROTATION = 25  

    #VELOCITY(SPEED) AT WHICH ROTATION WILL TAKE PLACE
    ROT_VEL = 20  

    #HOW FAST WILL ANIMATION CHANGE((HERE)HOW FAST THE BIRD WILL 
    #BE FLAPPING WINGS)
    ANIMATION_TIME = 5 

    def __init__(self, x, y):
        """
        INITIALIZE THE OBJECT
        :param x: starting x pos (int)
        :param y: starting y pos (int)
        :return: None
        """
        #POSITION OF THE BIRD IN X-Y PLANE
        self.x = x
        self.y = y

        #DEGREE OF TILT
        self.tilt = 0

        #TICK COUNT COUNTS INPUT TAKEN(FOR EVERY TOUCH/KEY INPUT 
        #THE COUNT WILL INC OR DEC 
        #DEPENDING ON IF THE TASK IS PERFORMED OR NOT)
        self.tick_count = 0

        #SPEED AT WHICH BIRD WILL BE MOVING
        self.vel = 0
        
        self.height = self.y

        #KEEPING TRACK OF WHICH IMAGE OF BIRD WE ARE CURRENTLY SHOWING
        self.img_count = 0

        #REFERENCE TO BIRD IMAGES
        self.img = self.IMGS[0]

    def jump(self):
        """
        THIS FUNCTION GETS CALLED WITH EVERY TICK COUNT 
        AS WITH EVERY TOUCH OR KEY CALL BIRD WILL FLY(JUMP(HERE)) 
        :param : None
        :return: None
        """
        #IN PYGAME DUE TO CO-ORDINATES SYSTEM(4th-QUADRENT),TO MOVE UPWARDS(JUMP) WE ARE ACTUALY 
        #MOVING FROM A NEGATIVE POINT TOWARDS ZERO
        self.vel = -10.5

        #THIS WILL KEEP TRACK WHEN WE LAST JUMPED
        self.tick_count = 0

        #FROM WHICH POSITION JUMP IS BEING MADE
        self.height = self.y

    def move(self):
        """
        THIS FUNCTION WILL MOVE THE BIRD AFTER EVERY SINGLE FRAME
        (IF FPS = 30,THIS FUNCTION WILL GET CALLED 30 TIMES PER SECOND) 
        :param : None
        :return: None
        """
        self.tick_count += 1

        #FOR DOWNWARD ACCELERATION

        #CALCULATE DISPLACEMENT(DISTANCE) IN PIXELS OR SAY TILES WE MOVED UPWARD WITH EVERY TIME 
        #WE WANT TO MOVE UPWARDS
        displacement = self.vel*(self.tick_count) + 1.5*(self.tick_count)**2

        #TERMINAL VELOCITY
        if displacement >= 16:

            #INCASE WE ARE GOING WAY DOWNWARDS WE SET A LIMIT THAT WE CAN NOT GO DOWNWARDS BELLOW A 
            #CERTAIN LIMIT BASED ON MAX POINT UPWARDS WE REACHED
            displacement = (displacement/abs(displacement)) * 16


        #SET THE UPWARD DISPLACEMENT LIMIT AS FROM EQUATION 
        #IN LINE 125 THE MORE IS THE TICK COUNT,
        #HIGHER WILL BE DISPLACEMENT 
        #LETS SAY A BIRD IS MOVING -1 UPWARDS FOR TICKCOUNT=3 
        #AND <-2 FOR TICKCOUNT=4 AND WILL GO EVEN HIGHER
        #WITH HIGHER TICK COUNT SO TO AVOID EXPONENTIAL INCREASE
        #WE SET UPPER LIMIT TO IT
        if displacement < 0:
            displacement -= 2

        #ADDING THE DISPLACEMENT TO OUT ACTUAL POSITION
        self.y = self.y + displacement

        #BY TILTING(HERE) IT MEANS TILTING ACTUAL IMAGE OF 
        #THE BIRD AFTER A CERTAIN POINT
        if displacement < 0 or self.y < self.height + 50:  #TILT UP
            
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        
        else:  #TILT DOWN
            
            if self.tilt > -90:
                self.tilt -= self.ROT_VEL

    def draw(self, win):
        """
        ANIMATE THE BIRD
        :param win: pygame window or surface
        :return: None
        """
        #COUNTING NUMBER OF IMAGES SHOWN
        self.img_count += 1

        #FOR ANIMATION OF BIRD,LOOP THROUGH THREE IMAGES(CREATING BIRD ANIMATION)
        #SHOWING BIRD TO BE FLAPPING THROUGH 3 IMAGES
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

        #WHEN FALLING DOWN INSTEAD OF FLAPPING,WINGS REMAINS STATIONARY
        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME*2


        #TILT THE BIRD
        blitRotateCenter(win, self.img, (self.x, self.y), self.tilt)

    def get_mask(self):
        """
        GET THE MASK(HITBOX) FOR THE CURRENT IMAGE OF THE BIRD FOR 
        COLISIONS BETWEEN IMAGES
        :param : None
        :return: None
        """
        return pygame.mask.from_surface(self.img)


class Pipe():
    """
    REPRESENTS PIPE OBJECT
    """
    #SPACE BETWEEN PIPES
    GAP = 200
    
    #VELOCITY OF THE PIPE    
    VEL = 5

    def __init__(self, x):
        """
        INITIALIZE PIPE OBJECT
        USING ONLY X CO-ORDINATE BECAUSE HEIGHT OF THE PIPE(Y CO-ORDINATE) 
        WILL BE GENERATED RANDOMLY
        :param x: int
        :return" None
        """
        self.x = x
        self.height = 0

        #KEEPING TRACK WHERE THE TOP AND BOTTOM OF THE PIPE IS
        self.top = 0
        self.bottom = 0

        #WE WILL USE THE IMAGE THAT WE HAD IN ITS ORIGINAL FORM FOR BOTTOM PIPE
        self.PIPE_BOTTOM = pipe_img

        #WE WILL FLIP THE IMAGE WE HAVE UPSIDE DOWN TO GET THE IMAGE OF THE TO PIPE
        self.PIPE_TOP = pygame.transform.flip(pipe_img, False, True)
        
        #KEEPING TRACK IF BIRD HAS PASSED THE PIPE AND CHECK FOR COLLISIONS
        self.passed = False

        #THIS METHOD WILL DEFINE POSITION OF THE TOP AND BOTTOM PIPES AND THE REQUIRED 
        #GAP BETWEEN THEM
        self.set_height()

    def set_height(self):
        """
        SET THE HEIGHT OF THE PIEP, FROM THE TOP OF THE SCREEN
        :return: None
        """
        #RANDOMLY GENERATING HEIGHT OF THE PIPE TO BE WITHIN RANGE OF SCREEN
        self.height = random.randrange(50, 350)

        #GETTING BOTTOM OF TOP PIPE BUT AS THIS PIPE WILL BE FLIPPED UPSIDE DOWN IT WILL ACTUALLY 
        #TOP OF IMAGE(EXTREME Y POSITION TOWARDS TOP)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP

    def move(self):
        """
        MOVE PIPE BASED ON VELOCITY
        :return: None
        """
        self.x -= self.VEL

    def draw(self, win):
        """
        DRAW BOTH THE TOP AND BOTTOM PIPE
        :param win: pygame window/surface
        :return: None
        """
        #BLIT DRAWS THE SOURCE SURFACE ON THE GIVEN SURFACE

        #DRAW TOP PIPE
        win.blit(self.PIPE_TOP, (self.x, self.top))
        #DRAW BOTTOM PIPE
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))


    def collide(self, bird, win):
        """
        RETURNS IF THE POINT IS COLLIDING WITH THE PIPE OR NOT USING APPROACH SIMILAR 
        TO HITBOX FOR AN OBJECT 
        :param bird: Bird object
        :return: Bool
        """
        #GETTING THE MASK(HITBOX OF THE BIRD)
        bird_mask = bird.get_mask()

        #GETTING MASK OF TOP PIPE
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)

        #GETTING MASK OF BOTTOM PIPE
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)

        #OFFSET = HOW FAR THIS MASKS ARE(BIRD MASK AND PIPE MASK)
        top_offset = (self.x - bird.x, self.top - bird.y)
        bottom_offset = (self.x - bird.x, self.bottom - bird.y)

        #FINDING IF POINT OF COLLISION (OR SAY POINT WHERE PIXELS OVERLAP) 
        #BETWEEN PIPE AT BOTTOM AND BIRD EXIST OR NOT
        b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        t_point = bird_mask.overlap(top_mask,top_offset)

        #IF COLLISION POINT EXIST RETURN TRUE
        if b_point or t_point:
            return True

        return False

class Base:
    """
    REPRESENTING MOVING BASE OF THE GAME
    """
    VEL = 5  #SAME AS VELOCITY OF PIPE SO BIRD SEEMS TO BE MOVING
    WIDTH = base_img.get_width()  #WIDTH OF BASE
    IMG = base_img

    def __init__(self, y):
        """
        INITIALIZE THE OBJECT
        :param y: int
        :return: None
        """
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):
        """
        MOVING THE FLOOR
        :return: None
        """

        #CONSIDER 2 SAME IMAGES OF BASE,AT THE BEGINNING OF THE GAME IMAGE1 WILL 
        #START AT X=0 ON X-AXIS AND IMAGE2 WILL BE AT X2(WIDTH OF IMAGE1).
        #AS OUR BASE MOVES IMAGE1 AND IMAGE2 WILL GET DISPLACED BY "VEL" UNITS 
        #TO THE LEFT SO THAT IT DOES NOT LOOK LIKE THERE ARE TWO DIFFERENT IMAGES
        self.x1 -= self.VEL
        self.x2 -= self.VEL
        if self.x1 + self.WIDTH < 0:

            #IF END POINT OF IMAGE1 IS AT X=0,IMAGE1 HAS BEEN DISPLACED 
            #BY "WIDTH" UNITS TO THE LEFT THUS IMAGE2 IS ON THE SCREEN 
            #AND IMAGE1 IS OUT OF THE SCREEN,SO WE NOW MOVE IMAGE2 TO 
            #POSITION WHERE ORIGINALLY IMAGE2 WAS WHEN IMAGE1 WAS 
            #STARTING AT X=0 AS NOW IMAGE2 STARTS AT X=0
            self.x1 = self.x2 + self.WIDTH

        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self, win):
        """
        BLIT/DRAW THE FLOOR
        :param win: the pygame surface/window
        :return: None
        """
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))


def blitRotateCenter(surf, image, topleft, angle):
    """
    ROTATE THE SURFACE(BIRD) TO MAKE IT LOOK FALLING AND BLIT IT TO THE WINDOW
    :param surf: the surface to blit to
    :param image: the image surface to rotate(BIRD IMAGE)
    :param topLeft: the top left position of the image
    :param angle: a float value for angle
    :return: None
    """
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center = image.get_rect(topleft = topleft).center)

    surf.blit(rotated_image, new_rect.topleft)

def draw_window(win, birds, pipes, base, score, gen, pipe_ind):
    """
    DRAWS THE WINDOW FOR MAIN GAME LOOP
    :param win: pygame window surface
    :param bird: a Bird object
    :param pipes: List of pipes
    :param score: score of the game (int)
    :param gen: current generation
    :param pipe_ind: index of closest pipe
    :return: None
    """
    if gen == 0:
        gen = 1
    #DRAW BG
    win.blit(bg_img, (0,0))

    #DRAW PIPES
    for pipe in pipes:
        pipe.draw(win)

    #DRAW PYGAME WINDOW
    base.draw(win)

    for bird in birds:
        #DRAW LINES FOR BIRD TO NEAREST PIPE INDEX TO DECIDE THE PATH
        if DRAW_LINES:
            try:
                #LINES WILL BE DRAWN IF DRAW_LINES==True ELSE WILL JUST CALCULATE TO DECIDE THE PATH
                pygame.draw.line(win, (255,0,0), (bird.x+bird.img.get_width()/2, 
                                bird.y + bird.img.get_height()/2),(
                                pipes[pipe_ind].x + pipes[pipe_ind].PIPE_TOP.get_width()/2, 
                                pipes[pipe_ind].height), 5)
                
                pygame.draw.line(win, (255,0,0), (bird.x+bird.img.get_width()/2, 
                                bird.y + bird.img.get_height()/2),(
                                pipes[pipe_ind].x + pipes[pipe_ind].PIPE_BOTTOM.get_width()/2, 
                                pipes[pipe_ind].bottom), 5)
            except:
                pass
        
        #DRAW BIRD
        bird.draw(win)

    #SHOW SCORE
    score_label = STAT_FONT.render("Score: " + str(score),1,(255,255,255))
    win.blit(score_label, (WIN_WIDTH - score_label.get_width() - 15, 10))

    #SHOW GENERATIONS
    score_label = STAT_FONT.render("Gens: " + str(gen-1),1,(255,255,255))
    win.blit(score_label, (10, 10))

    #SHOW NUMBER OF ALIVE BIRDS FROM THE POPULATION
    score_label = STAT_FONT.render("Alive: " + str(len(birds)),1,(255,255,255))
    win.blit(score_label, (10, 50))

    #UPDATING THE SCREEN TO SHOW ALL THINGS THAT NEEDED TO BE SHOWN USING BLIT
    pygame.display.update()


def eval_genomes(genomes, config):
    """
    RUNS THE SIMULATION OF THE CURRENT POPULATION OF BIRDS
    AND SETS THEIR FITNESS BASED ON THE DISTANCE THEY REACH IN GAME
    (BASICALLY FARTHER THE BIRD TRAVELS BETTER WILL BE BIRD'S FITNESS)
    """
    #DECLARING FLOBAL VARIABLES TO MODIFY THEM OUTSIDE THE CURRENT SCOPE
    global WIN, gen
    win = WIN
    gen += 1

    #CREATING LISTS THAT HOLDS THE GENOME(GE),
    #THE NEURAL NETWORK ASSOCIATED WITH GENOME(NETS) AND
    #BIRD OBJECT THAT USES THAT NETWORK TO PLAY(BIRDS)
    nets = []
    birds = []
    ge = []
    for genome_id, genome in genomes:
        #INITIALIZING FITNESS OF THE BIRD = 0 AT START
        genome.fitness = 0

        #CALLING NEAT ALGORITHM
        net = neat.nn.FeedForwardNetwork.create(genome, config)
    
        #APPENDING THE RESULT ABOVE ABOVE CALL,BIRDS AND GENOME
        nets.append(net)
        birds.append(Bird(230,350))
        ge.append(genome)

    #INITIALIZING OBJECTS AND SCORE
    base = Base(FLOOR)
    pipes = [Pipe(700)]
    score = 0

    clock = pygame.time.Clock()

    run = True
    #RUN UNTIL EXIT OR GIVEN CONDITION SATISFIES
    while run and len(birds) > 0:
        #TICKING THE FPS
        clock.tick(FPS)

        #GETTING THE INPUT
        for event in pygame.event.get():

            #IF PLAYER WANT TO QUIT
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
                break

        pipe_ind = 0
        if len(birds) > 0:

            #DETERMINE WHICH PIPE IS CLOSEST TOP PIPE OR BOTTOM PIPE
            if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width():  
                pipe_ind = 1                                                                 

        for x, bird in enumerate(birds):  
            #INCREASING THE FITNESS OF THE BIRD WITH EACH FRAME IT PASSES
            ge[x].fitness += 0.1
            bird.move()

            #SEND BIRD LOCATION,TOP PIPE AND BOTTOM PIPE LOCATION 
            #AND DETREMINE WHETHER TO JUMP OR NOT
            output = nets[birds.index(bird)].activate((bird.y, 
                    abs(bird.y - pipes[pipe_ind].height), 
                    abs(bird.y - pipes[pipe_ind].bottom)))

             #AS WE HAVE USED TANH FUNCTION IN COFIG FILE SO RESULT WILL BE 
             #BETWEEN -1 AND 1
            if output[0] > 0.5: 
                bird.jump()

        base.move()

        rem = []
        add_pipe = False
        for pipe in pipes:
            pipe.move()
            #CHECKING IF COLLISION HAS OCCURED OR NOT
            for x,bird in enumerate(birds):
                if pipe.collide(bird, win):

                    #IF COLLISION HAS OCCURED DECREASE THE FITNESS BECAUSE IF 
                    #THERE ARE 2 BIRDS ONE THAT HIT THE PIPE AND ANOTHER THAT 
                    #DIDN'T HIT THE PIPE,THE ONE THAT HIT THE PIPE SHOULD 
                    #HAVE LESS FITNESS
                    ge[x].fitness -= 1

                    #REMOVE THAT BIRD SO THAT IT IS NOW NOT DISPLAYED ON 
                    #THE SCREEN 
                    nets.pop(x)
                    ge.pop(x)
                    birds.pop(x)

            #IF PIPE IS NOT SHOWN PROPERLY ON THE SCREEN WE WILL REMOVE THAT
            #PIPE BUT AS WE ARE RUNNING THE FOR LOOP FOR PIPES,WE CANNOT 
            #REMOVE IT DIRECTLY SO WE WILL ADD SUCH PIPES TO ANOTHER ARRAY
            #REM[] AND THEN REMOVE THOSE PIPES FROM PIPES[](AS IN LINE-552)
            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)

            #AS SOON AS OUR BIRD PASSES THE PIPE,WE IMMEDIATELY GENERATE NEW
            #PIPE TO SHOW ON THE SCREEN
            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True
                add_pipe = True

        if add_pipe:
            #AS WE WILL ADD NEW PIPE ONLY AFTER BIRD PASSES CURRENT PIPE,
            #WE INCREASE SCORE BY 1 AS BIRD PASSED THE CURRENT PIPE 
            score += 1

            #IF BIRD PASSES THE PIPE WE INCREASE BIRD'S FITNESS
            #(EXTRA REWARD FOR PASSING THE PIPE)
            for genome in ge:
                genome.fitness += 5
            pipes.append(Pipe(WIN_WIDTH))

        for r in rem:
            #REMOVING THOSE UNUSABLE PIPES 
            pipes.remove(r)

        for bird in birds:
            #CHECKING FOR COLLISION WITH BASE
            if bird.y + bird.img.get_height() - 10 >= FLOOR or bird.y < -50:
                nets.pop(birds.index(bird))
                ge.pop(birds.index(bird))
                birds.pop(birds.index(bird))

        #CALLING THE FUNCTION
        draw_window(WIN, birds, pipes, base, score, gen, pipe_ind)


def run(config_file):
    """
    RUNS THE NEAT ALGORITHM TO TRAIN THE NEURAL NETWORK TO PLAY FLAPPY BIRD
    :param config_file: location of config file
    :return: None
    """
    #LOAD CONFIGURATION
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    #CREATE THE POPULATION WHICH IS THE TOP-LEVEL OBJECTFOR A NEAT RUN
    p = neat.Population(config)

    #ADD A STANDARD OUTPUT REPORTER TO SHOW PROGRESS IN THE TERMINAL
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    #RUN FOR UPTO 50 GENERATIONS
    winner = p.run(eval_genomes, 50)

    #SHOW FINAL STATS
    print('\nBest genome:\n{!s}'.format(winner))


if __name__ == '__main__': 
    '''
    THIS WILL ALWAYS BE TRUE AS WE ARE RUNNING CURRENT 
    FILE AND NOT IMPORTING IT TO ANY OTHER FILE TO EXECUTE IT
    '''
    #DETERMINE PATH TO CONFIGURATION FILE.THIS PATH MANIPULATION IS
    #HERE SO THAT THE SCRIP WILL RUN SUCESSFULLY REGARDLESS OF THE
    #CURRENT WORKING DIRECTORY
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.txt')
    run(config_path)
