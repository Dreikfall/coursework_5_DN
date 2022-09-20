from __future__ import annotations
from abc import ABC, abstractmethod

from equipment import Weapon, Armor
from classes import UnitClass
from random import choices


class BaseUnit(ABC):
    """
    Базовый класс юнита
    """

    def __init__(self, name: str, unit_class: UnitClass):
        """
        При инициализации класса Unit используем свойства класса UnitClass
        """
        self.name = name
        self.unit_class = unit_class
        self.hp = unit_class.max_health
        self.stamina = unit_class.max_stamina
        self.weapon = None
        self.armor = None
        self._is_skill_used = False

    @property
    def health_points(self):
        return round(self.hp, 1)

    @property
    def stamina_points(self):
        return round(self.stamina, 1)

    def equip_weapon(self, weapon: Weapon):
        # присваиваем нашему герою новое оружие
        self.weapon = weapon
        return f"{self.name} экипирован оружием {self.weapon.name}"

    def equip_armor(self, armor: Armor):
        self.armor = armor
        return f"{self.name} экипирован броней {self.armor.name}"

    def _count_damage(self, target: BaseUnit) -> int:
        '''логика расчета урона игрока. логика расчета брони цели
        здесь же происходит уменьшение выносливости атакующего при ударе
        и уменьшение выносливости защищающегося при использовании брони
        если у защищающегося нехватает выносливости - его броня игнорируется
        после всех расчетов цель получает урон - target.get_damage(damage)
        и возвращаем предполагаемый урон для последующего вывода пользователю в текстовом виде'''

        damage_weapon = self.weapon.damage
        damage_user = damage_weapon * self.unit_class.attack
        armor_target = self.get_armor_target(target)
        damage = round(damage_user - armor_target, 1)
        self.stamina = self.stamina - self.weapon.stamina_per_hit
        if target.stamina >= target.armor.stamina_per_turn:
            target.stamina = target.stamina - target.armor.stamina_per_turn
        target.get_damage(damage)
        return damage

    def get_damage(self, damage: int):
        self.hp = self.hp - damage
        return self.health_points

    @abstractmethod
    def hit(self, target: BaseUnit) -> str:
        """
        этот метод будет переопределен ниже
        """
        pass

    def use_skill(self, target: BaseUnit) -> str:
        """ метод использования умения. если умение уже использовано возвращаем строку
        Навык использован. Если же умение не использовано тогда выполняем функцию
        self.unit_class.skill.use(user=self, target=target)
        и уже эта функция вернем нам строку которая характеризует выполнение умения"""

        if self._is_skill_used:
            return "Навык уже использован."
        self._is_skill_used = True
        return self.unit_class.skill.use(user=self, target=target)

    def get_armor_target(self, target: BaseUnit):
        if target.stamina >= target.armor.stamina_per_turn:
            target.stamina = target.stamina - target.armor.stamina_per_turn
            armor_target = target.armor.defence * target.unit_class.armor
            return armor_target
        armor_target = 0
        return armor_target


class PlayerUnit(BaseUnit):

    def hit(self, target: BaseUnit) -> str:
        """ здесь происходит проверка достаточно ли выносливости для нанесения удара.
                вызывается функция self._count_damage(target) а также возвращается результат в виде строки"""

        if self.stamina < self.weapon.stamina_per_hit:
            return f"{self.name} попытался использовать {self.weapon.name}, но у него не хватило выносливости."
        damage = self._count_damage(target)
        if damage < self.get_armor_target(target):
            return f"{self.name} используя {self.weapon.name} наносит удар, но {target.armor.name} cоперника его останавливает."
        target.get_damage(damage)
        return f"{self.name} используя {self.weapon.name} пробивает {target.armor.name} соперника и наносит {damage} урона."


class EnemyUnit(BaseUnit):

    def hit(self, target: BaseUnit) -> str:
        action = choices(['hit', 'skill'], [90, 10])[0]
        if action == 'skill':
            if not self._is_skill_used:
                return self.use_skill(target)
        if self.stamina < self.weapon.stamina_per_hit:
            return f"{self.name} попытался использовать {self.weapon.name}, но у него не хватило выносливости."
        damage = self._count_damage(target)
        if damage < self.get_armor_target(target):
            return f"{self.name} используя {self.weapon.name} наносит удар, но Ваш(а) {target.armor.name} его останавливает."
        target.get_damage(damage)
        return f"{self.name} используя {self.weapon.name} пробивает {target.armor.name} и наносит Вам {damage} урона."


