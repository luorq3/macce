from enum import Enum, IntEnum

import pygame.sprite
import yaml

from macce.env.sprites import Ship
from macce.env.sprites import Fort
from macce.env.utils import *


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


def load_setting(file):
    path = f'setting/{file}.yaml'
    file = open(path, 'r')
    return yaml.safe_load(file.read())


def get_setting(game_version):
    return load_setting('scenarios')[game_version]


class Game:

    def __init__(self, game_version='2s_vs_2f'):
        self._screen_size = screen_size

        # load setting
        setting = get_setting(game_version)

        # game setting
        self.name = setting['name']

        # Sprite group
        self.attacker_group = pygame.sprite.Group()
        self.defender_group = pygame.sprite.Group()
        self.attacker_missile_group = pygame.sprite.Group()
        self.defender_missile_group = pygame.sprite.Group()

        # Create sprites
        self._init(setting)

        # hit mask
        # self.ship_mask = get_hitmask(images["ship"])
        # self.fort_mask = get_hitmask(images["fort"])
        # self.ship_missile_mask = get_hitmask(images["ship_missile"])
        # self.fort_missile_mask = get_hitmask(images["fort_missile"])

    def _init(self, setting):
        attacker = setting.get(self.ConsType.ATTACKER)
        if attacker.get(self.SpriteType.SHIP) is not None:
            ship = attacker[self.SpriteType.SHIP]
            ships = self._create_sprite(self.SpriteType.SHIP, **ship)
            self.attacker_group.add(ships)

        defender = setting.get(self.ConsType.DEFENDER)
        if defender.get(self.SpriteType.FORT) is not None:
            fort = defender[self.SpriteType.FORT]
            forts = self._create_sprite(self.SpriteType.FORT, **fort)
            self.attacker_group.add(forts)

    def _create_sprite(self, sprite_type, **kwargs):
        sprites = []
        if sprite_type == self.SpriteType.SHIP:
            coords = _ship_init_position(kwargs.get('number'))
            for x, y in coords:
                ship = Ship(Rect(x, y, *ship_size), self.attacker_missile_group)
                sprites.append(ship)

        elif sprite_type == self.SpriteType.FORT:
            coords = _fort_init_position(kwargs.get('number'))
            for x, y in coords:
                fort = Fort(Rect(x, y, *fort_size), self.defender_missile_group)
                sprites.append(fort)
        else:
            raise ValueError(f'Tried to create a {sprite_type} sprite,'
                             'but without such a sprite!')

        return sprites

    class ConsType(Enum):
        ATTACKER, DEFENDER = 'attacker', 'defender'

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
