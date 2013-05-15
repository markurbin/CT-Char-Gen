# Classic Traveller Book 1 specific data for character generation
# "The Traveller game in all forms is owned by Far 
# Future Enterprises. Copyright 1977 - 2013 Far Future Enterprises."
# Mark Urbin
# Rev 0.2

from random import randint


noble_table = ['Knight', 'Baron', 'Marquis', 'Count', 'Duke']
branch_Table = ['Imperial Army', 'Imperial Marines', 'Imperial Navy']
army_cash_table = [2000, 5000, 10000, 10000, 10000, 20000, 30000]
army_muster_table = ['Low Psg', '+1 int', '+2 edu', 'Gun', 'High Psg', 'Mid Psg', '+1 soc']
marine_cash_table = [2000, 5000, 5000, 10000, 20000, 30000, 40000]
marine_muster_table = ['Low Psg', '+2 int', '+1 edu', 'Blade', 'Travellers', 'High Psg', '+2 soc']


###################################################################
#  age_chech(grunt)
#  grunt is the character object
#  Returns True or False
#
#  performs Book 1 age checks, updates the character object
#
###################################################################
def age_check(grunt):
    'Perform the age check. Same for all branches'
    
    if False == grunt.alive:        #already dead, don't bother
        return True
    
    if (grunt.age >= 34) and (grunt.age <= 46):

        if (randint(1, 6) + randint(1, 6)) < 8:
            grunt.upp.str -= 1
            s = 'Str reduced by 1 at age %d' % grunt.age
            grunt.history.append(s)
            if grunt.upp.str <= 0:
                grunt.alive = 0
                return False

        if (randint(1, 6) + randint(1, 6)) < 7:
            grunt.upp.dex -= 1
            s = 'Dex reduced by 1 at age %d' % grunt.age
            grunt.history.append(s)
            if grunt.upp.dex <= 0:
                grunt.alive = 0
                return False

        if (randint(1, 6) + randint(1, 6)) < 7:
            grunt.upp.end -= 1
            s = 'End reduced by 1 age %d' % grunt.age
            grunt.history.append(s)
            if grunt.upp.end <= 0:
                grunt.alive = 0
                return False
    else:
        return True

    if (grunt.age >= 50) and (grunt.age <= 62):
 
        if (randint(1, 6) + randint(1, 6)) < 9:
            grunt.upp.str -= 1
            s = 'Str reduced by 1 at age %d' % grunt.age
            grunt.history.append(s)
            if grunt.upp.str <= 0:
                grunt.alive = False
                return False

        if (randint(1, 6) + randint(1, 6)) < 8:
            grunt.upp.dex -= 1
            s = 'Dex reduced by 1 at age %d' % grunt.age
            grunt.history.append(s)
            if grunt.upp.dex <= 0:
                grunt.alive = Falase
                return False
        if (randint(1, 6) + randint(1, 6)) < 9:
            grunt.upp.end -= 1
            s = 'Edu reduced by 1 at age %d' % grunt.age
            grunt.history.append(s)
            if grunt.upp.end <= 0:
                grunt.alive = False
                return False
    else:
        return False

    if grunt.age >= 66:

        if (randint(1, 6) + randint(1, 6)) < 9:
            grunt.upp.str -= 2
            s = 'Str reduced by 2 at age %d' % grunt.age
            grunt.history.append(s)
            if grunt.upp.str <= 0:
                grunt.alive = False
                return False
        if (randint(1, 6) + randint(1, 6)) < 9:
            grunt.upp.dex -= 2
            s = 'Dex reduced by 2 at age %d' % grunt.age
            grunt.history.append(s)
            if grunt.upp.dex <= 0:
                grunt.alive = False
                return False
        if (randint(1, 6) + randint(1, 6)) < 9:
            grunt.upp.end -= 2
            s = 'End reduced by 2 at age %d' % grunt.age
            grunt.history.append(s)
            if grunt.upp.end <= 0:
                alive = False
                return False
        if (randint(1, 6) + randint(1, 6)) < 9:
            grunt.upp.int -= 1
            s = 'int reduced by 1 at age %d' % grunt.age
            grunt.history.append(s)
            if grunt.upp.int <= 0:
                alive = False
                return False
    else:
        return True
    return True
#end of age_check()


###################################################################
#  apply_skill(grunt)
#  grunt is the character object
#  skill is a string containing the skill obtained
#
#  updates the character upp object
#
###################################################################
def apply_skill(grunt, skill): 

    if '+1 str' == skill:
        grunt.upp.str += 1
    if '+1 dex' == skill:
        grunt.upp.dex += 1
    if '+1 end'  == skill:
        grunt.upp.end +- 1
    if '+1 int' == skill:
        grunt.upp.int += 1
    if '+1 edu' == skill:
        grunt.upp.edu += 1
    if '+1 soc' == skill:
        grunt.upp.soc += 1
#end of apply_Skill


###################################################################
#  apply_marine_muster_cash(grunt, roll)
#  grunt is the character object
#  roll is the result of a simulated random die roll
#
#
#  Adds Book 1 muster cash roll results to the character object
#
###################################################################
#def apply_marine_muster_cash(grunt, roll):

#    if 0 == roll:
#        grunt.cash += marine_cash_table[0]
#    if 0 < roll < 3:
#        grunt.cash += marine_cash_table[1]
#    if 3 == cash:
#        grunt.cash += marine_cash_table[3]
#    if roll == 4:
#        grunt.cash += marine_cash_table[4]
#    if roll == 5:
#        grunt.cash += marine_cash_table[5]
#    if roll == 6:
#        grunt.cash += marine_cash_table[6]
    

###################################################################
#  apply_marine_muster_benefit(roll, grunt)
#  Roll is an integer ranging from 1 to 6
#  grunt is the character object
#  Returns nothing
#
#  applies Book 1 muster benefits, updates the character object
#
###################################################################
def apply_marine_muster_benefit(roll, grunt):

    print 'In apply_marine_muster benifit'
    print 'roll should be 1,2 or 6'
    print 'roll = ', roll   #debug
    if 1 == roll:
        grunt.upp.int += 2
    if 2 == roll:
        grunt.upp.edu += 1
    if 6 == roll:
        grunt.upp.soc += 2

###################################################################
#  retirement_pay(grunt)
#  grunt is the character object
#
#  updates the character upp object with retirement pay options
#
###################################################################
def retirement_pay(grunt):
    'Determine any retirement pay'

    if 5 == (grunt.term):
        grunt.r_pay = 4000
    if 6 == (grunt.term):
        grunt.r_pay = 6000
    if 7 == (grunt.term):
        grunt.r_pay = 8000
    if 8 == (grunt.term):
        grunt.r_pay = 10000

    if (grunt.term - 1) > 8:
        grunt.r_pay = 10000 + ((grunt.term - 8) * 2000)
# end of retirement_pay

###################################################################
#  muster_out_rolls(grunt)
#  grunt is the character object
#
#  updates the character object with the total number of mustering
#  out rolls.
#
#  Returns True
#
###################################################################
def muster_out_rolls(grunt):
    'Determine the number of mustering out rolls'

    grunt.muster_rolls = grunt.term
    if grunt.college:               #Not in the Navy if in college
        grunt.muster_rolls -= 1
    if grunt.medschool and (grunt.academy == False):
        grunt.muster_rolls -= 1

    if False == grunt.officer:      #Have to be an officer to get extra rolls
        return True
    if grunt.rank < 3:
        grunt.muster_rolls += 1
        return True
    if 3 <= grunt.rank <=4:
        grunt.muster_rolls += 2
        return True
    if grunt.rank > 4:
        grunt.muster_rolls += 3
        return True
    return True
#end of muster_out_rolls()

###################################################################
#  apply_army_muster_benefit(roll,grunt)
#  roll is an integer, the results of d6 roll
#  grunt is the character object
#  Returns True 
#
#  Applies Book 1 Army muster benefits, updates the character object
#
###################################################################
def apply_army_muster_benefit(roll, grunt):
    'apply muster benefits to upp'
    if 1 == roll:
        #upp['int'] += 1
	grunt.upp.int += 1
    if 2 == roll:
        #upp['edu'] += 2
	grunt.upp.edu += 2
    if 6 == roll:
        #upp['soc'] += 2
	grunt.upp.soc += 2
    return True
#end appy_army_muster_benefit

def apply_muster_out(grunt, bt):
    if grunt.branch == branch_Table[0]:  #Imperial Army
        for x in range(0,bt):
            if grunt.muster_loot[x] == '+1 int':
                grunt.upp.int += 1
            if grunt.muster_loot[x] == '+2 edu':
                grunt.upp.edu += 2
            if grunt.muster_loot[x] == '+1 soc':
                grunt.upp.soc += 1
    elif grunt.branch == branch_Table[1]:  #Imperial Marines
        for x in range(0,bt):
            if grunt.muster_loot[x] == '+2 int':
                grunt.upp.int += 2
            if grunt.muster_loot[x] == '+1 edu':
                grunt.upp.edu += 1
            if grunt.muster_loot[x] == '+2 soc':
                grunt.upp.soc += 2
    else:
        print 'In apply_muster_out and not in Army, Marines or Navy'
#end of apply_muster_out()
    
###################################################################
#  muster_out(grunt)
#  grunt is the character object
#  Returns nothing
#
#  performs Book 1 mustering out, updates the character object
#
###################################################################
def muster_out(grunt):
    'Dermine what cash and loot you get out alive with'

    muster_out_rolls(grunt)

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
        if branch_Table[0] == grunt.branch: #Army
            grunt.muster_cash.append(army_cash_table[roll])
            grunt.cash += army_cash_table[roll]
            s = 'Muster out Benefit of Cr%d' % army_cash_table[roll]
            grunt.history.append(s)
        elif branch_Table[1] == grunt.branch:   #Marines
            grunt.muster_cash.append(marine_cash_table[roll])
            grunt.cash +=marine_cash_table[roll]
            s = 'Muster out Benefit of Cr%d' % marine_cash_table[roll]
            grunt.history.append(s)


    for x in range(0, bt):
        roll = randint(0, 5)
        if grunt.rank > 4:
            roll += 1
        if branch_Table[0] == grunt.branch: #Army
            grunt.muster_loot.append(army_muster_table[roll])
            apply_army_muster_benefit(roll, grunt)
            s = 'Muster out Benefit of %s' % army_muster_table[roll]
            grunt.history.append(s)
        elif branch_Table[1] == grunt.branch:   #Marines
            grunt.muster_loot.append(marine_muster_table[roll])
            apply_marine_muster_benefit(roll, grunt)
            s = 'Muster out Benefit of %s' % marine_muster_table[roll]
            grunt.history.append(s)
        
    # apply_muster_out() to handle awards like +1 edu
    apply_muster_out(grunt, bt)
  
# end of muster_out()

###################################################################
#  Check_upp(grunt)
#  grunt is the character object
#  Returns nothing 
#
#  Makes sure all attributes do not exceed Hex F
#
###################################################################
def check_upp(grunt):
    'Capping attributes at F'

    if grunt.upp.str > 15:
        grunt.upp.str = 15
    if grunt.upp.dex > 15:
        grunt.upp.dex = 15
    if grunt.upp.end > 15:
        grunt.upp.end = 15
    if grunt.upp.int > 15:
        grunt.upp.int = 15
    if grunt.upp.edu > 15:
        grunt.upp.edu = 15
    if grunt.upp.soc > 15:
        grunt.upp.soc = 15
#end of check_upp()
