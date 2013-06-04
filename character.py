from dice import *
from arm_data import *
import b1_data2      #unique book 1 data
import b4_data2      #unique book 4 data
import b5_data       #unique book 5 data

enlisted_ranks = ['Private', 'Lance Corporal', 'Corporal', 'Lance Sergeant', 'Sergeant', 'Gunnery Sergeant', 'Leading Sergeant', 'First Sergeant', 'Sergeant Major']
officer_ranks = ['Second Lieutenant', 'First Lieutenant', 'Captain', 'Major', 'Lieutenant Colonel', 'Colonel', 'Brigadier General', 'Major General', 'Lieutenant General', 'General']

noble_ranks = ['Knight', 'Baron', 'Marquis', 'Count', 'Duke']


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
    pass

class upp(object):
    def __init__(self):
        self.str = dice(qty=2)
        self.dex = dice(qty=2)
        self.end = dice(qty=2)
        self.int = dice(qty=2)
        self.edu = dice(qty=2)
        self.soc = dice(qty=2)
    def get(self, statname):
        lname = statname.lower()
        if   statname=="str": return self.str
        elif statname=="dex": return self.dex
        elif statname=="end": return self.end
        elif statname=="int": return self.int
        elif statname=="edu": return self.edu
        elif statname=="soc": return self.soc
        else: raise InvalidStatName()
    def set(self, statname, newvalue):
        lname = statname.lower()
        if   statname=="str": self.str = newvalue
        elif statname=="dex": self.dex = newvalue
        elif statname=="end": self.end = newvalue
        elif statname=="int": self.int = newvalue
        elif statname=="edu": self.edu = newvalue
        elif statname=="soc": self.soc = newvalue
        else: raise InvalidStatName()
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
                self.skills=[]
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
                self.dateTimeCreated = 'Fake Time'              

        def is_army(self):
            return self.branch=='Imperial Army'
        def is_marine(self):
            return self.branch=='Imperial Marines'
        def is_navy(self):
            return self.branch=='Imperial Navy'

        def die(self, year=None, natural=False):
            self.alive = False
            if natural:
                s = 'Died of natural causes (stat reduced to 0)'
            else:
                s = 'Died in service to the Imperium during year %d of term %d' % (year,self.term)
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
            bits = skill.split()
            if len(bits)<2: return
            try:
                adjustment = int(bits[0])
                stat = bits[1].lower()
                
                self.stat_change(stat, adjustment, by_age)
            except ValueError:
                pass

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



# End of B4Char
