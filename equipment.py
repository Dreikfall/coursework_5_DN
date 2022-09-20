from dataclasses import dataclass, field
from random import uniform
import marshmallow_dataclass
import marshmallow
import json


@dataclass
class Armor:
    id: int
    name: str
    defence: float
    stamina_per_turn: float


@dataclass
class Weapon:
    id: int
    name: str
    min_damage: float
    max_damage: float
    stamina_per_hit: float

    @property
    def damage(self):
        return round(uniform(self.min_damage, self.max_damage), 1)


@dataclass
class EquipmentData:
    weapons: list[Weapon] = field(default_factory=list)
    armors: list[Armor] = field(default_factory=list)

    class Meta:
        unknown = marshmallow.EXCLUDE


class Equipment:

    def __init__(self):
        self.equipment = self._get_equipment_data()

    def get_weapon(self, weapon_name: str) -> Weapon:
        # возвращает объект оружия по имени
        for weapon in self.equipment.weapons:
            if weapon.name == weapon_name.lower():
                return weapon

    def get_armor(self, armor_name: str) -> Armor:
        # возвращает объект брони по имени
        for armor in self.equipment.armors:
            if armor.name == armor_name.lower():
                return armor

    def get_weapons_names(self) -> list:
        # возвращаем список с оружием
        return [i.name for i in self.equipment.weapons]

    def get_armors_names(self) -> list:
        # возвращаем список с броней
        return [i.name for i in self.equipment.armors]

    @staticmethod
    def _get_equipment_data() -> EquipmentData:
        # этот метод загружает json в переменную EquipmentData
        with open('./data/equipment.json', encoding='utf-8') as f:
            data = json.load(f)
        equipment_schema = marshmallow_dataclass.class_schema(EquipmentData)
        try:
            return equipment_schema().load(data)
        except marshmallow.exceptions.ValidationError:
            raise ValueError
