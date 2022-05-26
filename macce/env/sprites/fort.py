import pygame

from macce.env.sprites.base import SpriteBase
from macce.env.sprites.missile import Missile
from macce.env.utils import *


class Fort(SpriteBase):

    def __init__(self,
                 aorf: str,
                 index,
                 rect: Rect,
                 n_enemies,
                 missile_group: pygame.sprite.Group,
                 **kwargs):
        super(Fort, self).__init__(aorf, rect)
        self.health = kwargs['health'] if isinstance(kwargs['health'], int) else kwargs['health'][index]
        self.missile_group = missile_group
        self.interval = kwargs['fire_interval'] if isinstance(kwargs['fire_interval'], int) else kwargs['fire_interval'][index]
        self.n_enemies = n_enemies
        missile_class = [kwargs['missile_class']] if isinstance(kwargs['missile_class'], int) else kwargs['missile_class']
        self.missile_class_num = len(missile_class)
        missile_loadage = [kwargs['missile_loadage']] if isinstance(kwargs['missile_loadage'], int) else kwargs['missile_loadage']
        missile_conf = get_weapon()['missile']
        self.missiles = []
        for i, loadage in zip(missile_class, missile_loadage):
            missile = Missile(aorf, self.rect, loadage=loadage, **missile_conf[i])
            self.missiles.append(missile)
        self.miss_prob = [kwargs['miss_prob']] if isinstance(kwargs['miss_prob'], int) else kwargs['miss_prob']
        self.fire_count = 0
        self.max_action = self.n_enemies * self.missile_class_num
        self.miss_prob = [kwargs['miss_prob']] if isinstance(kwargs['miss_prob'], int) else kwargs['miss_prob']
        # self.angle = 0
        # self.radian = 0
        # self.turn_speed = 5

    def handle(self, action):
        self.fire_count = (self.fire_count + 1) % self.interval
        return 0

    # def update(self, target_x, target_y, *args: Any, **kwargs: Any) -> None:
    #     offset_x = target_x - self.rect.x
    #     offset_y = target_y - self.rect.y
    #
    #     self.radian = math.atan2(offset_x, offset_y)
    #
    #     self.angle = int(self.radian * 180 / math.pi)

    def get_missile_nums(self):
        return [missile.loadage for missile in self.missiles]

    def can_fire(self):
        return self.fire_count % self.interval

    def action_to_enemy(self, action):
        action -= 1
        assert (action < self.max_action), f"Action {action + 4} doesn't exist."

        enemy, missile = action % self.n_enemies, action // self.n_enemies
        return enemy, missile

    @staticmethod
    def not_fire_action_space():
        return [0]
