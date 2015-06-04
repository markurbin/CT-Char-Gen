# 15 April 2015 - added support for skills as a dictionary

from dice import *
from arm_data import *

army_life = ('Brawling', '+1 str', 'Gambling', '+1 dex', '+1 end', '+1 end', '+1 Pistol', '+1 soc', '+1 soc')
marine_life = ('Brawling', 'Gambling', '+1 str', '+1 dex', '+1 end', '+1 Blade', '+1 edu', '+1 soc', '+1 soc')

nco_skills = ('Hvy Wpns', 'Mechanical', 'Tactics', 'Hvy Wpns', 'Mechanical', 'Tactics', 'Leader', 'Leader', 'Admin', 'Instruction', 'Admin')
command_skills = ('+1 end', 'Gun Cmbt', 'Vehicle', 'Hvy Wpns', 'Leader', 'Tactics', 'Tactics', 'Leader')
staff_skills = ('Mechanical', 'Fwd Obs', 'Computer', 'Electronics', 'Medic', 'Instruction', 'Admin', 'Admin')
shipboard_skills = ('Fwd Obs', 'Ships Boat', 'Gunnery', 'Vac Suit', 'Gunnery', 'Vac Suit')

'''
def record(grunt, skillname):
    #grunt.skills.append(skillname)
    # if it is a stat increase, don't list it in skills, just apply it
    # record in history either way
    if '+' in skillname:
        grunt.apply_skill(skillname)
    else:
        grunt.skills[skillname] = grunt.skills.get(skillname,0) + 1
    grunt.history.append(skillname)
''' 

def life_skill(grunt):
    'get a skill from the army life table'

    roll = dice()
    if grunt.officer:
        if grunt.rank < 3:
            roll += 1
        elif grunt.rank < 6:
            roll += 2
        elif grunt.rank > 6:
            roll += 3

    if grunt.is_army():
        table = army_life
    elif grunt.is_marine():
        table = marine_life
    else:
        raise Exception()

    grunt.add_skill(table[roll-1] )
#end of life_skill


###################################################################
#  get_nco_skill(grunt)
#  grunt is the character object
#
#  updates the character object with a skill from the NCO Life table
#
###################################################################
def get_nco_skill(grunt):

    roll = dice()

    if grunt.rank == 4:   # Sergeant
        roll += 1
    elif grunt.rank == 5: # Gunnery Sergeant
        roll += 2
    elif grunt.rank == 6: # Leading Sergeant
        roll += 3
    elif grunt.rank == 7: # First Sergeant'
        roll += 4
    elif grunt.rank == 8: # Sergeant Major
        roll += 5

    grunt.add_skill(nco_skills[roll-1] )
#end of get_nco_skill

###################################################################
#  get_mos_skill(grunt)
#  grunt is the character object
#
#  updates the character object with a skill from the MOS table
#
###################################################################
def get_mos_skill(grunt):

    roll = dice()
    if grunt.TL >= 12:
        roll += 1
    #Army and Marine Arms are the same

    grunt.add_skill(arm_Table[grunt.arm]["mos"][roll-1] )
#end of get_mos_skill

def shipboard_skill(grunt):
    'get a shipboard skill. Only for Marines serving as ships troops'

    roll = dice()
    grunt.add_skill(shipboard_skills[roll-1] )
#end shipboard_skill 
    
def get_staff_skill(grunt):
    roll = dice()
    if (2 < grunt.rank < 6):
        roll += 1
    elif (grunt.rank > 5):
        roll += 2
    
    grunt.add_skill(staff_skills[roll-1] )
#end of get_staff_skill

def get_command_skill(grunt):
    roll = dice()
    if (2 < grunt.rank < 6):
        Roll += 1
    elif (grunt.rank > 5):
        Roll += 2

    grunt.add_skill(command_skills[roll-1] )
#end of get_command_skill

def gain_for_enlisted(grunt, ua, ga):
    if grunt.is_marine() and (ua == 'Shp Trp'):
        shipboard_skill(grunt)
    else:
        if coin_flip():
            life_skill(grunt)
        else:
            get_mos_skill(grunt)

def gain_for_NCO(grunt, ua, ga):
    sides = 3
    if (grunt.is_marine()) and ('Shp Trp' == ua):
        # if ship troops, additional skill table
        sides = 4

    choice = dice(sides=sides)
    if 1 == choice:
        life_skill(grunt)
    elif 2 == choice:
        get_mos_skill(grunt)
    elif 3 == choice:
        get_nco_skill(grunt)
    elif 4 == choice:
        shipboard_skill(grunt)

def gain_for_officer(grunt, ua, ga):
    if 'Command' == ga:
        roll = dice(sides=3)
        if 1 == roll:
            if grunt.is_marine() and ('Shp Trp' == ua):
                shipboard_skill(grunt)
            else:
                life_skill(grunt)
        elif 2 == roll:
            get_mos_skill(grunt)
        elif 3 == roll:
            get_command_skill(grunt)
    elif 'Staff' == ga:
        roll = dice(sides=3)
        if 1 == roll:
            if grunt.is_marine() and ('Shp Trp' == ua):
                shipboard_skill(grunt)
            else:
                life_skill(grunt)
        elif 2 == roll:
            get_mos_skill(grunt)
        elif 3 == roll:
            get_staff_skill(grunt)

def gain(grunt, ua, ga):
    'Skill assignment dependent on branch, arm and assignment'
    # 7/8/12 updated to include shipboard skills and cleaned up
    # officer skill assignment.

    if (grunt.officer == False):          #Not an officer
        if (grunt.rank < 2):          # Enlisted
            gain_for_enlisted(grunt, ua, ga)
        elif (grunt.rank > 1):     #NCO
            gain_for_NCO(grunt, ua, ga)
    else:   #Bleeding Officer
        gain_for_officer(grunt, ua, ga)
#end of get_skill
