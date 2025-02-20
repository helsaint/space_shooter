import pygame
from sprites import AnimatedExplosions
from constants import SCORE_UPDATE

class PlayerMeteorCollision:
    def __init__(self, player, meteor, damage_sound):
        self.player = player
        self.meteor = meteor
        self.damage_sound = damage_sound

    def update(self):
        meteor_hits = pygame.sprite.spritecollide(
            self.player, self.meteor, True,pygame.sprite.collide_mask
        )
        if(meteor_hits):
            self.damage_sound.play()

class LaserMetorCollision:
    def __init__(self, laser, meteor, all_sprites, meteor_explosion_sound):
        self.laser = laser
        self.meteor = meteor
        self.meteor_explosion_sound = meteor_explosion_sound
        self.all_sprites = all_sprites
        self.explosion_frames =[pygame.image.load(f"./images/explosion/{i}.png").convert_alpha()
                    for i in range(21)]

    def update(self):
        laser_hits = pygame.sprite.groupcollide(
            self.laser, self.meteor, True, True,pygame.sprite.collide_mask
        )
        if laser_hits:
            points = 1
            score_event = pygame.event.Event(SCORE_UPDATE, points=points)
            pygame.event.post(score_event)
            for key, value in laser_hits.items():
                AnimatedExplosions(self.all_sprites, self.explosion_frames, 
                                   key.rect.midtop)
                self.meteor_explosion_sound.play()