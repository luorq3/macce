from typing import Tuple

from pygame.rect import Rect
from pygame.sprite import Sprite


screen_size: Tuple[int, int] = (896, 896)

class SpriteBase(Sprite):

    def __init__(self, aorf: str, rect: Rect):
        super(SpriteBase, self).__init__()
        self.aorf = aorf
        self.screen_size = screen_size
        self.rect = rect
        self.center = self.get_center_coord()
        size = (self.rect.width, self.rect.height)
        self.max_rect = [screen - size for screen, size in zip(self.screen_size, size)]

    def get_center_coord(self):
        return [i + j / 2 for i, j in zip(self.rect[:2], self.rect[2:])]

    def is_attacker(self):
        return self.aorf == 'attacker'

    def is_defender(self):
        return self.aorf == 'defender'

    def handle(self, action):
        raise NotImplementedError(f"Tried to call `Missile.update()`,"
                                  f" but it hasn't been implemented yet!")
