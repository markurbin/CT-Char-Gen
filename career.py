# career.py
# Book 4 + Book 5 Career Logic - Final Cleaned Version

import random
from dice import *
import resolve
import schools
import arm_data
from career_navy import navy_term   # Book 5 Navy support

RETIREMENT_TERMS = 7

def select_initial_arm(grunt):
    """Select initial arm per Book 4 rules."""
    if grunt.branch == 'Imperial Army':
        # Equal chance for each arm
        grunt.arm = random.choice(['Infantry', 'Cavalry', 'Artillery', 'Support'])
    elif grunt.branch == 'Imperial Marines':
        # Mostly Infantry
        grunt.arm = 'Infantry' if random.random() < 0.8 else 'Support'
    else:
        grunt.arm = 'Infantry'  # fallback

    grunt.history.append(f'{grunt.branch} / {grunt.arm}')

def army_marine_xtraining_xfer(grunt):
    """Cross Training / Commando transfer for Army & Marines"""
    # Cross-training transfer
    if (not grunt.officer and 
        getattr(grunt, 'xtrained', None) and 
        grunt.xtrained and 
        grunt.arm not in grunt.xtrained):
        
        if coin_flip():
            old_arm = grunt.arm
            x = dice(sides=1 + len(grunt.xtrained))
            new_arm = grunt.xtrained[x - 2]
            grunt.history.append(f'Changing branch from {old_arm} to {new_arm}')
            grunt.arm = new_arm

    # Commando School transfer
    if "Commando School" in getattr(grunt, 'schools', []) and grunt.arm != "Commando":
        grunt.history.append(f'Transferred to Commando from {grunt.arm}')
        grunt.arm = "Commando"


def check_reenlist(grunt):
    """Check for re-enlistment at end of term."""
    if grunt.branch == 'Imperial Army':
        target = 7 if grunt.officer else 5
    elif grunt.branch == 'Imperial Marines':
        target = 6
    elif grunt.branch == 'Imperial Navy':
        target = 6
        if not grunt.officer and grunt.rank >= 4:
            target -= 1
        if grunt.officer:
            target -= 1
    else:
        target = 6

    roll = dice(qty=2)

    if roll > target:
        return False

    # Mandatory reenlistment after term 7+
    if grunt.term >= RETIREMENT_TERMS:
        return 'forced' if roll == 12 else False

    return True


def first_term(grunt):
    """First term basic & advanced training - Army/Marines only"""
    grunt.history.append('Term 1 Year 1')
    # Need to select an arm
    # For Army - Infrantry, Cavalry, Artillery, Support
    # For Marine - Infantry or support
    # Cannot enter Commando branch on elistment
    if grunt.branch == 'Imperial Army':
        roll = random.randint(0,3)
        grunt.arm = arm_data.arms[roll]
    else:
        roll = random.randint(0,1)
        if roll == 0:
            grunt.arm =  'Infantry'
        else:
            grunt.arm = 'Support'
    grunt.history.append(f'{grunt.branch} / {grunt.arm}')
    grunt.history.append('Basic Training: Cbt Rifleman')

    # Basic Training skill
    grunt.skills['Cbt Rifleman'] = grunt.skills.get('Cbt Rifleman', 0) + 1

    # Advanced Training (MOS skill)
    roll = dice()
    if getattr(grunt, 'TL', 12) >= 12:
        roll += 1
    roll = min(roll, 7)

    arm_entry = grunt.arm_entry(special_marine_infantry=False)
    entry = arm_entry["mos"][roll - 1]
    
    grunt.skills[entry] = grunt.skills.get(entry, 0) + 1
    grunt.history.append(f'Advanced Training: {entry}')

    grunt.age += 1  # Year 1 complete


def resolve_year(grunt, ua, ga):
    """Route year resolution for Army/Marines to the correct resolver."""
    if grunt.arm in ('Infantry', 'Cavalry', 'Artillery'):
        resolve.general(grunt, ua, ga)
    elif grunt.arm == 'Support':
        resolve.support(grunt, ua, ga)
    elif grunt.arm == 'Commando':
        resolve.commando(grunt, ua, ga)
    else:
        # Fallback
        resolve.general(grunt, ua, ga)


def army_marine_year(grunt):
    """Resolve one year for Army or Marine characters."""
    # Determine General Assignment (GA)
    roll = dice()
    if grunt.upp.edu >= 8:
        roll += 1
    if grunt.officer:
        roll = max(roll - 1, 0)

    ga = grunt.arm_entry(special_marine_infantry=False)["ga"][roll - 1]

    if grunt.officer:
        grunt.history.append(f'General assignment: {ga}')

    # Resolve the year
    if ga == 'Special':
        schools.special_assign(grunt)
    else:
        roll = dice(qty=2) - 1
        ua_table = grunt.arm_entry()["ua"]
        ua = ua_table[roll % len(ua_table)]
        resolve_year(grunt, ua, ga)

    if grunt.alive:
        grunt.age += 1


def army_marine_term(grunt):
    """Full 4-year term for Army / Marines"""
    for year in range(1, 5):
        if grunt.term == 1 and year == 1:
            first_term(grunt)
        else:
            grunt.history.append(f'Term {grunt.term} Year {year}')
            army_marine_year(grunt)

        # Stop immediately if character dies or is gravely wounded
        if not grunt.alive or getattr(grunt, 'musOut', False):
            break

    # End of term cleanup
    if getattr(grunt, 'musOut', False):
        grunt.history.append(f'Mustered out due to wounds in term {grunt.term}')
    elif grunt.alive:
        grunt.term += 1
        reenlist = check_reenlist(grunt)
        if reenlist == 'forced':
            grunt.history.append(f'Mandatory re-enlistment after term {grunt.term}')
            grunt.reenlist = True
        else:
            grunt.reenlist = reenlist
    else:
        grunt.die()

    grunt.history.append('#####')


def term(grunt):
    """Main dispatcher - This is the key function"""
    if grunt.is_navy():
        navy_term(grunt)          # Book 5 Navy
    else:
        army_marine_term(grunt)   # Book 4 Army/Marines


def career(grunt):
    """Main career entry point for all branches."""
    if grunt.branch == 'Imperial Navy':
        grunt.TL = 15
        grunt.arm = 'Line'      #added 04 June 2026

    while grunt.alive and grunt.reenlist and not getattr(grunt, 'musOut', False):
        term(grunt)
        if hasattr(grunt, 'age_check'):
            grunt.age_check()

    # Final adjustment: term count should reflect actual service terms
    if grunt.alive:
        grunt.term = max(grunt.term - 1, 0)

    if hasattr(grunt.upp, 'check'):
        grunt.upp.check()
