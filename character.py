# 15 April 2015 - Fixed defect in printing intial stats
# June 2015 - MU - Added add_skill() to B4Char

import time
from dice import *
from arm_data import *
import b5_data       #unique book 5 data
import career, muster

def generate(filename=None):
    grunt = B4Char()
    if filename!=None:
        grunt.load_file(filename)
    else:
        grunt.load_char('Marines','Infantry')
    grunt.career()
    grunt.muster_out()
    return grunt

def generate_multi(num_characters, *args, **kwargs):
    charlist = []
    for i in range(num_characters):
        grunt = generate(*args, **kwargs)
        charlist.append(grunt)
    return charlist


enlisted_ranks = ('Private', 'Lance Corporal', 'Corporal', 'Lance Sergeant', \
                  'Sergeant','Gunnery Sergeant', 'Leading Sergeant',\
                  'First Sergeant', 'Sergeant Major')
officer_ranks = ('Second Lieutenant', 'First Lieutenant', 'Captain', 'Major',\
                 'Lieutenant Colonel', 'Colonel', 'Brigadier General',\
                 'Major General','Lieutenant General', 'General')

noble_ranks = ('Knight', 'Baron', 'Marquis', 'Count', 'Duke')


age_bands = [
  {
    "range":{"lower":34, "upper": 46},
    "changes":{
      "str":{"roll": 8, "adj":-1},
      "dex":{"roll": 7, "adj":-1},
      "end":{"roll": 7, "adj":-1}
    }
  },
  {
    "range":{"lower":50, "upper":62},
    "changes":{
      "str":{"roll":9, "adj":-1},
      "dex":{"roll":8, "adj":-1},
      "end":{"roll":9, "adj":-1},
    }
  },
  {
    "range":{"lower":66, "upper":9999},
    "changes":{
      "str":{"roll":9, "adj":-2},
      "dex":{"roll":9, "adj":-2},
      "end":{"roll":9, "adj":-2},
      "int":{"roll":9, "adj":-2},
    }
  },
]

class InvalidStatName(Exception):
    def __init__(self, statkey, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)
        self.statkey = statkey
    def __str__(self):
        return "InvalidStatName(%s)" % self.statkey

class upp(object):
    def __init__(self):
        self.str = dice(qty=2)
        self.dex = dice(qty=2)
        self.end = dice(qty=2)
        self.int = dice(qty=2)
        self.edu = dice(qty=2)
        self.soc = dice(qty=2)
        self.o_str = self.str
        self.o_dex = self.dex
        self.o_end = self.end
        self.o_int = self.int
        self.o_edu = self.edu
        self.o_soc = self.soc
    def get(self, statname):
        lname = statname.lower()
        if   lname =="str": return self.str
        elif lname =="dex": return self.dex
        elif lname =="end": return self.end
        elif lname =="int": return self.int
        elif lname =="edu": return self.edu
        elif lname =="soc": return self.soc
        else: raise InvalidStatName(statname)
    def set(self, statname, newvalue):
        lname = statname.lower()
        if   lname=="str": self.str = newvalue
        elif lname=="dex": self.dex = newvalue
        elif lname=="end": self.end = newvalue
        elif lname=="int": self.int = newvalue
        elif lname=="edu": self.edu = newvalue
        elif lname=="soc": self.soc = newvalue
        else: raise InvalidStatName(statname)
    def adjust(self, statname, adjustment):
        self.set(statname, self.get(statname) + adjustment)
    def check(self):
        'Capping attributes at F'
        for statname in ["str", "dex", "end", "int", "edu", "soc"]:
            if self.get(statname)>15:
                self.set(statname, 15)
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
                self.skills=dict()
                self.schools=[]
                self.xTrained=[]
                self.branch = 'Imperial Army'  #IA by default
                self.arm = 'Infantry' #Infantry by default
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
                self.natural_death = True
                self.dateTimeCreated = time.asctime()  #Stick in a time/date stamp

        def is_army(self):
            return self.branch=='Imperial Army'
        def is_marine(self):
            return self.branch=='Imperial Marines'
        def is_navy(self):
            return self.branch=='Imperial Navy'

        def die(self,year):
            self.alive = False
            if self.natural_death:
                s = 'Died of natural causes (stat reduced to 0) during term %d' % (self.term)
            else:
                s = 'Died in service to the Imperium during term %d year %d' % (self.term,year)
            self.history.append(s)

        def stat_change(self, statname, adjustment, by_age=False):
            if adjustment==0: return
            self.upp.adjust(statname, adjustment)
            change = "reduced"
            if adjustment > 0: change = "increased"
            because = ""
            if by_age:
                because = " at age %d" % self.age
            self.history.append("%s %s by %d%s" % (statname.capitalize(), change, abs(adjustment), because))
            if self.upp.get(statname)<=0:
                self.die(natural=True)

        def apply_skill(self, skill, by_age=False):
            "Apply a skill string such as '+1 int'"
            
            skill = str(skill)
            bits = skill.split()

            if len(bits) < 2: 
                return
            try:
                adjustment = int(bits[0])
                stat = bits[1].lower()
               
                self.stat_change(stat, adjustment, by_age)
            except ValueError:
                pass
            except InvalidStatName:
                pass

        def add_skill(self,skill):
            'add a skill to the skill dict except stat changes'
            #added June 4, 2015 MU
            
            self.history.append(skill)
            if '+' not in skill:
                self.skills[skill] = self.skills.get(skill,0) + 1
            else:
                self.apply_skill(skill)
            return
        #end of add_skill
            
            
        def is_dead(self):
            return not self.alive

	def age_check(self):
	    'Perform the age check.'
	    if self.is_dead():  #already dead, don't bother
	        return False
	    for band in age_bands:
	        if band["range"]["lower"] <= self.age <= band["range"]["upper"]:
	            for stat, change in band["changes"].items():
	                if dice(qty=2) < change["roll"]:
	                    self.stat_change(stat, change["adj"], by_age=True)
                            if self.is_dead():
                                return False
	            break
	    return True

        def arm_entry(self, special_marine_infantry=True):
            if self.branch=='Imperial Navy':
                return None
            elif special_marine_infantry and (self.branch=='Imperial Marines') and (self.arm=='Infantry'):
                return marine_Table
            else:
                return arm_Table[self.arm]

        def noble_rank(self):
            self.upp.check()
            offset = 15 - len(noble_ranks)
            if self.upp.soc <= offset: return None #error condition

            t = noble_ranks[self.upp.soc - offset - 1]
            return t

        def military_rank(self):
            if self.officer:
                if (self.branch=='Imperial Marines') and (self.rank == 3):
                    return 'Force Commander'
                else:
                    return officer_ranks[self.rank]
            else:
                return enlisted_ranks[self.rank]
            
        def load_file(self, filename):
            'Read in upp, branch, and arm from a file.  It probably only makes sense to do this at the start.'

            try:
                infile = open(filename, 'r')
                line = infile.readline()
            except:
                #use default of Imperial Army Infantry and random UPP
                self.branch = 'Imperial Army'
                self.arm = 'Infantry'
                return True
            if len(line)<8:
                return False # line too short

            if line[0] != '?':    
                self.upp.str = int(line[0])
            if line[1] != '?':
                self.upp.dex = int(line[1])
            if line[2] != '?':
                self.upp.end = int(line[2])
            if line[3] != '?':
                self.upp.int = int(line[3])
            if line[4] != '?':
                self.upp.edu = int(line[4])
            if line[5] != '?':
                self.upp.soc = int(line[5])

            if 'M' == line[6]:
                self.branch = 'Imperial Marines'  # Imperial Marines
            elif 'A' == line[6]:
                self.branch = 'Imperial Army'  # Imperial Army
            elif 'N' == line[6]:
                self.branch = 'Imperial Navy'  # Imperial Navy

            if self.branch == 'Imperial Marines' or self.branch == 'Imperial Army':
                if 'I' == line[7]:
                    self.arm = 'Infantry'   #set arm to Infantry
                elif 'C' == line[7]:
                    self.arm = 'Cavalry'   #set arm to Cavalry
                elif 'I' == line[7]:
                    self.arm = 'Artillery'   #set arm to artillery  #Not valid for Marines to start in
                elif 'S' == line[7]:
                    self.arm = 'Support'   #set arm to Support'   #Not valid for Marines to start in
                elif 'X' == line[7]:
                    self.arm = 'Commando'   #set arm to Commando   #currently for testing only, can't start in Commandos
            else:
                if 'L' == line[7]:
                    self.arm = b5_data.navy_branch[0]  #Imperial Navy.  Set up later
                elif 'F' == line[7]:
                    self.arm = b5_data.navy_branch[1]
                elif 'G' == line[7]:
                    self.arm = b5_data.navy_branch[2]
                elif 'E' == line[7]:
                    self.arm = b5_data.navy_branch[3]
                elif 'M' == line[7]:
                    self.arm = b5_data.navy_branch[4]
                elif 'T' == line[7]:
                    self.arm = b5_data.navy_branch[5]
                else:
                    print 'error reading Navy branch'
            #print 'read in %s' % line
            return True
            
        def load_char(self, branch, arm):
            'branch, and arm as command line options'

            #use default of Imperial Army Infantry and random UPP
            if not branch:
                self.branch = 'Imperial Army'
            if not arm:
                self.arm = 'Infantry'

            if 'navy' in branch.lower():
                self.branch = 'Imperial Navy'
            elif 'marines' in branch.lower():
                self.branch = 'Imperial Marines'
            else:
                self.branch = 'Imperial Army'


            if self.branch == 'Imperial Marines' or self.branch == 'Imperial Army':
                if 'COMMANDO' in arm.upper():
                    self.arm = 'Commando'   #set arm to Commando   #currently for testing only, can't start in Commandos
                elif 'CAV' in arm.upper():
                    self.arm = 'Cavalry'   #set arm to Cavalry
                elif 'ART' in arm.upper():
                    self.arm = 'Artillery'   #set arm to artillery  #Not valid for Marines to start in
                elif 'SUPP' in arm.upper():
                    self.arm = 'Support'   #set arm to Support'   #Not valid for Marines to start in
                else:
                    self.arm = 'Infantry'  
            else:
                if 'T' in arm.upper():
                    self.arm = b5_data.navy_branch[5]  
                elif 'F' in arm.upper():
                    self.arm = b5_data.navy_branch[1]
                elif 'G' in arm.upper():
                    self.arm = b5_data.navy_branch[2]
                elif 'E' in arm.upper():
                    self.arm = b5_data.navy_branch[3]
                elif 'M' in arm.upper():
                    self.arm = b5_data.navy_branch[4]
                else:
                    self.arm = b5_data.navy_branch[0] #Line 
            #print 'read in %s' % line
            return True
        
        def career(self):
            return career.career(self)
        
        def muster_out(self):
            return muster.muster_out(self)


# End of B4Char
