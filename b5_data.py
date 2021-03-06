# Traveller Book 5 High Guard specific data and functions
# "The Traveller game in all forms is owned by Far 
# Future Enterprises. Copyright 1977 - 2015 Far Future Enterprises."
# Mark Urbin
# Feb 2013 - June 2015
#

#from sprint import sprint
from dice import *
import muster  
from arm_data import branches
import promotions #added 6/11/13 MU

arm_enlisted_Table = ('Technical Services', 'Crew', 'Crew', 'Engineering', 'Engineering', 'Line', 'Flight', 'Medical')
arm_officer_Table = ('Technical Services', 'Line', 'Line', 'Engineering', 'Engineering', 'Gunnery', 'Gunnery', 'Medical')
navy_life = ('Brawling', '+1 str', 'Carousing', 'Gambling', '+1 end', '+1 dex', '+1 end', '+1 edu', 'Carousing', 'Vacc Suit')
navy_cash_table = (1000, 5000, 5000, 10000, 20000, 50000, 50000)
navy_muster_table = ('Low Psg', '+1 int', '+2 edu', 'Blade', 'Travellers', 'High Psg', '+2 soc')

navy_branch = ('Line','Flight','Gunnery','Engineering','Medical','Technical Services')
line_crew = ('Mechanical','Electronics', 'Gun Cbt', 'Nav','Computer','Liaison','Zero-G Cbt','Vacc Suit' )
flight = ('Vacc Suit', 'Admin', 'Gun Cbt','Commo','Ships Boat','Nav','Pilot','Pilot')
gunnery = ('Fwd Obsv','Gun Cbt','Commo','Computer','Gunnery','Gunnery','Gunnery','Gunnery')
engineering = ('Mechanical','Electronic','Engineering','Mechanical','Vacc Suit','Engineering','Engineering','Engineering')
medical = ('Admin','Jot','Electronic','Admin','Medical','Computer','Medical','Medical')
technical = ('Mechanical','Mechanical','Electronic','Electronic','Computer','Computer','Gravitics','JoT')

sd_enl = ['Cross Trng', 'Specialist School', 'Recuiting School', 'Gunnery School', 'Engineering School', 'OCS', 'OCS']
sd_officer = ['Cross Trng','Intelligence School','Recruiting Duty','Naval Attache/Aide','Command College', 'Staff College','Staff College']
specialist_school_table = ['Admin', 'Medical', 'Liaison', 'Mechanical','Electronics','Gravitics','Vehicle','Navigation','Computer','Ships Boat','Communications','Vacc suit']

navy_life_skills = ['Brawling', '+1 str', 'Carousing', 'Gambling', '+1 end', '+1 dex', '+1 end','+1 edu','Carousing', 'Vacc Suit']
shipboard_skills = ['Gambling','+ dex','Blade Cbt','Mechanical','Ships Boat','Vacc Suit','Zero-G Cbt','Commo','Admin','Jot']
shoreduty_skills = ['Carousing','Vehicle','Fwd Obs','Vacc Suit','Liaison','Vehicle','Fwd Obs','Survival','Vacc Suit','Battle Dress']
po_skills = ['Vacc Suit', 'Blade Cbt', 'Mechanical', 'Medic', 'Leader', 'Zero-G Cbt', '+1 edu', 'Instruction', 'Admin']
command_skills = ['Vehicle','+1 end', 'Gun Cmbt',  'Ships Boat', 'Pilot', 'Ship Tactics', 'Leader','+1 soc','Leader','Ship Tactics']
staff_skills = ['Computer', 'Electronics', 'Gun Cbt', 'Admin','Bribery','Ship Tachtics','Fleet Tactics','+1 int','Ship Tactics','Fleet Tactics']

erank = ('Spacehand Recruit', 'Spacehand Apprentice', 'Able Spacehand','Petty Officer Third Class','Petty Officer Second Class', 'Petty Officer First Class', 'Chief Petty Officer', 'Senior Chief Petty Officer','Master Chief Petty Officer')
orank = ('Ensign','Sublieutenant','Lieutenant','Lieutenant Commander', 'Commander' , 'Captain', 'Commodore', 'Fleet Admiral', 'Sector Admiral', 'Grand Admiral')

###################################################################
#  apply_skill(grunt, skill)
#  grunt is the character object
#  skill is a text string
#
#  updates the character upp object
#  6/11/13 MU removed upp call no longer used
#
###################################################################
def apply_skill(grunt, skill): 
    
    print "Shouldn't be calling this function."
    return

    '''
    if '+1 str' == skill:
        grunt.upp.str += 1
    if '+1 dex' == skill:
        grunt.upp.dex += 1
    if '+1 end'  == skill:
        grunt.upp.edu += 1
    if '+1 int' == skill:
        grunt.upp.int += 1
    if '+1 edu' == skill:
        grunt.upp.edu += 1
    if '+1 soc' == skill:
        grunt.upp.soc += 1
    '''
#end of apply_Skill


###################################################################
#  apply_navy_muster_benefit(roll, grunt)
#  roll is the result of a d6 roll
#  grunt is the character object
#
#  updates the character upp object 
#
###################################################################
def apply_navy_muster_benefit(roll, grunt):
	'apply muster benefits to upp'
	if 1 == roll:
		#upp['int'] += 1
		grunt.upp.int += 1
	if 2 == roll:
		upp['edu'] += 2
	grunt.upp.edu += 2
	if 6 == roll:
		upp['soc'] += 2
	grunt.upp.soc += 2
	return
#end appy_navy_muster_benefit

###################################################################
#  apply_muster_out(grunt, bt)
#  grunt is the character object
#  bt is an integer value, result of a d6 roll
#
#  updates the character object with the results of muster out rolls
#
###################################################################
def apply_muster_out(grunt, bt):
	if grunt.branch == branches[2]:  #Imperial Navy
		for x in range(0,bt):
			if grunt.muster_loot[x] == '+1 int':
				grunt.upp.int += 1
			if grunt.muster_loot[x] == '+2 edu':
				grunt.upp.edu += 2
			if grunt.muster_loot[x] == '+2 soc':
				grunt.upp.soc += 2
	else:
		print 'In apply_muster_out and not in Navy'
#end of apply_muster_out()


###################################################################
#  muster_out(grunt)
#  grunt is the character object
#  
#
#  determines how many muster rolls of each type you get
#
###################################################################
def muster_out(grunt):
        'Dermine what cash and loot you get out alive with'

	muster.muster_out_rolls(grunt)

	if grunt.term >= 5:
	   b1_data2.retirement_pay(grunt)

	bt = 0  # number of Non Cash Loot rolls
	ct = 0  # number of cash rolls

	# muster_rolls is the total number of rolls available
	
	for x in range(0,grunt.muster_rolls):
		if ct >= 3:     #arbitary - max of 3 cash rolls
			bt += 1
		else:
			if 1 == randint(0, 1):   # flip a coin.
				ct += 1
			else:
				bt += 1

	if (bt > 0) and (ct == 0):      #Make sure there is at least 1 cash roll
		bt -= 1
		ct += 1 
	for x in range(0, ct):
		roll = randint(0, 5)

# alternate code skill.list.has_key('Gambling')
# will return True if it is the list
		
		if "Gambling" in grunt.skills:  
			roll += 1
		if branches[2] == grunt.branch:   #Navy
			grunt.muster_cash.append(navy_cash_table[roll])
			grunt.cash += navy_cash_table[roll]
			s = 'Muster out Benefit of Cr%d' % navy_cash_table[roll]
			grunt.history.append(s)

	for x in range(0, bt):
		roll = randint(0, 5)
		if grunt.rank > 4:
			roll += 1
		if branches[2] == grunt.branch:   #Navy
			grunt.muster_loot.append(navy_muster_table[roll])
			apply_navy_muster_benefit(roll, grunt)
			s = 'Muster out Benefit of %s' % navy_muster_table[roll]
			grunt.history.append(s)
	# apply_muster_out() to handle awards like +1 edu
	apply_muster_out(grunt, bt)
 
# end of muster_out()

def display_b5_rank(grunt):

	if grunt.officer == False:
		print erank[grunt.rank]
	else:
		print(orank[grunt.rank])

def get_branch_skill(grunt, bn):
    # June 2015 MU Updated to use dictionary for skills

	#print 'Debug: bn = ', bn

    if bn > 5:
		bn = randint(0,5)
		print 'Debug: bn changed to ', bn
    dm = 0
    dm += 2 #Everybody is Imperial Navy for now
    roll = dm + randint(0,5)
    if bn == 0:
         entry = line_crew[roll]
    elif bn == 1:
         entry = flight[roll]
    elif bn == 2:
         entry = gunnery[roll]
    elif bn == 3:
         entry = engineering[roll]
    elif bn == 4:
         entry = medical[roll]
    elif bn == 5:
         entry = technical[roll]
    else:
         print 'in get_branch_skill() and we have a problem'
         print 'bn = ', bn
         return False
         
    grunt.add_skill(entry)
    return True
#end of get_branch_skill()      

def navy_spec_school(grunt):
    'Specialist School for Naval enlisted'

    dm = dice(7)-1
    roll = dm + dice()
    if roll == 1:
        ssSkill = 'Admin'
    elif roll == 2:
        ssSkill = 'Medical'
    elif roll == 3:
        ssSkill = 'Liaison'
    elif roll == 4:
        ssSkill = 'Mechanical'
    elif roll == 5:
        ssSkill = 'Electronics'
    elif roll == 6:
        ssSkill = 'Gravitics'
    elif roll == 7:
        ssSkill = 'Vehicle'
    elif roll == 8:
        ssSkill = 'Nav'
    elif roll == 9:
        ssSkill = 'Computer'
    elif roll == 10:
        ssSkill = 'Ships Boat'
    elif roll == 11:
        ssSkill = 'Communications'
    else:
        ssSkill = 'Vac Suit'
 
    grunt.skills(ssSkill)    

#end navy_spec_school()

def sa_select(grunt):
	'select Specific Assignment'
	
	dm = 0
	if grunt.college and grunt.officer == False:
		dm += 1
	roll = dm + randint(1,6) + randint(1,6)
	if roll == 2:
		sa = 'Battle'
	elif roll == 3 or roll == 10:
		sa = 'Shore Duty'
	elif roll == 4:
		sa = 'Siege'
	elif roll == 5 or roll == 9:
		sa = 'Strike'
	elif roll == 6 or roll == 8:
		sa = 'Patrol'
	elif roll == 7:
		sa = 'Training'
	elif roll > 10:
		sa = 'Special Duty'

	return sa
#end of sa_select

def navy_xtrain(grunt):
        'Cross training in the Imperial Navy, not cross dressing'
        trained = False
	roll = 0
	if not grunt.officer:
		if grunt.arm == 'Crew':
			roll = randint(1,5)
			grunt.xtrained.append(navy_branch[roll])
			s = 'Cross Trained in ' + navy_branch[roll]
			grunt.history.append(s)
			get_branch_skill(grunt, roll)
		else:
			x = 0
			while x <= 5 and not trained:
				if navy_branch[x] == grunt.branch:
					roll = x                #Find a branch grunt isn't in.
					while roll == x:
						roll = randint(0,5)
					trained = True
				else:
					x += 1
			if trained == False:
				print 'in navy_xtrain() and we have a problem.'
			grunt.xtrained.append(navy_branch[roll])
			s = 'Cross Trained in ' + navy_branch[roll]
			grunt.history.append(s)
			get_branch_skill(grunt, roll)
				
	else:
		x = 0
		while x < 6  and not trained:
			if navy_branch[x] == grunt.branch:
				roll = x
				while roll == x:
					roll = randint(0,5)
			else:
				x += 1
				trained = True
		grunt.xtrained.append(navy_branch[roll])
		s = 'Cross Trained in ' + navy_branch[roll]
		grunt.history.append(s)
		#Resolve year in xtrained branch
		command = False
		command = navy_cmd_check(grunt)
		sa = sa_select(grunt)
		if roll == 0:
			lc_res(grunt, sa, command)
		elif roll == 1:
			flight_res(grunt, sa, command)
		elif roll == 2:
			gunnery_res(grunt, sa, command)
		elif roll == 3:
			eng_res(grunt, sa, command)
		elif roll == 4:
			medical_res(grunt, sa, command)
		elif roll == 5:
			tech_res(grunt, sa, command)

							  

def check_college_admin(grunt):
    'Check for College Admission'

    grunt.history.append('Applying to College')
    dm = 0
    if grunt.upp.edu >= 9:
        dm += 2
    roll = dm + dice(2)
    if roll >= 9:
        grunt.history.append('Accepted to College')
        return True
    else:
        grunt.history.append('Not accepted to college')
        return False   #no aging
#end of check_college_admin
	

def check_college(grunt):
	'check for college completion'
	
	if college(grunt):
         return True
	else:
		grunt.college_fail = True
		grunt.history.append('Failed College')
	return False

			
#end of check_college()

def college(grunt):
    'Go off to college'
	
    dm = 0
    if grunt.upp.edu >= 8:
        dm += 2
        roll = dm + randint(1,6) + randint(1,6)
        if roll >= 7:
            #Completed college
            grunt.college = True
		
            dm = 0
            if grunt.upp.soc >= 10:
                dm += 1
            roll = dm + randint(1,6) + randint(1,6)
            if roll >= 8:
                grunt.history.append('Navy Officer Training Corps')
                grunt.notc = True
                grunt.officer = True
                grunt.rank = 0
                #check for edu increase
		dm = 0
		if grunt.upp.int >= 9:
			dm += 1
		roll = dm + randint(1,6) - 2
		if roll < 1:
			roll = 1
		grunt.upp.edu += roll
		if grunt.upp.edu > 12:
			grunt.upp.edu = 12
		s = 'College increased EDU by %d' % roll
		grunt.history.append(s)
			#check for honors
		dm = 0
		if grunt.upp.edu >= 10:
			dm += 1
		roll = dm + randint(1,6) + randint(1,6)
		if roll >= 10:
			grunt.honors = True
			grunt.history.append('Graduated College with Honors')
		else:
			grunt.history.append('Graduated College')
		grunt.age += 4   #College takes four years
		return True
	else:
		grunt.age += 1  #failing college takes 1 year
		return False
# end of college()

def Naval_Academy(grunt):
    'Naval Academy process'
    # June 2015 MU Skills now handled as a dictionary
    dm = 0
    if grunt.upp.soc >= 10:
		dm += 2
    roll = dm + randint(1,6) + randint(1,6)
    if roll >= 10:   #admitted into Academy
        grunt.history.append('Accepted to Naval Academy')
        dm = 0       #Check to see if graduated
        if grunt.upp.int >= 8:
			dm += 2
        roll = dm + randint(1,6) + randint(1,6)
        if roll >= 9:
           grunt.history.append('Graduated Naval Academy')
           grunt.academy = True
			#Success full graduation, check for skills
           if randint(1,6) >= 4:
               grunt.add_skill('Vacc Suit')
           if randint(1,6) >= 4:
               grunt.add_skill('Nav')
           if randint(1,6) >= 4:
               grunt.add_skill('Engineering')
			#Add to education
           dm = 0
           if grunt.upp.int >= 9:
               dm += 1
           roll = dm + randint(1,6) - 3
           if roll < 1:
              roll = 1
           grunt.upp.edu += roll
           if grunt.upp.edu > 12:
			grunt.upp.edu = 12
           s = 'Edu +%d' % roll
           grunt.history.append(s)
			#check for honors
           dm = 0
           if grunt.upp.int >=9:
			dm += 1
           roll = dm + randint(1,6) + randint(1,6)
           if roll >= 9:
			grunt.honors = True
			grunt.history.append('Graduated Naval Academy with Honors')
           grunt.age += 4  #Four years to complete
           grunt.officer = True
           grunt.rank = 0
           return True
        else:
			#short three year term next
		grunt.history.append('Failed Naval Academy')
		grunt.age += 1  #one year to fail
		return False
    else:
		grunt.history.append('Not accepted to Naval Academy')
		return False   #no aging if not accepted
#end of Naval_Academy

def flight_school(grunt):
    'Flight School'
    # June 2015 MU updated skills to be a dictionary

    dm = 0
    if grunt.upp.dex >= 9:
        dm += 1
    roll = dm + randint(1,6) + randint(1,6)
    if roll >= 9:
        grunt.history.append('Accepted to Flight School')
        dm = 0
        if grunt.upp.int >= 8:
		dm += 1
        roll = dm + randint(1,6) + randint(1,6)
        if roll >=7:   #graduate flight school
            grund.add_skill('Pilot')
            if randint(1,6) >= 4:
                grund.add_skill('Pilot')
            if randint(1,6) >= 4:
                grund.add_skill('Ships Boat')
            if randint(1,6) >= 4:
                grund.add_skill('Nav')
            grunt.history.append('Graduated Flight School')
            grunt.flight = True
            grunt.age += 1   #pass or fail, takes one year
            return True
        else:
			grunt.history.append('Failed Flight School')
			grunt.flight_fail = True
			grunt.age += 1   #pass or fail, takes one year
			return False
    else:
		grunt.history.append('Not accepted to Flight School')
		return False



#end of flight_school()

def medical_school(grunt):

    dm = 0
    if grunt.upp.edu >= 10:
        dm += 2
    roll = dm + dice(2)
    if roll >= 9:
        grunt.history.append('Accepted to Medical School')
        dm = 0
        if grunt.upp.int >= 9:
            dm += 2
        roll = dm + dice(2)
        if roll >=8:   #graduate medical school
            grunt.schools.append('Medical')
            grunt.upp.edu += 1
            grunt.history.append('+1 edu')
            if grunt.upp.edu > 12:
                grunt.upp.edu = 12
                grunt.history.append('edu capped at F')
            
            grunt.add_skill('Medic')
            grunt.add_skill('Medic')
            grunt.add_skill('Medic')
            grunt.add_skill('Medic')
            grunt.add_skill('Medic')
            grunt.add_skill('Admin')
            grunt.officer = True
            grunt.rank = 2
            grunt.medschool = True
            grunt.age += 4   #Medical School takes four years
            dm = 0
            if grunt.upp.edu >= 11:
                dm += 1
            roll = dm + dice(2)
            if roll >= 11:
                grunt.history.append('Graduated Medical School with Honors')
                grunt.add_skill('Medic')
                grunt.add_skill('Computer')
            else:
                grunt.history.append('Granduated Medical School')
            return True
        else:
            grunt.history.append('Failed medical School')
            grunt.med_fail = True
            grunt.age += 1   #Only 1 year.
            return False
    else:
        grunt.history.append('Not accepted to Medical School')  #no aging if not accepted
        return False
#end of medical_school()

def navy_e_school(grunt):
    'Enlisted Engineering School'

    if dice() >= 5:
        grunt.add_skill('Mechanical')
    if dice() >= 5:
        grunt.add_skill('Electronics')
    if dice() >= 5:
        grunt.add_skill('Gravitics')
    if dice() >= 5:
        grunt.add_skill('Engineering')
        

#end navy_e_school()
							

def navy_ocs(grunt):
   'navy_ocs'

   grunt.officer = True
   grunt.rank = 0
   grunt.schools.append('OCS')

   roll = dice()-1
   cSkill = command_skills[roll]
   grunt.add_skill(cSkill)
   roll = dice()-1
   sSkill = staff_skills[roll]
   grunt.add_skill(sSkill)
   roll = dice()-1
   nbranch_skill(grunt,roll)
#end of navy_osc
	

def navy_bat(grunt):
    'Basic and Advanced Training'

    roll1 = dice()-1
    roll2 = dice()-1
    if grunt.officer:
        if (grunt.rank > 2) and (grunt.rank < 6):
            roll1 += 2
        if grunt.rank > 6:
            roll1 += 4
        grunt.add_skill(staff_skills[roll1])
        nbranch_skill(grunt, roll2)
    else:
         nbranch_skill(grunt, roll1)
         nbranch_skill(grunt, roll2)
    grunt.age += 1

    grunt.bat = True
#end of navy_bat()

def nbranch_skill(grunt, roll):
    'add a Navy branch skill'

    roll += 2  #Imperial Navy by default
    if roll > 6:
		roll = 6
    if grunt.arm == 'Line' or grunt.arm == 'Crew':
		nbSkill = line_crew[roll]
    elif grunt.arm == 'Flight':
		nbSkill = flight[roll]
    elif grunt.arm == 'Gunnery':
		nbSkill = gunnery[roll]
    elif grunt.arm == 'Engineering':
		nbSkill = engineering[roll]
    elif grunt.arm == 'Medical':
		nbSkill = medical[roll]
    elif grunt.arm == 'Technical Services':
		nbSkill = technical[roll]
    else:
		print 'In nbranch_skill and an error has occured'
  
    grunt.add_skill(nbSkill)    
		
#end nbranch_skill()

def navy_aa(grunt):
    'Navy Attache or Aide Duty'

    if dice() < 5:
        grunt.upp.soc += 1
        grunt.rank + 1
        grunt.history.append('Naval Attache')
        grunt.history.append('+1 SOC')
        if grunt.rank < 9:
            grunt.history.append('Promotion to %s' % orank[grunt.rank])
    else:
        grunt.history.append('Aide to Flag Officer')
        grunt.upp.soc += 1
        grunt.history.append('+1 SOC')
#end of navy_aa()

def navy_cmd_check(grunt):
    'check for command - Officers only'
                                    
    command = False
    dm = 0
    if grunt.rank < 2:
        dm -= 2
    if grunt.rank >= 2 and grunt.rank < 4:
        dm -= 1
    if grunt.upp.soc >= 11:
        dm += 1
    if grunt.upp.int <= 7:
        dm -= 1
    if grunt.upp.edu <= 7:
        dm -= 1
    roll = dm + dice(2)
    if roll < 0:
        roll = 1
    if grunt.arm == 'Line':
        if roll >= 7:
            command = True
    elif grunt.arm == 'Flight':
        if roll >= 8:
            command = True
    elif grunt.arm == 'Gunnery':
        if roll >= 9:
            command = True
    elif grunt.arm == 'Engineering':
        if roll >= 10:
            command = True
    elif grunt.arm == 'Medical':
        if roll >= 11:
            command = True
    elif grunt.arm == 'Technical Services':
        if roll >= 12:
            command = True
    return command
#end of navy_cmd_check()

def select_navy_branch(grunt):
    'select Naval branch(arm)'

    if grunt.medschool:
        grunt.arm = navy_branch[4]
        grunt.history.append('Assigned to Medical Branch')
        grunt.navalBranch = True
        return True
    if 'Flight' in grunt.schools:
        grunt.arm = navy_branch[1]
        grunt.history.append('Assigned to Flight Branch')
        grunt.navalBranch = True
        return True
    
    dm = 0
    dm -= 2  #Imperial Navy by default
    if grunt.upp.edu >= 9:
        dm +- 2
    if grunt.upp.int >= 10:
        dm += 2
    roll = dm + dice()

    if roll <= 0:
        grunt.arm = navy_branch[5]
        grunt.history.append('Assigned to Technical Services Branch')
    elif roll < 3:
        if grunt.officer:
            grunt.arm = navy_branch[0]
            grunt.history.append('Assigned to Line Branch')
        else:
            grunt.arm = 'Crew'
            grunt.history.append('Assigned to Crew Branch')
    elif roll == 3:
        grunt.arm = navy_branch[3]
        grunt.history.append('Assigned to Engineering Branch')
    elif roll == 4:
        if grunt.officer:
            grunt.arm = navy_branch[2]
            grunt.history.append('Assigned to Gunnnery Branch')
        else:
            grunt.arm = navy_branch[3]
            grunt.history.append('Assigned to Engineering Branch')
    elif roll == 5:
        if grunt.officer:
            grunt.arm = navy_branch[0]
            grunt.history.append('Assigned to Line Branch')
        else:
            grunt.arm = navy_branch[2]
            grunt.history.append('Assigned to Gunnnery Branch')
    elif roll == 6:
        if grunt.officer:
            grunt.arm = navy_branch[1]
            grunt.history.append('Assigned to Flight Branch')
        else:
            grunt.arm = navy_branch[2]
            grunt.history.append('Assigned to Gunnnery Branch')
    else:
        grunt.arm = navy_branch[4]
        grunt.history.append('Assigned to Medical Branch')
    grunt.navalBranch = True

#end of select_navy_branch()

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

	#DM of +2 if Imperial Navy & getting a branch skill
	#DM +4 if O1+ for Navy Life
	#DM +4 if O1+ for Shipboard Life
	#DM +4 if O1+ for Shore Duty Life
	#DM +2 if E5+ for Petty Officer
	#DM +4 if E7+ for Petty Officer
	#DM +2 if O4+ for Command Officer & Staff Officer
	#DM +4 if O7+ for Command Officer & Staff Officer

def navy_life_skill(grunt):

    dm = 0
    if grunt.officer:
        dm += 4
    roll = dm + dice()-1
    grunt.add_skill(navy_life_skills[roll])
    #apply_skill(grunt,navy_life_skills[roll])

#end of navy_life_skill()
	
def shipboard_life_skill(grunt):

    dm = 0
    if grunt.officer:
        dm += 4
    roll = dm + dice()-1
    grunt.add_skill(shipboard_skills[roll])
    
#end of shipboard_life_skill()

def get_command_skill(grunt):
    dm = 0
    if grunt.officer and (grunt.rank >= 3 and grunt.rank < 6):
        dm += 2
    elif grunt.officer and grunt.rank >= 6:
        dm += 4
    roll = dm + dice()-1
    grunt.add_skill(command_skills[roll])

#end of get_command_skill()

def get_staff_skill(grunt):
     dm = 0
     if grunt.officer and (grunt.rank >= 3 and grunt.rank < 6):
         dm += 2
     elif grunt.officer and grunt.rank >= 6:
         dm += 4
     roll = dm + dice()-1
     grunt.add_skill(staff_skills[roll])


#end of get_staff_skill()
	 
def shore_duty_life_skill(grunt):

    dm = 0
    if grunt.officer:
        dm += 4
    roll = dm + dice()-1
    grunt.add_skill(shoreduty_skills[roll])

#end of get_staff_skill()

def get_po_skill(grunt):
    #DM +2 if E5+ for Petty Officer
    #DM +4 if E7+ for Petty Officer
    
    dm = 0
    if False == grunt.officer and (grunt.rank >= 3 and grunt.rank < 6):
        dm += 2
    elif False == grunt.officer and grunt.rank >= 6:
        dm += 4
    roll = dm + dice()-1
    grunt.add_skill(po_skills[roll])

#end of get_po_skill

def get_navy_skill(grunt, command, sa):
    'Get a skill and apply it'

    if coin_flip():
        roll = 2 + dice()-1
        if roll > 5:
            roll = 5
        get_branch_skill(grunt, roll)
    else:
        if grunt.officer:
            if (sa != 'Training' or sa != 'Shore Duty'):
                x = dice(sides=3)
                if x == 1:
                    navy_life_skill(grunt)
                elif x == 2:
                    shipboard_life_skill(grunt)
                elif x == 3:
                    if command:
                        get_command_skill(grunt)
                    else:
                        get_staff_skill(grunt)
            else:
                x = dice(sides=3)
                if x == 1:
                    navy_life_skill(grunt)
                elif x == 2:
                    shore_duty_life_skill(grunt)
                elif x == 3:
                    if command:
                        get_command_skill(grunt)
                    else:
                        get_staff_skill(grunt)
        elif grunt.rank > 2:
            if (sa != 'Training' or sa != 'Shore Duty'):
                x = dice(sides=3)
                if x == 1:
                    navy_life_skill(grunt)
                elif x == 2:
                    shipboard_life_skill(grunt)
                elif x == 3:
                    get_po_skill(grunt)
            else:
                x = dice(sides=3)
                if x == 1:
                    navy_life_skill(grunt)
                elif x == 2:
                    shore_duty_life_skill(grunt)
                elif x == 3:
                    get_po_skill(grunt)
        else:
            if (sa != 'Training' or sa != 'Shore Duty'):
                if coin_flip():
                    navy_life_skill(grunt)
                else:
                    shipboard_life_skill(grunt)
            else:
                if coin_flip():
                    navy_life_skill(grunt)
                else:
                    shore_duty_life_skill(grunt)
#end of get_navy_skill
			


def navy_sd(grunt):
    'Deal with Navy Special Duty'

    dm = 0
    if grunt.college or grunt.upp.soc >= 11:
        dm += 1
    roll = dm = dice()-1
    if grunt.officer:
        s = 'Special Duty: %s' % sd_officer[roll]
        grunt.history.append(s)
        if roll == 0:
            navy_xtrain(grunt)
        elif roll == 1:
            if dice() >= 4:
                grunt.add_skill('Forgery')
            if dice() >= 4:
                grunt.add_skill('Gun Cbt')
            if dice() >= 4:
                grunt.add_skill('Bribery')
            if dice() >= 4:
                grunt.add_skill('Streetwise')
            if dice() >= 4:
                grunt.add_skill('Interrogation')
        elif roll == 2:
            grunt.add_skill('Recruiting')
        elif roll == 3:
            navy_aa(grunt)
        elif roll == 4:
            if dice() >= 4:
                grunt.add_skill('Ship Tactics')
            if dice() >= 4:
                grunt.add_skill('Fleet Tactics')
            if dice() >= 4:
                grunt.add_skill('Leader')
            if dice() >= 4:
                grunt.add_skill('Admin')
        elif roll > 4:
            if dice() >= 4:
                grunt.add_skill('Fleet Tactics')
            if dice() >= 4:
                grunt.add_skill('Liaison')
            if dice() >= 4:
                grunt.add_skill('Computer')
            if dice() >= 4:
                grunt.add_skill('Admin')
    else:
        s = 'Special Duty: %s' % sd_enl[roll]
        grunt.history.append(s)
        if roll == 0:
            navy_xtrain(grunt)
        elif roll == 1:
            navy_spec_school(grunt)
        elif roll == 2:
            grunt.add_skill('Recruiting')
            if dice() >= 4:
                grunt.add_skill('Admin')
        elif roll == 3:
            if dice() >= 5:
                grunt.add_skill('Ships Lasers')
            if dice() >= 5:
                grunt.add_skill('Ships Missiles')
            if dice() >= 5:
                grunt.add_skill('Ships Particle Accelerators')
            if dice() >= 5:
                grunt.add_skill('Ships Energy Weapons')
            if dice() >= 5:
                grunt.add_skill('Meson Weapons')
            if dice() >= 5:
                grunt.add_skill('Screens')
        elif roll == 4:
            navy_e_school(grunt)
        elif roll > 4:
            if grunt.age > 34:
                grunt.history.append('Too old for OCS')
                navy_sd(grunt)
            else:
                navy_ocs(grunt)

#end of navy_sd()
	

def lc_res(grunt, sa, command):
    'resolve year: Navy Line or Crew'

    s = 'Assigment is %s' % sa
    if command:
        s = s + ' Command'
    grunt.history.append(s)
    auto = 0
    no_chance = 20
    combat_action = False
 
    if sa == 'Training':
        survival_target = auto  #auto survival
        dec_target = no_chance  #No chance for decoration
        combat_action = False
        if grunt.officer:
            promot_target = no_chance  # officers not elibile for promotion
        else:
            promot_target = 6
        skill_target = 7
    elif sa == 'Shore Duty':
        combat_action = False
        survival_target = 4  
        dec_target = 12  
        if grunt.officer:
            promot_target = no_chance  # officers not elibile for promotion
        else:
            promot_target = 7
        skill_target = 7   
    elif sa == 'Patrol':
        combat_action = True
        survival_target = 4  
        dec_target = 11
        promot_target = 7
        skill_target = 6
    elif sa == 'Siege':
        combat_action = True
        survival_target = 5  
        dec_target = 10  
        promot_target = 8
        skill_target = 6
        
    elif sa == 'Strike':
        combat_action = True
        survival_target = 6  
        dec_target = 7  
        promot_target = 7
        skill_target = 5
        
    elif sa == 'Battle':
        combat_action = True
        survival_target = 6  
        dec_target = 6
        promot_target = 6
        skill_target = 5
    else:
        print 'In lc_res with a problem'
        combat_action = False
        survival_target = 2
        dec_target = 2
        promot_target = 2
        skill_target = 2

    #Apply DMs
    p_dm = 0
    s_dm = 0
    if grunt.upp.edu >= 8:
        p_dm += 1
    if grunt.upp.soc >= 9:
        p_dm += 1
    #survival DM.  +1 if any branch skill level is 2+
    dm = False
    x = len(line_crew)
    while x >= 0 and dm == False:
        pass
        ''' Need to fix this later
        if grunt.skills.count(line_crew[x-1]) >= 2:
            dm = True
        x -= 1
        '''
    if dm:
        s_dm += 1

    
    sroll = s_dm + dice(qty=2)
    if sroll < survival_target:
        s = 'Failed survival target of %d' % survival_target
        grunt.history.append(s)
        grunt.alive = False
        return False
    else:
        if ((sroll == survival_target) and combat_action):
            grunt.decorations.append('Wound Badge awarded in ' + sa)
            grunt.history.append('Wound Badge awarded in ' + sa)

    #Decoration check
    droll = dice(qty=2)
    if droll >= dec_target:
        promotions.get_medal(grunt, droll, dec_target, sa)
        s = 'Received a %s' % grunt.decorations[-1]
        grunt.history.append(s)

    #Promotion check - Officers can only be promoted once per term.
    p_roll = p_dm + dice(qty=2)
    if (False == grunt.officer):
        if p_roll >= promot_target:
            e_promote(grunt)
        else:
            if (grunt.promote_this_term == False):
                if p_roll >= promot_target:
                    o_promote(grunt)

    #Skill check 
    s_roll = dice(qty=2)
    if s_roll >= skill_target:
        get_navy_skill(grunt, command, sa)

#end lc_res

def flight_res(grunt, sa, command):
    'resolve year: Navy Flight'

    s = 'Assigment is %s' % sa
    if command:
        s = s + ' Command'
	grunt.history.append(s)
    auto = 0
    no_chance = 20
    combat_action = False
 
    if sa == 'Training':
        survival_target = 3
        dec_target = no_chance  #No chance for decoration
        combat_action = False
        promot_target = no_chance  #No chance for promotion
        skill_target = 7
    elif sa == 'Shore Duty':
        combat_action = False
        survival_target = 3  
        dec_target = no_chance  
        promot_target = 11
        skill_target = no_chance 
    elif sa == 'Patrol':
        combat_action = True
        survival_target = 3  
        dec_target = 10
        promot_target = 11
        skill_target = 7
    elif sa == 'Siege':
        combat_action = True
        survival_target = 3  
        dec_target = 9  
        promot_target = 10
        skill_target = 7
        
    elif sa == 'Strike':
        combat_action = True
        survival_target = 3  
        dec_target = 9  
        promot_target = 9
        skill_target = 6
        
    elif sa == 'Battle':
        combat_action = True
        survival_target = 4  
        dec_target = 8
        promot_target = 9
        skill_target = 6

    #Apply DMs
    d_dm = 0
    s_dm = 0
    p_dm = 0
    #survival DM is the pilot skill level
    s_dm = grunt.skills.count('Pilot')
    #decoration, in Battle or Strike only, DM is = TB1 rank number
    if (sa == 'Battle' or sa == 'Strike') and grunt.officer:
        if grunt.rank < 2:
            p_dm += 1
        elif grunt.rank == 2:
            p_dm +=2
        elif grunt.rank == 3:
            p_dm += 3
        elif grunt.rank == 4:
            p_dm = 4
        elif grunt.rank < 7:
            p_dm += 5
        else:
            p_dm += 6

    # Survival check
    sroll = s_dm + dice(qty=2)
    if sroll < survival_target:
        s = 'Failed survival target of %d' % survival_target
        grunt.history.append(s)
        grunt.alive = False
        return False
    else:
        if ((sroll == survival_target) and combat_action):
            grunt.decorations.append('Wound Badge awarded in ' + sa)
            grunt.history.append('Wound Badge awarded in ' + sa)

    #Decoration check
    droll = d_dm + dice(qty=2)
    if droll >= dec_target:
        promotions.get_medal(grunt, droll, dec_target, sa)
        s = 'Received a %s' % grunt.decorations[-1]
        grunt.history.append(s)

    #Promotion check - Officers can only be promoted once per term.
    p_roll = dice(qty=2)
    if (False == grunt.officer):
        if p_roll >= promot_target:
            e_promote(grunt)
        else:
            if (grunt.promote_this_term == False):
                if p_roll >= promot_target:
                    o_promote(grunt)

    #Skill check 
    s_roll = dice(qty=2)
    if s_roll >= skill_target:
        get_navy_skill(grunt, command, sa)
#end flight_res

def gunnery_res(grunt, sa, command):
    'resolve year: Navy Gunnery'

    s = 'Assigment is %s' % sa
    if command:
        s = s + ' Command'
	grunt.history.append(s)
 
    auto = 0
    no_chance = 20
    combat_action = False
 
    if sa == 'Training':
        combat_action = False
        survival_target = auto
        dec_target = no_chance  #No chance for decoration
        if grunt.officer:
            promot_target = no_chance  #No chance for promotion
        else:
            promot_target = 6
        skill_target = 8
    elif sa == 'Shore Duty':
        combat_action = False
        survival_target = 3  
        dec_target = 12  
        if grunt.officer:
            promot_target = no_chance  #No chance for promotion
        else:
            promot_target = 6
        skill_target = no_chance 
    elif sa == 'Patrol':
        combat_action = True
        survival_target = 4  
        dec_target = 11
        promot_target = 8
        skill_target = 7
    elif sa == 'Siege':
        combat_action = True
        survival_target = 5  
        dec_target = 10  
        promot_target = 10
        skill_target = 7
        
    elif sa == 'Strike':
        combat_action = True
        survival_target = 5  
        dec_target = 9  
        promot_target = 7
        skill_target = 6
        
    elif sa == 'Battle':
        combat_action = True
        survival_target = 6  
        dec_target = 7
        promot_target = 6
        skill_target = 6

    #Apply DMs
    d_dm = 0
    s_dm = 0
    p_dm = 0
    #survival no DM
    #decoration, DM +1 if dex 10+
    #promotion, DM +1 if dex 9+
    if grunt.upp.dex >= 10:
        d_dm += 1
    if grunt.upp.dex >= 9:
        d_dm += 1

    # Survival check, no DM coded yet
    sroll = s_dm + dice(qty=2)
    if sroll < survival_target:
        s = 'Failed survival target of %d' % survival_target
        grunt.history.append(s)
        grunt.alive = False
        return False
    else:
        if ((sroll == survival_target) and combat_action):
            grunt.decorations.append('Wound Badge awarded in ' + sa)
            grunt.history.append('Wound Badge awarded in ' + sa)

    #Decoration check
    droll = d_dm + dice(qty=2)
    if droll >= dec_target:
        promotions.get_medal(grunt, droll, dec_target, sa)
        s = 'Received a %s' % grunt.decorations[-1]
        grunt.history.append(s)

    #Promotion check - Officers can only be promoted once per term.
    p_roll = p_dm + dice(qty=2)
    if (False == grunt.officer):
        if p_roll >= promot_target:
            e_promote(grunt)
        else:
            if (grunt.promote_this_term == False):
                if p_roll >= promot_target:
                    o_promote(grunt)

    #Skill check 
    s_roll = dice(qty=2)
    if s_roll >= skill_target:
        get_navy_skill(grunt, command, sa)
#end gunnery_res

def eng_res(grunt, sa, command):
    'resolve year: Navy Engineering'

    s = 'Assigment is %s' % sa
    if command:
        s = s + ' Command'
	grunt.history.append(s)

    auto = 0
    no_chance = 20
    combat_action = False
 
    if sa == 'Training':
        combat_action = False
        survival_target = auto
        dec_target = no_chance  #No chance for decoration
        if grunt.officer:
            promot_target = no_chance  #No chance for promotion
        else:
            promot_target = 7
        skill_target = 7
    elif sa == 'Shore Duty':
        combat_action = False
        survival_target = auto  
        dec_target = no_chance
        if grunt.officer:
            promot_target = no_chance  #No chance for promotion
        else:
            promot_target = 7
        skill_target = 8
    elif sa == 'Patrol':
        combat_action = True
        survival_target = 3
        dec_target = 12
        promot_target = 5
        skill_target = 6
    elif sa == 'Siege':
        combat_action = True
        survival_target = 4 
        dec_target = 11
        promot_target = 8
        skill_target = 7
        
    elif sa == 'Strike':
        combat_action = True
        survival_target = 5  
        dec_target = 7
        promot_target = 6
        skill_target = 6
        
    elif sa == 'Battle':
        combat_action = True
        survival_target = 5
        dec_target = 7
        promot_target = 6
        skill_target = 5
    else:
        print 'In eng_res and we have a problem'
        print 'sa = ', sa

    #Apply DMs
    d_dm = 0
    s_dm = 0
    p_dm = 0
    # Survival +1 if eng 4+
    #if grunt.skills.count('Engineering') >= 4:
    #    s_dm += 1
        

    # Survival check
    sroll = s_dm + dice(qty=2)
    if sroll < survival_target:
        s = 'Failed survival target of %d' % survival_target
        grunt.history.append(s)
        grunt.alive = False
        return False
    else:
        if ((sroll == survival_target) and combat_action):
            grunt.decorations.append('Wound Badge awarded in ' + sa)
            grunt.history.append('Wound Badge awarded in ' + sa)

    #Decoration check
    droll = d_dm + dice(qty=2)
    if droll >= dec_target:
        promotions.get_medal(grunt, droll, dec_target, sa)  #added promotions. 6/11/13 MU
        s = 'Received a %s' % grunt.decorations[-1]
        grunt.history.append(s)

    #Promotion check - Officers can only be promoted once per term.
    p_roll = p_dm + dice(qty=2)
    if (False == grunt.officer):
        if p_roll >= promot_target:
            e_promote(grunt)
        else:
            if (grunt.promote_this_term == False):
                if p_roll >= promot_target:
                    o_promote(grunt)

    #Skill check 
    s_roll = dice(qty=2)
    if s_roll >= skill_target:
        get_navy_skill(grunt, command, sa)

#end eng_res

def medical_res(grunt, sa, command):
    'resolve year: Navy Medical'

    s = 'Assigment is %s' % sa
    if command:
	s = s + ' Command'
	grunt.history.append(s)
    auto = 0
    no_chance = 20
    combat_action = False
 
    if sa == 'Training':
        combat_action = False
        survival_target = auto
        dec_target = no_chance  #No chance for decoration
        if grunt.officer:
            promot_target = no_chance  #No chance for promotion
        else:
            promot_target = 7
        skill_target = 8
    elif sa == 'Shore Duty':
        combat_action = False
        survival_target = auto  
        dec_target = no_chance
        promot_target = 6
        skill_target = 6
    elif sa == 'Patrol':
        combat_action = True
        survival_target = 3
        dec_target = no_chance
        promot_target = 7
        skill_target = 7
    elif sa == 'Siege':
        combat_action = True
        survival_target = 3 
        dec_target = no_chance
        promot_target = 8
        skill_target = 7
        
    elif sa == 'Strike':
        combat_action = True
        survival_target = 3
        dec_target = 11
        promot_target = 6
        skill_target = 7
        
    elif sa == 'Battle':
        combat_action = True
        survival_target = 4
        dec_target = 10
        promot_target = 6
        skill_target = 6
    

    #Apply DMs
    d_dm = 0
    s_dm = 0
    p_dm = 0
    # Survival +1 if eng 4+
    if grunt.skills.count('Medic') >= 5:
        p_dm += 1
        

    # Survival check, no DM coded yet
    sroll = s_dm + dice(qty=2)
    if sroll < survival_target:
        s = 'Failed survival target of %d' % survival_target
        grunt.history.append(s)
        grunt.alive = False
        return False
    else:
        if ((sroll == survival_target) and combat_action):
            grunt.decorations.append('Wound Badge awarded in ' + sa)
            grunt.history.append('Wound Badge awarded in ' + sa)

    #Decoration check
    droll = d_dm + dice(qty=2)
    if droll >= dec_target:
        promotions.get_medal(grunt, droll, dec_target, sa)
        s = 'Received a %s' % grunt.decorations[-1]
        grunt.history.append(s)

    #Promotion check - Officers can only be promoted once per term.
    p_roll = p_dm + dice(qty=2)
    if (False == grunt.officer):
        if p_roll >= promot_target:
            e_promote(grunt)
        else:
            if (grunt.promote_this_term == False):
                if p_roll >= promot_target:
                    o_promote(grunt)

    #Skill check 
    s_roll = dice(qty=2)
    if s_roll >= skill_target:
        get_navy_skill(grunt, command, sa)

#end medical_res



def tech_res(grunt, sa, command):
    'resolve year: Navy Technical Services'
    s = 'Assigment is %s' % sa
    if command:
	s = s + ' Command'
	grunt.history.append(s)
    auto = 0
    no_chance = 20
    combat_action = False
 
    if sa == 'Training':
	combat_action = False
	survival_target = auto
	dec_target = no_chance  #No chance for decoration
	if grunt.officer:
            promot_target = no_chance  #No chance for promotion
	else:
            promot_target = 7
            skill_target = 7
    elif sa == 'Shore Duty':
	combat_action = False
	survival_target = 3
	dec_target = no_chance
	promot_target = 8
	skill_target = 8
    elif sa == 'Patrol':
	combat_action = True
	survival_target = 3
	dec_target = no_chance
	promot_target = 9
	skill_target = 9
    elif sa == 'Siege':
	combat_action = True
	survival_target = 3 
	dec_target = no_chance
	promot_target = 8
	skill_target = 7
		
    elif sa == 'Strike':
	combat_action = True
	survival_target = 3
	dec_target = 9
	promot_target = 8
	skill_target = 7
		
    elif sa == 'Battle':
	combat_action = True
	survival_target = 3
	dec_target = 8
	promot_target = 7
	skill_target = 7
	

    #Apply DMs
    d_dm = 0
    s_dm = 0
    p_dm = 0
    # Promotion if any branch skill  3+
   

    dm = False
    x = len(technical)
    while x >= 0 and dm == False:
        #if grunt.skills.count(technical[x-1]) >= 3:
        #    dm = True
        #Fix this later
        x -= 1
    if dm:
        s_dm += 1
        

    # Survival check, no DM coded yet
    sroll = s_dm + dice(qty=2)
    if sroll < survival_target:
        s = 'Failed survival target of %d' % survival_target
        grunt.history.append(s)
        grunt.alive = False
        return False
    else:
        if ((sroll == survival_target) and combat_action):
            grunt.decorations.append('Wound Badge awarded in ' + sa)
            grunt.history.append('Wound Badge awarded in ' + sa)

    #Decoration check
    droll = d_dm + dice(qty=2)
    if droll >= dec_target:
        promotions.get_medal(grunt, droll, dec_target, sa)
        s = 'Received a %s' % grunt.decorations[-1]
        grunt.history.append(s)

    #Promotion check - Officers can only be promoted once per term.
     #survival DM.  +1 if any branch skill level is 2+
    dm = False
    x = len(technical)
    while x >= 0 and dm == False:
#        if grunt.skills.count(line_crew[x-1]) >= 2:
#            dm = True
# Fix this later
        x -= 1
    if dm:
        s_dm += 1
    
    p_roll = p_dm + dice(qty=2)
    if (False == grunt.officer):
        if p_roll >= promot_target:
            e_promote(grunt)
        else:
            if (grunt.promote_this_term == False):
                if p_roll >= promot_target:
                    o_promote(grunt)

    #Skill check 
    s_roll = dice(qty=2)
    if s_roll >= skill_target:
        get_navy_skill(grunt, command, sa)
#end tech_res

def navy_med_or_flight(grunt):
    'deal with second term if graduated college or the academy'
    #Can only go to flight school if graduated Academy or completed NOTC
    #Need to graduate with Honors for both Flight and Medical school

    if grunt.academy or grunt.notc:
        if coin_flip():
            medical_school(grunt)
        else:
            flight_school(grunt)
    else:
        medical_school(grunt)
    if grunt.medschool:
            grunt.reenlist = True
            grunt.history.append('#####')
            return True
    if grunt.flight:
        return True
    return False
#end of navy_med_or_flight()

def navy_year_one(grunt):
	'Deal with the first year in the Navy'

	if grunt.upp.soc >= 8:
		Naval_Academy(grunt)
		if grunt.academy:
			grunt.reenlist = True
			grunt.history.append('#####')
			return True
	
	if check_college_admin(grunt):
		check_college(grunt)
	else:
		#was not admitted into college, go straight to the Navy
		return False
	

	if grunt.college:
		grunt.reenlist = True
		grunt.history.append('#####')
		return True

	return False
#end of navy_year_one()

def navy_year(grunt, year):

    'Work through a year in the Navy'

    command = False
    sa = 'unknown'
    if grunt.officer:
        command = navy_cmd_check(grunt)

    if grunt.reten:
        sa = grunt.sa
        grunt.reten = False
    else:
        sa = sa_select(grunt)

    if sa == 'Special Duty':
        navy_sd(grunt)
        grunt.age += 1
        return True

    if grunt.arm == 'Line' or grunt.arm == 'Crew':
        lc_res(grunt, sa, command)
    elif grunt.arm == 'Flight':
        flight_res(grunt, sa, command)
    elif grunt.arm == 'Gunnery':
        gunnery_res(grunt, sa, command)
    elif grunt.arm == 'Engineering':
        eng_res(grunt, sa, command)
    elif grunt.arm == 'Medical':
        medical_res(grunt, sa, command)
    elif grunt.arm == 'Technical Services':
        tech_res(grunt, sa, command)

    if grunt.alive:
        grunt.age += 1

    # check for retention
    # No retention at end of the term.
    if year < 4:
        if 6 == dice():
            print 'Retention is True'
            print 'Unless retained last year'
            grunt.reten = True
            grunt.sa = sa
            return True
        else:
            return True
    else:
        return True


# end of navy_year()
