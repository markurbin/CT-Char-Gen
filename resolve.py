from dice import *
import promotions
import skills

AUTO = 0
NO_CHANCE = 20

wound_badges = {
    "Support": "Wound Badge",
    "Marine": "Wound Badge",
    "Commando": "Purple Heart",
    "General": "Wound Badge",
}

promotion_bonuses = {
    "Support": {"int":True,  "end":True},
    "Marine":  {"int":False, "end":True},
    "Commando":{"int":False, "end":False},
    "General": {"int":False, "end":False},
}

target_numbers = {}
target_numbers['Trng'] = {
  "Support":{
    "combat":False,
    "survive":AUTO,
    "decorate":NO_CHANCE,
    "promote":6,
    "officer_promote":NO_CHANCE,
    "ribbon":False,
    "skill":8
  },
  "Marine":{
    "combat":False,
    "survive":AUTO,
    "decorate":NO_CHANCE,
    "promote":6,
    "officer_promote":NO_CHANCE,
    "ribbon":False,
    "skill":7
  },
  "Commando":{
    "combat":False,
    "survive":3,
    "decorate":NO_CHANCE,
    "promote":8,
    "officer_promote":NO_CHANCE,
    "ribbon":False,
    "skill":6
  },
  "General":{
    "combat":False,
    "survive":AUTO,
    "decorate":NO_CHANCE,
    "promote":6,
    "officer_promote":NO_CHANCE,
    "ribbon":False,
    "skill":7
  },
}
target_numbers['Intl Sec'] = {
  "Support":{
    "combat":True,
    "survive":4,
    "decorate":NO_CHANCE,
    "promote":6,
    "officer_promote":NO_CHANCE,
    "ribbon":True,
    "skill":NO_CHANCE,
  },
  "Marine":{
    "combat":True,
    "survive":4,
    "decorate":12,
    "promote":6,
    "officer_promote":NO_CHANCE,
    "ribbon":True,
    "skill":NO_CHANCE,
  },
  "Commando":{
    "combat":True,
    "survive":4,
    "decorate":NO_CHANCE,
    "promote":7,
    "officer_promote":NO_CHANCE,
    "ribbon":True,
    "skill":NO_CHANCE,
  },
  "General":{
    "combat":True,
    "survive":4,
    "decorate":12,
    "promote":6,
    "officer_promote":NO_CHANCE,
    "ribbon":True,
    "skill":NO_CHANCE
  },
}
target_numbers['Pol Act'] = {
  "Support":{
    "combat":True,
    "survive":4,
    "decorate":10,
    "promote":9,
    "officer_promote":9,
    "ribbon":True,
    "skill":7,
  },
  "Marine":{
    "combat":True,
    "survive":5,
    "decorate":8,
    "promote":8,
    "officer_promote":8,
    "ribbon":True,
    "skill":7,
  },
  "Commando":{
    "combat":True,
    "survive":4,
    "decorate":9,
    "promote":8,
    "officer_promote":8,
    "ribbon":True,
    "skill":7,
  },
  "General":{
    "combat":True,
    "survive":5,
    "decorate":9,
    "promote":8,
    "officer_promote":8,
    "ribbon":True,
    "skill":7
  },
}
target_numbers['Ctr Ins'] = {
  "Support":{
    "combat":True,
    "survive":5,
    "decorate":11,
    "promote":10,
    "officer_promote":10,
    "ribbon":True,
    "skill":7,
  },
  "Marine":{
    "combat":True,
    "survive":5,
    "decorate":9,
    "promote":9,
    "officer_promote":9,
    "ribbon":True,
    "skill":8,
  },
  "Commando":{
    "combat":True,
    "survive":5,
    "decorate":8,
    "promote":7,
    "officer_promote":7,
    "ribbon":True,
    "skill":6,
  },
  "General":{
    "combat":True,
    "survive":5,
    "decorate":10,
    "promote":9,
    "officer_promote":9,
    "ribbon":True,
    "skill":8
  },
}
target_numbers['Raid'] = {
  "Support":{
    "combat":True,
    "survive":6,
    "decorate":7,
    "promote":7,
    "officer_promote":7,
    "ribbon":True,
    "skill":6,
  },
  "Marine":{
    "combat":True,
    "survive":6,
    "decorate":5,
    "promote":6,
    "officer_promote":6,
    "ribbon":True,
    "skill":5,
  },
  "Commando":{
    "combat":True,
    "survive":6,
    "decorate":5,
    "promote":6,
    "officer_promote":6,
    "ribbon":True,
    "skill":5,
  },
  "General":{
    "combat":True,
    "survive":6,
    "decorate":6,
    "promote":6,
    "officer_promote":6,
    "ribbon":True,
    "skill":5
  },
}
target_numbers['Garr'] = {
  "Support":{
    "combat":False,
    "survive":AUTO,
    "decorate":NO_CHANCE,
    "promote":7,
    "officer_promote":NO_CHANCE,
    "ribbon":False,
    "skill":NO_CHANCE,
  },
  "Marine":{
    "combat":False,
    "survive":AUTO,
    "decorate":NO_CHANCE,
    "promote":9,
    "officer_promote":NO_CHANCE,
    "ribbon":False,
    "skill":NO_CHANCE,
  },
  "Commando":{
    "combat":False,
    "survive":AUTO,
    "decorate":NO_CHANCE,
    "promote":9,
    "officer_promote":NO_CHANCE,
    "ribbon":False,
    "skill":NO_CHANCE,
  },
  "General":{
    "combat":False,
    "survive":AUTO,
    "decorate":NO_CHANCE,
    "promote":6,
    "officer_promote":NO_CHANCE,
    "ribbon":False,
    "skill":NO_CHANCE
  },
}
target_numbers['Shp Trp'] = {
  "Marine":{
    "combat":False,
    "survive":4,
    "decorate":12,
    "promote":6,
    "officer_promote":NO_CHANCE,
    "ribbon":False,
    "skill":6
  },
}

def survival_check(grunt, survival_target, combat_action, ua, medal_name):
    # Survival check, no DM coded yet
    roll = dice(qty=2)
    if roll < survival_target:
        s = 'Failed survival target of %d' % survival_target
        grunt.history.append(s)
        grunt.alive = False
        return False
    else:
        if (roll == survival_target) and combat_action:
            promotions.award_medal(grunt, medal_name, ua)
        return True

def decoration_check(grunt, dec_target, ua):
    #Decoration check
    roll = dice(qty=2)
    if roll >= dec_target:
        promotions.get_medal(grunt, roll, dec_target, ua)

def promotion_check(grunt, promot_target, int_bonus=True, end_bonus=True):
    #Promotion check
    roll = dice(qty=2)
    if int_bonus and (grunt.upp.int >= 8):
        roll += 1 # +1 DM if int 8+
    if end_bonus and (grunt.arm == 'Commando') and (grunt.upp.end >= 8):
        roll += 1 # Commandos get a +1 promotion DM if endurance is 8+
    if grunt.officer:
        if not grunt.promote_this_term:
            if roll >= promot_target:
                promotions.promote(grunt)
    else:
        if roll >= promot_target:
            promotions.promote(grunt)

def skill_check(grunt, skill_target, ga, ua):
    #Skill check 
    roll = dice(qty=2)
    if roll >= skill_target:
        skills.gain(grunt, ua, ga)



def resolve(grunt, ua, ga, unit_type):
    s = 'Unit Assigment is %s' % ua
    grunt.history.append(s)
    combat_action = False

    unit_type = "Support"
    
    table = target_numbers[ua][unit_type]

    combat_action = table["combat"]
    survival_target = table["survive"]
    dec_target = table["decorate"]
    if grunt.officer:
        promot_target = table["officer_promote"]
    else:
        promot_target = table["promote"]
    skill_target = table["skill"]
    if table["ribbon"]:
        promotions.award_ribbon(grunt, ga, ua)

    if not survival_check(grunt, survival_target, combat_action, ua, wound_badges[unit_type]):
        return False
    decoration_check(grunt, dec_target, ua)
    int_bonus = promotion_bonuses[unit_type]["int"]
    end_bonus = promotion_bonuses[unit_type]["end"]
    promotion_check(grunt, promot_target, int_bonus=int_bonus, end_bonus=end_bonus)
    skill_check(grunt, skill_target, ga, ua)


def support(grunt, ua, ga):
    'resolve year: support A or M'
    return resolve(grunt, ua, ga, "Support")

def marine(grunt, ua, ga):
    'resolve year: Marine Infantry'
    return resolve(grunt, ua, ga, "Marine")

def commando(grunt, ua, ga):
    'resolve year: Commando'
    return resolve(grunt, ua, ga, "Commando")

def general(grunt, ua, ga):
    'resolve year: infantry, Cav or artilery'
    return resolve(grunt, ua, ga, "General")
