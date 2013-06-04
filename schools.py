from dice import *
from arm_data import *
import skills

specialist_school_table = ['Admin', 'Medical', 'Commo', 'Computer', 'Mechanical', 'Electronics']

schools = {}
schools['Commando School'] = {
  "threshold":5,
  "skills":['Brawling', 'Gun Cmbt', 'Demolition', 'Wilderness Survival', 'Recon', 'Vac Suit', 'Blade Cbt', 'Instruction']
}

schools['Intelligence School'] = {
  "threshold":4,
  "skills":['Forgery', 'Bribery', 'Streetwise', 'Interrogation']
}

schools['Command College'] = {
  "threshold":4,
  "skills":['Tactics', 'Leadership', 'Recon']
}

schools['Staff College'] = {
  "threshold":4,
  "skills":['Admin', 'Engineering', 'Computer']
}


def cross_train(grunt):
    'Book 4 cross training'
    if grunt.is_navy():
        print 'X-Training in the navy!' #debug
        b5_data.navy_xtrain(grunt)
    else:
        if grunt.arm == 'Commando':
            arm_index = dice(sides=4)-1 # any of the other arms
        else:
            arm_index = dice(sides=3) # any but Commando/Infantry

        if arms[arm_index] == grunt.arm:
	    arm_index = 0  # can't cross-train in your own arm; set to infantry

        crossarm = arms[arm_index]
        grunt.xtrained.append(crossarm)
        s = 'Cross-trained in ' + crossarm
        grunt.history.append(s)
        get_mos_skill(grunt)
#end of cross_train

def specialist_school(grunt):
    roll = dice()
    school = specialist_school_table[roll - 1]
    s = 'Attended %s school' % school
    grunt.history.append(s)
    
    skills.record(grunt, school)
    
    school_text = 'Specialist School: ' + school
    grunt.schools.append(school_text)
#send of specialist_school

def pf_training(grunt):
    grunt.schools.append('Protected Forces')
    grunt.history.append('Protected Forces Training')
    # need to add check for number of skills
    # if has level 2 in any of the listed skills
    # then the character is an instructor at the school
    # and gets one level of Instruction skill

    if dice() >= 3:
        skills.record(grunt, 'Vac Suit')
    else:
        # just history, no skill?
        grunt.history.append('Vac Suit')
    if dice() >= 3:
        skills.record(grunt, 'Zero-G Cbt')
    else:
        # just history, no skill?
        grunt.history.append('Zero-G Cbt')
#end of pf_training

def ocs(grunt):
    if grunt.officer == True:
        raise Exception("Officers cannot attend OCS")
    grunt.history.append('Attending OCS')
    grunt.schools.append('OCS')
    grunt.officer = True
    grunt.rank = 0

    skills.get_command_skill(grunt)
    skills.get_staff_skill(grunt)

    #IA and IM, in addition get a MOS Table skill
    if grunt.is_army() or grunt.is_marine():
        roll = dice()
        skill = grunt.arm_entry(special_marine_infantry=False)["mos"][roll-1]
        skills.record(grunt, skill)
    else:
        raise Exception("Navy cannot attend OCS")
#end of ocs

def recruiting(grunt):
    skills.record(grunt, 'Recruiting')

def officer_recruiting(grunt):
    recruiting(grunt)
    grunt.specials.append('Recruiting')

def officer_special_assign(grunt, school):
    # TODO: need to add check for number of skills
    # if has level 2 in any of the listed skills
    # then the character is an instructor at the school
    # and gets one level of Instruction skill
    # TODO: is that for all schools?

    grunt.schools.append(school)
    grunt.history.append(school)

    threshold = schools[school]["threshold"]
    for skill in schools[school]["skills"]:
        if dice() >= threshold:
            skills.record(grunt, skill)

def attache_or_aide(grunt):
    if dice()-1 > 3:
        grunt.upp.soc += 1
        grunt.specials.append('Aide to General officer')
        grunt.history.append('Aide to General officer')
        grunt.history.append('+1 Soc')
    else:
        grunt.stat_change("soc", 1)
        grunt.rank += 1   #Not using promote() here because this can override the 1 promotion per term rule
        if grunt.rank > 8:
            grunt.rank = 8
            grunt.history.append('Already at Max Officer rank. No promotion')
        grunt.specials.append('Military Attache')
        grunt.history.append('Military Attache')
        grunt.history.append('+1 Soc & promotion')  

def intelligence_school(grunt):
    officer_special_assign(grunt, 'Intelligence School')
def command_college(grunt):
    officer_special_assign(grunt, 'Command College')
def staff_college(grunt):
    officer_special_assign(grunt, 'Staff College')
def commando_school(grunt):
    officer_special_assign(grunt, 'Commando School')

sa_enl = [
    {"name":'Cross Trng', "apply":cross_train},
    {"name":'Specialist School', "apply":specialist_school},
    {"name":'Commando School', "apply":commando_school},
    {"name":'Protected Forces', "apply":pf_training},
    {"name":'Recruiting', "apply":recruiting},
    {"name":'OCS', "apply":ocs},
    {"name":'OCS', "apply":ocs},
]
sa_officer = [
    {"name":'Intelligence School', "apply":intelligence_school},
    {"name":'Command College', "apply":command_college},
    {"name":'Staff College', "apply":staff_college},
    {"name":'Commando School', "apply":commando_school},
    {"name":'Recruiting', "apply":officer_recruiting},
    {"name":'Military Attache/Aide', "apply":attache_or_aide},
]

def special_assign(grunt):
    roll = dice()-1
    if grunt.officer:    
        s = 'Special Assignment is %s' % sa_officer[roll]["name"]
        grunt.history.append(s)
        sa_officer[roll]["apply"](grunt)
    else:
        s = 'Special Assignment is %s' % sa_enl[roll]["name"]
        grunt.history.append(s)
        sa_enl[roll]["apply"](grunt)
#end of special_assignment

