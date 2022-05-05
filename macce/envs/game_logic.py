from enum import Enum, IntEnum
from typing import Tuple

import pygame.sprite

from macce.envs.sprites import Ship
from macce.envs.sprites import Fort
from macce.envs.utils import *

"""
炮台均匀分布在防守方陆地上
(x - 448)^2 + y^2 = 210^2
    from x to y
"""
def _fort_init_position(nums):
    coords = []
    x = fort_beach_rect.x
    gap = fort_beach_rect.width / (nums + 1)
    for i in range(nums):
        x += gap
        y = math.sqrt(210 ** 2 - (x - 448) ** 2)
        coords.append((x, y))

    return coords


def _ship_init_position(nums):
    coords = []
    x = 0
    gap = 856 / (nums + 1)
    for i in range(nums):
        x += gap
        y = ship_init_rect.y
        coords.append((x, y))

    return coords


class GameLogic:

    def __init__(self, images, screen_size: Tuple[int, int], ship_num=2, fort_num=2):
        self._screen_size = screen_size

        # Sprite group
        self.ship_group = pygame.sprite.Group()
        self.fort_group = pygame.sprite.Group()
        self.ship_missile_group = pygame.sprite.Group()
        self.fort_missile_group = pygame.sprite.Group()

        # hit mask
        self.ship_mask = get_hitmask(images["ship"])
        self.fort_mask = get_hitmask(images["fort"])
        self.ship_missile_mask = get_hitmask(images["ship_missile"])
        self.fort_missile_mask = get_hitmask(images["fort_missile"])

        # Create sprite
        self._create_sprite(self.SpriteType.SHIP, ship_num)
        self._create_sprite(self.SpriteType.FORT, fort_num)

    def _create_sprite(self, sprite_type, nums):
        if sprite_type == self.SpriteType.SHIP:
            coords = _ship_init_position(nums)
            for x, y in coords:
                ship = Ship(self._screen_size, Rect(x, y, *ship_size), self.ship_missile_group)
                self.ship_group.add(ship)

        elif sprite_type == self.SpriteType.FORT:
            coords = _fort_init_position(nums)
            for x, y in coords:
                fort = Fort(self._screen_size, Rect(x, y, *fort_size), self.fort_missile_group)
                self.fort_group.add(fort)
        else:
            raise ValueError(f'Tried to create a {sprite_type} sprite,'
                             'but without such a sprite!')

    class SpriteType(Enum):
        SHIP, FORT = 'ship', 'fort'

    class Reward(IntEnum):
        FIRE, HIT, BE_HIT, DESTROY, BE_DESTROY, VICTORY, DEFEATED = 0, 1, -1, 2, -2, 3, -3

    def update_state(self, actions: list):
        ship_actions = actions[0]
        fort_actions = actions[1]

        alive = True
        reward = [0] * 2
        reward_list = [[]] * 2
        print(f"update_state start, reward:{reward}")

        self.ship_missile_group.update()
        self.fort_missile_group.update()

        ships = self.ship_group.sprites()
        forts = self.fort_group.sprites()
        ship_missiles = self.ship_missile_group.sprites()
        fort_missiles = self.fort_missile_group.sprites()

        for ship, action in zip(ships, ship_actions):
            if action in [1, 2, 3, 4]:
                ship.move(action)
            elif action == 5:
                ship.fire()

        for fort, action in zip(forts, fort_actions):
            if action in [1, 2]:
                fort.turn(action)
            elif action == 3:
                fort.fire()

        # Collision check
        # 1.Was Fort be hit
        for fort in forts:
            if not fort.alive():
                continue
            for missile in ship_missiles:
                if not missile.alive():
                    continue
                collided = pixel_collision(fort.rect, missile.rect, self.fort_mask, self.ship_missile_mask)
                if collided:
                    missile.kill()
                    fort.hp -= 1
                    reward[0] += self.Reward.HIT
                    reward[1] += self.Reward.BE_HIT
                    reward_list[0].append(self.Reward.HIT)
                    reward_list[1].append(self.Reward.BE_HIT)
                    if fort.hp == 0:
                        fort.kill()
                        reward[0] += self.Reward.DESTROY
                        reward[1] += self.Reward.BE_DESTROY
                        reward_list[0].append(self.Reward.DESTROY)
                        reward_list[1].append(self.Reward.BE_DESTROY)
                    # When victory, jump out of the loops to avoid calculating the wrong reward
                    if len(self.fort_group.sprites()) == 0:
                        reward[0] += self.Reward.VICTORY
                        reward[1] += self.Reward.DEFEATED
                        reward_list[0].append(self.Reward.VICTORY)
                        reward_list[1].append(self.Reward.DEFEATED)
                        alive = False
                        break

        # 2.Was Ship be hit
        for ship in ships:
            if not ship.alive():
                continue
            for missile in fort_missiles:
                if not missile.alive():
                    continue
                collided = pixel_collision(ship.rect, missile.rect, self.ship_mask, self.fort_missile_mask)
                if collided:
                    missile.kill()
                    ship.hp -= 1
                    reward[0] += self.Reward.BE_HIT
                    reward[1] += self.Reward.HIT
                    reward_list[0].append(self.Reward.BE_HIT)
                    reward_list[1].append(self.Reward.HIT)
                    if ship.hp == 0:
                        ship.kill()
                        reward[0] += self.Reward.BE_DESTROY
                        reward[1] += self.Reward.DESTROY
                        reward_list[0].append(self.Reward.BE_DESTROY)
                        reward_list[1].append(self.Reward.DESTROY)
                    if len(self.ship_group.sprites()) == 0:
                        reward[0] += self.Reward.DEFEATED
                        reward[1] += self.Reward.VICTORY
                        reward_list[0].append(self.Reward.DEFEATED)
                        reward_list[1].append(self.Reward.VICTORY)
                        alive = False
                        break

        print(f"update_state end, reward:{reward}")
        print(f"reward list:{reward_list}")

        return reward, alive
