import json

import numpy as np
import matplotlib.pyplot as plt

npc_info = json.load(open('files/NPCInfo.json', encoding='utf8'))
npc_info = npc_info[0]['Properties']['ContentInfoDB']
basics = npc_info['_NpcInfo_array']
skills = npc_info['_NpcSkillLinkInfo_array']
gauges = npc_info['_NpcGaugeGrowthInfo_array']
stats = npc_info['_NpcStatInfo_array']

# print(len(basics), len(skills), len(gauges), len(stats))

def print_enemies():
    stats.sort(key=lambda e: e['_health_power'])
    for st in stats:
        '''for k in st.keys():
            if k.endswith('_defence') and st[k] > 0:'''
        print(st['_code_name'], st['_health_power'],
              st['_physical_reduce'] / 100,
              st['_physical_slash_reduce'] / 100, st['_physical_strike_reduce'] / 100, st['_physical_pierce_reduce'] / 100, ':',
              st["_fire_reduce"] / 100, st["_electric_reduce"] / 100, st["_acid_reduce"] / 100)


projectile_info = json.load(open('files/ProjectileInfo.json', encoding='utf8'))
projectile_info = projectile_info[0]['Properties']['ContentInfoDB']['_ProjectileInfo_array']


def print_projectiles():
    for p in projectile_info:
        print(p['_code_name'], p['_physical_attack'], p['_fire_attack'], p['_electric_attack'], p['_acid_attack'])


spbuffs = json.load(open('files/SpecialBuffInfo.json', encoding='utf8'))[0]['Properties']['ContentInfoDB']['_SpecialBuffInfo_array']
def print_spbuffs():
    for s in spbuffs:
        print(s['_code_name'])

skills = json.load(open('files/SkillInfo.json', encoding='utf8'))[0]['Properties']['ContentInfoDB']['_Skill_array']
def print_skills():
    for s in skills:
        if s['_destruction_defence_mod'] != 0:
            print(s['_code_name'], s['_require_stamina_point'], s['_consume_stamina_point'], s['_destruction_defence_mod'])

skillhits = json.load(open('files/SkillHitInfo.json', encoding='utf8'))[0]['Properties']['ContentInfoDB']['_SkillHitInfo_array']
def print_skillhits():
    # ['_physical_damage_ratio', '_consume_stamina_ratio']
    # stat = '_attack_gain_frenzy_point_ratio'
    # skillhits.sort(key=lambda e: e[stat])
    skillhits2 = []
    for s in skillhits:
        name = s['_code_name']
        phys = s['_physical_damage_ratio']
        elem = s['_element_damage_ratio']
        stam = s['_consume_stamina_ratio']
        s['stamina_effectiveness'] = phys / stam if stam != 0 else np.Inf
        if name.startswith('Hit_PC') or name.startswith('FatalATK'):
            skillhits2.append(s)
    skillhits2.sort(key=lambda e: e['stamina_effectiveness'])
    for s in skillhits2:
        phys = s['_physical_damage_ratio']
        elem = s['_element_damage_ratio']
        stam = s['_consume_stamina_ratio']
        se = s['stamina_effectiveness']
        if not elem:
            continue
        print(skillhits.index(s), s['_code_name'], s['_tough_damage_ratio'])  #str(phys) + (f'({elem})' if elem != phys else ''), stam, np.round(se, 3))


'''e1 = [e for e in stats if e['_code_name'] == 'Hotel_Puppet_Training_Basic_00'][0]
e2 = [e for e in stats if e['_code_name'] == 'Hotel_Puppet_Training_Armless_09'][0]
for k, v in e1.items():
    if e2[k] != v:
        print(k, v, e2[k])'''

allitems = json.load(open('files/ItemInfo.json', encoding='utf8'))[0]['Properties']['ContentInfoDB']
itemCommon = allitems['_ItemCommon_array']
correct = allitems['_CorrectionWeaponFirstStat_array']
armor = allitems['_ItemParts_array']
collectable = allitems['_ItemCollection_array']
consumable = allitems['_ItemConsume_array']
bladeweight = allitems['_BladeWeight_array']
monsterWeapon = allitems['_ItemWeaponMonster_array']
arm = allitems['_ItemSlaveArm_array']
handle = allitems['_ItemHandle_array']
blade = allitems['_ItemBlade_array']
reinforce = allitems['_ItemWeaponReinforce_array']

fig, ax = plt.subplots(1,1)
colors = plt.cm.jet(np.linspace(0,1,30))
color_ctr = 0

def print_corrections():
    global color_ctr
    rng = list(range(1, 101))
    for i in rng:
        print(f'{i}', end=' ')
    print()
    for corr in correct:
        name = corr['_code_name']
        data = np.array([corr["_stat_level" + str(i)] for i in rng])
        if not any(data):
            continue
        data = data / 100 # / data.max()
        print(name, end=' ')
        # for d in data:
        #     print(f'{d}', end=', ')
        print(data.max())
        ax.plot(rng, data, label=name[len('correction_ratio_'):], color=colors[color_ctr])
        color_ctr += 1
    ax.set_xlabel('Stat level')
    ax.set_ylabel('Damage boost, %')
    ax.set_title("Lies of P damage scaling")
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    ax.set_xticks(np.linspace(0, 100, 21))
    ax.grid()
    plt.subplots_adjust(right=0.8)
    plt.show()

def print_bladeweight():
    for i in bladeweight:
        print(i['_code_name'], i["_stamina_consume_ratio"], *[i[prop] for prop in i.keys() if prop.endswith('_rate')])

def print_handle():
    for h in handle:
        print(handle.index(h), h['_code_name'], h['_attack_speed'], h['_perfect_guard_decrease_enemy_weapon_durability'], h['_guard_duration_ratio'])

print_corrections()

