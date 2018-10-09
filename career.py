# 15 April 2015 - added support for skills as a dictionary

from dice import *
from career_navy import *
import resolve
import schools

RETIREMENT_TERMS = 7




def army_marine_xtraining_xfer(grunt):
    'Cross Training transfer for Army & Marines'
    # MU 6/11/13 added old branch to history

    #Check for Cross Training
    if ((False == grunt.officer) and grunt.xtrained) and (grunt.arm not in grunt.xtrained):
        if coin_flip():   # 50% chance
            old_arm = grunt.arm
            x = dice(sides= 1+len(grunt.xtrained) )
            new_arm = grunt.xtrained[x-2]
            s = 'Changing branch from %s to %s' % (old_arm, new_arm)
            grunt.history.append(s)
            grunt.arm = new_arm

    # if not commando and attended commando school, give chance to join commandos
    if ("Commando School" in grunt.schools) and (grunt.arm != "Commando"):
            #No choice! Going Commando!
        s = 'Transfered to Commando arm from %s arm at start of term %d' % (grunt.arm, grunt.term)
        grunt.history.append(s)
        grunt.arm = "Commando"
#end of army_marine_xtraining_xfer

def check_reenlist(grunt):
    'Check for re-enlistment'
    # if a 12 is rolled, you have to reenlist, even if at
    # or past the manditory retirement
    # return values:
    #   False    - failed reenlist
    #   True     - successful reenlist
    #   'forced' - Forced reenlist

    rvalue = False
    if grunt.branch == 'Imperial Army':
        target = 7 #IA
        if grunt.officer == False:
            target -= 2
    elif grunt.branch == 'Imperial Marines':
        target = 6  #IM
    elif grunt.branch == 'Imperial Navy':
        target = 6  #IN
        if (grunt.officer == False) and grunt.rank >=4:
            target -= 1
        if grunt.officer:
            target -=  1
    roll = dice(qty=2)
    if roll > target:
        return False
    else:
        if grunt.term >= RETIREMENT_TERMS:
            if 12==roll:
                rvalue = 'forced'
            else:
                rvalue = False
        else:
            rvalue = True

    if (grunt.branch == 'Imperial Army') or (grunt.branch == 'Imperial Marines'):
        army_marine_xtraining_xfer(grunt)
    return rvalue
#end check_reenlist()


def first_term(grunt):
    'First term, year 1 is unique; Being nice, no survival roll first year'

    #grunt.skills.append('Cbt Rifleman') # Required first skill for Army & Marines
    grunt.skills['Cbt Rifleman'] = grunt.skills.get('Cbt Rifleman',0) + 1
    grunt.history.append('Term 1 Year 1')
    grunt.history.append(grunt.branch + ' ' + grunt.arm)
    grunt.history.append('Basic Training: Cbt Rifleman')
    roll = dice()
    if grunt.TL >= 12:
        roll += 1
        
    entry = grunt.arm_entry(special_marine_infantry=False)["mos"][roll-1]
    #grunt.skills.append(entry)
    grunt.skills[entry] = grunt.skills.get(entry,0) + 1
    s = 'Advance Training: %s' % entry
    grunt.history.append(s)
    
    return
#end first_term()

    
def resolve_year(grunt, ua, ga):
    #now resolve the year
    if grunt.is_army():
        if (grunt.arm == 'Infantry') or (grunt.arm == 'Cavalry') or (grunt.arm == 'Artillery'):
            resolve.general(grunt, ua, ga)
        elif grunt.arm == 'Support':
            resolve.support(grunt, ua, ga)
        elif grunt.arm == 'Commando':
            resolve.commando(grunt, ua, ga)
    elif grunt.is_marine():
        if grunt.arm == 'Infantry':
            resolve.marine(grunt, ua, ga)
        elif (grunt.arm == 'Cavalry') or (grunt.arm == 'Artillery'):
            resolve.general(grunt, ua, ga)
        elif grunt.arm == 'Support':
            resolve.support(grunt, ua, ga)
        elif grunt.arm == 'Commando':
            resolve.commando(grunt, ua, ga)   #MU 6/11/13 added commando option to Marines


def army_marine_year(grunt):
    'Serve 1 year in the Imperial Army/Marines'
    # Determine General assignment
    roll = dice()
    # edu bonus not optional at this point
    # if Edu >= 8, +1 to the die rolll
    if grunt.upp.edu >= 8:
        roll += 1

    #bucking for command 
    if grunt.officer:
       roll = roll - 1
       if roll < 0: roll = 0

    ga = grunt.arm_entry(special_marine_infantry=False)["ga"][roll-1]

    if grunt.officer:
        s = 'General assignment is %s' % ga
        grunt.history.append(s)

    # determine unit assignment
    if ga == 'Special':
        schools.special_assign(grunt)
    else:
        roll = dice(qty=2) - 1
        ua = grunt.arm_entry()["ua"][roll-1]

        resolve_year(grunt, ua, ga)

    if grunt.alive:
        grunt.age += 1

# end of army_marine_year()


def army_marine_term(grunt):
    'Work through a 4 year term in the Army or Marines'
    
    promote_this_term = False
    for year in range(1,5):
        if grunt.term==1 and year==1:
            first_term(grunt)  # Basic & Advanced Training, Year 1
            grunt.age += 1
        else:
            s = 'Term %d Year %d' % (grunt.term, year)
            grunt.history.append(s)
            army_marine_year(grunt)
            if grunt.is_dead(): break

    if grunt.alive:
        grunt.term += 1
        reenlist = check_reenlist(grunt)
        if 'forced' == reenlist:
            s = 'Mandatory re-enlistment after term %d' % grunt.term
            grunt.history.append(s)
            grunt.reenlist = True
        else:
            grunt.reenlist = reenlist
    else:
        grunt.die(year)
    grunt.history.append('#####')
#end army_marine_term()


def term(grunt):
    if grunt.is_navy():
        navy_term(grunt)
    else:
        army_marine_term(grunt)

def career(grunt):
    if grunt.branch=='Imperial Navy':
        grunt.TL = 15 # Imperial Navy TL is F
    while grunt.alive and grunt.reenlist:
        term(grunt)
        grunt.age_check()
    if grunt.alive:
        grunt.term -= 1 # magic offset
    grunt.upp.check()
    
