import pygame

from macce.envs.sprites.base import SpriteBase
from macce.envs.sprites.fort_missile import FortMissile
from macce.envs.utils import *


class Fort(SpriteBase):

    def __init__(self,
                 rect: Rect,
                 missile_group: pygame.sprite.Group,
                 hp: int = 5,
                 turn_speed: int = 5):
        super(Fort, self).__init__(rect)
        self.hp = hp
        self.angle = 0
        self.radian = 0
        self.missile_group = missile_group
        self.turn_speed = turn_speed

    def fire(self):
        missile = FortMissile(
            self.screen_size,
            Rect(*self.get_center_coord(), *fort_missile_size),
            self.radian, self.angle)
        self.missile_group.add(missile)

    def update(self, target_x, target_y, *args: Any, **kwargs: Any) -> None:
        offset_x = target_x - self.rect.x
        offset_y = target_y - self.rect.y

        self.radian = math.atan2(offset_x, offset_y)

        self.angle = int(self.radian * 180 / math.pi)

    def turn(self, action):
        if action == 1:
            self.angle -= self.turn_speed
        elif action == 2:
            self.angle += self.turn_speed

        self.radian = self.angle * math.pi / 180
