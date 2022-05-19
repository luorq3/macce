from macce.env.sprites.base import SpriteBase
from macce.env.sprites.missile import Missile
from macce.env.utils import *

import pygame


class Ship(SpriteBase):

    def __init__(self,
                 aorf: str,  # defender or attacker
                 index,
                 rect: Rect,
                 missile_group: pygame.sprite.Group,
                 turn_angle: float = 5, **kwargs):
        SpriteBase.__init__(self, aorf, rect)
        self.health = kwargs['health'][index]
        self.missile_group = missile_group
        self.speed = kwargs['speed'][index]
        self.radian = math.pi
        self.turn_angle = turn_angle

    def fire(self, enemy):
        # missile = Missile(Rect(*self.get_center_coord(), *ship_missile_size))
        # self.missile_group.add(missile)
        pass

    def move_forward(self):

        offset_x = self.speed * math.sin(self.radian)
        offset_y = self.speed * math.cos(self.radian)

        if 0 < self.rect.x + offset_x < self.max_rect[0] \
                and 0 < self.rect.y + offset_y < self.max_rect[1]:
            self.rect.x = self.rect.x + offset_x
            self.rect.y = self.rect.y + offset_y
        else:
            self.kill()

    def turn(self, turn_right):
        if turn_right:
            radian = angle_to_radian(self.turn_angle)
        else:
            radian = -angle_to_radian(self.turn_angle)
        self.radian += radian

    def handle(self, action):
        if action == 0:
            return
        elif action == 1:
            self.move_forward()
        elif action == 2 or action == 3:
            self.turn(action % 2)
        else:
            self.fire(action)

    def angle(self):
        return radian_to_angle(self.radian)

    # todo 返回数组分别表示各种炮弹数量
    def get_bombs_num(self):
        pass

    # todo 攻击间隔
    def can_fire(self):
        pass
