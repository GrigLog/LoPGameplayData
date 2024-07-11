from enum import Enum
from dataclasses import dataclass
import numpy as np
import json


class Damage(Enum):
    PHYS = 0
    FIRE = 1
    ELEC = 2
    ACID = 3

class Letter(Enum):
    S = 'S'
    A = 'A'
    B = 'B'
    C = 'C'
    D = 'D'
    NULL = 'NULL'

class Stat(Enum):
    STR = 'motivity'
    DEX = 'technique'
    ADV = 'advance'


class Stats:
    def __init__(self, str, dex, adv):
        assert 1 <= str <= 100
        assert 1 <= dex <= 100
        assert 1 <= adv <= 100
        self.str = str
        self.dex = dex
        self.adv = adv


allitems = json.load(open('files/ItemInfo.json', encoding='utf8'))[0]['Properties']['ContentInfoDB']
itemCommon = allitems['_ItemCommon_array']
correct = allitems['_CorrectionWeaponFirstStat_array']
graphs = {}
rng = list(range(1, 101))
for corr in correct:
    name = corr['_code_name']
    data = np.array([corr["_stat_level" + str(i)] for i in rng])
    data = data / 10000  # / data.max()
    graphs[name] = data



def get_scaling(stat: Stat, letter: Letter):
    return graphs[f'correction_ratio_attack_{stat.value}_{letter.value}']

@dataclass
class Handle:
    letter_str: Letter
    letter_dex: Letter
    letter_adv: Letter

@dataclass
class Blade:
    dmg_phys: int
    dmg_elem: int
    element: Damage  # PHYS if none
    upgrade: int = 0

    def with_upgrade(self, upgrade):
        self.upgrade = upgrade
        return self

@dataclass
class Weapon:
    blade: Blade
    handle: Handle
    unique: bool = False

    def get_damage(self, stats: Stats, type: Damage):
        up = (0.1 if not self.unique else 0.2) * self.blade.upgrade
        if type == Damage.PHYS:
            r1 = get_scaling(Stat.STR, self.handle.letter_str)[stats.str - 1]
            r2 = get_scaling(Stat.DEX, self.handle.letter_dex)[stats.dex - 1]
            return int(self.blade.dmg_phys * (1 + up + r1 + r2))
        r = get_scaling(Stat.ADV, self.handle.letter_adv)[stats.adv - 1]
        if type == self.blade.element:
            return int(self.blade.dmg_elem * (1 + up + r))
        return 0

    def get_damages(self, stats: Stats):
        return [self.get_damage(stats, type) for type in Damage]

    def get_value(self, stats):
        return sum(self.get_damages(stats))


def find_best_stats(minimum: Stats, points: int, weapon: Weapon):
    results = []
    for i in range(0, points + 1):
        for j in range(0, points + 1 - i):
            k = points - i - j
            try:
                stats = Stats(minimum.str + i, minimum.dex + j, minimum.adv + k)
            except:
                continue
            v = weapon.get_value(stats)
            results.append((v, (minimum.str + i, minimum.dex + j, minimum.adv + k)))
    results.sort(key=lambda e: -e[0])
    return results


s = Stats(10, 35, 7)
s_low = Stats(5, 11, 6)

rapB = Blade(98, 0, Damage.PHYS)
spearB = Blade(57, 51, Damage.ACID)
rapH = Handle(Letter.D, Letter.B, Letter.NULL)
spearH = Handle(Letter.D, Letter.D, Letter.A)
rap = Weapon(rapB, rapH)
spear = Weapon(spearB, spearH)
rap_mine = Weapon(rapB.with_upgrade(6), Handle(Letter.NULL, Letter.A, Letter.NULL))


print(rap.get_damage(s, Damage.PHYS))
print(spear.get_damages(s))  # 80, 58
spear.blade.upgrade = 2
print(spear.get_damages(s))
print(rap_mine.get_damages(s))

print(find_best_stats(s, 10, rap_mine))
rap.blade.upgrade = 6
print(find_best_stats(s, 10, rap))







