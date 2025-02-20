import pygame
from random import randint
from sprites import Star, Player, Meteor
from collision_handler import PlayerMeteorCollision, LaserMetorCollision
from constants import SCORE_UPDATE


#Right now this only shows the time in seconds so have to fix it.
def display_score(score):
    current_time = int(pygame.time.get_ticks()/1000)
    color = (240,240,240)
    text_surf = font.render(str(score), True, color=color)
    text_rect = text_surf.get_frect(midbottom = (WINDOW_WIDTH/2,WINDOW_HEIGHT-50))
    pygame.draw.rect(display_surface, color, text_rect.inflate(20,20).move(0,-4), 5,10)
    display_surface.blit(text_surf, text_rect)
    

#general setup
pygame.init()
pygame.display.set_caption("Space Shooter 🌠")

# Window
DISPLAY_INFO = pygame.display.Info()
WINDOW_WIDTH, WINDOW_HEIGHT = DISPLAY_INFO.current_w - 100, DISPLAY_INFO.current_h - 100
SPACE_COLOR = (11, 11, 69)
NUMBER_STARS = 20

clock = pygame.time.Clock()
score = 0

#surfaces
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
star_surface = pygame.image.load("./images/star.png").convert_alpha()
meteor_surface = pygame.image.load("./images/meteor.png").convert_alpha()
font = pygame.font.Font("./images/Oxanium-Bold.ttf", 20)

#sound
laser_sound = pygame.mixer.Sound("./audio/laser.wav")
meteor_explosion_sound = pygame.mixer.Sound("./audio/explosion.wav")
damage_sound = pygame.mixer.Sound("./audio/damage.ogg")

#sprites
all_sprites = pygame.sprite.Group()
meteor_sprites = pygame.sprite.Group()
laser_sprites = pygame.sprite.Group()
for i in range(NUMBER_STARS):
    Star(all_sprites, star_surface, (WINDOW_WIDTH, WINDOW_HEIGHT))
player = Player(all_sprites, laser_sprites, (WINDOW_WIDTH, WINDOW_HEIGHT),
                laser_sound)

#meteor event
meteor_event = pygame.event.custom_type()
pygame.time.set_timer(meteor_event, 1000)
player_meteor_collision = PlayerMeteorCollision(player, meteor_sprites, 
                                                damage_sound)
laser_meteor_collision = LaserMetorCollision(laser_sprites, meteor_sprites,
                                             all_sprites, meteor_explosion_sound)

#check if game is running
running = True
while running:
    dt = clock.tick() / 1000

    for event in pygame.event.get():
        #Checks if we have quit the game
        if event.type == pygame.QUIT:
            running = False
        #Creates a meteor in a random location and adds it to two groups
        if event.type == meteor_event:
            x,y = randint(0, WINDOW_WIDTH), randint(-200,-100)
            meteor = Meteor((all_sprites, meteor_sprites), meteor_surface, (x,y))
            meteor_sprites.add(meteor)
        if event.type == SCORE_UPDATE:
            score += event.points
            print("test")

    #updates
    all_sprites.update(dt)
    player_meteor_collision.update()
    laser_meteor_collision.update()
    
    #background display
    display_surface.fill(SPACE_COLOR)

    all_sprites.draw(display_surface)
    display_score(score)

    #draw the display surface
    pygame.display.update()

pygame.quit()
