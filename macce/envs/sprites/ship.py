from typing import Tuple
from macce.envs.sprites.base import SpriteBase, Movable
from macce.envs.sprites.ship_missile import ShipMissile
from macce.envs.utils import *

import pygame

# TODO: ship 不能移动到陆地上
class Ship(SpriteBase, Movable):

    def __init__(self,
                 screen_size: Tuple[int, int],
                 rect: Rect,
                 missile_group: pygame.sprite.Group,
                 speed: int = 10,
                 hp: int = 5):
        SpriteBase.__init__(self, screen_size, rect)
        Movable.__init__(self, self, speed)
        self.hp = hp
        # self.missile_group = pygame.sprite.Group()
        self.missile_group = missile_group

    def fire(self):
        missile = ShipMissile(self.screen_size, Rect(*self.get_center_coord(), *ship_missile_size))
        self.missile_group.add(missile)

    # def handle(self, action):
    #     reward = 0
        # if action in [1, 2, 3, 4]:
        #     self.move(action)
        # if action == 5:
        #     self.fire()
        #
        # return 0


# s = Ship(pygame.surface.Surface((10, 10)), (50, 50), (10, 10), (0, 0))
