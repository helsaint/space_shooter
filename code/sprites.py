import pygame
from random import randint, uniform


class Player(pygame.sprite.Sprite):

    def __init__(self, groups, laser_group, window_dimension, laser_sound):
        super().__init__(groups)
        self.all_sprites = groups
        self.laser_group = laser_group
        self.laser_sound = laser_sound
        self.image = pygame.image.load("./images/player.png").convert_alpha()
        self.rect = self.image.get_frect(
            center=(window_dimension[0]/2, window_dimension[1]/2))
        self.direction = pygame.Vector2(0,0)
        self.speed = 300
        self.laser_surface = pygame.image.load("./images/laser.png").convert_alpha()

        #Laser Cooldown
        self.can_shoot = True
        self.laser_shoot_time = 0
        self.cooldown_duration = 500

        #mask
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        self.direction = self.direction.normalize() if self.direction else self.direction
        self.rect.center += self.direction * self.speed * dt

        recent_keys = pygame.key.get_just_pressed()
        if recent_keys[pygame.K_SPACE] and self.can_shoot:
            laser = Laser(self.laser_surface, self.rect.midtop)
            self.all_sprites.add(laser)
            self.laser_group.add(laser)
            self.laser_sound.play()
            self.can_shoot = False
            self.laser_shoot_time = pygame.time.get_ticks()
            print(laser)
        
        self.laser_timer()

    def laser_timer(self):
        if not(self.can_shoot):
            current_time = pygame.time.get_ticks()
            if (current_time - self.laser_shoot_time > self.cooldown_duration):
                self.can_shoot = True

class Star(pygame.sprite.Sprite):
    def __init__(self, groups, star_surface, window_dimension):
        super().__init__(groups)
        self.image = star_surface
        self.rect = self.image.get_frect(
            center=(randint(0,window_dimension[0]),randint(0, window_dimension[1])))
        
class Meteor(pygame.sprite.Sprite):
    def __init__(self, groups, meteor_surface, position):
        super().__init__(groups)
        self.original_surface = meteor_surface
        self.image = meteor_surface
        self.rect = self.image.get_frect(
            center=(position[0], position[1])
        )
        self.creation_time = pygame.time.get_ticks()
        self.life_time = 3000
        self.direction = pygame.Vector2(uniform(-0.5,0.5), 1)
        self.speed = randint(400,500)
        self.rotation_speed = randint(40,80)
        self.rotation = 0

        #mask
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, dt):
        self.rect.center += self.direction * self.speed * dt
        self.rotation += self.rotation_speed * dt
        if (pygame.time.get_ticks() - self.creation_time > self.life_time):
            self.kill()
        self.image = pygame.transform.rotozoom(self.original_surface, self.rotation,1)
        self.rect = self.image.get_frect(center=self.rect.center)

class Laser(pygame.sprite.Sprite):
    def __init__(self, laser_surface, position):
        super().__init__()
        self.image = laser_surface
        self.rect = self.image.get_frect(
            midbottom=position
        )

        #mask
        self.mask = pygame.mask.from_surface(self.image)
    
    def update(self, dt):
        self.rect.centery -= 400 * dt
        if self.rect.bottom < 0:
            self.kill()

class AnimatedExplosions(pygame.sprite.Sprite):
    def __init__(self, groups, frames, position):
        super().__init__(groups)
        self.index = 0
        self.image = frames[self.index]
        self.frames = frames
        self.rect = self.image.get_frect(center = position)

    def update(self, dt):
        self.index += 20*dt
        if (self.index < len(self.frames)):
            self.image = self.frames[int(self.index)]
        else:
            self.kill()