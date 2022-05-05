from typing import Tuple
from macce.envs.sprites.base import Missile

from pygame.rect import Rect


class ShipMissile(Missile):

    def __init__(self,
                 screen_size: Tuple[int, int],
                 rect: Rect,
                 speed: int = 5):
        super(ShipMissile, self).__init__(screen_size, rect, speed)

    def update(self):
        self.distance += self.speed

        if self.over_range():
            self.kill()
        else:
            self.rect.y -= self.speed
            if self.rect.y < 0:
                self.kill()
