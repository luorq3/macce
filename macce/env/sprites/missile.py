from abc import ABC
from typing import Any

from pygame.rect import Rect
from macce.env.sprites.base import SpriteBase


class Missile(SpriteBase, ABC):

    def __init__(self,
                 aorf,
                 rect: Rect,
                 speed: int = 5,
                 **kwargs
                 ):
        super(Missile, self).__init__(aorf, rect)
        self.glide_range = kwargs['range']
        self.damage = kwargs['damage']
        self.interval = kwargs['interval']
        self.loadage = kwargs['loadage']
        self.penalty = kwargs['penalty']
        self.speed = speed
        self.distance = 0
        self.fix_coord()

    def fix_coord(self):
        real_coord = [i - j / 2 for i, j in zip(self.rect[:2], self.rect[2:])]
        self.rect = Rect(*real_coord, *self.rect[2:])

    def over_range(self):
        return self.distance > self.glide_range

    def update(self, *args: Any, **kwargs: Any) -> None:
        raise NotImplementedError(f"Tried to call `Missile.update()`,"
                                  f" but it hasn't been implemented yet!")
