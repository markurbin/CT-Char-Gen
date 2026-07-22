# resolve.py
# Book 4 - Army / Marine Year Resolution
# Cleaned version - safer lookups, fixed missing entries

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
    "Support": {"int": True,  "end": True},
    "Marine":  {"int": False, "end": True},
    "Commando": {"int": False, "end": False},
    "General": {"int": False, "end": False},
}

target_numbers = {
    'Trng': {
        "Support":   {"combat": False, "survive": AUTO,      "decorate": NO_CHANCE, "promote": 6,  "officer_promote": NO_CHANCE, "ribbon": False, "skill": 8},
        "Marine":    {"combat": False, "survive": AUTO,      "decorate": NO_CHANCE, "promote": 6,  "officer_promote": NO_CHANCE, "ribbon": False, "skill": 7},
        "Commando":  {"combat": False, "survive": 3,         "decorate": NO_CHANCE, "promote": 8,  "officer_promote": NO_CHANCE, "ribbon": False, "skill": 6},
        "General":   {"combat": False, "survive": AUTO,      "decorate": NO_CHANCE, "promote": 6,  "officer_promote": NO_CHANCE, "ribbon": False, "skill": 7},
    },
    'Intl Sec': {
        "Support":   {"combat": True,  "survive": 4,         "decorate": NO_CHANCE, "promote": 6,  "officer_promote": NO_CHANCE, "ribbon": True,  "skill": NO_CHANCE},
        "Marine":    {"combat": True,  "survive": 4,         "decorate": 12,        "promote": 6,  "officer_promote": NO_CHANCE, "ribbon": True,  "skill": NO_CHANCE},
        "Commando":  {"combat": True,  "survive": 4,         "decorate": NO_CHANCE, "promote": 7,  "officer_promote": NO_CHANCE, "ribbon": True,  "skill": NO_CHANCE},
        "General":   {"combat": True,  "survive": 4,         "decorate": 12,        "promote": 6,  "officer_promote": NO_CHANCE, "ribbon": True,  "skill": NO_CHANCE},
    },
    'Pol Act': {
        "Support":   {"combat": True,  "survive": 4,         "decorate": 10,        "promote": 9,  "officer_promote": 9,         "ribbon": True,  "skill": 7},
        "Marine":    {"combat": True,  "survive": 5,         "decorate": 8,         "promote": 8,  "officer_promote": 8,         "ribbon": True,  "skill": 7},
        "Commando":  {"combat": True,  "survive": 4,         "decorate": 9,         "promote": 8,  "officer_promote": 8,         "ribbon": True,  "skill": 7},
        "General":   {"combat": True,  "survive": 5,         "decorate": 9,         "promote": 8,  "officer_promote": 8,         "ribbon": True,  "skill": 7},
    },
    'Ctr Ins': {
        "Support":   {"combat": True,  "survive": 5,         "decorate": 11,        "promote": 10, "officer_promote": 10,        "ribbon": True,  "skill": 7},
        "Marine":    {"combat": True,  "survive": 5,         "decorate": 9,         "promote": 9,  "officer_promote": 9,         "ribbon": True,  "skill": 8},
        "Commando":  {"combat": True,  "survive": 5,         "decorate": 8,         "promote": 7,  "officer_promote": 7,         "ribbon": True,  "skill": 6},
        "General":   {"combat": True,  "survive": 5,         "decorate": 10,        "promote": 9,  "officer_promote": 9,         "ribbon": True,  "skill": 8},
    },
    'Raid': {
        "Support":   {"combat": True,  "survive": 6,         "decorate": 7,         "promote": 7,  "officer_promote": 7,         "ribbon": True,  "skill": 6},
        "Marine":    {"combat": True,  "survive": 6,         "decorate": 5,         "promote": 6,  "officer_promote": 6,         "ribbon": True,  "skill": 5},
        "Commando":  {"combat": True,  "survive": 6,         "decorate": 5,         "promote": 6,  "officer_promote": 6,         "ribbon": True,  "skill": 5},
        "General":   {"combat": True,  "survive": 6,         "decorate": 6,         "promote": 6,  "officer_promote": 6,         "ribbon": True,  "skill": 5},
    },
    'Garr': {
        "Support":   {"combat": False, "survive": AUTO,      "decorate": NO_CHANCE, "promote": 7,  "officer_promote": NO_CHANCE, "ribbon": False, "skill": NO_CHANCE},
        "Marine":    {"combat": False, "survive": AUTO,      "decorate": NO_CHANCE, "promote": 9,  "officer_promote": NO_CHANCE, "ribbon": False, "skill": NO_CHANCE},
        "Commando":  {"combat": False, "survive": AUTO,      "decorate": NO_CHANCE, "promote": 9,  "officer_promote": NO_CHANCE, "ribbon": False, "skill": NO_CHANCE},
        "General":   {"combat": False, "survive": AUTO,      "decorate": NO_CHANCE, "promote": 6,  "officer_promote": NO_CHANCE, "ribbon": False, "skill": NO_CHANCE},
    },
    'Shp Trp': {
        "Marine":    {"combat": False, "survive": 4,         "decorate": 12,        "promote": 6,  "officer_promote": NO_CHANCE, "ribbon": False, "skill": 6},
    }
}


def survival_check(grunt, survival_target, combat_action, ua, medal_name):
    """Check survival for the year. Handles death or grave wounding."""
    roll = dice(qty=2)
    
    if roll < survival_target:
        grunt.history.append(f'Failed survival target of {survival_target} (rolled {roll})')
        
        if not getattr(grunt, 'noKill', False):
            # Gravely wounded -> will muster out at end of term
            grunt.history.append(f'Gravely wounded in service and will muster out in term {grunt.term}')
            grunt.musOut = True
            grunt.alive = True   # Still alive for mustering out
            return False
        else:
            grunt.history.append(f'Gravely wounded and mustered out in term {grunt.term}')
            grunt.musOut = True
            return False
    else:
        # Survival passed
        if roll == survival_target and combat_action:
            promotions.award_medal(grunt, medal_name, ua)
        return True


def decoration_check(grunt, dec_target, ua):
    """Check for decorations / medals."""
    roll = dice(qty=2)
    if roll >= dec_target:
        promotions.get_medal(grunt, roll, dec_target, ua)


def promotion_check(grunt, promot_target, int_bonus=True, end_bonus=True):
    """Check for promotion this year."""
    roll = dice(qty=2)

    # DMs
    if int_bonus and getattr(grunt.upp, 'int', 0) >= 8:
        roll += 1
    if end_bonus and getattr(grunt, 'arm', '') == 'Commando' and getattr(grunt.upp, 'end', 0) >= 8:
        roll += 1

    # Apply promotion
    if grunt.officer:
        if not getattr(grunt, 'promote_this_term', False):
            if roll >= promot_target:
                promotions.promote(grunt)
    else:
        if roll >= promot_target:
            promotions.promote(grunt)


def skill_check(grunt, skill_target, ga, ua):
    """Check for skill gain this year."""
    if dice(qty=2) >= skill_target:
        skills.gain(grunt, ua, ga)


def resolve(grunt, ua, ga, unit_type):
    """Main resolver for Army/Marine year assignments."""
    grunt.history.append(f'Unit Assignment is {ua}')

    # Safe table lookup with fallback
    table = target_numbers.get(ua, {}).get(unit_type) or target_numbers.get(ua, {}).get("General")
    if not table:
        table = {"combat": False, "survive": AUTO, "decorate": NO_CHANCE, 
                 "promote": 7, "officer_promote": NO_CHANCE, "ribbon": False, "skill": 7}

    combat_action = table.get("combat", False)
    survival_target = table.get("survive", AUTO)
    dec_target = table.get("decorate", NO_CHANCE)
    promot_target = table.get("officer_promote" if grunt.officer else "promote", 7)
    skill_target = table.get("skill", 7)

    if table.get("ribbon", False):
        promotions.award_ribbon(grunt, ga, ua)

    # Run checks
    if not survival_check(grunt, survival_target, combat_action, ua, wound_badges.get(unit_type, "Wound Badge")):
        return False

    decoration_check(grunt, dec_target, ua)

    int_bonus = promotion_bonuses.get(unit_type, {}).get("int", True)
    end_bonus = promotion_bonuses.get(unit_type, {}).get("end", True)
    promotion_check(grunt, promot_target, int_bonus=int_bonus, end_bonus=end_bonus)

    skill_check(grunt, skill_target, ga, ua)

    return True


# Dispatch functions
# Dispatch functions
def support(grunt, ua, ga):
    """Support arm year resolution"""
    return resolve(grunt, ua, ga, "Support")


def marine(grunt, ua, ga):
    """Marine Infantry year resolution"""
    return resolve(grunt, ua, ga, "Marine")


def commando(grunt, ua, ga):
    """Commando year resolution"""
    return resolve(grunt, ua, ga, "Commando")


def general(grunt, ua, ga):
    """General (Infantry/Cavalry/Artillery) year resolution"""
    return resolve(grunt, ua, ga, "General")


