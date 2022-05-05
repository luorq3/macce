from enum import IntEnum

from macce.envs.sprites.base import SpriteBase


class Movable:

    def __init__(self,
                 sprite: SpriteBase,
                 speed: int):
        super(Movable, self).__init__()
        self.rect = sprite.rect
        self.speed = speed
        self.max_rect = sprite.max_rect

    class Direction(IntEnum):
        UP, DOWN, LEFT, RIGHT = 1, 2, 3, 4

    def move(self, direction):
        if direction == self.Direction.UP:
            self._move_up()
        elif direction == self.Direction.DOWN:
            self._move_down()
        elif direction == self.Direction.LEFT:
            self._move_left()
        elif direction == self.Direction.RIGHT:
            self._move_right()

    def _move_up(self):
        if self.rect.y > self.speed:
            self.rect.y -= self.speed
        else:
            self.rect.y = 0

    def _move_down(self):
        if self.rect.y < self.max_rect[1]:
            self.rect.y += self.speed
        else:
            self.rect.y = self.max_rect[1]

    def _move_left(self):
        if self.rect.x > self.speed:
            self.rect.x -= self.speed
        else:
            self.rect.x = 0

    def _move_right(self):
        if self.rect.x < self.max_rect[0]:
            self.rect.x += self.speed
        else:
            self.rect.x = self.max_rect[0]
