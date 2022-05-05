from macce.env.sprites.base import Missile

from pygame.rect import Rect


class ShipMissile(Missile):

    def __init__(self,
                 rect: Rect,
                 speed: int = 5):
        super(ShipMissile, self).__init__(rect, speed)

    def update(self):
        self.distance += self.speed

        if self.over_range():
            self.kill()
        else:
            self.rect.y -= self.speed
            if self.rect.y < 0:
                self.kill()
