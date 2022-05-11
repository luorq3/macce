from macce.env.sprites.base import SpriteBase, Movable
from macce.env.sprites import Missile
from macce.env.utils import *

import pygame

# TODO: ship 不能移动到陆地上
class Ship(SpriteBase, Movable):

    def __init__(self,
                 aorf: str,  # defender or attacker
                 rect: Rect,
                 missile_group: pygame.sprite.Group,
                 speed: int = 10,
                 hp: int = 5):
        SpriteBase.__init__(self, aorf, rect)
        Movable.__init__(self, self, speed)
        self.hp = hp
        self.missile_group = missile_group

    def fire(self):
        missile = Missile(Rect(*self.get_center_coord(), *ship_missile_size))
        self.missile_group.add(missile)

    def handle(self, action):
        pass
