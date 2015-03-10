# Cowsheet.png Source : http://documentation.flatredball.com/frb/docs/images/6/62/Cowsheet.png

import pygame
import random

__author__="Florian Wirth"

# ------------------------------------------------------------------------------
#                           --- Start Global Constants ---
# Constant values that won't change
# ------------------------------------------------------------------------------

# Colors
BLACK     = (   0,   0,   0)
WHITE     = ( 255, 255, 255)
GREEN     = (   0,  88,  36)
DARKGREEN = (   0,  33,  13)

# Screen-Size
SCREEN_WIDTH  = 1024
SCREEN_HEIGHT = 768

# ------------------------------------------------------------------------------
#                           --- End Global Constants ---
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
#                           --- Start Classes ---
# Define all the classes needed for the game
# ------------------------------------------------------------------------------

# --- SpriteSheet Class
#
class SpriteSheet(object):
    """ Class for loading Spritesheets """
    
    sprite_sheet = None
    
    
    def __init__(self,file_name):
        """ Constructor function """
        
        self.sprite_sheet = pygame.image.load(file_name).convert()
        
        
    def get_image(self,x,y,width,height):
        """ Load the File """
        
        image = pygame.Surface([width,height]).convert()
        image.blit(self.sprite_sheet,(0,0),(x,y,width,height))
        transColor = image.get_at((0,0))
        image.set_colorkey(transColor)
        return image
    
    
# --- Player Class   
#
class Player(pygame.sprite.Sprite):
    """ Define the PlayerCow """
    
    # --- Attributes
    # Used for moving the character
    flap_height  = 0
    travel_speed = 2
    
    cow_sprites  = []
   
    
    def __init__(self):
        """ Constructor function """
        
        pygame.sprite.Sprite.__init__(self)
        
        # Load SpriteSheet
        sprite_sheet = SpriteSheet("images/CowSheet.png")

        image = sprite_sheet.get_image(0,23,64,45)
        image = pygame.transform.flip(image,1,0)
        self.cow_sprites.append(image)
        image = sprite_sheet.get_image(1,208,62,48)
        image = pygame.transform.flip(image,1,0)
        self.cow_sprites.append(image)
        
        # Set starting image
        self.image = self.cow_sprites[0]
        self.rect = self.image.get_rect()

        
    def update(self):    
        
        # Use gravity
        self.calc_grav()     
        
        # Move right and flap
        # - Moving right at a constant speed
        self.rect.x += self.travel_speed
        # - Whenever the player hits the jump button, flap
        self.rect.y += self.flap_height
        
        
    def calc_grav(self):
        """ Calculate effect of gravity. """
        
        self.flap_height += .14

    def flap(self): 
        """ Flap """
        
        # "Animation"
        self.image = self.cow_sprites[1]
        
        # "Flap"
        self.flap_height = -4


# --- Obstacle Class
#
class Obstacle(pygame.sprite.Sprite):
    """ Appearing Obstacle, the user has to dodge """
    
    hole_size  = 0
    height     = 0
    difficulty = 1
    
    def __init__(self,pos,top_height,difficulty):
        """ Constructor function """
        
        pygame.sprite.Sprite.__init__(self)
        
        self.difficulty = difficulty
        
        # The harder the difficulty, the smaller the hole to pass through gets
        if   self.difficulty == 1 or 2:
            self.hole_size = random.randrange(150,200)
        elif self.difficulty == 3:
            self.hole_size = random.randrange(140,180)
        else:
            self.hole_size = random.randrange(130,160)
        
        # Calculate the height_dimension of the Obstacle for both top and bottom side of the screen
        if pos == "top":
            self.height = top_height - 50
        else:
            self.height = SCREEN_HEIGHT - self.hole_size - top_height - 118
        
        # Load Surface Image
        image = pygame.image.load("images/obstacle.jpg").convert()
        image = pygame.transform.scale(image,(40,self.height))
        
        self.image = image
        self.rect = self.image.get_rect()
        
        # Either top or bottom side Obstacle
        if pos == "top":
            self.rect.y = 50
        else:
            self.rect.y = SCREEN_HEIGHT - self.height - 118
        
        # Start position of the Obstacle (right outside the screen)
        self.rect.x = SCREEN_WIDTH + 50
    
    
    def update(self):
        """ Move the Obstacles """
        
        # Move Obstacles with constant speed
        self.rect.x -= 3


# --- WindowBorders Class
#
class WindowBorders(pygame.sprite.Sprite):
    """ Create borders so the player can't move outside the window """
    
    def __init__(self,pos):
        """ Constructor function """
        
        pygame.sprite.Sprite.__init__(self)
        
        if pos == "left":
            self.image = pygame.Surface([5,SCREEN_HEIGHT-168])
        else:
            self.image = pygame.Surface([SCREEN_WIDTH-45,5])
        
        self.image.fill(BLACK)
        
        self.rect = self.image.get_rect()
        self.rect.x = 50
        
        if   pos == "top":
            self.rect.y = 45
        elif pos == "left":
            self.rect.y = 50
        else:
            self.rect.y = SCREEN_HEIGHT-118
        
        
# --- TitleScreen Class
#
class TitleScreen():
    """ Represents the title screen, showed at game start """
    
    screen           = None
    frame            = 0
    cow_sprites      = []
    highscores       = []
    scored           = []
    show_highscores  = False
    show_help_screen = False
        
    def __init__(self,screen,highscores):
        """ Constructor function """
        
        self.screen = screen
        self.frame = 0
        self.show_help_screen = False
        self.scored = highscores
        
         # Load SpriteSheet
        sprite_sheet = SpriteSheet("images/CowSheet.png")
            
        # Add frames to a List to scroll through
        image = sprite_sheet.get_image(0,23,64,45)
        image = pygame.transform.flip(image,1,0)
        image = pygame.transform.scale(image,(320,225))
        self.cow_sprites.append(image)
        image = sprite_sheet.get_image(64,23,64,45)
        image = pygame.transform.flip(image,1,0)
        image = pygame.transform.scale(image,(320,225))
        self.cow_sprites.append(image)
        image = sprite_sheet.get_image(128,23,64,45)
        image = pygame.transform.flip(image,1,0)
        image = pygame.transform.scale(image,(320,225))
        self.cow_sprites.append(image)
        image = sprite_sheet.get_image(192,23,64,45)
        image = pygame.transform.flip(image,1,0)
        image = pygame.transform.scale(image,(320,225))
        self.cow_sprites.append(image)
        image = sprite_sheet.get_image(0,85,64,45)
        image = pygame.transform.flip(image,1,0)
        image = pygame.transform.scale(image,(320,225))
        self.cow_sprites.append(image)
        image = sprite_sheet.get_image(64,85,64,45)
        image = pygame.transform.flip(image,1,0)
        image = pygame.transform.scale(image,(320,225))
        self.cow_sprites.append(image)
        image = sprite_sheet.get_image(128,85,64,45)
        image = pygame.transform.flip(image,1,0)
        image = pygame.transform.scale(image,(320,225))
        self.cow_sprites.append(image)
        image = sprite_sheet.get_image(192,85,64,45)
        image = pygame.transform.flip(image,1,0)
        image = pygame.transform.scale(image,(320,225))
        self.cow_sprites.append(image)
        
        self.image = self.cow_sprites[0]
        self.rect = self.image.get_rect()
        
    def update(self):
        """ Animate the Cow """
        
        if self.frame < len(self.cow_sprites)-1:
            self.image = self.cow_sprites[self.frame]
            self.frame += 1
        else:
            self.frame = 0
      
    
    def draw(self):
        """ Draw the Screen / Help Screen """
        
        
        # Represents the Highscorescreen
        while self.show_highscores:
            
            self.show_highscores = self.handle_highscores()
            
            font1 = pygame.font.SysFont("Comic Sans MS",50)
            font2 = pygame.font.SysFont("Comic Sans MS",30)
            font3 = pygame.font.SysFont("Comic Sans MS",25)
            font4 = pygame.font.SysFont("Comic Sans MS",15)
            
            title     = font1.render("Highscores",True,WHITE)
            
            # Reinitialize Highscores
            self.highscores = []
            
            for i in range(10):                                               
                self.highscores.append(font2.render(str(i+1) + ".  " + str(self.scored[i]) + "  Cow-Points",True,WHITE))
            
            copyright = font4.render("Game created by Florian Wirth",True,WHITE)
            quit      = font3.render("[Esc] - Back",True,WHITE)

            
            screen_hor = pygame.Surface([1024,50])
            screen_vert = pygame.Surface([50,768])
            keybox = pygame.Surface([1024,118])
            
            screen_hor.fill(DARKGREEN)
            screen_vert.fill(DARKGREEN)
            keybox.fill(DARKGREEN)
            
            
            self.screen.fill(GREEN)
            
            self.screen.blit(screen_hor, [0,0])
            self.screen.blit(screen_vert,[0,0])
            self.screen.blit(screen_vert,[974,0])
            self.screen.blit(keybox,     [0,650])
            
            
            self.screen.blit(title,  [(SCREEN_WIDTH//2) - (title.get_width()//2)    , 100])
            # Blit Top 10 Scores
            for i in range(10):
                self.screen.blit(self.highscores[i],[(SCREEN_WIDTH//2)-(self.highscores[i].get_width()//2),(220+35*i)])
                
            self.screen.blit(copyright, [(SCREEN_WIDTH//2)-(copyright.get_width()//2-310) , (SCREEN_HEIGHT-85)-(copyright.get_height()//2)])
            self.screen.blit(quit,   [(SCREEN_WIDTH//2)-(quit.get_width()//2-390)   , (SCREEN_HEIGHT-40)-(quit.get_height()//2)])
            
            pygame.display.flip()
        
        
        
        # Represents the Help Screen
        while self.show_help_screen:
           
            # If Escape is pressed, change help_screen to False, and close it
            self.show_help_screen = self.handle_help_screen()
            
            # Initialize everything for the screen
            font1 = pygame.font.SysFont("Comic Sans MS",50)
            font2 = pygame.font.SysFont("Comic Sans MS",20)
            font3 = pygame.font.SysFont("Comic Sans MS",35)
            font4 = pygame.font.SysFont("Comic Sans MS",25)
            font5 = pygame.font.SysFont("Comic Sans MS",15)
            
            title     = font1.render("Help",True,WHITE)
            descr_1   = font2.render("You have to navigate the cow Mooh out of the farm to save her from",True,WHITE)
            descr_2   = font2.render("the slaughterhouse. Miracolously she gained the ability to fly by",True,WHITE)
            descr_3   = font2.render("eating an enchanted chicken. Help Mooh to make the escape!",True,WHITE)
            rules     = font3.render("Rules",True,WHITE)
            help_1    = font4.render("You can use the chicken power by pressing [Arrow-Up]",True,WHITE)
            help_2    = font4.render("Avoid the obstacles and moving out of the screen",True,WHITE)
            copyright = font5.render("Game created by Florian Wirth",True,WHITE)
            quit      = font4.render("[Esc] - Back",True,WHITE)
            
            
            screen_hor = pygame.Surface([1024,50])
            screen_vert = pygame.Surface([50,768])
            box_hor = pygame.Surface([703,3])
            box_vert = pygame.Surface([3,130])
            keybox = pygame.Surface([1024,118])
            
            screen_hor.fill(DARKGREEN)
            screen_vert.fill(DARKGREEN)
            box_hor.fill(WHITE)
            box_vert.fill(WHITE)
            keybox.fill(DARKGREEN)
            
            # Backgroundcolor
            self.screen.fill(GREEN)
            
            # Create borders for stylepoints
            self.screen.blit(screen_hor, [0,0])
            self.screen.blit(screen_vert,[0,0])
            self.screen.blit(screen_vert,[974,0])
            self.screen.blit(keybox,     [0,650])
            self.screen.blit(box_hor,    [150,430])
            self.screen.blit(box_vert,   [150,430])
            self.screen.blit(box_vert,   [850,430])
            self.screen.blit(box_hor,    [150,560])
            
            
            # Blit the text
            self.screen.blit(title,     [(SCREEN_WIDTH//2) - (title.get_width()//2)       , 100])
            self.screen.blit(descr_1,   [(SCREEN_WIDTH//2) - (descr_1.get_width()//2)     , 200])
            self.screen.blit(descr_2,   [(SCREEN_WIDTH//2) - (descr_2.get_width()//2)     , 240])
            self.screen.blit(descr_3,   [(SCREEN_WIDTH//2) - (descr_3.get_width()//2)     , 280])
            self.screen.blit(rules,     [(SCREEN_WIDTH//2) - (rules.get_width()//2)       , 370])
            self.screen.blit(help_1,    [(SCREEN_WIDTH//2) - (help_1.get_width()//2)      , 450])
            self.screen.blit(help_2,    [(SCREEN_WIDTH//2) - (help_2.get_width()//2)      , 500])
            self.screen.blit(copyright, [(SCREEN_WIDTH//2)-(copyright.get_width()//2-310) , (SCREEN_HEIGHT-85)-(copyright.get_height()//2)])
            self.screen.blit(quit,      [(SCREEN_WIDTH//2)-(quit.get_width()//2-390)      , (SCREEN_HEIGHT-40)-(quit.get_height()//2)])
            
            # Update the screen
            pygame.display.flip()
        
        
        
        # Represents the Title Screen
        
        # Initialize everything for the screen
        font1 = pygame.font.SysFont("Comic Sans MS",50)
        font2 = pygame.font.SysFont("Comic Sans MS",40)
        font3 = pygame.font.SysFont("Comic Sans MS",15)
        font4 = pygame.font.SysFont("Comic Sans MS",25)
        
        welcome   = font1.render("Welcome to Flappy Mooh",True,WHITE)
        start     = font2.render("Press [Space]",True,WHITE)
        hgscore   = font4.render("[H] - Highscores",True,WHITE)
        copyright = font3.render("Game created by Florian Wirth",True,WHITE)
        help      = font4.render("[I] - Help",True,WHITE)
        quit      = font4.render("[Esc] - Quit",True,WHITE)
        
        
        screen_hor = pygame.Surface([1024,50])
        screen_vert = pygame.Surface([50,768])
        keybox = pygame.Surface([1024,118])
        
        screen_hor.fill(DARKGREEN)
        screen_vert.fill(DARKGREEN)
        keybox = pygame.Surface([1024,118])
        keybox.fill(DARKGREEN)
        
        
        # Blit everything on the screen
        self.screen.fill(GREEN)
        
        # Create borders for stylepoints
        self.screen.blit(screen_hor, [0,0])
        self.screen.blit(screen_vert,[0,0])
        self.screen.blit(screen_vert,[974,0])
        self.screen.blit(keybox,     [0,650])
        
        self.screen.blit(welcome,   [(SCREEN_WIDTH//2)-(welcome.get_width()//2)       , (100)])
        self.screen.blit(self.image,[(SCREEN_WIDTH//2-160)                            , (250)])
        self.screen.blit(copyright, [(SCREEN_WIDTH//2)-(copyright.get_width()//2-310) , (SCREEN_HEIGHT-85)-(copyright.get_height()//2)])
        self.screen.blit(start,     [(SCREEN_WIDTH//2)-(start.get_width()//2)         , (SCREEN_HEIGHT-200)-(start.get_height()//2)])
        self.screen.blit(hgscore,   [(SCREEN_WIDTH//2)-(hgscore.get_width()//2+360)   , (SCREEN_HEIGHT-40)-(hgscore.get_height()//2)])
        self.screen.blit(help,      [(SCREEN_WIDTH//2)-(help.get_width()//2-220)      , (SCREEN_HEIGHT-40)-(help.get_height()//2)])
        self.screen.blit(quit,      [(SCREEN_WIDTH//2)-(quit.get_width()//2-390)      , (SCREEN_HEIGHT-40)-(quit.get_height()//2)])
        
        # Update the screen
        pygame.display.flip()
        
    def process_events(self):
        """ Handle user inputs at the title screen"""
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return False
                if event.key == pygame.K_ESCAPE:
                    exit() 
                if event.key == pygame.K_i:
                    self.show_help_screen = True
                if event.key == pygame.K_h:
                    self.show_highscores = True
        
        return True
        
    def handle_help_screen(self):
        """ Handle user input to close the help screen """
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                        return False
            
        return True
    
    def handle_highscores(self):
        """ Handle user input to close the highscore screen """
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                        return False
            
        return True
   
    def update_scores(self,score_list):
        
        self.scored = score_list
                
# --- ShowGameOver Class
#
class GameOver():
    """ Represents the endgame screen, containing reached score """
    
    screen     = None
    score      = 0
    
    def __init__(self, screen, score):
        
        self.screen = screen
        self.score = score
        
        self.screen.fill(GREEN)
        
        font1 = pygame.font.SysFont("Comic Sans MS",50)
        font2 = pygame.font.SysFont("Comic Sans MS",40)
        font3 = pygame.font.SysFont("Comic Sans MS",30)
        font4 = pygame.font.SysFont("Comic Sans MS",25)
        
        welcome  = font1.render("GAME OVER!",True,WHITE)
        endscore = font2.render("You scored "+str(self.score)+" Cow-Points!",True,WHITE)
        restart  = font3.render("[Space] - Try Again",True,WHITE)
        quit     = font4.render("[Esc] - Back to Menu",True,WHITE)
        
        
        screen_hor = pygame.Surface([1024,50])
        screen_vert = pygame.Surface([50,768])
        keybox = pygame.Surface([1024,118])
        
        screen_hor.fill(DARKGREEN)
        screen_vert.fill(DARKGREEN)
        keybox.fill(DARKGREEN)
        
        deadcow = pygame.image.load("images/DeadCow.jpg")
        deadcow = pygame.transform.scale(deadcow,(250,250))
        deadcow = pygame.transform.flip(deadcow,1,0)
        
        # Create borders for stylepoints
        self.screen.blit(screen_hor, [0,0])
        self.screen.blit(screen_vert,[0,0])
        self.screen.blit(screen_vert,[974,0])
        self.screen.blit(keybox,     [0,650])
        
        self.screen.blit(deadcow,[SCREEN_WIDTH//2-125,200])
        
        self.screen.blit(welcome,  [(SCREEN_WIDTH//2)-(welcome.get_width()//2)     , (100)])
        self.screen.blit(endscore, [(SCREEN_WIDTH//2)-(endscore.get_width()//2)    , (SCREEN_HEIGHT//2+180)-(endscore.get_height()//2)])
        self.screen.blit(restart,  [(SCREEN_WIDTH//2)-(restart.get_width()//2+250) , (SCREEN_HEIGHT-60)-(restart.get_height()//2)])
        self.screen.blit(quit,     [(SCREEN_WIDTH//2)-(quit.get_width()//2-340)    , (SCREEN_HEIGHT-40)-(quit.get_height()//2)])
        


# --- ShowScoreboard Class
#
class ShowScoreboard():
    
    screen = None
    score  = 0
    gates_passed = 0
    
    def __init__(self,screen,score,gates_passed):
        
        self.screen = screen
        self.score = score
        self.gates_passed = gates_passed
        
        font    = pygame.font.SysFont("Comic Sans MS", 50)
        font2   = pygame.font.SysFont("Comic Sans MS", 20)
        title   = font2.render("Flappy Mooh",True, WHITE)
        label1  = font.render("Score: "+str(self.score), True, WHITE)
        label2  = font.render("Gates: "+str(self.gates_passed//2), True, WHITE)
        self.screen.blit(title,[SCREEN_WIDTH//2-title.get_width()//2,10])
        self.screen.blit(label1,[740,670])
        self.screen.blit(label2,[80,670])


# --- Highscores class
#
class Highscores():
    
    scores    = []
    filename  = ""
    
    def __init__(self):
        
        self.filename = "files/highscores.txt"
    
    def readdoc(self):
        
        file = open(self.filename, "r")
        for line in file:
             self.scores.append(int(line.strip()))
        file.close()
    
    def get(self):
        
        self.readdoc()
        return self.scores
         
    def safe_file(self,newscores):
        
        file = open(self.filename, "w")
        for entry in newscores:
            file.write(str(entry)+"\n")
        file.close()
            

# --- World Class
#
class World():
    """ Class to initialize the Cow-World """
        
    backgrounds = [None,None,None,None,None]
    
    world_shift = 0
    level_limit = 0
    world_limit = 0
    
    
    def __init__(self,player):
        """ Constructor function """
        
        self.player = player
        
        # Load the background 5 times, to blit it 5 times
        for i in range (5):
            self.backgrounds[i] = pygame.image.load("images/level.png").convert()
        
        #self.background.set_colorkey(BLACK)
        self.level_limit = 2400
        self.world_limit = 5 * self.level_limit
        
    
    def draw(self,screen):
        """ Draw everything of this world """
        
        # Win screen scrolls in after the game is done
        self.win_screen(screen,(self.world_limit+self.world_shift//2+400,200))
              
        # Blit the same background after one is passed
        for i in range(5):
            screen.blit(self.backgrounds[i],(i*self.level_limit+self.world_shift//2,50))
        
        screen_hor = pygame.Surface([1024,50])
        screen_vert = pygame.Surface([50,768])
        keybox = pygame.Surface([1024,118])
        
        screen_hor.fill(DARKGREEN)
        screen_vert.fill(DARKGREEN)
        keybox.fill(DARKGREEN)
        
        screen.blit(screen_hor, [0,0])
        screen.blit(screen_vert,[0,0])
        screen.blit(keybox,     [0,650])
        
    def shift_world(self,shift_x):
        """ When the player moves towards the end of the screen, scroll the world """
        
        self.world_shift += shift_x
        
        
    def win_screen(self,screen,pos):
        
        screen.fill(WHITE)
        
        font = pygame.font.SysFont("Comic Sans MS",50)
                
        you_win = font.render("YOU WIN!",True,BLACK)
        screen.blit(you_win, pos)
        
# ------------------------------------------------------------------------------
#                           --- End Classes ---
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
#                           --- Start Game Class ---
# This represents an instance of the game that is created. To reset the game
# simply create another instance of the game.
# ------------------------------------------------------------------------------

class Game():
    """ Represents one instance of the Game """
    
    # Local variables
    score          = 0
    gates_passed   = 0
    label          = None
    game_over      = False
    start          = True
    leftborder     = None
    
    # The Player
    player         = None
    
    # Sprite groups/lists
    obstacle_list  = None
    all_sprites    = None
        
    world = None
    
    # Initialize
    def __init__(self):
        """ Constructor function """
        
        self.score = 0
        self.gates_passed = 0
        self.game_over = False
        self.start = True
        self.highscores = Highscores()
        
        # Create sprite lists
        self.obstacle_list  = pygame.sprite.Group()
        self.all_sprites    = pygame.sprite.Group()
        
        # Create the player
        self.player         = Player()
        self.player.rect.x  = 70
        self.player.rect.y  = 55
        self.all_sprites.add(self.player)
        
        # Create Borders
        topborder = WindowBorders("top")
        bottomborder = WindowBorders("bottom")
        self.leftborder = WindowBorders("left")
        self.obstacle_list.add(topborder)
        self.obstacle_list.add(bottomborder)
        self.all_sprites.add(self.leftborder)
        
        # Load Level
        self.world = World(self.player)
        
    
    def process_events(self):    
        """ Handles user inputs and processes events"""
        
        # Event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.player.flap()
                if event.key == pygame.K_SPACE:
                    if self.game_over:
                        self.__init__()
            
        # Score is connected to the value of how far the world has been shifted
        self.score = -self.world.world_shift // 10
        
        # If the player gets near the right side, shift the world left (-x)
        if self.player.rect.right >= 350:
            diff = self.player.rect.right - 350
            self.player.rect.right = 350
            self.world.shift_world(-diff)

        # Check collisions
        obstacle_hit_list = pygame.sprite.spritecollide(self.player, self.obstacle_list, False)
        for hit in obstacle_hit_list: 
            self.game_over = True
        
        # Removes obstacles from the screen, after they hit the "border" on the left side of the screen
        obstacle_remove_list = pygame.sprite.spritecollide(self.leftborder,self.obstacle_list,True)
        for hit in obstacle_remove_list:
            self.gates_passed += 1
        
        return False
 
    
    def run_logic(self):
        """ updates the sprites """
        
        if not self.game_over:
            # Update the sprites
            self.obstacle_list.update()
            self.all_sprites.update()
            
        
    def display_frame(self, screen):
        """ Display the game """
        
        if self.game_over:
            GameOver(screen,self.score)
            
        if not self.game_over:
            self.world.draw(screen)
            self.obstacle_list.draw(screen)
            self.all_sprites.draw(screen)
            ShowScoreboard(screen,self.score,self.gates_passed)
        
        pygame.display.flip()
    
    
    def add_obstacles(self,difficulty):
        """ Adds obstacles to the screen """
        
        # "calculate" possible position of the hole
        if   difficulty == 1:
            value = random.randrange(200,250)
        elif difficulty == 2:
            value = random.randrange(140,300)
        elif difficulty == 3:
            value = random.randrange(75,468)
        elif difficulty == 4:
            value = random.randrange(75,468)
        else:
            value = random.randrange(75,468)

        # Used to add two surfaces (top AND bottom) at once (see obstacle class)
        self.obstacle_list.add(Obstacle("top",value,difficulty))
        self.obstacle_list.add(Obstacle("bot",value,difficulty))
        
        
    def return_score(self):
        """ Used to get current score in main() """
        
        return self.score
    
    def show_start(self):
        
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.player.flap()
                if event.key == pygame.K_ESCAPE:
                    if self.game_over:
                        self.__init__()    
                        return True
                if event.key == pygame.K_SPACE:
                    if self.game_over:
                        self.__init__()    
                        return False
        
        return False
    
    def safe_highscore(self):
        
        if self.game_over == True:
            return True
        
        return False
 
# ------------------------------------------------------------------------------
#                           --- End Game Class ---
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
#                           --- Start Main Function ---
# Used to run the program
# ------------------------------------------------------------------------------

def main():
    """ Main Program """
    
    # Pygame Init
    pygame.init()
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)
    pygame.mouse.set_visible(False)
    
    pygame.display.set_caption("Flappy Mooh")      
    
    # Create objects and set data
    done           = False               # if True: restart main() method
    clock          = pygame.time.Clock() # pygame.Clock
    game           = Game()              # game instance
    obstacle_timer = 0                   # loops through the program, used for generating obstacles
    difficulty     = 1                   # 1-5 (1 easiest, 5 hardest)
    start          = True                # only at first start
    highscores     = Highscores()
    score_list     = highscores.get()
    title_screen   = TitleScreen(screen,score_list) # titlescreen instance
    updatescores   = False
    safe_flag      = 1
    
    # Game loop
    while not done:
        
        # This part handles the highscore file and prints it on the screen
        updatescores = game.safe_highscore()
            
        if updatescores and safe_flag == 1:
            
            if game.return_score() > int(score_list[9]):
                score_list[9] = game.return_score()
                score_list = sorted(score_list,reverse=True)
                highscores.safe_file(score_list)
                title_screen.update_scores(score_list)
            
            highscores.safe_file(score_list)
            
            safe_flag = 0
        
        
        # TitleScreen loop 
        while start:

            # Draw title screen
            title_screen.draw()
            
            # Animates the title cow
            pygame.time.wait(400)
            title_screen.update()
            
            safe_flag = 1
            
            # Process events
            start = title_screen.process_events()
            
        start = game.show_start()
        
        # Process events (Exit, Keystrokes, etc)
        done = game.process_events()
        
        # Update object positions, check for collisions
        game.run_logic()
        
        # Draw the current frame
        game.display_frame(screen)
        
        # Pause for the next frame
        clock.tick(100)

        
        # Set the difficulty based on reached score
        if game.return_score() == 0:
            difficulty = 1        
        if game.return_score() == 200:
            difficulty = 2                
        elif game.return_score() == 600:
            difficulty = 3
        elif game.return_score() == 1000:
            difficulty = 4            
        elif game.return_score() == 2500:
            difficulty = 5
            
        # Add obstacles during runtime depending on difficulty
        if difficulty == 1 or 2:
            if obstacle_timer % 120 == 0:
                game.add_obstacles(difficulty)
        else:
            if obstacle_timer % 100 == 0:
                game.add_obstacles(difficulty)
                
        obstacle_timer += 1

# ------------------------------------------------------------------------------
#                           --- End Main Function ---
# ------------------------------------------------------------------------------


if __name__ == "__main__":
    main()