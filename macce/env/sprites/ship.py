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
                 hp: int = 5,
                 turn_radian: int = 5):
        SpriteBase.__init__(self, aorf, rect)
        self.hp = hp
        self.missile_group = missile_group
        self.init_rect = rect.copy()
        self.speed = speed
        self.distance = 0
        self.radian = 0
        self.turn_radian = turn_radian

    def fire(self):
        missile = Missile(Rect(*self.get_center_coord(), *ship_missile_size))
        self.missile_group.add(missile)

    def move_forward(self):
        self.distance += self.speed

        offset_x = self.distance * math.sin(self.radian)
        offset_y = self.distance * math.cos(self.radian)

        if 0 < self.init_rect.x + offset_x < self.max_rect[0] \
                and 0 < self.init_rect.y + offset_y < self.max_rect[1]:
            self.rect.x = self.init_rect.x + offset_x
            self.rect.y = self.init_rect.y + offset_y
        else:
            self.kill()

    def turn(self, turn_right):
        if turn_right:
            radian = self.turn_radian
        else:
            radian = -self.turn_radian
        self.radian += radian

    def handle(self, action):
        if action == 1:
            self.move_forward()
        elif action == 2 or action == 3:
            self.turn(action % 2)
        else:
            # self.fire()
            print("fire!!!")
