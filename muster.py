from dice import *
import b5_data

army_cash_table = [2000, 5000, 10000, 10000, 10000, 20000, 30000]
army_muster_table = ['Low Psg', '+1 int', '+2 edu', 'Gun', 'High Psg', 'Mid Psg', '+1 soc']
marine_cash_table = [2000, 5000, 5000, 10000, 20000, 30000, 40000]
marine_muster_table = ['Low Psg', '+2 int', '+1 edu', 'Blade', 'Travellers', 'High Psg', '+2 soc']


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
        grunt.stat_change("int", 2)
    if 2 == roll:
        grunt.stat_change("edu", 1)
    if 6 == roll:
        grunt.stat_change("soc", 2)

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

    if not grunt.officer:      #Have to be an officer to get extra rolls
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
	grunt.stat_change("int", 1)
    if 2 == roll:
	grunt.stat_change("edu", 2)
    if 6 == roll:
	grunt.stat_change("soc", 2)
    return True
#end appy_army_muster_benefit

    
###################################################################
#  muster_out(grunt)
#  grunt is the character object
#  Returns nothing
#
#  performs Book 1 mustering out, updates the character object
#
###################################################################
def muster_out(grunt):
    'Determine what cash and loot you get out alive with'

    if grunt.is_dead():
        return False
    
    if grunt.is_navy():
        return b5_data2.muster_out(grunt)

    muster_out_rolls(grunt)

    if grunt.term >= 5:
        retirement_pay(grunt)

    bt = 0  # number of Non Cash Loot rolls
    ct = 0  # number of cash rolls

    # muster_rolls is the total number of rolls available
    
    for x in range(0,grunt.muster_rolls):
        if ct >= 3:     #arbitary - max of 3 cash rolls
            bt += 1
        else:
            if coin_flip():   # flip a coin.
                ct += 1
            else:
                bt += 1

    if (bt > 0) and (ct == 0):      #Make sure there is at least 1 cash roll
        bt -= 1
        ct += 1 
    for x in range(0, ct):
        roll = dice()

# alternate code skill.list.has_key('Gambling')
# will return True if it is the list
        
        if "Gambling" in grunt.skills:  
            roll += 1
        if grunt.is_army():
            cash = army_cash_table[roll-1]
        else:
            cash = marine_cash_table[roll-1]

        grunt.muster_cash.append(cash)
        grunt.cash += cash
        s = 'Muster out Benefit of Cr%d' % cash
        grunt.history.append(s)

    for x in range(0, bt):
        roll = dice()
        if grunt.rank > 4:
            roll += 1
        if grunt.is_army():
            loot = army_muster_table[roll-1]
            apply_army_muster_benefit(roll-1, grunt)
        elif grunt.is_marine():
            loot = marine_muster_table[roll-1]
            apply_marine_muster_benefit(roll-1, grunt)

        grunt.muster_loot.append(loot)
        s = 'Muster out Benefit of %s' % loot
        grunt.apply_skill(loot)
        grunt.history.append(s)
    return True
# end of muster_out()

