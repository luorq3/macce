from typing import Tuple

import pygame
from macce.env.utils import load_images

# Sea blue
FILL_BACKGROUND_COLOR = (135, 206, 235)
# Black
# FILL_BACKGROUND_COLOR = (0, 0, 0)


class Renderer:

    def __init__(self, screen_size: Tuple[int, int], *groups):
        self._screen_width = screen_size[0]
        self._screen_height = screen_size[1]

        self.display = None
        self.surface = pygame.Surface(screen_size)

        self.images = load_images(convert=False)

        self.attacker_group = groups[0]
        self.defender_group = groups[1]
        self.attacker_missile_group = groups[2]
        self.defender_missile_group = groups[3]

        self._clock = pygame.time.Clock()

    def make_display(self) -> None:
        self.display = pygame.display.set_mode((self._screen_width, self._screen_height))
        for name, value in self.images.items():
            if value is None:
                continue

            if type(value) in (tuple, list):
                self.images[name] = tuple([img.convert_alpha() for img in value])
            else:
                self.images[name] = (value.convert() if name == "background" else value.convert_alpha())

    def draw_surface(self) -> None:
        if self.images["background"] is not None:
            self.surface.blit(self.images["background"], (0, 0))
        else:
            self.surface.fill(FILL_BACKGROUND_COLOR)

        pygame.draw.circle(self.surface, (233, 150, 122), (self._screen_width / 2, 0), 224)

        for ship in self.attacker_group.sprites():
            self.surface.blit(pygame.transform.rotate(self.images['ship'], ship.angle()), ship.rect[:2])
        for fort in self.defender_group.sprites():
            # self.surface.blit(pygame.transform.rotate(self.images['fort'], fort.angle),
            #                   fort.rect[:2])
            self.surface.blit(self.images['fort'], fort.rect[:2])

        for missile in self.attacker_missile_group.sprites():
            self.surface.blit(self.images['ship_missile'], missile.rect[:2])

        for missile in self.defender_missile_group.sprites():
            self.surface.blit(pygame.transform.rotate(self.images['fort_missile'], missile.angle),
                              missile.rect[:2])

    def update_display(self):
        if self.display is None:
            raise RuntimeError(
                "Tried to update the display, but a display hasn't been "
                "created yet! To create a display for the renderer, you must "
                "call the `make_display()` method."
            )

        self.display.blit(self.surface, [0, 0])
        pygame.display.update()
