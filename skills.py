# 15 April 2015 - added support for skills as a dictionary
# 22 July 2026 - MU - massive update - Lots of bug fixes

from dice import *
from arm_data import *
# Navy tables import - add this line
from navy_tables import (
    line_crew, flight, gunnery, engineering, 
    medical, technical
)

# Life Skill Tables
army_life = ('Brawling', '+1 str', 'Gambling', '+1 dex', '+1 end', '+1 end', '+1 Pistol', '+1 soc', '+1 soc')
marine_life = ('Brawling', 'Gambling', '+1 str', '+1 dex', '+1 end', '+1 Blade', '+1 edu', '+1 soc', '+1 soc')
navy_life = ('Brawling', '+1 str', 'Carousing', 'Gambling', '+1 end', '+1 dex', '+1 end', '+1 edu', 'Carousing', 'Vacc Suit')
scout_life = ('+1 str', '+1 dex', 'Vacc Suit', 'Pilot', 'Nav', 'Jack-o-T', 'Gun Cbt', 'Recon')
merchant_life = ('Steward', 'Broker', 'Admin', 'Vacc Suit', 'Gun Cbt', 'Pilot', 'Jack-o-T', '+1 end', '+1 soc')

nco_skills = ('Hvy Wpns', 'Mechanical', 'Tactics', 'Hvy Wpns', 'Mechanical', 'Tactics', 'Leader', 'Leader', 'Admin', 'Instruction', 'Admin')
command_skills = ('+1 end', 'Gun Cmbt', 'Vehicle', 'Hvy Wpns', 'Leader', 'Tactics', 'Tactics', 'Leader')
staff_skills = ('Mechanical', 'Fwd Obs', 'Computer', 'Electronics', 'Medic', 'Instruction', 'Admin', 'Admin')
shipboard_skills = ('Fwd Obs', 'Ships Boat', 'Gunnery', 'Vac Suit', 'Gunnery', 'Vac Suit')

def record(grunt, skillname):
    """Core function to record a skill or stat increase."""
    if skillname is None or not skillname:
        grunt.history.append("DEBUG: Skipped None skill in record()")  # optional
        return

    if isinstance(skillname, str) and '+' in skillname:
        grunt.apply_skill(skillname)
    else:
        grunt.skills[skillname] = grunt.skills.get(skillname, 0) + 1

    grunt.history.append(skillname)

def life_skill(grunt):
    """Life Skill Table - General skill from branch life table"""
    roll = dice()
    
    if grunt.officer:
        # Officers get a bonus based on rank
        roll = min(roll + (grunt.rank // 2), len(army_life))  # using army_life length as max

    if grunt.branch == 'Imperial Army':
        table = army_life
    elif grunt.branch == 'Imperial Marines':
        table = marine_life
    elif grunt.branch == 'Imperial Navy':
        table = navy_life
    elif grunt.branch == 'Scouts':
        table = scout_life
    elif grunt.branch == 'Merchant':
        table = merchant_life
    else:
        table = army_life  # safe fallback

    roll = min(roll, len(table))
    record(grunt, table[roll - 1])

# === YOUR ORIGINAL FUNCTIONS GO HERE (copy them in unchanged) ===
# get_nco_skill, get_mos_skill, shipboard_skill, get_staff_skill,
# get_command_skill, gain_for_enlisted, gain_for_NCO, gain_for_officer, gain

###################################################################
#  get_nco_skill(grunt)
#  grunt is the character object
#
#  updates the character object with a skill from the NCO Life table
#
###################################################################
def get_nco_skill(grunt):
    """NCO Life Skill Table"""
    roll = dice()

    if grunt.rank == 4:      # Sergeant
        roll += 1
    elif grunt.rank == 5:    # Gunnery Sergeant
        roll += 2
    elif grunt.rank == 6:    # Leading Sergeant
        roll += 3
    elif grunt.rank == 7:    # First Sergeant
        roll += 4
    elif grunt.rank == 8:    # Sergeant Major
        roll += 5

    roll = min(roll, len(nco_skills))
    record(grunt, nco_skills[roll - 1])
#end of get_nco_skill

###################################################################
#  get_mos_skill(grunt)
#  grunt is the character object
#
#  updates the character object with a skill from the MOS table
#
###################################################################
def get_mos_skill(grunt):
    """Get branch-specific MOS skill for Army/Marine or Navy"""
    roll = dice()
    if grunt.TL >= 12:
        roll += 1
    roll = min(roll, 7) - 1   # prevent index errors

    if grunt.is_navy():
        # === NAVY BRANCH SKILLS ===
        if grunt.arm in ('Line', 'Crew'):
            skill = line_crew[roll]
        elif grunt.arm == 'Flight':
            skill = flight[roll]
        elif grunt.arm == 'Gunnery':
            skill = gunnery[roll]
        elif grunt.arm == 'Engineering':
            skill = engineering[roll]
        elif grunt.arm == 'Medical':
            skill = medical[roll]
        elif grunt.arm == 'Technical Services':
            skill = technical[roll]
        else:
            skill = 'Vacc Suit'                     # safe fallback
    else:
        # === ARMY / MARINE ===
        skill = arm_Table[grunt.arm]["mos"][roll]

    record(grunt, skill)

    
def shipboard_skill(grunt):
    """Shipboard skill for Marines serving as Ship's Troops."""
    roll = dice()
    roll = min(roll, len(shipboard_skills))
    
    record(grunt, shipboard_skills[roll - 1])
    
def get_staff_skill(grunt):
    """Officer Staff Skill Table"""
    roll = dice()
    if (2 < grunt.rank < 6):
        roll += 1
    elif (grunt.rank > 5):
        roll += 2

    roll = min(roll, len(staff_skills))
    record(grunt, staff_skills[roll - 1])
#end of get_staff_skill

def get_command_skill(grunt):
    """Officer Command Skill Table"""
    roll = dice()
    if (2 < grunt.rank < 6):
        roll += 1
    elif (grunt.rank > 5):
        roll += 2

    roll = min(roll, len(command_skills))
    record(grunt, command_skills[roll - 1])

def gain_for_enlisted(grunt, ua, ga):
    """Enlisted skill gain logic"""
    if grunt.is_marine() and (ua == 'Shp Trp'):
        shipboard_skill(grunt)
    else:
        if coin_flip():
            life_skill(grunt)
        else:
            get_mos_skill(grunt)

def gain_for_NCO(grunt, ua, ga):
    """NCO skill gain logic"""
    sides = 3
    if grunt.is_marine() and (ua == 'Shp Trp'):
        sides = 4   # Extra option for Ship Troops

    choice = dice(sides=sides)
    if choice == 1:
        life_skill(grunt)
    elif choice == 2:
        get_mos_skill(grunt)
    elif choice == 3:
        get_nco_skill(grunt)
    elif choice == 4:
        shipboard_skill(grunt)

def gain_for_officer(grunt, ua, ga):
    """Officer skill gain logic"""
    if ga == 'Command':
        roll = dice(sides=3)
        if roll == 1:
            if grunt.is_marine() and (ua == 'Shp Trp'):
                shipboard_skill(grunt)
            else:
                life_skill(grunt)
        elif roll == 2:
            get_mos_skill(grunt)
        elif roll == 3:
            get_command_skill(grunt)

    elif ga == 'Staff':
        roll = dice(sides=3)
        if roll == 1:
            if grunt.is_marine() and (ua == 'Shp Trp'):
                shipboard_skill(grunt)
            else:
                life_skill(grunt)
        elif roll == 2:
            get_mos_skill(grunt)
        elif roll == 3:
            get_staff_skill(grunt)

def gain(grunt, ua=None, ga=None):
    """Main skill gain dispatcher.
    Routes to the correct gain function based on branch and rank."""
    
    # Special branches
    if grunt.branch in ('Scouts', 'Merchant'):
        if coin_flip():
            life_skill(grunt)
        else:
            get_mos_skill(grunt)
        return

    # Navy / Army / Marine logic
    if not grunt.officer:
        if grunt.rank < 2:          # Enlisted
            gain_for_enlisted(grunt, ua, ga)
        else:                       # NCO
            gain_for_NCO(grunt, ua, ga)
    else:                           # Officer
        gain_for_officer(grunt, ua, ga)

