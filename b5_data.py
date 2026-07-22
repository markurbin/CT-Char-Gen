# b5_data.py
# Traveller Book 5 - High Guard (Imperial Navy)
# All major functions included and cleaned

import random
from dice import *
import promotions
import skills
from navy_res import get_staff_skill
# Import Navy year resolvers - avoid circular import issues
# Safe import to avoid circular dependency
import navy_res

# ====================== TABLES ======================
# moved the tables to a seperate file 30 April 2026
from navy_tables import (
    navy_branch, line_crew, flight, gunnery, engineering, 
    medical, technical, staff_skills, command_skills,
    shipboard_skills, sd_enl, sd_officer, specialist_school_table,
    erank
)

# ====================== HELPER FUNCTIONS ======================
def apply_skill(grunt, skill):
    """Apply a single skill or stat increase.
    Delegates stat changes to character.py's method."""
    
    if skill is None or (isinstance(skill, str) and not skill.strip()):
        grunt.history.append("DEBUG: apply_skill skipped None/empty")  # optional
        return

    # Stat increase (e.g. '+1 edu', '+1 dex')
    if isinstance(skill, str) and skill.startswith('+'):
        grunt.apply_skill(skill)          # character.py handles parsing
        return

    # Normal skill
    grunt.skills[skill] = grunt.skills.get(skill, 0) + 1
    grunt.history.append(skill)


def navy_bat(grunt):
    """Basic & Advanced Training for enlisted Navy characters."""
    grunt.history.append('Basic & Advanced Training in year 1 of term 1')

    for _ in range(2):
        skill = get_branch_skill(grunt, dice())
        skill = get_branch_skill(grunt, dice())
        if skill is None:
            grunt.history.append("DEBUG: navy_bat got None skill - arm was " + str(getattr(grunt, 'arm', None)))
            continue
        grunt.skills[skill] = grunt.skills.get(skill, 0) + 1
        grunt.history.append(skill)

    grunt.bat = True


def select_navy_branch(grunt):
    """
    Assign the character's final Navy branch.
    Education outcomes (Medical/Flight School) have absolute priority.
    """

    #grunt.history.append('DEBUG: Starting select_navy_branch')
    # === 1. Pre-enlistment education paths take precedence ===
    if getattr(grunt, 'medschool', False):
        grunt.arm = 'Medical'
        grunt.history.append('Assigned to Medical branch (Medical School graduate)')
        return

    if getattr(grunt, 'flight', False) or 'Flight' in getattr(grunt, 'schools', []):
        grunt.arm = 'Flight'
        grunt.history.append('Assigned to Flight branch (Flight School graduate)')
        return

    # === 2. Direct enlist or failed education path ===
    if getattr(grunt, 'arm', None) in (None, '', 'Line'):
        dm = -2
        if getattr(grunt.upp, 'edu', 0) >= 9:
            dm += 2
        if getattr(grunt.upp, 'int', 0) >= 10:
            dm += 2

        roll = dm + dice()
        roll = max(min(roll, 5), 0)          # CRITICAL: Force range 0-5

        navy_options = ['Technical Services', 'Engineering', 'Gunnery', 'Line', 'Flight', 'Medical']
        
        grunt.arm = navy_options[roll]
        grunt.history.append(f'Assigned to {grunt.arm} branch')
    else:
        # Already has a valid branch (edge case)
        grunt.history.append('DEBUG: In select_navy_branch - assiging grunt.arm is ' + str(grunt.arm))
        
# End of select_navy_branch

# Commenting out for now, duplicate from navy_res.py
'''
def get_staff_skill(grunt, roll):
    """Return a skill from the officer staff skills table.
    Used in officer BAT and some special assignments."""
    roll = min(max(roll, 1), len(staff_skills))
    return staff_skills[roll - 1]
'''

# ====================== SPECIAL & EDUCATION ======================

def navy_spec_school(grunt):
    """Navy Specialist School for enlisted personnel."""
    grunt.history.append('Attended Specialist School')

    dm = random.randint(0, 6)      # DM 0 to 6
    roll = min(dm + dice(), len(specialist_school_table))
    
    skill = specialist_school_table[roll - 1]

    skills.record(grunt, skill)
    grunt.schools.append(f'Specialist School: {skill}')


def get_branch_skill(grunt, roll):
    """
    Return a skill from the current Navy branch's skill table.
    Used heavily in BAT and skill gains.
    """
    #branch = getattr(grunt, 'navalBranch', 'Technical Services')
    branch = grunt.arm

    if branch not in navy_branch:
        print("DEBUG: error in b5_data.py get_branch_skill - Branch not set.")

    if branch is None or branch not in navy_branch:
        # print("DEBUG: get_branch_skill fallback - arm was None")
        grunt.history.append("DEBUG: get_branch_skill fallback - arm was None")
        branch = 'Line'   # safe default for Navy

    if branch in ('Line', 'Crew'):
        table = line_crew
    elif branch == 'Flight':
        table = flight
    elif branch == 'Gunnery':
        table = gunnery
    elif branch == 'Engineering':
        table = engineering
    elif branch == 'Medical':
        table = medical
    else:  # Technical Services or fallback
        table = technical

    # Safe roll clamping
    roll = min(max(roll, 1), len(table))

    skill = table[roll - 1]
    return skill

#end of get_branch_skill()  

# Commenting out for now, duplicate from navy_res.py
'''
def shipboard_life_skill(grunt):
    """Shipboard Life Skill Table (used in some Navy assignments)"""
    dm = 4 if grunt.officer else 0
    roll = dm + dice()
    roll = max(min(roll, len(shipboard_skills)), 1)

    skill = shipboard_skills[roll - 1]
    skills.record(grunt, skill)
'''
    
def navy_xtrain(grunt):
    """Cross Training in another Navy branch."""
    #grunt.history.append('DEBUG: Starting navy_xtrain')
    trained = False
    roll = 0
    current_idx = None

    # Get current branch index safely
    if grunt.arm in navy_branch:
        current_idx = navy_branch.index(grunt.arm)

    if not grunt.officer:
        # Enlisted cross-training
        if grunt.arm == 'Crew':
            roll = random.randint(0, len(navy_branch)-1)
        else:
            while not trained:
                roll = random.randint(0, len(navy_branch)-1)
                if roll != current_idx:
                    trained = True
    else:
        # Officer cross-training
        while not trained:
            roll = random.randint(0, len(navy_branch)-1)
            if roll != current_idx:
                trained = True

    target_branch = navy_branch[roll]
    grunt.xtrained.append(target_branch)
    grunt.history.append(f'Cross Trained in {target_branch}')

    # Grant one skill from the new branch
    get_branch_skill(grunt, roll + 1)   # 1-based for skill table
    #grunt.history.append('DEBUG: Leaving navy_xtrain')

def navy_e_school(grunt):
    """Enlisted Engineering School"""
    grunt.history.append('Attended Enlisted Engineering School')

    # Each skill has ~33% chance (roll 5 or 6 on 1d6)
    if dice() >= 5:
        skills.record(grunt, 'Mechanical')
    if dice() >= 5:
        skills.record(grunt, 'Electronics')
    if dice() >= 5:
        skills.record(grunt, 'Gravitics')
    if dice() >= 5:
        skills.record(grunt, 'Engineering')

def navy_ocs(grunt):
    """Officer Candidate School (OCS) - Navy"""
    #grunt.history.append('DEBUG: Starting navy_ocs')
    if grunt.officer:
        grunt.history.append('Already an officer - cannot attend OCS')
        return False

    grunt.history.append('Attending Navy OCS')
    grunt.schools.append('OCS')
    grunt.officer = True
    grunt.rank = 0

    # Command and Staff skills
    skills.record(grunt, command_skills[dice() - 1])
    skills.record(grunt, staff_skills[dice() - 1])

    # Branch skill
    navy_res.nbranch_skill(grunt, dice() - 1)

    grunt.history.append('Graduated Navy OCS')
    return True

def navy_officer_bat(grunt):
    """Basic & Advanced Training for Navy officers.
    Called after College, Naval Academy, or OCS graduation."""
    
    grunt.history.append('Officer Basic & Advanced Training')

    for _ in range(2):
        if random.random() < 0.5:
            # Branch skill
            skill = get_branch_skill(grunt, dice())
            skill = get_branch_skill(grunt, dice())
            if skill is None:
                grunt.history.append("DEBUG: navy_bat got None skill - arm was " + str(getattr(grunt, 'arm', None)))
                continue
        else:
            # Staff skill
            skill = navy_res.get_staff_skill(grunt)
            if skill is None:
                grunt.history.append("DEBUG: navy_bat got None skill - arm was " + str(getattr(grunt, 'arm', None)))
                continue

        grunt.skills[skill] = grunt.skills.get(skill, 0) + 1
        grunt.history.append(skill)

    grunt.bat = True

def navy_aa(grunt):
    """Naval Attache / Aide to Flag Officer - Special Assignment (Book 5)"""
    roll = dice()  # 1d6

    if roll <= 4:                                      # 1-4 = Naval Attache
        grunt.history.append('Naval Attache')
        
        # Automatic promotion
        if grunt.rank < 8:          # safety cap
            grunt.rank += 1
            grunt.history.append(f'Promoted to {erank[grunt.rank] if not grunt.officer else "next rank"}')
        
        # +1 Social
        grunt.upp.soc += 1
        grunt.history.append('+1 Soc')

    else:                                              # 5-6 = Aide to Flag Officer
        grunt.history.append('Aide to Flag Officer')
        grunt.upp.soc += 1
        grunt.history.append('+1 Soc')

        # 75% chance to influence next assignment toward Command flavor
        if random.random() < 0.75:
            grunt.history.append('Used influence to secure next assignment as Command')
            grunt.reten = True                        # Force next year to repeat assignment type
            grunt.command_influence = True            # Flag for flavor suffix in navy_year
        else:
            grunt.history.append('Did not secure preferred command slot')

def navy_sd(grunt):
    """Navy Special Duty Assignment (Book 5)"""
    #grunt.history.append('DEBUG: Starting navy_sd')
    dm = 1 if (getattr(grunt, 'college', False) or grunt.upp.soc >= 11) else 0
    roll = dm + dice() - 1
    roll = max(min(roll, 6), 0)

    if grunt.officer:
        grunt.history.append(f'Special Duty: {sd_officer[roll]}')

        if roll == 0:                    # Cross Training
            navy_xtrain(grunt)
        elif roll == 1:                  # Intelligence School
            grunt.history.append('Intelligence School')
            for sk in ['Forgery', 'Bribery', 'Streetwise', 'Interrogation']:
                if dice() >= 4:
                    skills.record(grunt, sk)
        elif roll == 2:                  # Recruiting
            skills.record(grunt, 'Recruiting')
        elif roll == 3:                  # Naval Attache / Aide
            navy_aa(grunt)
        elif roll == 4:                  # Command College
            grunt.history.append('Command College')
            for sk in ['Ship Tactics', 'Fleet Tactics', 'Leader', 'Admin']:
                if dice() >= 4:
                    skills.record(grunt, sk)
        else:                            # Staff College (roll 5-6)
            grunt.history.append('Staff College')
            for sk in ['Fleet Tactics', 'Liaison', 'Computer', 'Admin']:
                if dice() >= 4:
                    skills.record(grunt, sk)
    else:
        # Enlisted Special Duty
        grunt.history.append(f'Special Duty: {sd_enl[roll]}')

        if roll == 0:                    # Cross Training
            navy_xtrain(grunt)
        elif roll == 1:                  # Specialist School
            navy_spec_school(grunt)
        elif roll == 2:                  # Recruiting
            skills.record(grunt, 'Recruiting')
            if dice() >= 4:
                skills.record(grunt, 'Admin')
        elif roll == 3:                  # Gunnery School
            grunt.history.append('Gunnery School')
            for sk in ['Ships Lasers', 'Ships Missiles', 'Ships Particle Accelerators',
                       'Ships Energy Weapons', 'Meson Weapons', 'Screens']:
                if dice() >= 5:
                    skills.record(grunt, sk)
        elif roll == 4:                  # Engineering School
            navy_e_school(grunt)
        else:                            # OCS (roll 5-6)
            if grunt.age > 34:
                grunt.history.append('Too old for OCS')
                grunt.history.append('Should reroll for sepecial assignment TBDL')
            else:
                navy_ocs(grunt)
# end of navy_sd


# Education functions (college, Naval_Academy, flight_school, medical_school) already cleaned
def check_college(grunt):
    """Wrapper for college completion check."""
    if college(grunt):
        return True
    else:
        grunt.college_fail = True
        grunt.history.append('Failed College')
        return False

def check_college_admin(grunt):
    """Apply to College"""
    grunt.history.append('Applying to College')
    grunt.applied_college = True
    dm = 2 if grunt.upp.edu >= 9 else 0
    if dice(2) + dm >= 9:
        grunt.history.append('Accepted to College')
        return True
    grunt.history.append('Not accepted to College')
    return False


def college(grunt):
    """College - 4 years or failure (+1 year)"""
    grunt.history.append('Attending College')

    dm = 2 if grunt.upp.edu >= 8 else 0
    if dice(2) + dm < 7:          # Failed to graduate
        grunt.history.append('Failed to graduate College')
        grunt.college_fail = True
        grunt.age += 1
        return False

    # Successful graduation
    grunt.college = True
    grunt.age += 4

    # NOTC roll
    dm = 1 if grunt.upp.soc >= 10 else 0
    if dice(2) + dm >= 8:
        grunt.notc = True
        grunt.officer = True
        grunt.rank = 0
        grunt.history.append('Accepted into Navy Officer Training Corps → Commissioned Ensign')
    else:
        grunt.history.append('Did not receive NOTC commission')

    # EDU gain
    dm = 1 if grunt.upp.int >= 9 else 0
    edu_gain = max(dm + dice() - 3, 1)
    grunt.upp.edu = min(grunt.upp.edu + edu_gain, 12)
    grunt.history.append(f'College increased EDU by {edu_gain}')

    # Honors
    dm = 1 if grunt.upp.int >= 9 else 0
    if dice(2) + dm >= 10:
        grunt.honors = True
        grunt.history.append('Graduated College with Honors')
    else:
        grunt.history.append('Graduated College')

    return True

def navy_short_term_one(grunt):
    """Handle the special 3-year first term """
    """This is for four options:
            1. Attending Flight School (pass or fail)
            2. Failing the Naval Academy
            3. Failing Medical School
            4. Failing College
    """
    grunt.history.append('=== Short 3-Year First Term ===')

    # Year 1: Basic & Advanced Training (enlisted & officers)
    if grunt.officer:
        navy_officer_bat(grunt)
    else:
        navy_bat(grunt)
        grunt.bat = True
    grunt.age += 1      # Age the first year

    # Years 2 and 3: Normal assignments (navy_year already adds age)
    for year in range(2, 4):
        if not grunt.alive:
            break
        grunt.history.append(f'Term 1 Year {year}')
        navy_year(grunt, year)
        if not grunt.alive or getattr(grunt, 'musOut', False):
            break
    grunt.age += 2 #Account for years 2 & 3 MU 21 July 2026

    grunt.history.append('#####')
    return 0   # Handling aging here instead of returning

def Naval_Academy(grunt):
    """Naval Academy - 4 years or failure (+1 year)"""
    grunt.history.append('Applied to Naval Academy')
    grunt.applied_academy = True

    dm = 2 if grunt.upp.soc >= 10 else 0
    if dm + dice(2) < 10:
        #grunt.history.append('Not accepted to Naval Academy')
        # Do NOT set academy_fail here. Normal direct enlist path.
        return False

    grunt.history.append('Accepted to Naval Academy')

    dm = 2 if grunt.upp.int >= 8 else 0
    if dm + dice(2) < 9:          # Accepted but failed to graduate
        grunt.history.append('Failed Naval Academy')
        grunt.academy_fail = True   # Only set on actual failure after acceptance
        grunt.age += 1
        return False

    # Successful graduation (rest unchanged)
    grunt.history.append('Graduated Naval Academy')
    grunt.academy = True
    grunt.officer = True
    grunt.rank = 0

    if dice() >= 4: skills.record(grunt, 'Vacc Suit')
    if dice() >= 4: skills.record(grunt, 'Nav')
    if dice() >= 4: skills.record(grunt, 'Engineering')

    dm = 1 if grunt.upp.int >= 9 else 0
    edu_gain = max(dm + dice() - 3, 1)
    grunt.upp.edu = min(grunt.upp.edu + edu_gain, 12)
    grunt.history.append(f'Edu +{edu_gain}')

    dm = 1 if grunt.upp.int >= 9 else 0
    if dm + dice(2) >= 9:
        grunt.honors = True
        grunt.history.append('Graduated Naval Academy with Honors')
    else:
        grunt.history.append('Graduated Naval Academy')

    grunt.age += 4
    grunt.officer = True
    grunt.rank = 0
    return True


def medical_school(grunt):
    """Medical School - 4 years"""
    dm = 2 if grunt.upp.edu >= 10 else 0
    if dm + dice(2) < 9:
        grunt.history.append('Not accepted to Medical School')
        return False

    grunt.history.append('Accepted to Medical School')

    dm = 2 if grunt.upp.int >= 9 else 0
    if dm + dice(2) < 8:
        grunt.history.append('Failed Medical School')
        grunt.med_fail = True   # This should trigger a short (3 year) first term
        grunt.age += 1          # handle the 1 year aging here
        return False

    grunt.history.append('Graduated Medical School')
    grunt.schools.append('Medical')
    grunt.medschool = True
    grunt.officer = True
    grunt.rank = 2

    skills.record(grunt, 'Medic')
    skills.record(grunt, 'Medic')
    skills.record(grunt, 'Medic')
    skills.record(grunt, 'Admin')

    grunt.upp.edu = min(grunt.upp.edu + 1, 12)
    grunt.history.append('+1 Edu')

    # Honors in Med School
    dm = 1 if grunt.upp.edu >= 11 else 0
    if dm + dice(2) >= 11:
        grunt.history.append('Graduated Medical School with Honors')
        skills.record(grunt, 'Medic')
        skills.record(grunt, 'Computer')

    grunt.age += 4
    grunt.arm = 'Medical'
    
    # IMPORTANT: Do NOT call OBAT here. Set flag so it happens in Term 1 Year 1
    grunt.needs_officer_bat = True
    return True

def flight_school(grunt):
    """Flight School - only 1 year"""

    dm = 1 if grunt.upp.dex >= 9 else 0
    if dm + dice(2) < 9:
        grunt.history.append('Not accepted to Flight School')
        return False

    grunt.history.append('Accepted to Flight School')
    #character ages 1 year regardless of pass/fail.
    grunt.age += 1
    #Attending Flight School is followed by a short (3 year) first term regardless of Pass/Fail

    dm = 1 if grunt.upp.int >= 8 else 0
    if dm + dice(2) < 7:
        grunt.history.append('Failed Flight School')
        grunt.flight_fail = True   
        return False

    grunt.history.append('Graduated Flight School')
    grunt.schools.append('Flight')
    grunt.flight = True
    grunt.officer = True
    grunt.rank = 2                     # Lieutenant per your rule

    skills.record(grunt, 'Pilot')
    if dice() >= 4: skills.record(grunt, 'Pilot')
    if dice() >= 4: skills.record(grunt, 'Ships Boat')
    if dice() >= 4: skills.record(grunt, 'Nav')
    
    # Flag so OBAT happens in Term 1 Year 1 (not during pre-enlistment)
    
    grunt.needs_officer_bat = True
    return True

def handle_honors_advanced_school(grunt):
    """Honors Graduate Advanced School Assignment"""
    # Aging is handled by flight and medical school functions. 
    grunt.history.append('Honors Graduate → Eligible for Advanced School')

    # Can they go to Flight School?
    can_flight = (
        getattr(grunt, 'academy', False) or
        (getattr(grunt, 'college', False) and getattr(grunt, 'notc', False))
    )

    advanced_success = False

    if can_flight:
        if coin_flip():
            advanced_success = medical_school(grunt)
        else:
            advanced_success = flight_school(grunt)
    else:
        # College honors but no NOTC → Medical School only
        grunt.history.append('College Honors without NOTC → Medical School only')
        advanced_success = medical_school(grunt)

    # CRITICAL FIX: Only revert to enlisted if they are NOT a Naval Academy graduate
    if not advanced_success:
        if getattr(grunt, 'academy', False):
            grunt.history.append('No advanced school - but remains officer (Naval Academy graduate)')
        elif not getattr(grunt, 'notc', False):
            grunt.officer = False
            grunt.rank = 0
            grunt.history.append('No NOTC and advanced school failed - reverting to enlisted')
        else:
            grunt.history.append('No Advanced school - but remains officer (via NOTC)')

    # Fallback branch assignment if needed
    if not (getattr(grunt, 'medschool', False) or getattr(grunt, 'flight', False)):
        grunt.history.append('Advanced school path failed - falling back to normal branch')
        select_navy_branch(grunt)

    # Ensure officer status is consistent
    if not getattr(grunt, 'officer', False):
        grunt.rank = 0

    # Ensure branch is set if medical or flight school succeeded
    if getattr(grunt, 'medschool', False):
        grunt.arm = 'Medical'
    elif getattr(grunt, 'flight', False):
        grunt.arm = 'Flight'

    # Do NOT call navy_officer_bat() here.
    # The flag is already set inside medical_school() / flight_school()
    return

# ====================== RESOLVE YEAR FUNCTIONS ======================
# moved to navy_res.py 30 April 2027


# ====================== MAIN NAVY YEAR ======================
def sa_select(grunt):
    """Select Specific Assignment (SA) for the year - Book 5 style"""
    dm = 1 if (getattr(grunt, 'college', False) and not grunt.officer) else 0
    roll = dm + dice(2)

    if roll == 2:
        return 'Battle'
    elif roll in (3, 10):
        return 'Shore Duty'
    elif roll == 4:
        return 'Siege'
    elif roll in (5, 9):
        return 'Strike'
    elif roll in (6, 8):
        return 'Patrol'
    elif roll == 7:
        return 'Training'
    else:
        return 'Special Duty'

def prenlist(grunt):
    """Pure education path logic. No service year or assignment code allowed here."""
    # ====================== NAVAL ACADEMY PATH ======================
    if grunt.upp.soc >= 8:
        if Naval_Academy(grunt):
            # Successful Academy graduation
            if getattr(grunt, 'honors', False):
                handle_honors_advanced_school(grunt)
            else:
                select_navy_branch(grunt)
            return True
        else:
            # Failed Naval Academy → Direct to enlisted Navy (no College attempt)
            # Only show "Failed Naval Academy" if academy_fail was set (i.e. accepted but failed)
            if getattr(grunt, 'academy_fail', False):
                grunt.history.append('Failed Naval Academy - proceeding as enlisted')
            else:
                grunt.history.append('Not accepted to Naval Academy - proceeding as enlisted')
            return False

    # ====================== COLLEGE PATH ======================
    if check_college_admin(grunt):
        if check_college(grunt):
            if getattr(grunt, 'honors', False):
                handle_honors_advanced_school(grunt)
            else:
                select_navy_branch(grunt)
            return True
        else:
            grunt.history.append('College failed - continuing as enlisted')
            return False

    return False  # No education path taken

def navy_year_one(grunt):
    """
    SINGLE ENTRY POINT for all pre-enlistment logic.
    Returns the number of years aged during pre-enlistment education.
    The education functions (college, Naval_Academy, etc.) already age the character.
    We return the correct number of years so navy_term can add them properly.
    """
    grunt.history.append('=== Pre-Enlistment Education Phase===')

    education_completed = prenlist(grunt)

    if education_completed:
        if getattr(grunt, 'flight', False):
            # Flight School already aged 1 year inside flight_school()
            return 1
        else:
            # College / Naval Academy / Medical School paths already aged 4 years inside those functions
            if getattr(grunt, 'officer', False):
                grunt.needs_officer_bat = True
            
            grunt.history.append('#####')
            return 0    #Not computing age here anymore
    else:
        # Direct Enlist or failed education path = 0 additional years
        grunt.history.append('No pre-enlistment education - Direct Enlistment')
        
        grunt.arm = None
        select_navy_branch(grunt)

        grunt.bat = False   
        #grunt.history.append('DEBUG: NYA Age = ' + str(grunt.age))
        grunt.history.append('#####')
        return 0  #Not computing age here anymore
# end of navy_year_one


def navy_year(grunt, year):
    """
    Resolve one year of actual Navy service.
    Called from career_navy.py after pre-enlistment is complete.
    """
    # The next three lines are DEBUG lines
    #cAge = grunt.age
    #ageString = "Current Age at the start of navy_year is " + str(grunt.age)
    #grunt.history.append(ageString)

    # Determine if this is a command position
    command = grunt.officer and navy_res.navy_cmd_check(grunt)

    # Handle retention (repeat same assignment)
    if getattr(grunt, 'reten', False):
        sa = getattr(grunt, 'sa', 'Patrol')
        grunt.reten = False
    else:
        sa = sa_select(grunt)

    # Log the assignment with proper Command/Staff flavor for officers
    if sa == 'Special Duty' or not grunt.officer:
        s = f'Assignment: {sa}'
    else:
        suffix = " - Command" if (command or getattr(grunt, 'command_influence', False)) else " - Staff"
        s = f'Assignment: {sa}{suffix}'
    
    grunt.history.append(s)

    # Clear influence flag after use
    if hasattr(grunt, 'command_influence'):
        delattr(grunt, 'command_influence')

    # Route to the correct resolver
    if sa == 'Special Duty':
        navy_sd(grunt)
    elif grunt.arm in ('Line', 'Crew'):
        navy_res.lc_res(grunt, sa, command)
    elif grunt.arm == 'Flight':
        navy_res.flight_res(grunt, sa, command)
    elif grunt.arm == 'Gunnery':
        navy_res.gunnery_res(grunt, sa, command)
    elif grunt.arm == 'Engineering':
        navy_res.eng_res(grunt, sa, command)
    elif grunt.arm == 'Medical':
        navy_res.medical_res(grunt, sa, command)
    elif grunt.arm == 'Technical Services':
        navy_res.tech_res(grunt, sa, command)
    else:
        navy_res.lc_res(grunt, sa, command)

    # ====================== CENTRALIZED AGE FIX ======================
    # ONLY add 1 year if this is a normal service year
    if grunt.alive:
        # Skip age increment for Term 1 Year 1 if education already aged the character
        skip_education_year = (grunt.term == 1 and year == 1 and 
                              (getattr(grunt, 'academy', False) or 
                               getattr(grunt, 'college', False) or 
                               getattr(grunt, 'medschool', False) or 
                               getattr(grunt, 'flight', False)))
        
        if not skip_education_year:
            #grunt.age += 1
            #grunt.history.append("DEBUG: NOT Adding 1 year to age in navy_year") 
            pass
    # ================================================================

    # The next three lines are DEBUG lines
    #cAge = grunt.age
    #ageString = "Current Age at the end of navy_year is " + str(grunt.age)
    #grunt.history.append(ageString)
    
    return True
# end of navy_year


# ====================== MUSTER OUT ======================
def muster_out_navy(grunt):
    """Delegate to unified muster system"""
    import muster
    muster.muster_out(grunt)


# ====================== FINAL LOADER ======================
print("b5_data.py loaded successfully (fully cleaned version)")
