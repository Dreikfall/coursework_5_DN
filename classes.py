from dataclasses import dataclass

from skills import Skill, FuryPunch, HardShot


@dataclass
class UnitClass:
    name: str
    max_health: float
    max_stamina: float
    attack: float
    stamina: float
    armor: float
    skill: Skill


fury_punch = FuryPunch()
hard_shot = HardShot()

WarriorClass = UnitClass('Воин', 60.0, 30.0, 0.8, 0.9, 1.2, fury_punch)

ThiefClass = UnitClass('Вор', 50.0, 25.0, 1.5, 1.2, 1.0, hard_shot)

unit_classes = {
    ThiefClass.name: ThiefClass,
    WarriorClass.name: WarriorClass
}

