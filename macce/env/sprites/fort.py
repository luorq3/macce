import pygame

from macce.env.sprites.base import SpriteBase
from macce.env.sprites.missile import Missile
from macce.env.utils import *


class Fort(SpriteBase):

    def __init__(self,
                 aorf: str,
                 index,
                 rect: Rect,
                 missile_group: pygame.sprite.Group,
                 **kwargs):
        super(Fort, self).__init__(aorf, rect)
        self.health = kwargs['health'] if isinstance(kwargs['health'], int) else kwargs['health'][index]
        self.angle = 0
        self.radian = 0
        self.missile_group = missile_group
        # self.turn_speed = 5
        bomb_class = [kwargs['bomb_class']] if isinstance(kwargs['bomb_class'], int) else kwargs['bomb_class']
        bomb_loadage = [kwargs['bomb_loadage']] if isinstance(kwargs['bomb_class'], int) else kwargs['bomb_class']
        bombs = get_weapon()['bomb']
        self.missiles = []
        for i, loadage in zip(bomb_class, bomb_loadage):
            missile = Missile(aorf, self.rect, loadage=loadage, **bombs[i])
            self.missiles.append(missile)

    def fire(self, action):
        assert (
            self.can_fire()
        ), f"Agent cannot fire."

        enemy, bomb = self.action_to_enemy(action)

    def update(self, target_x, target_y, *args: Any, **kwargs: Any) -> None:
        offset_x = target_x - self.rect.x
        offset_y = target_y - self.rect.y

        self.radian = math.atan2(offset_x, offset_y)

        self.angle = int(self.radian * 180 / math.pi)

    # todo 返回数组分别表示各种炮弹数量
    def get_bombs_num(self):
        pass

    # todo 攻击间隔
    def can_fire(self):
        pass

    def action_to_enemy(self, action):
        enemy, bomb = 0, 0
        return enemy, bomb
