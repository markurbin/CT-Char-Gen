# Code samples: http://wiki.python.org/moin/SimplePrograms
# Traveller Book 4 & 5 character Generation using classes
# November 2012 - Mark Urbin
# "The Traveller game in all forms is owned by Far 
# Future Enterprises. Copyright 1977 - 2013 Far Future 
# Enterprises."
#
# R3 - Adding read UPP, Branch & Arm from config file
# Adding Book 5 'High Guard' support and moving more functions
# out to modules
#

from random import randint
import time
#import sprint       #to print to to screen or file
import b1_data2      #unique book 1 data
import b4_data2      #unique book 4 data
import b5_data      #unique book 5 data
#import branch_win   #wxpython module to pop up a window to pick the branch

class upp(object):
    def __init__(self):
        self.str = randint(1,6) + randint(1,6)
        self.dex = randint(1,6) + randint(1,6)
        self.end = randint(1,6) + randint(1,6)
        self.int = randint(1,6) + randint(1,6)
        self.edu = randint(1,6) + randint(1,6)
        self.soc = randint(1,6) + randint(1,6)
#End of upp class

class B4Char(object):
        def __init__(self):
                self.upp = self.init_upp = upp()
                #self.age = CharAge()
                self.age = 18
                self.race = 'Human'     #Human by default
                self.raceSubType = 'Mixed'   #Mixed by default
                self.hpName = 'Sylea'       # Sylea by default
                self.hpTL = 12
                self.TL = 12
                self.skills=[]
                self.schools=[]
                self.xTrained=[]
                self.branch = 'Imperial Army'  #IA by default
                self.arm = b4_data2.arm_Table[0] #Infantry by default
                self.old_arms = []
                self.xtrained = []
                self.specials = []
                self.officer = False #enlisted by default
                self.rank = 0  
                self.term = 1
                self.cash = 0
                self.r_pay = 0
                self.decorations = []
                self.ribbons = []
                self.muster_rolls = 0
                self.muster_loot = []
                self.muster_cash = []
                self.alive = True
                self.reenlist = True
                self.history = []
                self.promote_this_term = False
                self.reten = False
                self.sa = 'Unknown'
                self.college = False
                self.college_fail = False
                self.notc = False
                self.academy = False
                self.academy_fail = False
                self.honors = False
                self.medschool = False
                self.med_fail = False
                self.flight = False
                self.flight_fail = False
                self.navalBranch = False
                self.bat = False
                self.dateTimeCreated = 'Fake Time'              
# End of B4Char



def army_marine_xtraining_xfer(grunt):
    'Cross Training transfer for Army & Marines'

    #Check for Cross Training
    if ((False == grunt.officer) and grunt.xtrained) and (grunt.arm not in grunt.xtrained):
        if 1 == randint(0,1):   # 50% chance
            old_arm = grunt.arm
            s = len(grunt.xtrained)
            x = randint(0,s)
            new_arm = grunt.xtrained[x-1]
            s = 'Changing branch from %s to %s' % (old_arm, new_arm)
            grunt.history.append(s)
            grunt.arm = new_arm

    # if not commando and attended commando school, give chance to join commandos
    if (b4_data2.arm_Table[4] in grunt.schools) and (grunt.arm != b4_data2.arm_Table[4]):
            #No choice! Going Commando!
        grunt.arm = b4_data2.arm_Table[4]
        s = 'Transfered to Commando arm at start of term %d' % grunt.term
        grunt.history.append(s)       
#end of army_marine_xtraining_xfer

def check_reenlist(grunt):
    'Check for re-enlistment'
    # if a 12 is rolled, you have to reenlist, even if at
    # or past the manditory retirement
    # return values:
    #   0 - failed reenlist
    #   1 - successful reenlist
    #   2 - Forced reenlist

    rvalue = 0
    if grunt.branch == b1_data2.branch_Table[0]:
        target = 7 #IA
        if grunt.officer == False:
            target -= 2
    elif grunt.branch == b1_data2.branch_Table[1]:
        target = 6  #IM
    elif grunt.branch == b1_data2.branch_Table[2]:
        target = 6  #IN
        if (grunt.officer == False) and grunt.rank >=4:
            target -= 1
        if grunt.officer:
            target -=  1
    roll = randint(1,6) + randint(1,6)
    if roll > target:
        return False
    else:
        if (12 == roll) and (grunt.term >= 7):
            rvalue = 2
        else:
            rvalue = True

    if ((grunt.branch == b1_data2.branch_Table[0]) or (grunt.branch == b1_data2.branch_Table[1])):
        army_marine_xtraining_xfer(grunt)
    return rvalue
    
#end check_reenlist()


def first_term(grunt):
    'First term, year 1 is unique; Being nice, no survival roll first year'

    grunt.skills.append('Cbt Rifleman') # Required first skill for Army & Marines
    grunt.history.append('Term 1 Year 1')
    grunt.history.append(grunt.branch + ' ' + grunt.arm)
    grunt.history.append('Basic Training: Cbt Rifleman')
    roll = randint(0,5)
    if grunt.TL >= 12:
        roll += 1
        
    # Can't be in commando arm first term
    #Just doing IA Infantry for now
    if b4_data2.arm_Table[0] == grunt.arm:
        grunt.skills.append(b4_data2.mos_inf[roll])
        s = 'Advance Training: %s' % b4_data2.mos_inf[roll]
        grunt.history.append(s)
    elif b4_data2.arm_Table[1] == grunt.arm:  #Cavalry
        grunt.skills.append(b4_data2.mos_cav[roll])
        s = 'Advance Training: %s' % b4_data2.mos_cav[roll]
        grunt.history.append(s)
    elif b4_data2.arm_Table[2] == grunt.arm:  #Artillery
        grunt.skills.append(b4_data2.mos_art[roll])
        s = 'Advance Training: %s' % b4_data2.mos_art[roll]
        grunt.history.append(s)
    elif b4_data2.arm_Table[3] == grunt.arm:  #Support
        grunt.skills.append(b4_data2.mos_sup[roll])
        s = 'Advance Training: %s' % b4_data2.mos_sup[roll]
        grunt.history.append(s)
    
    return
#end first_term()

    
def army_year(grunt):
    'Serve 1 year in the Imperial Army'
    # Determina General assignment
    roll = randint(0,5)
        # edu bonus not optional at this point
        # if Edu >= 8, +1 to the die rolll
    if grunt.upp.edu >= 8:
        roll += 1

# bucking for command
    if grunt.officer:
        roll = roll - 1
        if roll < 0: roll = 0
    if grunt.arm == b4_data2.arm_Table[0]:
        ga = b4_data2.ga_inf[roll]
    elif grunt.arm == b4_data2.arm_Table[1]:
        ga = b4_data2.ga_cav[roll]
    elif grunt.arm == b4_data2.arm_Table[2]:
        ga = b4_data2.ga_art[roll]
    elif grunt.arm == b4_data2.arm_Table[3]:
        ga = b4_data2.ga_sup[roll]
    elif grunt.arm == b4_data2.arm_Table[4]:
        ga = b4_data2.ga_com[roll]
    else:
        print 'in army_year and we have a problem'
    
    if grunt.officer:
        s = 'General assignment is %s' % ga
        grunt.history.append(s)

    if ga == 'Special':
        b4_data2.special_assign(grunt)

    else:               # determine unit assignment
        roll = (randint(1,6) + randint(1,6)) - 2
        if grunt.branch == b1_data2.branch_Table[0]:
            if grunt.arm == b4_data2.arm_Table[0]:
                ua = b4_data2.ua_inf[roll]
            elif grunt.arm == b4_data2.arm_Table[1]:
                ua = b4_data2.ua_cav[roll]
            elif grunt.arm == b4_data2.arm_Table[2]:
                ua = b4_data2.ua_art[roll]
            elif grunt.arm == b4_data2.arm_Table[3]:
                ua = b4_data2.ua_sup[roll]
            elif grunt.arm == b4_data2.arm_Table[4]:
                ua = b4_data2.ua_com[roll]
        elif grunt.branch == b1_data2.branch_Table[1]:           #When I add Marines, need to make sure I support all arms
            if grunt.arm == b4_data2.arm_Table[0]:
                ua = b4_data2.ua_mar[roll]
            elif grunt.arm == b4_data2.arm_Table[2]:
                ua = b4_data2.ua_sup[roll]
            elif grunt.arm == b4_data2.arm_Table[3]:
                ua = b4_data2.ua_com[roll]
        
        #now resolve the year
        if (grunt.branch) == b1_data2.branch_Table[0]:
            if (grunt.arm == b4_data2.arm_Table[0]) or (grunt.arm == b4_data2.arm_Table[1]) or (grunt.arm == b4_data2.arm_Table[2]):
                b4_data2.ica_res(grunt, ua, ga)
            elif grunt.arm == b4_data2.arm_Table[3]:
                b4_data2.sup_res(grunt, ua, ga)
            elif grunt.arm == b4_data2.arm_Table[4]:
                b4_data2.com_res(grunt, ua, ga)

    if grunt.alive:
        grunt.age += 1
# end of army_year()

def army_term(grunt):
    'Work through a 4 year term in the Army'
    
    year = 1
    if (grunt.term == 1):
        first_term(grunt)  # Basic & Advanced Training, Year 1
        grunt.age += 1
        year = 2      # Start Year 2
        grunt.promote_this_term = False
        grunt.history.append('Term 1 Year 2')
        army_year(grunt)   # Year 2
        if grunt.alive:
            year = 3
            grunt.history.append('Term 1 Year 3')
            army_year(grunt)   #Year 3
        if grunt.alive:
            year = 4
            grunt.history.append('Term 1 Year 4')
            army_year(grunt)   #Year 4 end of Term 1
    else:
        promote_this_term = False
        for year in range(1,5):
            s = 'Term %d Year %d' % (grunt.term, year)
            grunt.history.append(s)
            army_year(grunt)
            if (grunt.alive == False): break

    if grunt.alive:
        grunt.term += 1
        if grunt.term >= 7:
            if 2 == check_reenlist(grunt):
                s = 'Manditory reenlistment after term %d' % grunt.term
                grunt.history.append(s)
                grunt.reenlist = True
            else:
                grunt.reenlist = False
        elif True == check_reenlist(grunt):
            grunt.reenlist = True
        else:
            grunt.reenlist = False
    else:
        s = 'Died in service to the Imperium during year %d of term %d' % (year,grunt.term)
        grunt.history.append(s)
    grunt.history.append('#####')
#end army_term()


def army_career(grunt):
    'Work through terms in the Imperial Army'
    while grunt.alive and grunt.reenlist:
        army_term(grunt)
        if grunt.age >= 34:
            check = b1_data2.age_check(grunt)
            if (False == check) and (False == grunt.alive):
                grunt.history.append('Died of natural causes, stat reduced to 0...')
    if grunt.alive:
        grunt.term -= 1  #get the final number of terms right
    b1_data2.check_upp(grunt)
    
# end of army_career()


def marine_year(grunt):
    'Serve 1 year in the Imperial Marines'
    # Determina General assignment
    roll = randint(0,5)
        # edu bonus not optional at this point
        # if Edu >= 8, +1 to the die rolll
    if grunt.upp.edu >= 8:
        roll += 1

    #bucking for command 
    if grunt.officer:
       roll = roll - 1
       if roll < 0: roll = 0
    if grunt.arm == b4_data2.arm_Table[0]:
        ga = b4_data2.ga_inf[roll]
    elif grunt.arm == b4_data2.arm_Table[1]:
        ga = b4_data2.ga_cav[roll]
    elif grunt.arm == b4_data2.arm_Table[2]:
        ga = b4_data2.ga_art[roll]
    elif grunt.arm == b4_data2.arm_Table[3]:
        ga = b4_data2.ga_sup[roll]
    elif grunt.arm == b4_data2.arm_Table[4]:
        ga = b4_data2.ga_com[roll]

    if grunt.officer:
        s = 'General assignment is %s' % ga
        grunt.history.append(s)

    if ga == 'Special':
        b4_data2.special_assign(grunt)
    else:               # determine unit assignment
        roll = (randint(1,6) + randint(1,6)) - 2
        if grunt.branch == b1_data2.branch_Table[0]:
            if grunt.arm == b4_data2.arm_Table[0]:
                ua = b4_data2.ua_inf[roll]
            elif grunt.arm == b4_data2.arm_Table[1]:
                ua = b4_data2.ua_cav[roll]
            elif grunt.arm == b4_data2.arm_Table[2]:
                ua = b4_data2.ua_art[roll]
            elif grunt.arm == b4_data2.arm_Table[3]:
                ua = b4_data2.ua_sup[roll]
            elif grunt.arm == b4_data2.arm_Table[4]:
                ua = b4_data2.ua_com[roll]
        elif grunt.branch == b1_data2.branch_Table[1]:           #When I add Marines, need to make sure I support all arms
            if grunt.arm == b4_data2.arm_Table[0]:
                ua = b4_data2.ua_mar[roll]
            elif grunt.arm == b4_data2.arm_Table[1]:
                ua = b4_data2.ua_cav[roll]
            elif grunt.arm == b4_data2.arm_Table[2]:
                ua = b4_data2.ua_sup[roll]
            elif grunt.arm == b4_data2.arm_Table[3]:
                ua = b4_data2.ua_com[roll]
            elif grunt.arm == b4_data2.arm_Table[4]:
                ua = b4_data2.ua_com[roll]
        else:
            print 'debug  error condition, ua is not set. Setting to raid'
            ua = 'Raid'

        if (grunt.branch == b1_data2.branch_Table[1]):   # i.e. a Marine
            if (grunt.arm == b4_data2.arm_Table[1]) or (grunt.arm == b4_data2.arm_Table[2]):
                b4_data2.ica_res(grunt, ua, ga)          # Cavalry or Artillery
            elif grunt.arm == b4_data2.arm_Table[3]:
                b4_data2.sup_res(grunt, ua, ga)          #Support
            elif grunt.arm == b4_data2.arm_Table[0]:    #Marine Infantry
                b4_data2.mar_res(grunt, ua, ga)
            elif (((grunt.arm == b1_data2.branch_Table[0]) and (grunt.arm == b4_data2.arm_Table[4])) or ((grunt.branch == b4_data2.arm_Table[1]) and (grunt.arm == b4_data2.arm_Table[2]))):
                b4_data2.com_res(grunt, ua, ga)    #Commando

    if grunt.alive:
        grunt.age += 1

# end of marine_year()

def marine_term(grunt):
    'Work through a 4 year term in the Marines'
    
    year = 1
    if (grunt.term == 1):
        first_term(grunt)  # Basic & Advanced Training, Year 1
        grunt.age += 1
        year = 2      # Start Year 2
        grunt.promote_this_term = False
        grunt.history.append('Term 1 Year 2')
        marine_year(grunt)   # Year 2
        if grunt.alive:
            year = 3
            grunt.history.append('Term 1 Year 3')
            marine_year(grunt)   #Year 3
        if grunt.alive:
            year = 4
            grunt.history.append('Term 1 Year 4')
            marine_year(grunt)   #Year 4 end of Term 1
    else:
        for year in range(1,5):
            s = 'Term %d Year %d' % (grunt.term, year)
            grunt.history.append(s)
            marine_year(grunt)
            if (False == grunt.alive): break

    if grunt.alive:
        grunt.term += 1
        if grunt.term >= 7:
            if 2 == check_reenlist(grunt):
                s = 'Manditory reenlistment after term %d' % grunt.term
                grunt.history.append(s)
                grunt.reenlist = True
            else:
                grunt.reenlist = False
        elif True == check_reenlist(grunt):
            grunt.reenlist = True
        else:
            grunt.reenlist = False
    else:
        s = 'Died in service to the Imperium during year %d of term %d' % (year,grunt.term)
        grunt.history.append(s)
    grunt.history.append('#####')

#end of marine_term()

def marine_career(grunt):

    while grunt.alive and grunt.reenlist:
        marine_term(grunt)
        if grunt.age >= 34:
            check = b1_data2.age_check(grunt)
            if (False == check) and (False == grunt.alive):
                grunt.history.append('Died of natural causes, stat reduced to 0...')
    if grunt.alive:
        grunt.term -= 1  #get the final number of terms right
    b1_data2.check_upp(grunt)
# end of marine_career()

  

def navy_term(grunt):
    'Work through a 4 year term in the Imperial Navy'

    year = 1
    if (grunt.term == 1):
        if b5_data.navy_year_one(grunt):
            grunt.term += 1
            return True  #Completed College or the Academy in four years
        else:
            if grunt.college_fail == True:
                year += 1   #Didn't complete college 
                grunt.history.append('Finish 3 years of term')
            if grunt.academy_fail == True:
                year += 1   #Didn't complete the Academy
                grunt.history.append('Finish 3 years of term')
            
    if grunt.term == 2 and grunt.honors:
        #Medical school or flight school
        if b5_data.navy_med_or_flight(grunt):
            if grunt.medschool:
                grunt.term += 1
                return True   #completed four year term
            if grunt.flight:
                grunt.history.append('Finish 3 years of term')
                year += 1
        if grunt.flight_fail or grunt.med_fail:
            year += 1  #failing flight or medical school takes a year

    if grunt.navalBranch == False:
        b5_data.select_navy_branch(grunt)

    if grunt.bat == False:
        s = 'Basic & Advanced Training in year %d of term %d' % (year, grunt.term)
        grunt.history.append(s)
        b5_data.navy_bat(grunt)
        year += 1
    
    #complete the term
    while year <= 4 and grunt.alive:
        s = 'Term %d Year %d' % (grunt.term, year)
        grunt.history.append(s)
        b5_data.navy_year(grunt, year)
        year += 1
                    
    if grunt.alive:
        grunt.term += 1
        
        if grunt.term >= 7:
            if 2 == check_reenlist(grunt):  
                s = 'Manditory reenlistment after term %d' % grunt.term
                grunt.history.append(s)
                grunt.reenlist = True
            else:
                grunt.reenlist = False
        elif True == check_reenlist(grunt):
            grunt.reenlist = True
        else:
            grunt.reenlist = False
    else:
        s = 'Died in service to the Imperium during year %d of term %d' % (year,grunt.term)
        grunt.history.append(s)
    grunt.history.append('#####')
    return True

# end of navy_term()


def navy_career(grunt):
    'Work through a career in the Imperial Navy'
    # SubSector and planetary navies come later

    grunt.TL = 15   #Imperial Navy TL is F
    while grunt.alive and grunt.reenlist:
        navy_term(grunt)
        if grunt.age >= 34:
            check = b1_data2.age_check(grunt)
            if (False == check) and (False == grunt.alive):
                grunt.history.append('Died of natural causes, stat reduced to 0...')
    if grunt.alive:
        grunt.term -= 1  #get the final number of terms right
    b1_data2.check_upp(grunt)
# end of navy_career()


def display_noble_rank(grunt):
    'Display the nobla rank, from Knight to Duke'
#Keep soc maxed at 15 for now

    if grunt.upp.soc > 15:
        grunt.upp.soc = 15
    if grunt.upp.soc < 11: return False #error condition

    t = b1_data2.noble_table[grunt.upp.soc - 11]
    t2 = 'Noble Title: '
    s = t2 + t 
    print s
    return True
#end of display_noble_rank

def print_upp(char):
    'Print the UPP to the screen'
    print( '%x%x%x%x%x%x' % (char.upp.str, char.upp.dex, char.upp.end, char.upp.int, char.upp.edu, char.upp.soc))

def print_init_upp(char):
    'Print the UPP to the screen'
    print( '%x%x%x%x%x%x' % (char.init_upp.str, char.init_upp.dex, char.init_upp.end, char.init_upp.int, char.init_upp.edu, char.init_upp.soc))

def print_history(char):
    #print out the character history
    print 'Character Generation History:'
    for item in char.history:
        print item

def print_Char_Data(grunt):

    print 'created %s' % grunt.dateTimeCreated
    print_upp(grunt)
    print 'Age: ', grunt.age
    print 'terms served: ',grunt.term
    display_noble_rank(grunt)
    if grunt.college and grunt.honors:
        print 'Graduated College with honors'
    elif grunt.college:
        print 'Granduated College'
    if grunt.notc:
        print 'Navy Officer Training Corps'
    if grunt.academy and grunt.honors:
        print 'Graduated Naval Academy with honors'
    elif grunt.academy:
        print 'Graduated Naval Academy'
    print '%s %s' % (grunt.branch, grunt.arm)
    if grunt.branch == b1_data2.branch_Table[2]:
        b5_data.display_b5_rank(grunt)
    else:
        b4_data2.display_b4_rank(grunt)
    print 'Cr: ', grunt.cash
    if grunt.alive == False:
        print 'DEAD!!!!!!!!!!!!!!!!'
    if grunt.xtrained:
        grunt.xtrained.sort()
        print 'Cross Trained in:'
        for item in grunt.xtrained:
            print item
    if grunt.schools:
        grunt.schools.sort()
        print 'Schools attended:'
        for item in grunt.schools:
            print item
    if grunt.specials:
        grunt.specials.sort()
        print 'Special Assigments:'
        for item in grunt.specials:
            print item
    if grunt.ribbons:
        grunt.ribbons.sort()
        print 'Ribbons:'
        for item in grunt.ribbons:
            print item
    if grunt.decorations:
        grunt.decorations.sort()
        print 'Decorations:'
        for item in grunt.decorations:
            print item
    print 'Skills:'
    grunt.skills.sort()
    for item in grunt.skills:
        print item

    if grunt.muster_cash:
        print 'Muster out Cash: '
        grunt.muster_cash.sort()
        total_mc = 0
        for item in grunt.muster_cash:
            total_mc += item
        print 'Cr%d' % total_mc
    
    if grunt.muster_loot:
        print 'Mustered out with:'
        grunt.muster_loot.sort()
        for item in grunt.muster_loot:
            print item
    if grunt.r_pay > 0:
        print 'Annual retirement pay: Cr', grunt.r_pay
#end print_Char_data

def looper(loop):
    alive = 0
    dead = 0
    officer = 0
    alive_Officer = 0

    count = 0
    for i in range(loop):
        b4g = B4Char()
        army_career(b4g)
        if b4g.alive:
           b4_data2.muster_out(b4g)
           alive += 1
           if b4g.officer:
               alive_Officer += 1
        else:
            dead += 1
        if b4g.officer:
            officer += 1

    print 'alive = ', alive
    print 'dead = ', dead
    print 'officer = ', officer
    print 'Alive Officer = ', alive_Officer
#end of looper

def write_csv(grunt):
    'capture data to a csv file for analysis'

# alive, age, officer, rank, upp

#end write_csv

def looper2(loop):
    
    outfile = open('random_chars.csv', 'a')
    count = 0
    for i in range(loop):
        b4g = B4Char()
        army_career(b4g)
        if b4g.alive:
           b4_data2.muster_out(b4g)
           s = 'Alive, '
        else:
            s = 'Dead, '
        s = s + ('%d, ' % b4g.age)
        if b4g.officer:
            s = s + 'Officer, ' +  b4_data2.orank[b4g.rank]
        else:
            s = s + 'Enlisted, ' + b4_data2.erank[mb4g.rank]
        s = s + (', %d ' % b4g.term)
        #print s
        sprint.sprint(False, s,outfile)
    outfile.close()
#end of looper2

def read_config(grunt):
    'Read in a config file'

    #Set the UPP, Branch and Arm
    line = 'fail'
    infile = open('uppba.txt', 'r')
    line = infile.readline()

    if line[0] != '?':    
        grunt.upp.str = int(line[0])
    if line[1] != '?':
        grunt.upp.dex = int(line[1])
    if line[2] != '?':
        grunt.upp.end = int(line[2])
    if line[3] != '?':
        grunt.upp.int = int(line[3])
    if line[4] != '?':
        grunt.upp.edu = int(line[4])
    if line[5] != '?':
        grunt.upp.soc = int(line[5])

    if 'M' == line[6]:
        grunt.branch = b1_data2.branch_Table[1]  # Imperial Marines
    elif 'A' == line[6]:
        grunt.branch = b1_data2.branch_Table[0]  # Imperial Army
    elif 'N' == line[6]:
        grunt.branch = b1_data2.branch_Table[2]  # Imperial Navy

    if grunt.branch == b1_data2.branch_Table[1] or grunt.branch == b1_data2.branch_Table[0]:
        if 'I' == line[7]:
            grunt.arm = b4_data2.arm_Table[0]   #set arm to Infantry
        elif 'C' == line[7]:
            grunt.arm = b4_data2.arm_Table[1]   #set arm to Cavalry
        elif 'I' == line[7]:
            grunt.arm = b4_data2.arm_Table[2]   #set arm to artillery
        elif 'S' == line[7]:
            grunt.arm = b4_data2.arm_Table[3]   #set arm to Support'
        elif 'X' == line[7]:
            grunt.arm = b4_data2.arm_Table[4]   #set arm to Commando
    else:
        grunt.branch = b5_data.arm_enlisted_Table[0]  #Imperial Navy.  Set up later

    #print 'read in %s' % line

# end of read_config

def single_Char():
    print '********************'
    b4g = B4Char()   #Initialize the character

    #check for init file & use it
    read_config(b4g)

    
    print 'starting upp: '
    print_init_upp(b4g)
    b4g.dateTimeCreated=time.asctime()  #Stick in a time/date stamp

    #Sb4g.arm = b4_data2.arm_Table[4]   #debug - set arm to Commando

    if b4g.branch == b1_data2.branch_Table[0]:
        army_career(b4g)
    elif b4g.branch == b1_data2.branch_Table[1]:
        marine_career(b4g)
    elif b4g.branch == b1_data2.branch_Table[2]:
        navy_career(b4g)

    if b4g.alive:  
        if b4g.branch == b1_data2.branch_Table[0] or b4g.branch == b1_data2.branch_Table[1]:
            b1_data2.muster_out(b4g)
        else:
            b4_data2.muster_out(b4g)
            
    print_history(b4g)
    print '+++++'
    print_Char_Data(b4g)
#end of single_char

# Start of main code execution   

single_Char()

#looper(100)

#looper2(20)


# Then the final character data, including the final UPP, any noble title, schools, etc.

