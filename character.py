# 15 April 2015 - Fixed defect in printing intial stats
# June 2015 - MU - Added add_skill() to B4Char
# July 2026 - MU - Massive update - A lot of bug fixes

import time
import random
from dice import *
from arm_data import *
import muster
import career

def generate_book4(filename=None, noKill=True):
    """Convenience function for Book 4 only"""
    grunt = B4Char()
    grunt.noKill = noKill
    if filename:
        grunt.load(filename)
    grunt.career()
    grunt.muster_out()#removed 06 June 2026
    return grunt


class B4Char(object):
    def __init__(self):
        self.upp = self.init_upp = upp()
        self.age = 18
        self.race = 'Human'
        self.raceSubType = 'Mixed'
        self.hpName = 'Sylea'
        self.noKill = False
        self.musOut = False
        self.hpTL = 12
        self.TL = 12            # This is the default for Imperial Military
        self.skills = dict()
        self.schools = []
        #self.xTrained = []     #removed 06 June 2026
        self.branch = 'Imperial Army'
        self.arm = 'Infantry'
        self.xtrained = []
        #self.specials = []     #removed 06 June 2026
        self.officer = False
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

        # Navy education flags
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
        #self.navalBranch = 'Line'          # set default to Line removed 04 June 2026. Just use .arm
        self.bat = False                # bat stands for Basic and Advanced Training

        self.dateTimeCreated = time.asctime()

    def is_army(self):
        return self.branch == 'Imperial Army'

    def is_marine(self):
        return self.branch == 'Imperial Marines'

    def is_navy(self):
        return self.branch == 'Imperial Navy'

    def is_dead(self):
        return not self.alive

    def die(self):
        """Mark character as dead and record the event."""
        if not self.alive:
            return
        self.alive = False
        self.history.append(f'Died at age {self.age} after {self.term} terms')

    def arm_entry(self, special_marine_infantry=True):
        """Return the correct arm table for the current branch/arm."""
        if self.branch == 'Imperial Navy':
            return None
        elif special_marine_infantry and self.branch == 'Imperial Marines' and self.arm == 'Infantry':
            return marine_Table
        else:
            return arm_Table.get(self.arm)

    def military_rank(self):
        """Return correct rank string for the current branch"""
        if self.is_navy():
            if self.officer:
                officer_ranks = ('Ensign', 'Sublieutenant', 'Lieutenant', 'Lieutenant Commander',
                                 'Commander', 'Captain', 'Commodore', 'Fleet Admiral',
                                 'Sector Admiral', 'Grand Admiral')
                return officer_ranks[self.rank] if self.rank < len(officer_ranks) else 'Grand Admiral'
            else:
                enlisted_ranks = ('Spacehand Recruit', 'Spacehand Apprentice', 'Able Spacehand',
                                  'Petty Officer Third Class', 'Petty Officer Second Class',
                                  'Petty Officer First Class', 'Chief Petty Officer',
                                  'Senior Chief Petty Officer', 'Master Chief Petty Officer')
                return enlisted_ranks[self.rank] if self.rank < len(enlisted_ranks) else 'Master Chief Petty Officer'
        else:
            # Army / Marines (Book 4 ranks)
            if self.officer:
                officer_ranks = ('2nd Lt', '1st Lt', 'Captain', 'Major', 'Lt Colonel',
                                 'Colonel', 'Brig Gen', 'Maj Gen', 'Lt Gen', 'General')
                return officer_ranks[self.rank] if self.rank < len(officer_ranks) else 'General'
            else:
                enlisted_ranks = ('Private', 'Lance Cpl', 'Cpl', 'Lance Sgt', 'Sergeant',
                                  'Gunnery Sgt', 'Leading Sgt', '1st Sgt', 'Sgt Major')
                return enlisted_ranks[self.rank] if self.rank < len(enlisted_ranks) else 'Sgt Major'

    def apply_skill(self, skill, by_age=False):
        """Apply a skill or stat increase (e.g. '+1 int')."""
        if skill is None or (isinstance(skill, str) and not skill.strip()):
            # print("DEBUG - hit skill = None in character.py apply_skill")
            # self.history.append("DEBUG - hit skill = None in character.py apply_skill")
            return

        # print("DEBUG: Using apply_skill\n")  # keep commented unless debugging

        if isinstance(skill, str) and '+' in skill:
            bits = skill.split()
            if len(bits) >= 2:
                try:
                    adj = int(bits[0])
                    stat = bits[1].lower()
                    self.stat_change(stat, adj, by_age)
                except:
                    pass
        else:
            from skills import record
            record(self, skill)


    def stat_change(self, statname, adjustment, by_age=False):
        """Safely adjust a UPP stat with bounds checking."""
        statname = statname.lower()
        
        if statname == "str":
            self.upp.str = max(1, min(15, self.upp.str + adjustment))
        elif statname == "dex":
            self.upp.dex = max(1, min(15, self.upp.dex + adjustment))
        elif statname == "end":
            self.upp.end = max(1, min(15, self.upp.end + adjustment))
        elif statname == "int":
            self.upp.int = max(1, min(15, self.upp.int + adjustment))
        elif statname == "edu":
            self.upp.edu = max(1, min(15, self.upp.edu + adjustment))
        elif statname == "soc":
            self.upp.soc = max(1, min(15, self.upp.soc + adjustment))


    def career(self):
        """Dispatch to the correct career path"""
        # leaving this because it might come in hand for Scouts & Merchants
        if self.is_navy():
            self.arm = 'Line'               # added 04 June 2026
            return career.career(self)      # Full Navy career
        else:
            return career.career(self)      # Full Army/Marine career (via dispatcher)

    def muster_out(self):
        return muster.muster_out(self)


class upp(object):
    def __init__(self):
        self.str = dice(qty=2)
        self.dex = dice(qty=2)
        self.end = dice(qty=2)
        self.int = dice(qty=2)
        self.edu = dice(qty=2)
        self.soc = dice(qty=2)

    def adjust(self, statname, adjustment):
        if statname == "str": self.str += adjustment
        elif statname == "dex": self.dex += adjustment
        elif statname == "end": self.end += adjustment
        elif statname == "int": self.int += adjustment
        elif statname == "edu": self.edu += adjustment
        elif statname == "soc": self.soc += adjustment

    def check(self):
        for attr in ['str', 'dex', 'end', 'int', 'edu', 'soc']:
            val = getattr(self, attr)
            if val > 15:
                setattr(self, attr, 15)
            if val < 1:
                setattr(self, attr, 1)

