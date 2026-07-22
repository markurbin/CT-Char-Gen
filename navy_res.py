# navy_res.py
# Book 5 - Navy Year Resolution Functions
# Centralized and cleaned - no circular imports

from dice import *
import promotions
import skills
import schools
from navy_tables import *   # All Navy tables (line_crew, flight, etc.)
# Explicit exports for b5_data.py
__all__ = [
    'lc_res', 'flight_res', 'gunnery_res', 'eng_res', 
    'medical_res', 'tech_res', 'nbranch_skill', 
    'navy_cmd_check', 'get_navy_skill'
]
'''
from navy_res import (
    lc_res, flight_res, gunnery_res, 
    eng_res, medical_res, tech_res,
    nbranch_skill, navy_cmd_check   # ← Add this
)
'''

# ====================== NAVY SKILL HELPERS ======================

def nbranch_skill(grunt, roll):
    """Add a skill from the current Navy branch's skill table."""
    roll = min(roll + 2, 6)

    if grunt.arm in ('Line', 'Crew'):
        skill_list = line_crew
    elif grunt.arm  == 'Flight':
        skill_list = flight
    elif grunt.arm  == 'Gunnery':
        skill_list = gunnery
    elif grunt.arm  == 'Engineering':
        skill_list = engineering
    elif grunt.arm  == 'Medical':
        skill_list = medical
    elif grunt.arm  == 'Technical Services':
        skill_list = technical
    else:
        # This should never happen — log it clearly
        grunt.history.append(f'ERROR: Unknown Navy branch "{getattr(grunt, "arm", None)}" in nbranch_skill - using Line/Crew fallback')
        skill_list = line_crew

    skill = skill_list[roll - 1]
    skills.record(grunt, skill)

def navy_cmd_check(grunt):
    """Check if officer is in a Command position this year."""
    if not grunt.officer:
        return False

    dm = 0
    if grunt.rank < 2:
        dm -= 2
    elif grunt.rank < 4:
        dm -= 1

    if grunt.upp.soc >= 11:
        dm += 1
    if grunt.upp.int <= 7:
        dm -= 1
    if grunt.upp.edu <= 7:
        dm -= 1

    roll = dm + dice(2)
    roll = max(roll, 1)   # minimum roll of 1

    # Branch-specific command thresholds
    if grunt.arm == 'Line':
        return roll >= 7
    elif grunt.arm  == 'Flight':
        return roll >= 8
    elif grunt.arm  == 'Gunnery':
        return roll >= 9
    elif grunt.arm  == 'Engineering':
        return roll >= 10
    elif grunt.arm  == 'Medical':
        return roll >= 11
    elif grunt.arm  == 'Technical Services':
        return roll >= 12

    return False
#end of navy_cmd_check()

def navy_life_skill(grunt):
    """Navy Life Skill Table"""
    dm = 4 if grunt.officer else 0
    roll = dm + dice()
    roll = max(min(roll, len(navy_life)), 1)

    skill = navy_life[roll - 1]
    skills.record(grunt, skill)


def shipboard_life_skill(grunt):
    dm = 4 if grunt.officer else 0
    roll = dm + dice() - 1
    roll = max(min(roll, len(shipboard_skills) - 1), 0)
    skill = shipboard_skills[roll]
    skills.record(grunt, skill)


def shore_duty_life_skill(grunt):
    """Shore Duty Life Skill Table"""
    dm = 4 if grunt.officer else 0
    roll = dm + dice()
    roll = max(min(roll, len(shoreduty_skills)), 1)

    skill = shoreduty_skills[roll - 1]
    skills.record(grunt, skill)


def get_command_skill(grunt):
    """Officer Command Skill Table"""
    dm = 0
    if grunt.officer:
        if 3 <= grunt.rank <= 5:
            dm += 2
        elif grunt.rank >= 6:
            dm += 4

    roll = dm + dice() - 1
    roll = max(min(roll, len(command_skills)), 1)

    skill = command_skills[roll - 1]
    skills.record(grunt, skill)


def get_staff_skill(grunt):
    """Officer Staff Skill Table"""
    roll = dice()
    if (2 < grunt.rank < 6):
        roll += 1
    elif (grunt.rank > 5):
        roll += 2

    roll = min(roll, len(staff_skills))
    skill = staff_skills[roll - 1]
    return skill   # already safe, but the guard above helps


def get_po_skill(grunt):
    """Petty Officer Skill Table (for senior enlisted)"""
    dm = 0
    if not grunt.officer:
        if 3 <= grunt.rank <= 5:
            dm += 2
        elif grunt.rank >= 6:
            dm += 4

    roll = dm + dice() - 1
    roll = max(min(roll, len(po_skills)), 1)

    skill = po_skills[roll - 1]
    skills.record(grunt, skill)


def get_navy_skill(grunt, command, sa):
    """Main skill gain dispatcher for Navy characters."""
    if coin_flip():
        # 50% chance: Branch skill
        roll = min(2 + dice() - 1, 6)
        nbranch_skill(grunt, roll)
    else:
        # 50% chance: Life / Role-based skill
        if grunt.officer:
            if sa not in ('Training', 'Shore Duty'):
                choice = dice(3)
                if choice == 1:
                    navy_life_skill(grunt)
                elif choice == 2:
                    shipboard_life_skill(grunt)
                else:
                    get_command_skill(grunt) if command else get_staff_skill(grunt)
            else:
                # Shore Duty / Training
                choice = dice(3)
                if choice == 1:
                    navy_life_skill(grunt)
                elif choice == 2:
                    shore_duty_life_skill(grunt)
                else:
                    get_command_skill(grunt) if command else get_staff_skill(grunt)
        else:
            # Enlisted
            if grunt.rank > 2:
                choice = dice(3)
                if choice == 1:
                    navy_life_skill(grunt)
                elif choice == 2:
                    shipboard_life_skill(grunt)
                else:
                    get_po_skill(grunt)
            else:
                # Junior enlisted
                if coin_flip():
                    navy_life_skill(grunt)
                else:
                    shipboard_life_skill(grunt)


# ====================== RESOLVE YEAR FUNCTIONS ======================

def lc_res(grunt, sa, command):
    """Resolve one year for Line/Crew branch (most common path)"""
   
    # ====================== ASSIGNMENT PARAMETERS ======================
        # ====================== ASSIGNMENT PARAMETERS ======================
    if sa == 'Training':
        survival_target = 0
        decoration_target = 20
        combat_action = False
        promotion_target = 6 if not grunt.officer else 20
        skill_target = 7

    elif sa == 'Shore Duty':
        survival_target = 4
        decoration_target = 12
        combat_action = False
        promotion_target = 7 if not grunt.officer else 20
        skill_target = 7

    elif sa == 'Patrol':
        survival_target = 4
        decoration_target = 11
        combat_action = True
        promotion_target = 7
        skill_target = 6

    elif sa == 'Siege':
        survival_target = 5
        decoration_target = 10
        combat_action = True
        promotion_target = 8
        skill_target = 6

    elif sa == 'Strike':
        survival_target = 6
        decoration_target = 7
        combat_action = True
        promotion_target = 7
        skill_target = 5

    elif sa == 'Battle':
        survival_target = 6
        decoration_target = 6
        combat_action = True
        promotion_target = 6
        skill_target = 5

    else:
        # This should NEVER be hit in normal operation
        grunt.history.append(f'***ERROR!!!: Unknown assignment {sa} in lc_res - using safe fallback')
        survival_target = 0          # Auto survive
        decoration_target = 20
        combat_action = False
        promotion_target = 20
        skill_target = 20

    # ====================== ROLLS ======================
    # Survival DM: +1 if any Line skill at level 2+
    s_dm = 1 if any(grunt.skills.get(skill, 0) >= 2 for skill in line_crew) else 0
    sroll = s_dm + dice(qty=2)

    if sroll < survival_target:
        grunt.history.append(f'Failed survival target of {survival_target} (rolled {sroll})')
        grunt.alive = False
        return False
    elif sroll == survival_target and combat_action:
        grunt.decorations.append(f'Wound Badge awarded in {sa}')
        grunt.history.append(f'Wound Badge awarded in {sa}')

    # Decoration
    droll = dice(qty=2)
    if droll >= decoration_target:
        promotions.get_medal(grunt, droll, decoration_target, sa)

    # Promotion
    p_dm = (1 if getattr(grunt.upp, 'edu', 0) >= 8 else 0) + (1 if getattr(grunt.upp, 'soc', 0) >= 9 else 0)
    p_roll = p_dm + dice(qty=2)

    if not grunt.officer:
        if p_roll >= promotion_target:
            promotions.promote(grunt)
    elif not getattr(grunt, 'promote_this_term', False):
        if p_roll >= promotion_target:
            promotions.promote(grunt)

    # Skill Gain
    if dice(qty=2) >= skill_target:
        get_navy_skill(grunt, command, sa)

    return True
# end of lc_res


def flight_res(grunt, sa, command):
    """Resolve one year for Flight branch"""

    # ====================== ASSIGNMENT PARAMETERS ======================
       # ====================== ASSIGNMENT PARAMETERS ======================
    if sa == 'Training':
        survival_target = 3
        decoration_target = 20
        combat_action = False
        promotion_target = 20          # Very hard for officers during training
        skill_target = 7

    elif sa == 'Shore Duty':
        survival_target = 3
        decoration_target = 20
        combat_action = False
        promotion_target = 11
        skill_target = 20              # Usually no skill gain on shore duty

    elif sa == 'Patrol':
        survival_target = 3
        decoration_target = 10
        combat_action = True
        promotion_target = 11
        skill_target = 7

    elif sa == 'Siege':
        survival_target = 3
        decoration_target = 9
        combat_action = True
        promotion_target = 10
        skill_target = 7

    elif sa == 'Strike':
        survival_target = 3
        decoration_target = 9
        combat_action = True
        promotion_target = 9
        skill_target = 6

    elif sa == 'Battle':
        survival_target = 4
        decoration_target = 8
        combat_action = True
        promotion_target = 9
        skill_target = 6

    else:
        # This should NEVER be hit in normal operation
        grunt.history.append(f'***ERROR!!!: Unknown assignment {sa} in flight_res - using safe fallback')
        survival_target = 0
        decoration_target = 20
        combat_action = False
        promotion_target = 20
        skill_target = 20

    # ====================== DMs ======================
    s_dm = grunt.skills.get('Pilot', 0)                    # Pilot skill helps survival
    d_dm = 1 if getattr(grunt.upp, 'dex', 0) >= 10 else 0
    p_dm = 1 if getattr(grunt.upp, 'dex', 0) >= 9 else 0

    # Officer command bonus in combat assignments
    if sa in ('Battle', 'Strike') and grunt.officer:
        if grunt.rank <= 1:
            p_dm += 1
        elif grunt.rank == 2:
            p_dm += 2
        elif grunt.rank == 3:
            p_dm += 3
        elif grunt.rank == 4:
            p_dm += 4
        elif grunt.rank <= 6:
            p_dm += 5
        else:
            p_dm += 6

    # ====================== ROLLS ======================
    # Survival
    sroll = s_dm + dice(qty=2)
    if sroll < survival_target:
        grunt.history.append(f'Failed survival target of {survival_target} (rolled {sroll})')
        grunt.alive = False
        return False
    elif sroll == survival_target and combat_action:
        grunt.decorations.append(f'Wound Badge awarded in {sa}')
        grunt.history.append(f'Wound Badge awarded in {sa}')

    # Decoration
    droll = d_dm + dice(qty=2)
    if droll >= decoration_target:
        promotions.get_medal(grunt, droll, decoration_target, sa)

    # Promotion
    p_roll = p_dm + dice(qty=2)
    if not grunt.officer:
        if p_roll >= promotion_target:
            promotions.promote(grunt)
    elif not getattr(grunt, 'promote_this_term', False):
        if p_roll >= promotion_target:
            promotions.promote(grunt)

    # Skill Gain
    if dice(qty=2) >= skill_target:
        get_navy_skill(grunt, command, sa)

    return True
#end of flight_res


def gunnery_res(grunt, sa, command):
    """Resolve one year for Gunnery branch"""

        # ====================== ASSIGNMENT PARAMETERS ======================
    if sa == 'Training':
        survival_target = 0          # Auto success
        decoration_target = 20
        combat_action = False
        promotion_target = 6 if not grunt.officer else 20
        skill_target = 8

    elif sa == 'Shore Duty':
        survival_target = 3
        decoration_target = 12
        combat_action = False
        promotion_target = 6 if not grunt.officer else 20
        skill_target = 20            # Usually no skill gain on shore duty

    elif sa == 'Patrol':
        survival_target = 4
        decoration_target = 11
        combat_action = True
        promotion_target = 8
        skill_target = 7

    elif sa == 'Siege':
        survival_target = 5
        decoration_target = 10
        combat_action = True
        promotion_target = 10
        skill_target = 7

    elif sa == 'Strike':
        survival_target = 5
        decoration_target = 9
        combat_action = True
        promotion_target = 7
        skill_target = 6

    elif sa == 'Battle':
        survival_target = 6
        decoration_target = 7
        combat_action = True
        promotion_target = 6
        skill_target = 6

    else:
        # This should NEVER be hit in normal operation
        grunt.history.append(f'ERROR: Unknown assignment {sa} in gunnery_res - using safe fallback')
        survival_target = 0
        decoration_target = 20
        combat_action = False
        promotion_target = 20
        skill_target = 20

    # ====================== DMs ======================
    d_dm = 1 if getattr(grunt.upp, 'dex', 0) >= 10 else 0
    p_dm = 1 if getattr(grunt.upp, 'dex', 0) >= 9 else 0

    # ====================== ROLLS ======================
    # Survival (Gunnery has no major skill DM on survival)
    sroll = dice(qty=2)
    if sroll < survival_target:
        grunt.history.append(f'Failed survival target of {survival_target} (rolled {sroll})')
        grunt.alive = False
        return False
    elif sroll == survival_target and combat_action:
        grunt.decorations.append(f'Wound Badge awarded in {sa}')
        grunt.history.append(f'Wound Badge awarded in {sa}')

    # Decoration
    droll = d_dm + dice(qty=2)
    if droll >= decoration_target:
        promotions.get_medal(grunt, droll, decoration_target, sa)

    # Promotion
    p_roll = p_dm + dice(qty=2)
    if not grunt.officer:
        if p_roll >= promotion_target:
            promotions.promote(grunt)
    elif not getattr(grunt, 'promote_this_term', False):
        if p_roll >= promotion_target:
            promotions.promote(grunt)

    # Skill Gain
    if dice(qty=2) >= skill_target:
        get_navy_skill(grunt, command, sa)

    return True
# end of gunnery_res

def eng_res(grunt, sa, command):
    """Resolve one year for Engineering branch"""

        # ====================== ASSIGNMENT PARAMETERS ======================
    if sa == 'Training':
        survival_target = 0
        decoration_target = 20
        combat_action = False
        promotion_target = 7 if not grunt.officer else 20
        skill_target = 7
    elif sa == 'Shore Duty':
        survival_target = 0
        decoration_target = 20
        combat_action = False
        promotion_target = 7 if not grunt.officer else 20
        skill_target = 8
    elif sa == 'Patrol':
        survival_target = 3
        decoration_target = 12
        combat_action = True
        promotion_target = 5
        skill_target = 6
    elif sa == 'Siege':
        survival_target = 4
        decoration_target = 11
        combat_action = True
        promotion_target = 8
        skill_target = 7
    elif sa == 'Strike':
        survival_target = 5
        decoration_target = 7
        combat_action = True
        promotion_target = 6
        skill_target = 6
    elif sa == 'Battle':
        survival_target = 5
        decoration_target = 7
        combat_action = True
        promotion_target = 6
        skill_target = 5
    else:
        # This should NEVER be hit in normal operation
        grunt.history.append(f'***ERROR!!!: Unknown assignment {sa} in eng_res - using safe fallback')
        survival_target = 0          # Auto survive
        decoration_target = 20
        combat_action = False
        promotion_target = 20
        skill_target = 20

    # Survival DM
    s_dm = 1 if grunt.skills.get('Engineering', 0) >= 4 else 0

    # Rolls
    sroll = s_dm + dice(qty=2)
    if sroll < survival_target:
        grunt.history.append(f'Failed survival target of {survival_target} (rolled {sroll})')
        grunt.alive = False
        return False
    elif sroll == survival_target and combat_action:
        grunt.decorations.append(f'Wound Badge awarded in {sa}')
        grunt.history.append(f'Wound Badge awarded in {sa}')

    droll = dice(qty=2)
    if droll >= decoration_target:
        promotions.get_medal(grunt, droll, decoration_target, sa)

    p_roll = dice(qty=2)
    if not grunt.officer:
        if p_roll >= promotion_target:
            promotions.promote(grunt)
    elif not getattr(grunt, 'promote_this_term', False):
        if p_roll >= promotion_target:
            promotions.promote(grunt)

    if dice(qty=2) >= skill_target:
        get_navy_skill(grunt, command, sa)

    return True

def medical_res(grunt, sa, command):
    """Resolve one year for Medical branch"""

    # ====================== ASSIGNMENT PARAMETERS ======================
    if sa == 'Training':
        survival_target = 3
        decoration_target = 20
        combat_action = False
        promotion_target = 7 if not grunt.officer else 20
        skill_target = 8

    elif sa == 'Shore Duty':
        survival_target = 3
        decoration_target = 20
        combat_action = False
        promotion_target = 6 if not grunt.officer else 20
        skill_target = 6

    elif sa == 'Patrol':
        survival_target = 3
        decoration_target = 20
        combat_action = True
        promotion_target = 7
        skill_target = 7

    elif sa == 'Siege':
        survival_target = 3
        decoration_target = 20
        combat_action = True
        promotion_target = 8
        skill_target = 7

    elif sa == 'Strike':
        survival_target = 3
        decoration_target = 11
        combat_action = True
        promotion_target = 6
        skill_target = 7

    elif sa == 'Battle':
        survival_target = 4
        decoration_target = 10
        combat_action = True
        promotion_target = 6
        skill_target = 6

    else:
        # This should NEVER be hit in normal operation
        grunt.history.append(f'***ERROR!!!: Unknown assignment {sa} in medical_res - using safe fallback')
        survival_target = 0
        decoration_target = 20
        combat_action = False
        promotion_target = 20
        skill_target = 20

    # ====================== ROLLS ======================
    # Survival (Medical branch is generally very safe)
    sroll = dice(qty=2)
    if sroll < survival_target:
        grunt.history.append(f'Failed survival on {sa} (rolled {sroll})')
        if not getattr(grunt, 'noKill', False):
            grunt.alive = False
        return False
    elif sroll == survival_target and combat_action:
        promotions.award_medal(grunt, "Wound Badge", sa)

    # Decoration
    droll = dice(qty=2)
    if droll >= decoration_target:
        promotions.get_medal(grunt, droll, decoration_target, sa)

    # Promotion
    p_roll = dice(qty=2)
    if not grunt.officer:
        if p_roll >= promotion_target:
            promotions.promote(grunt)
    elif not getattr(grunt, 'promote_this_term', False):
        if p_roll >= promotion_target:
            promotions.promote(grunt)

    # Skill Gain
    if dice(qty=2) >= skill_target:
        get_navy_skill(grunt, command, sa)

    return True
#end of medical_res


def tech_res(grunt, sa, command):
    """Resolve one year for Technical Services branch"""

    if sa == 'Training':
        survival_target = 0
        decoration_target = 20
        combat_action = False
        promotion_target = 7 if not grunt.officer else 20
        skill_target = 7
    elif sa == 'Shore Duty':
        survival_target = 3
        decoration_target = 20
        combat_action = False
        promotion_target = 8
        skill_target = 8
    elif sa == 'Patrol':
        survival_target = 3
        decoration_target = 20
        combat_action = True
        promotion_target = 9
        skill_target = 9
    elif sa == 'Siege':
        survival_target = 3
        decoration_target = 20
        combat_action = True
        promotion_target = 8
        skill_target = 7
    elif sa == 'Strike':
        survival_target = 3
        decoration_target = 9
        combat_action = True
        promotion_target = 8
        skill_target = 7
    elif sa == 'Battle':
        survival_target = 3
        decoration_target = 8
        combat_action = True
        promotion_target = 7
        skill_target = 7
    else:
        # This should NEVER be hit in normal operation
        grunt.history.append(f'ERROR: Unknown assignment {sa} in tech_res - using safe fallback')
        survival_target = 0
        decoration_target = 20
        combat_action = False
        promotion_target = 20
        skill_target = 20

    # Survival DM from high Technical skills
    s_dm = 1 if any(grunt.skills.get(skill, 0) >= 3 for skill in technical) else 0

    # Rolls
    sroll = s_dm + dice(qty=2)
    if sroll < survival_target:
        grunt.history.append(f'Failed survival target of {survival_target} (rolled {sroll})')
        grunt.alive = False
        return False
    elif sroll == survival_target and combat_action:
        grunt.decorations.append(f'Wound Badge awarded in {sa}')
        grunt.history.append(f'Wound Badge awarded in {sa}')

    droll = dice(qty=2)
    if droll >= decoration_target:
        promotions.get_medal(grunt, droll, decoration_target, sa)

    p_roll = dice(qty=2)
    if not grunt.officer:
        if p_roll >= promotion_target:
            promotions.promote(grunt)
    elif not getattr(grunt, 'promote_this_term', False):
        if p_roll >= promotion_target:
            promotions.promote(grunt)

    if dice(qty=2) >= skill_target:
        get_navy_skill(grunt, command, sa)

    return True