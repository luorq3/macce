from macce.env.sprites.base import SpriteBase
from macce.env.sprites.missile import Missile
from macce.env.utils import *

import pygame


class Ship(SpriteBase):

    def __init__(self,
                 aorf: str,  # defender or attacker
                 index,
                 rect: Rect,
                 n_enemies,
                 missile_group: pygame.sprite.Group,
                 turn_angle: float = 5, **kwargs):
        SpriteBase.__init__(self, aorf, rect)
        self.health = kwargs['health'] if isinstance(kwargs['health'], int) else kwargs['health'][index]
        self.missile_group = missile_group
        self.speed = kwargs['speed'] if isinstance(kwargs['speed'], int) else kwargs['speed'][index]
        self.interval = kwargs['fire_interval'] if isinstance(kwargs['fire_interval'], int) else kwargs['fire_interval'][index]
        self.radian = math.pi
        self.turn_angle = turn_angle
        self.n_enemies = n_enemies
        missile_class = [kwargs['missile_class']] if isinstance(kwargs['missile_class'], int) else kwargs['missile_class']
        self.missile_class_num = len(missile_class)
        missile_loadage = [kwargs['missile_loadage']] if isinstance(kwargs['missile_loadage'], int) else kwargs['missile_loadage']
        missile_conf = get_weapon()['missile']
        self.missiles = []
        for i, loadage in zip(missile_class, missile_loadage):
            missile = Missile(aorf, self.rect, loadage=loadage, **missile_conf[i])
            self.missiles.append(missile)
        self.fire_count = 0
        self.max_action = self.n_enemies * self.missile_class_num
        self.miss_prob = [kwargs['miss_prob']] if isinstance(kwargs['miss_prob'], int) else kwargs['miss_prob']

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
        self.fire_count = (self.fire_count + 1) % self.interval

        if action == 0:
            return 0

        if action == 1:
            self.move_forward()
        else:
            self.turn(action % 2)

        return 0

    def angle(self):
        return radian_to_angle(self.radian)

    def get_missile_nums(self):
        return [missile.loadage for missile in self.missiles]

    def can_fire(self):
        return self.fire_count % self.interval

    def action_to_enemy(self, action):
        action -= 4
        assert (action < self.max_action), f"Action {action + 4} doesn't exist."

        enemy, missile = action % self.n_enemies, action // self.n_enemies
        return enemy, missile

    @staticmethod
    def not_fire_action_space():
        return [0, 1, 2, 3]
