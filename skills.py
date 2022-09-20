from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from unit import BaseUnit


class Skill(ABC):
    """
    Базовый класс умения
    """
    user = None
    target = None

    @property
    @abstractmethod
    def name(self):
        pass

    @property
    @abstractmethod
    def stamina(self):
        pass

    @property
    @abstractmethod
    def damage(self):
        pass

    @abstractmethod
    def skill_effect(self) -> str:
        pass

    def _is_stamina_enough(self):
        return self.user.stamina > self.stamina

    def use(self, user: BaseUnit, target: BaseUnit) -> str:
        """
        Проверка, достаточно ли выносливости у игрока для применения умения.
        Для вызова скилла везде используем просто use
        """
        self.user = user
        self.target = target
        if self._is_stamina_enough():
            return self.skill_effect()
        return f"{self.user.name} попытался использовать {self.name} но у него не хватило выносливости."


class FuryPunch(Skill):
    def __init__(self):
        self._name = 'Свирепый пинок'
        self._stamina = 6
        self._damage = 12

    @property
    def name(self):
        return self._name

    @property
    def stamina(self):
        return self._stamina

    @property
    def damage(self):
        return self._damage

    def skill_effect(self):
        self.user.stamina = self.user.stamina_points - self.stamina
        self.target.get_damage(self.damage)
        return f'{self.user.name} использует {self.name} и наносит {self.damage} урона сопернику.'

    @name.setter
    def name(self, value):
        self._name = value

    @stamina.setter
    def stamina(self, value):
        self._stamina = value

    @damage.setter
    def damage(self, value):
        self._damage = value


class HardShot(Skill):
    _name = 'Мощный укол'
    _stamina = 5
    _damage = 15

    @property
    def name(self):
        return self._name

    @property
    def stamina(self):
        return self._stamina

    @property
    def damage(self):
        return self._damage

    def skill_effect(self):
        self.user.stamina = self.user.stamina_points - self.user.stamina
        self.target.get_damage(self.damage)
        return f'{self.user.name} использует {self.name} и наносит {self.damage} урона сопернику.'

    @name.setter
    def name(self, value):
        self._name = value

    @stamina.setter
    def stamina(self, value):
        self._stamina = value

    @damage.setter
    def damage(self, value):
        self._damage = value
