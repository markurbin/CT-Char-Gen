# Traveller Book 4 Mercenary specific data and functions
# "The Traveller game in all forms is owned by Far 
# Future Enterprises. Copyright 1977 - 2013 Far Future Enterprises."
# 
# Mark Urbin

from b1_data2 import apply_skill
from b1_data2 import branch_Table
from random import randint

arm_Table = ['Infantry', 'Cavalry', 'Artillery', 'Support', 'Commando']  #same table as the Imperial Marines
army_life = ['Brawling', '+1 str', 'Gambling', '+1 dex', '+1 end', '+1 end', '+1 Pistol', '+1 soc', '+1 soc']
marine_life = ['Brawling', 'Gambling', '+1 str', '+1 dex', '+1 end', '+1 Blade', '+1 edu', '+1 soc', '+1 soc']

mos_art = ['FA Gunner', 'FA Gunner', 'Vehicle', 'Mechanical', 'Fwd Obs', 'Computer', 'Electronics']
mos_cav = ['Vehicle', 'Vehicle', 'Vehicle', 'Hvy Wpns', 'Hvy Wpns', 'Mechanical', 'Computer']
mos_inf = ['Gun Cmbt', 'Gun Cmbt', 'Hvy Wpns', 'Hvy Wpns', 'Vehicle', 'Recon', 'Vac Suit']
mos_mar = ['Gun Cmbt', 'Gun Cmbt', 'Zero-G', 'Zero-G', 'Hvy Wpns', 'Fwd Obs', 'Battle dress']
mos_sup = ['Vehicle', 'Cmbt Eng', 'Vehicle', 'Mechanical', 'Electronics', 'Medic', 'Computer']
mos_com = ['Gun Cmbt', 'Gun Cmbt', 'Hvy Wpns', 'Demolition', 'Survival', 'Recon', 'Battle dress']

ga_art = ['Command', 'Command', 'Command', 'Staff', 'Staff', 'Staff', 'Special', 'Special']
ga_cav = ['Command', 'Command', 'Command', 'Command', 'Staff', 'Staff', 'Special', 'Special']
ga_inf = ['Command', 'Command', 'Command', 'Command', 'Staff', 'Staff', 'Special', 'Special']
ga_mar = ['Command', 'Command', 'Command', 'Command', 'Staff', 'Staff', 'Special', 'Special']
ga_sup = ['Command', 'Command', 'Staff', 'Staff', 'Staff', 'Staff', 'Special', 'Special']
ga_com = ['Command', 'Command', 'Command', 'Command', 'Staff', 'Special', 'Special']

ua_art = ['Raid', 'Trng', 'Ctr Ins', 'Pol Act', 'Garr', 'Garr', 'Garr', 'Trng', 'Pol Act', 'Ctr Ins', 'Trng']
ua_cav = ['Raid', 'Trng', 'Ctr Ins', 'Pol Act', 'Garr', 'Garr', 'Garr', 'Trng', 'Pol Act', 'Intl Sec', 'Trng']
ua_inf = ['Raid', 'Trng', 'Ctr Ins', 'Ctr Ins', 'Garr', 'Garr', 'Garr', 'Trng', 'Pol Act', 'Intl Sec', 'Intl Sec']
ua_mar = ['Raid', 'Raid', 'Ctr Ins', 'Intl Sec', 'Shp Trp', 'Garr', 'Shp Trp', 'Trng', 'Ctr Ins', 'Pol Act', 'Pol Act']
ua_sup = ['Raid', 'Intl Sec', 'Ctr Ins', 'Garr', 'Garr', 'Garr', 'Garr', 'Trng', 'Pol Act', 'Intl Sec', 'Pol Act', ]
ua_com = ['Raid', 'Raid', 'Ctr Ins', 'Pol Act', 'Intl Sec', 'Garr', 'Trng', 'Trng', 'Ctr Ins', 'Raid', 'Raid']

sa_enl = ['Cross Trng', 'Specialist School', 'Commando School', 'Protected Forces', 'Recruiting', 'OCS', 'OCS']
sa_officer = ['Intelligence School', 'Command College', 'Staff College', 'Commando School', 'Recruiting', 'Military Attache/Aide']
specialist_school_table = ['Admin', 'Medical', 'Commo', 'Computer', 'Mechanical', 'Electronics']

nco_skills = ['Hvy Wpns', 'Mechanical', 'Tactics', 'Hvy Wpns', 'Mechanical', 'Tactics', 'Leader', 'Leader', 'Admin', 'Instruction', 'Admin']
command_skills = ['+1 end', 'Gun Cmbt', 'Vehicle', 'Hvy Wpns', 'Leader', 'Tactics', 'Tactics', 'Leader']
staff_skills = ['Mechanical', 'Fwd Obs', 'Computer', 'Electronics', 'Medic', 'Instruction', 'Admin', 'Admin']
shipboard_skills = ['Fwd Obs', 'Ships Boat', 'Gunnery', 'Vac Suit', 'Gunnery', 'Vac Suit']
erank = ['Private', 'Lance Corporal', 'Corporal', 'Lance Sergeant', 'Sergeant', 'Gunnery Sergeant', 'Leading Sergeant', 'First Sergeant', 'Sergeant Major']
orank = ['Second Lieutenant', 'First Lieutenant', 'Captain', 'Major', 'Lieutenant Colonel', 'Colonel', 'Brigadier General', 'Major General', 'Lieutenant General', 'General']

###################################################################
#  army_life_skill(grunt)
#  grunt is the character object
#
#  updates the character object with a skill from the Army Life table
#
###################################################################
def army_life_skill(grunt):
    'get a skill from the army life table'

    roll = randint(0,5)
    if grunt.officer:
        if grunt.rank < 3:
            roll += 1
        elif grunt.rank < 6:
            roll += 2
        elif grunt.rank > 6:
            roll += 3

    
    grunt.skills.append(army_life[roll])
    grunt.history.append(army_life[roll])
    apply_skill(grunt,army_life[roll])
#end of army_life_skill

###################################################################
#  marine_life_skill(grunt)
#  grunt is the character object
#
#  updates the character object with a skill from the Marine Life table
#
###################################################################
def marine_life_skill(grunt):
    'get a skill from the marine life table'

    roll = randint(0,5)
    if grunt.officer:
        if grunt.rank < 3:
            roll += 1
        elif grunt.rank < 6:
            roll += 2
        elif grunt.rank > 6:
            roll += 3

    grunt.skills.append(marine_life[roll])
    apply_skill(grunt,marine_life[roll])
    grunt.history.append(marine_life[roll])
#end marine_life_skill

###################################################################
#  get_nco_skill(grunt)
#  grunt is the character object
#
#  updates the character object with a skill from the NCO Life table
#
###################################################################
def get_nco_skill(grunt):

    roll = randint(0,5)

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

    grunt.skills.append(nco_skills[roll])
    grunt.history.append(nco_skills[roll])
#end of get_nco_skill

###################################################################
#  get_mos_skill(grunt)
#  grunt is the character object
#
#  updates the character object with a skill from the MOS table
#
###################################################################
def get_mos_skill(grunt):

    roll = randint(0,5)
    if grunt.TL >= 12:
        roll += 1
#Army and Marine Arms are the same

    if grunt.arm == arm_Table[0]:
        grunt.skills.append(mos_inf[roll])
        grunt.history.append(mos_inf[roll])
    elif grunt.arm == arm_Table[1]:
        grunt.skills.append(mos_cav[roll])
        grunt.history.append(mos_cav[roll])

    elif grunt.arm == arm_Table[2]:
        grunt.skills.append(mos_art[roll])
        grunt.history.append(mos_art[roll])

    elif grunt.arm == arm_Table[3]:
        grunt.skills.append(mos_sup[roll])
        grunt.history.append(mos_sup[roll])

    elif grunt.arm == arm_Table[4]:
        grunt.skills.append(mos_com[roll])
        grunt.history.append(mos_com[roll])
#end of get_mos_skill


###################################################################
#  display_b4_rank(grunt)
#  grunt is the character object
#
#  prints the characters B4 rank to the screen
#
###################################################################
def display_b4_rank(grunt):
    'prints the characters B4 rank to the screen'

    if grunt.officer == False:
        print erank[grunt.rank]
    else:
        if (grunt.branch == 'Imperial Marines') and (grunt.rank == 3):
            print('Force Commander')
        else:
            print(orank[grunt.rank])

def get_medal(grunt, roll, target, ua):

    if (roll - target) >= 6:
        grunt.decorations.append('SEH awarded in %s' % ua)
        grunt.history.append('SEH awarded in %s' % ua)
    elif (3 <= (roll - target) < 6):
        grunt.decorations.append('MCG awarded in %s' % ua)
        grunt.history.append('MCG awarded in %s' % ua)
    elif (roll - target) < 3:
        grunt.decorations.append('MCUF awarded in %s' % ua)
        grunt.history.append('MCUF awarded in %s' % ua)
#end of get_medal

def e_promote(grunt):

    if grunt.officer:
        o_promote(grunt)
        return False
    grunt.rank += 1
    if grunt.rank > 8:
        grunt.rank = 8
        s = 'No promotion avilable until after OCS' 
        grunt.history.append(s)
        return True
    else:
        s = 'Promoted to %s' % erank[grunt.rank]
        grunt.history.append(s)
        return True
#end e_promote

def o_promote(grunt):

    if (False == grunt.officer):   #error condition, should never hit this
        e_promote(grunt)
        return False
    if grunt.rank == 9:
        grunt.rank = 9
        s = 'No further romotion availiable.' 
        grunt.history.append(s)
    else:
        grunt.rank += 1
        grunt.promote_this_term = True
        s = 'Promoted to %s' % orank[grunt.rank]
        grunt.history.append(s)
    return True
#end of o_promote

def shipboard_skill(grunt):
    'get a shipboard skill. Only for Marines serving as ships troops'

    roll = randint(0,5)
    grunt.skills.append(shipboard_skills[roll])
    grunt.history.append(shipboard_skills[roll])
#end shipboard_skill 
    
def get_staff_skill(grunt):

    roll = randint(0,5)
    if (2 < grunt.rank < 6):
        roll += 1
    elif (grunt.rank > 5):
        roll += 2
    
    grunt.skills.append(staff_skills[roll])
    grunt.history.append(staff_skills[roll])
#end of get_staff_skill


def get_command_skill(grunt):

    roll = randint(0,5)
    if (2 < grunt.rank < 6):
        Roll += 1
    elif (grunt.rank > 5):
        Roll += 2

    
    grunt.skills.append(command_skills[roll])
    grunt.history.append(command_skills[roll])
#end of get_command_skill

def commando_school(grunt):

    grunt.schools.append('Commando')
    # need to add check for number of skills
    # if has level 2 in any of the listed skills
    # then the character is an instructor at the school
    # and gets one leve of Instruction skill
    
    if randint(0,5) >= 4:
        grunt.skills.append('Brawling')
        grunt.history.append('Brawling')
    if randint(0,5) >= 4:
        grunt.skills.append('Gun Cmbt')
        grunt.history.append('Gun Cmbt')
    if randint(0,5) >= 4:
        grunt.skills.append('Demolition')
        grunt.history.append('Demolition')
    if randint(0,5) >= 4:
        grunt.skills.append('Wilderness Survival')
        grunt.history.append('Wilderness Survival')
    if randint(0,5) >= 4:
        grunt.skills.append('Recon')
        grunt.history.append('Recon')
    if randint(0,5) >= 4:
        grunt.skills.append('Vac Suit')
        grunt.history.append('Vac Suit')
    if randint(0,5) >= 4:
        grunt.skills.append('Blade Cbt')
        grunt.history.append('Blade Cbt')
    if randint(0,5) >= 4:
        grunt.skills.append('Instruction')
        grunt.history.append('Instruction')
#end of Commando_school

def cross_train(grunt):
    'Book 4 cross training'
    
    if grunt.branch == branch_Table[0]:
        if grunt.arm == arm_Table[0]:
            roll = randint(1,3)
            grunt.xtrained.append(arm_Table[roll])
            s = 'Cross Trained in ' + arm_Table[roll]
            grunt.history.append(s)
            get_mos_skill(grunt)
        elif grunt.arm == arm_Table[1]:
            roll = randint(1,3)
            if roll == 1:
                roll = 0    #Can't x-train in your arm, setting to infantry
            grunt.xtrained.append(arm_Table[roll])
            s = 'Cross Trained in ' + arm_Table[roll]
            grunt.history.append(s)
            get_mos_skill(grunt)
        elif grunt.arm == arm_Table[2]:
            roll = randint(1,3)
            if roll == 2:
                roll = 0    #Can't x-train in your arm, setting to infantry
            grunt.xtrained.append(arm_Table[roll])
            s = 'Cross Trained in ' + arm_Table[roll]
            grunt.history.append(s)
            get_mos_skill(grunt)
        elif grunt.arm == arm_Table[3]:
            roll = randint(1,3)
            if roll == 3:
                roll = 0    #Can't x-train in your arm, setting to infantry
            grunt.xtrained.append(arm_Table[roll])
            s = 'Cross Trained in ' + arm_Table[roll]
            grunt.history.append(s)
            get_mos_skill(grunt)
        elif grunt.arm == arm_Table[4]:
            roll = randint(0,3)  #x-training commandos is easy
            grunt.xtrained.append(arm_Table[roll])
            s = 'Cross Trained in ' + arm_Table[roll]
            grunt.history.append(s)
            get_mos_skill(grunt)
    elif grunt.branch == branch_Table[1]:
        if grunt.arm == arm_Table[0]:
            roll = randint(1,3)
            grunt.xtrained.append(arm_Table[roll])
            s = 'Cross Trained in '  + arm_Table[roll]
            grunt.history.append(s)
            get_mos_skill(grunt)
        elif grunt.arm == arm_Table[1]:
            roll = randint(1,3)
            if roll == 1:
                roll = 0    #Can't x-train in your arm, setting to infantry
            grunt.xtrained.append(arm_Table[roll])
            s = 'Cross Trained in ' + arm_Table[roll]
            grunt.history.append(s)
            get_mos_skill(grunt)
        elif grunt.arm == arm_Table[2]:
            roll = randint(1,3)
            if roll == 2:
                roll = 0    #Can't x-train in your arm, setting to infantry
            grunt.xtrained.append(arm_Table[roll])
            s = 'Cross Trained in ' + arm_Table[roll]
            grunt.history.append(s)
            get_mos_skill(grunt)
        elif grunt.arm == arm_Table[3]:
            roll = randint(1,3)
            if roll == 3:
                roll = 0    #Can't x-train in your arm, setting to infantry
            grunt.xtrained.append(arm_Table[roll])
            s = 'Cross Trained in ' + arm_Table[roll]
            grunt.history.append(s)
            get_mos_skill(grunt)
        elif grunt.arm == arm_Table[4]:
            roll = randint(0,3)  #x-training commandos is easy
            grunt.xtrained.append(arm_Table[roll])
            s = 'Cross Trained in ' + arm_Table[roll]
            grunt.history.append(s)
            get_mos_skill(grunt)
    elif grunt.branch == branch_Table[2]:
        print 'X-Training in the navy!' #debug
        b5_data.navy_xtrain(grunt)
#end of cross_train

def specialist_school(grunt):
  
    roll = randint(0,5)
    s = 'Attended %s school' % specialist_school_table[roll]
    grunt.history.append(s)
    
    grunt.skills.append(specialist_school_table[roll])
    grunt.history.append(specialist_school_table[roll])
    
    school = 'Specialist School: ' + specialist_school_table[roll]
    grunt.schools.append(school)
#send of specialist_school

def pf_training(grunt):

    grunt.schools.append('Protected Forces')
    grunt.history.append('Protected Forces Training')
    # need to add check for number of skills
    # if has level 2 in any of the listed skills
    # then the character is an instructor at the school
    # and gets one level of Instruction skill

    if randint(0,5) >= 2:
        grunt.skills.append('Vac Suit')
    grunt.history.append('Vac Suit')
    if randint(0,5) >= 2:
        grunt.skills.append('Zero-G Cbt')
    grunt.history.append('Zero-G Cbt')
#end of pf_training

def ocs(grunt):

    if grunt.officer == True:
        print('Already an officer, cannot attend OCS')
        return False
    grunt.history.append('Attending OCS')
    grunt.schools.append('OCS')
    grunt.officer = True
    grunt.rank = 0
    #1 skill off command Skills and another off Staff Skills
    roll_1 = randint(0,5)
    roll_2 = randint(0,5)
    grunt.skills.append(command_skills[roll_1])
    grunt.skills.append(staff_skills[roll_2])
    grunt.history.append(command_skills[roll_1])
    grunt.history.append(staff_skills[roll_2])

    #IA and IM, in addition get a MOS Table skill
    if (grunt.branch == branch_Table[0]) or (grunt.branch == branch_Table[1]):
        roll_1 = randint(0,5)
        if grunt.arm == 0:
            grunt.skills.append(mos_inf[roll_1])
            grunt.history.append(mos_inf[roll_1])
        elif grunt.arm == 1:
            grunt.skills.append(mos_cav[roll_1])
            grunt.history.append(mos_cav[roll_1])
        elif grunt.arm == 2:
            grunt.skills.append(mos_art[roll_1])
            grunt.history.append(mos_art[roll_1])
        elif grunt.arm == 3:
            grunt.skills.append(mos_sup[roll_1])
            grunt.history.append(mos_sup[roll_1])
        elif grunt.arm == 2:
            grunt.skills.append(mos_com[roll_1])
            grunt.history.append(mos_com[roll_1])
    else:
        print 'in OCS, not in Imperial Army or Imperial Marines'
#end of ocs

def special_assign(grunt):

    roll = randint(0,5)

    if grunt.officer:    
        s = 'Special Assignment is %s' % sa_officer[roll]
        grunt.history.append(s)
        if 0 == roll:
            grunt.schools.append(sa_officer[roll])
            grunt.history.append(sa_officer[roll])
            if randint(0,5) >= 3:
                grunt.skills.append('Forgery')
                grunt.history.append('Forgery')
            if randint(0,5) >= 3:
                grunt.skills.append('Bribery')
                grunt.history.append('Bribery')
            if randint(0,5) >= 3:
                grunt.skills.append('Streetwise')
                grunt.history.append('Streetwise')
            if randint(0,5) >= 3:
                grunt.skills.append('Interrogation')
                grunt.history.append('Interrogation')
        elif 1 == roll:
            grunt.schools.append(sa_officer[roll])
            grunt.history.append(sa_officer[roll])
            if randint(0,5) >= 3:
                grunt.skills.append('Tactics')
                grunt.history.append('Tactics')
            if randint(0,5) >= 3:
                grunt.skills.append('Leadership')
                grunt.history.append('Leadership')
            if randint(0,5) >= 3:
                grunt.skills.append('Recon')
                grunt.history.append('Recon')
        elif 2 == roll:
            grunt.schools.append(sa_officer[roll])
            grunt.history.append(sa_officer[roll])
            if randint(0,5) >= 3:
                grunt.skills.append('Admin')
                grunt.history.append('Admin')
            if randint(0,5) >= 3:
                grunt.skills.append('Engineering')
                grunt.history.append('Engineering')
            if randint(0,5) >= 3:
                grunt.skills.append('Computer')
                grunt.history.append('Computer')
        elif 3 == roll:
            commando_school(grunt)
        elif 4 == roll:
            grunt.specials.append(sa_officer[roll])
            grunt.history.append(sa_officer[roll])
            grunt.skills.append('Recruiting')
            #grunt.history.append('Recruiting')
        elif 5 == roll:
            if randint(0,5) > 3:
                grunt.upp.soc += 1
                grunt.specials.append('Aide to General officer')
                grunt.history.append('Aide to General officer')
                grunt.history.append('+1 Soc')
            else:
                grunt.upp.soc += 1
                grunt.rank += 1   #Not using o_promote() here because this can override the 1 promotion per term rule
                if grunt.rank > 8:
                    grunt.rank = 8
                    grunt.history.append('Already at Max Officer rank. No promotion')
                grunt.specials.append('Military Attache')
                grunt.history.append('Military Attache')
                grunt.history.append('+1 Soc & promotion')  
    else:
        s = 'Special Assignment is %s' % sa_enl[roll]
        grunt.history.append(s)
        if roll == 0:
            cross_train(grunt)
        elif roll == 1:
            specialist_school(grunt)
        elif roll == 2:
            commando_school(grunt)
        elif roll == 3:
            pf_training(grunt)
        elif roll == 4:
            grunt.skills.append('Recruiting')
            grunt.history.append('Recruiting')
        elif roll == 5:
            ocs(grunt)
#end of special_assignment

def get_skill(grunt, ua, ga):
    'Skill assignment dependent on branch, arm and assignment'
    # 7/8/12 updated to include shipboard skills and cleaned up
    # officer skill assignment.

    if (grunt.officer == False):          #Not an officer'
        if (grunt.rank < 2):          # Enlisted
            if grunt.branch == branch_Table[0]:      # Army - Army Life of MOS skill
                if (1 == randint(0, 1)):
                    army_life_skill(grunt)
                else:
                    get_mos_skill(grunt)
            elif grunt.branch == branch_Table[1]:    # Marine, if shipboard troops roll of shp trp table
                if ua == 'Shp Trp':
                    shipboard_skill(grunt)
                else:
                    if (1 == randint(0, 1)):
                        marine_life_skill(grunt)
                    else:
                        get_mos_skill(grunt)
                        
         
        elif (grunt.rank > 1):     #NCO
            if (branch_Table[1] == grunt.branch) and ('Shp Trp' == ua):     # if ship troops, additional skill table
                choice = randint(0,3)
            else:
                choice = randint(0, 2)
            if 0 == choice:
                if grunt.branch == branch_Table[0]:
                    army_life_skill(grunt)
                elif grunt.branch == branch_Table[1]:
                    marine_life_skill(grunt)
            elif 1 == choice:
                get_mos_skill(grunt)
            elif 2 == choice:
                get_nco_skill(grunt)
            elif 3 == choice:
                shipboard_skill(grunt)
    else:   #Bleeding Officer
        if 'Command' == ga:
            roll = randint(0,2)
            if 0 == roll:
                if branch_Table[0] == grunt.branch:     #Army
                    army_life_skill(grunt)
                elif branch_Table[1] == grunt.branch:   #Marine
                    if 'Shp Trp' == ua:
                        shipboard_skill(grunt)
                    else:
                        marine_life_skill(grunt)
            elif 1 == roll:
                get_mos_skill(grunt)
            elif 2 == roll:
                get_command_skill(grunt)
        elif 'Staff' == ga:
            roll = randint(0,2)
            if 0 == roll:
                if branch_Table[0] == grunt.branch:     #Army
                    army_life_skill(grunt)
                elif branch_Table[1] == grunt.branch:   #Marine
                    if 'Shp Trp' == ua:
                        shipbard_skill(grunt)
                    else:
                        marine_life_skill(grunt)
            elif 1 == roll:
                get_mos_skill(grunt)
            elif 2 == roll:
                get_staff_skill(grunt)
#end of get_skill

def sup_res(grunt, ua, ga):
    'resolve year: support A or M'

    s = 'Unit Assigment is %s' % ua
    grunt.history.append(s)
    auto = 0
    no_chance = 20
    combat_action = 0
    
    
    if ua == 'Trng':
        combat_action = False
        survival_target = auto  #auto survival
        dec_target = no_chance  #No chance for decoration
        if grunt.officer:
            promot_target = no_chance  # officers not elibile for promotion
        else:
            promot_target = 6
        skill_target = 8
    elif ua == 'Intl Sec':
        combat_action = True
        survival_target = 4  
        dec_target = no_chance  
        if grunt.officer:
            promot_target = no_chance  # officers not elibile for promotion
            if ga == 'Command':          
                grunt.ribbons.append(ua + ' Combat Command Ribbon')
                grunt.history.append(ua + ' Combat Command Ribbon')
            else:
                grunt.ribbons.append(ua + ' Combat Ribbon')
                grunt.history.append(ua + ' Combat Ribbon')
        else:
            promot_target = 6
            grunt.ribbons.append(ua + ' Combat Ribbon')
            grunt.history.append(ua + ' Combat Ribbon')
        skill_target = no_chance   # no skill improvement
    elif ua == 'Pol Act':
        combat_action = True
        survival_target = 4  
        dec_target = 10  
        promot_target = 9
        skill_target = 7
        if grunt.officer:
            if ga == 'Command':
                grunt.ribbons.append(ua + ' Combat Command Ribbon')
                grunt.history.append(ua + ' Combat Command Ribbon')
            else:
                grunt.ribbons.append(ua + ' Combat Ribbon')
                grunt.history.append(ua + ' Combat Ribbon')
        else:
            grunt.ribbons.append(ua + ' Combat Ribbon')
            grunt.history.append(ua + ' Combat Ribbon')
    elif ua == 'Ctr Ins':
        combat_action = True
        survival_target = 5  
        dec_target = 11  
        promot_target = 10
        skill_target = 7
        if grunt.officer:
            if ga == 'Command':
                grunt.ribbons.append(ua + ' Combat Command Ribbon')
                grunt.history.append(ua + ' Combat Command Ribbon')
            else:
                grunt.ribbons.append(ua + ' Combat Ribbon')
                grunt.history.append(ua + ' Combat Ribbon')
        else:
            grunt.ribbons.append(ua + ' Combat Ribbon')
            grunt.history.append(ua + ' Combat Ribbon')
    elif ua == 'Raid':
        combat_action = True
        survival_target = 6  
        dec_target = 7  
        promot_target = 7
        skill_target = 6
        if grunt.officer:
            if ga == 'Command':
                grunt.ribbons.append(ua + ' Combat Command Ribbon')
                grunt.history.append(ua + ' Combat Command Ribbon')
            else:
                grunt.ribbons.append(ua + ' Combat Ribbon')
                grunt.history.append(ua + ' Combat Ribbon')
        else:
            grunt.ribbons.append(ua + ' Combat Ribbon')
            grunt.history.append(ua + ' Combat Ribbon')
    elif ua == 'Garr':
        combat_action = False
        survival_target = auto  
        dec_target = no_chance 
        if grunt.officer:
            promot_target = no_chance  # officers not elibile for promotion
        else:
            promot_target = 7
        skill_target = no_chance

    #roll 2 dice
#   roll = randint(1, 6) + randint(1,6)

    # Survival check, no DM coded yet
    sroll = randint(1, 6) + randint(1,6)
    if sroll < survival_target:
        s = 'Failed survival target of %d' % survival_target
        grunt.history.append(s)
        grunt.alive = False
        return 0
    else:
        if ((sroll == survival_target) and combat_action):
            grunt.decorations.append('Wound Badge awarded in ' + ua)

    #Decoration check
    droll = randint(1, 6) + randint(1,6)
    if droll >= dec_target:
        get_medal(grunt, droll, dec_target, ua)
        s = 'Received a %s' % decorations[-1]
        grunt.history.append(s)

    #Promotion check
    p_roll = randint(1, 6) + randint(1,6)
    if grunt.upp.int >= 8:  # +1 DM if int 8+
        p_roll += 1
    if (grunt.arm == arm_Table[4]) and (grunt.upp.end >= 8):
        p_roll += 1     #Commandos get a +1 promotion DM if endurance is 8+
    if grunt.officer:
        if (grunt.promote_this_term == False):
            if p_roll >= promot_target:
                o_promote(grunt)
    else:
        if p_roll >= promot_target:
            e_promote(grunt)

    #Skill check 
    s_roll = randint(1, 6) + randint(1,6)
#    print 'Skill check: roll: %d Target: %d' % (s_roll, skill_target)
    if s_roll >= skill_target:
        get_skill(grunt,ua, ga)
#End of sup_res

def mar_res(grunt, ua, ga):
    'resolve year: Marine Infantry'
    #sprint.sprint(sorf,'resolve year: Marine Infantry',outfile)
    
    s = 'Unit Assigment is %s' % ua
    grunt.history.append(s)
    auto = 0
    no_chance = 20
    combat_action = 0
    
    
    if ua == 'Trng':
        combat_action = False
        survival_target = auto  #auto survival for training
        dec_target = no_chance  #No chance for decoration
        if grunt.officer:
            promot_target = no_chance  # officers not elibile for promotion
        else:
            promot_target = 6
        skill_target = 7
    elif ua == 'Intl Sec':
        combat_action = True
        survival_target = 4  
        dec_target = 12  
        if grunt.officer:
            promot_target = no_chance  # officers not elibile for promotion
            if ga == 'Command':          
                grunt.ribbons.append(ua + ' Combat Command Ribbon')
                grunt.history.append(ua + ' Combat Command Ribbon')
            else:
                grunt.ribbons.append(ua + ' Combat Ribbon')
                grunt.history.append(ua + ' Combat Ribbon')
        else:
            promot_target = 6
            grunt.ribbons.append(ua + ' Combat Ribbon')
            grunt.history.append(ua + ' Combat Ribbon')
        skill_target = no_chance   # no skill improvement
    elif ua == 'Pol Act':
        combat_action = True
        survival_target = 5  
        dec_target = 8  
        promot_target = 8
        skill_target = 7
        if grunt.officer:
            if ga == 'Command':
                grunt.ribbons.append(ua + ' Combat Command Ribbon')
                grunt.history.append(ua + ' Combat Command Ribbon')
            else:
                grunt.ribbons.append(ua + ' Combat Ribbon')
                grunt.history.append(ua + ' Combat Ribbon')
        else:
            grunt.ribbons.append(ua + ' Combat Ribbon')
            grunt.history.append(ua + ' Combat Ribbon')
    elif ua == 'Ctr Ins':
        combat_action = True
        survival_target = 5  
        dec_target = 9  
        promot_target = 9
        skill_target = 8
        if grunt.officer:
            if ga == 'Command':
                grunt.ribbons.append(ua + ' Combat Command Ribbon')
                grunt.history.append(ua + ' Combat Command Ribbon')
            else:
                grunt.ribbons.append(ua + ' Combat Ribbon')
                grunt.history.append(ua + ' Combat Ribbon')
        else:
            grunt.ribbons.append(ua + ' Combat Ribbon')
            grunt.history.append(ua + ' Combat Ribbon')
    elif ua == 'Raid':
        combat_action = True
        survival_target = 6  
        dec_target = 5  
        promot_target = 6
        skill_target = 5
        if grunt.officer:
            if ga == 'Command':
                grunt.ribbons.append(ua + ' Combat Command Ribbon')
                grunt.history.append(ua + ' Combat Command Ribbon')
            else:
                grunt.ribbons.append(ua + ' Combat Ribbon')
                grunt.history.append(ua + ' Combat Ribbon')
        else:
            grunt.ribbons.append(ua + ' Combat Ribbon')
            grunt.history.append(ua + ' Combat Ribbon')
    elif ua == 'Garr':
        combat_action = False
        survival_target = auto  
        dec_target = no_chance 
        if grunt.officer:
            promot_target = no_chance  # officers not elibile for promotion
        else:
            promot_target = 9
        skill_target = no_chance
    elif ua == 'Shp Trp':
        survival_target = 4  
        dec_target = 12 
        if grunt.officer:
            promot_target = no_chance  # officers not elibile for promotion
        else:
            promot_target = 6
        skill_target = 6

 

    #Decoration check
    droll = randint(1, 6) + randint(1,6)
    if droll >= dec_target:
        get_medal(grunt, droll, dec_target, ua)
        s = 'Received a %s' % grunt.decorations[-1]
        grunt.history.append(s)

    #Promotion check
    p_roll = randint(1, 6) + randint(1,6)
    if (grunt.arm == arm_Table[4]) and (grunt.upp.end >= 8):
        p_roll += 1     #Commandos get a +1 promotion DM if endurance is 8+
    if grunt.officer:
        if False == grunt.promote_this_term:
            if p_roll >= promot_target:
                o_promote(grunt)
    else:
        if p_roll >= promot_target:
            e_promote(grunt)

    #Skill check 
    s_roll = randint(1, 6) + randint(1,6)
#    print 'Skill check: roll: %d Target: %d' % (s_roll, skill_target)
    if s_roll >= skill_target:
        get_skill(grunt,ua, ga)

        # Survival check, no DM coded yet
    sroll = randint(1, 6) + randint(1,6)
    if sroll < survival_target:
        s = 'Failed survival target of %d with a roll of %d' % (survival_target, sroll)
        grunt.history.append(s)
        grunt.alive = False
        return 0
    else:
        if ((sroll == survival_target) and combat_action):
            grunt.decorations.append('Wound Badge awarded in ' + ua)
            grunt.history.append('Wound Badge awarded in ' + ua)   
# end of mar_res()

def com_res(grunt, ua, ga):
    'resolve year: Commando'

    print 'resolve year: Commando'  #debug
    s = 'Unit Assigment is %s' % ua
    grunt.history.append(s)
    auto = 0
    no_chance = 20
    combat_action = False
   
    if ua == 'Trng':
        survival_target = 3  #No auto survival for commando training
        dec_target = no_chance  #No chance for decoration
        if grunt.officer:
            promot_target = no_chance  # officers not elibile for promotion
        else:
            promot_target = 8
        skill_target = 6
    elif ua == 'Intl Sec':
        combat_action = True
        survival_target = 4  
        dec_target = no_chance  # no decoration for Internal Security
        if grunt.officer:
            promot_target = no_chance  # officers not elibile for promotion
            if ga == 'Command':          
                grunt.ribbons.append(ua + ' Combat Command Ribbon')
                grunt.history.append(ua + ' Combat Command Ribbon')
            else:
                grunt.ribbons.append(ua + ' Combat Ribbon')
                grunt.history.append(ua + ' Combat Ribbon')
        else:
            promot_target = 7
            grunt.ribbons.append(ua + ' Combat Ribbon')
            grunt.history.append(ua + ' Combat Ribbon')
        skill_target = no_chance   # no skill improvement
    elif ua == 'Pol Act':
        combat_action = True
        survival_target = 4  
        dec_target = 9  
        promot_target = 8
        skill_target = 7
        if grunt.officer:
            if ga == 'Command':
                grunt.ribbons.append(ua + ' Combat Command Ribbon')
                grunt.history.append(ua + ' Combat Command Ribbon')
            else:
                grunt.ribbons.append(ua + ' Combat Ribbon')
                grunt.history.append(ua + ' Combat Ribbon')
        else:
            grunt.ribbons.append(ua + ' Combat Ribbon')
            grunt.history.append(ua + ' Combat Ribbon')
    elif ua == 'Ctr Ins':
        combat_action = True
        survival_target = 5  
        dec_target = 8  
        promot_target = 7
        skill_target = 6
        if grunt.officer:
            if ga == 'Command':
                grunt.ribbons.append(ua + ' Combat Command Ribbon')
                grunt.history.append(ua + ' Combat Command Ribbon')
            else:
                grunt.ribbons.append(ua + ' Combat Ribbon')
                grunt.history.append(ua + ' Combat Ribbon')
        else:
            grunt.ribbons.append(ua + ' Combat Ribbon')
            grunt.history.append(ua + ' Combat Ribbon')
    elif ua == 'Raid':
        combat_action = True
        survival_target = 6  
        dec_target = 5  
        promot_target = 6
        skill_target = 5
        if grunt.officer:
            if ga == 'Command':
                grunt.ribbons.append(ua + ' Combat Command Ribbon')
                grunt.history.append(ua + ' Combat Command Ribbon')
            else:
                grunt.ribbons.append(ua + ' Combat Ribbon')
                grunt.history.append(ua + ' Combat Ribbon')
        else:
            grunt.ribbons.append(ua + ' Combat Ribbon')
            grunt.history.append(ua + ' Combat Ribbon')
    elif ua == 'Garr':
        survival_target = auto  
        dec_target = no_chance 
        if grunt.officer:
            promot_target = no_chance  # officers not elibile for promotion
        else:
            promot_target = 9
        skill_target = no_chance


    # Survival check, no DM coded yet
    sroll = randint(1, 6) + randint(1,6)
    if sroll < survival_target:
        s = 'Failed survival target of %d' % survival_target
        grunt.history.append(s)
        grunt.alive = False
        return 0
    else:
        if ((sroll == survival_target) and combat_action):
            grunt.decorations.append('Purple Heart awarded in ' + ua)
            grunt.history.append('Purple Heart awarded in ' + ua)

    #Decoration check
    droll = randint(1, 6) + randint(1,6)
    if droll >= dec_target:
        get_medal(grunt,droll, dec_target, ua)
        s = 'Received a %s' % grunt.decorations[-1]
        grunt.history.append(s)

    #Promotion check
    if (grunt.officer and (grunt.promote_this_term == 0)):
        if (randint(1, 6) + randint(1,6)) >= promot_target:
            o_promote(grunt)
    else:
        p_roll = randint(1, 6) + randint(1,6)
#        print 'enlisted promotion check: roll: %d target: %d' % (p_roll, promot_target)
        if p_roll >= promot_target:
            e_promote(grunt)

    #Skill check 
    s_roll = randint(1, 6) + randint(1,6)
    if s_roll >= skill_target:
        get_skill(grunt, ua, ga)
#end of com_res

def ica_res(grunt, ua, ga):
    'resolve year: infantry, Cav or artilery'

    s = 'Unit Assigment is %s' % ua
    grunt.history.append(s)
    auto = 0
    no_chance = 20
    combat_action = 0
 
    if ua == 'Trng':
        survival_target = auto  #auto survival
        dec_target = no_chance  #No chance for decoration
        if grunt.officer:
            promot_target = no_chance  # officers not elibile for promotion
        else:
            promot_target = 6
        skill_target = 7
    elif ua == 'Intl Sec':
        combat_action = 1
        survival_target = 4  
        dec_target = 12  
        if grunt.officer:
            promot_target = no_chance  # officers not elibile for promotion
            if ga == 'Command':
                grunt.ribbons.append(ua + ' Combat Command Ribbon')
                grunt.history.append(ua + ' Combat Command Ribbon')
            else:
                grunt.ribbons.append(ua + ' Combat Ribbon')
                grunt.history.append(ua + ' Combat Ribbon')
        else:
            promot_target = 6
            grunt.ribbons.append(ua + ' Combat Ribbon')
            grunt.history.append(ua + ' Combat Ribbon')
        skill_target = no_chance   # no skill improvement
    elif ua == 'Pol Act':
        combat_action = 1
        survival_target = 5  
        dec_target = 9  
        promot_target = 8
        skill_target = 7
        if grunt.officer:
            if ga == 'Command':
                grunt.ribbons.append(ua + ' Combat Command Ribbon')
                grunt.history.append(ua + ' Combat Command Ribbon')
            else:
                grunt.ribbons.append(ua + ' Combat Ribbon')
                grunt.history.append(ua + ' Combat Ribbon')
        else:
            grunt.ribbons.append(ua + ' Combat Ribbon')
            grunt.history.append(ua + ' Combat Ribbon')
    elif ua == 'Ctr Ins':
        combat_action = 1
        survival_target = 5  
        dec_target = 10  
        promot_target = 9
        skill_target = 8
        if grunt.officer:
            if ga == 'Command':
                grunt.ribbons.append(ua + ' Combat Command Ribbon')
                grunt.history.append(ua + ' Combat Command Ribbon')
            else:
                grunt.ribbons.append(ua + ' Combat Ribbon')
                grunt.history.append(ua + ' Combat Ribbon')
        else:
            grunt.ribbons.append(ua + ' Combat Ribbon')
            grunt.history.append(ua + ' Combat Ribbon')
    elif ua == 'Raid':
        combat_action = 1
        survival_target = 6  
        dec_target = 6  
        promot_target = 6
        skill_target = 5
        if grunt.officer:
            if ga == 'Command':
                grunt.ribbons.append(ua + ' Combat Command Ribbon')
                grunt.history.append(ua + ' Combat Command Ribbon')
            else:
                grunt.ribbons.append(ua + ' Combat Ribbon')
                grunt.history.append(ua + ' Combat Ribbon')
        else:
            grunt.ribbons.append(ua + ' Combat Ribbon')
            grunt.history.append(ua + ' Combat Ribbon')
    elif ua == 'Garr':
        survival_target = auto  
        dec_target = no_chance 
        if grunt.officer:
            promot_target = no_chance  # officers not elibile for promotion
        else:
            promot_target = 6
        skill_target = no_chance

    # Survival check, no DM coded yet
    sroll = randint(1, 6) + randint(1,6)
    if sroll < survival_target:
        s = 'Failed survival target of %d' % survival_target
        grunt.history.append(s)
        grunt.alive = False
        return False
    else:
        if ((sroll == survival_target) and combat_action):
            grunt.decorations.append('Wound Badge awarded in ' + ua)
            grunt.history.append('Wound Badge awarded in ' + ua)

    #Decoration check
    droll = randint(1, 6) + randint(1,6)
    if droll >= dec_target:
        get_medal(grunt, droll, dec_target, ua)
        s = 'Received a %s' % grunt.decorations[-1]
        grunt.history.append(s)

    #Promotion check - Officers can only be promoted once per term.
    p_roll = randint(1, 6) + randint(1,6)
    if (False == grunt.officer):
        if p_roll >= promot_target:
            e_promote(grunt)
        else:
            if (grunt.promote_this_term == False):
                if p_roll >= promot_target:
                    o_promote(grunt)

    #Skill check 
    s_roll = randint(1, 6) + randint(1,6)
    if s_roll >= skill_target:
        get_skill(grunt, ua, ga)
#end ics_res

def sup_res(grunt, ua, ga):
    'resolve year: support Army or Marines'

    s = 'Unit Assigment is %s' % ua
    grunt.history.append(s)
    auto = 0
    no_chance = 20
    combat_action = 0
    
    
    if ua == 'Trng':
        survival_target = auto  #auto survival
        dec_target = no_chance  #No chance for decoration
        if grunt.officer:
            promot_target = no_chance  # officers not elibile for promotion
        else:
            promot_target = 6
        skill_target = 8
    elif ua == 'Intl Sec':
        combat_action = 1
        survival_target = 4  
        dec_target = no_chance  
        if grunt.officer:
            promot_target = no_chance  # officers not elibile for promotion
            if ga == 'Command':          
                grunt.ribbons.append(ua + ' Combat Command Ribbon')
                grunt.history.append(ua + ' Combat Command Ribbon')
            else:
                grunt.ribbons.append(ua + ' Combat Ribbon')
                grunt.history.append(ua + ' Combat Ribbon')
        else:
            promot_target = 6
            grunt.ribbons.append(ua + ' Combat Ribbon')
            grunt.history.append(ua + ' Combat Ribbon')
        skill_target = no_chance   # no skill improvement
    elif ua == 'Pol Act':
        combat_action = 1
        survival_target = 4  
        dec_target = 10  
        promot_target = 9
        skill_target = 7
        if grunt.officer:
            if ga == 'Command':
                grunt.ribbons.append(ua + ' Combat Command Ribbon')
                grunt.history.append(ua + ' Combat Command Ribbon')
            else:
                grunt.ribbons.append(ua + ' Combat Ribbon')
                grunt.history.append(ua + ' Combat Ribbon')
        else:
            grunt.ribbons.append(ua + ' Combat Ribbon')
            grunt.history.append(ua + ' Combat Ribbon')
    elif ua == 'Ctr Ins':
        combat_action = 1
        survival_target = 5  
        dec_target = 11  
        promot_target = 10
        skill_target = 7
        if grunt.officer:
            if ga == 'Command':
                grunt.ribbons.append(ua + ' Combat Command Ribbon')
                grunt.history.append(ua + ' Combat Command Ribbon')
            else:
                grunt.ribbons.append(ua + ' Combat Ribbon')
                grunt.history.append(ua + ' Combat Ribbon')
        else:
            grunt.ribbons.append(ua + ' Combat Ribbon')
            grunt.history.append(ua + ' Combat Ribbon')
    elif ua == 'Raid':
        combat_action = 1
        survival_target = 6  
        dec_target = 7  
        promot_target = 7
        skill_target = 6
        if grunt.officer:
            if ga == 'Command':
                grunt.ribbons.append(ua + ' Combat Command Ribbon')
                grunt.history.append(ua + ' Combat Command Ribbon')
            else:
                grunt.ribbons.append(ua + ' Combat Ribbon')
                grunt.history.append(ua + ' Combat Ribbon')
        else:
            grunt.ribbons.append(ua + ' Combat Ribbon')
            grunt.history.append(ua + ' Combat Ribbon')
    elif ua == 'Garr':
        survival_target = auto  
        dec_target = no_chance 
        if grunt.officer:
            promot_target = no_chance  # officers not elibile for promotion
        else:
            promot_target = 7
        skill_target = no_chance

    #roll 2 dice
    # Survival check, no DM coded yet
    sroll = randint(1, 6) + randint(1,6)
    if sroll < survival_target:
        s = 'Failed survival target of %d' % survival_target
        grunt.history.append(s)
        grunt.alive = False
        return 0
    else:
        if ((sroll == survival_target) and combat_action):
            grunt.decorations.append('Wound Badge awarded in ' + ua)
            grunt.history.append('Wound Badge awarded in ' + ua)

    #Decoration check
    droll = randint(1, 6) + randint(1,6)
    if droll >= dec_target:
        get_medal(grunt, droll, dec_target, ua)
        s = 'Received a %s' % grunt.decorations[-1]
        grunt.history.append(s)

    #Promotion check
    if (grunt.officer and (grunt.promote_this_term == False)):
        if (randint(1, 6) + randint(1,6)) >= promot_target:
            o_promote(grunt)
    else:
        p_roll = randint(1, 6) + randint(1,6)
        if p_roll >= promot_target:
            e_promote(grunt)

    #Skill check 
    s_roll = randint(1, 6) + randint(1,6)
    if s_roll >= skill_target:
        get_skill(grunt, ua, ga)
#end of supp_res
