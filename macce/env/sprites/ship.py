from macce.env.sprites.base import SpriteBase
from macce.env.sprites.missile import Missile
from macce.env.utils import *

import pygame


class Ship(SpriteBase):

    def __init__(self,
                 aorf: str,  # defender or attacker
                 rect: Rect,
                 missile_group: pygame.sprite.Group,
                 speed: int = 10,
                 hp: int = 5):
        SpriteBase.__init__(self, aorf, rect)
        self.hp = hp
        self.missile_group = missile_group
        self.speed = speed
        self.distance = 0
        self.radian = 0

    def fire(self):
        missile = Missile(Rect(*self.get_center_coord(), *ship_missile_size))
        self.missile_group.add(missile)

    def move_forward(self):
        pass

    def turn(self, turn_up):
        pass

    def handle(self, action):
        if action == 1:
            self.move_forward()
        elif action == 2 or action == 3:
            self.turn(action % 2)
        else:
            self.fire()

