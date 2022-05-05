from typing import Tuple

import pygame
from pygame.rect import Rect


class SpriteBase(pygame.sprite.Sprite):

    def __init__(self,
                 screen_size: Tuple[int, int],
                 rect: Rect):
        super(SpriteBase, self).__init__()
        self.screen_size = screen_size
        self.rect = rect
        self.center = [0, 0]
        size = (self.rect.width, self.rect.height)
        self.max_rect = [screen - size for screen, size in zip(self.screen_size, size)]

    def get_center_coord(self):
        return [i + j / 2 for i, j in zip(self.rect[:2], self.rect[2:])]
