# muster.py
# Unified Muster Out for Books 4 and 5

"""
    1 roll per term of service
	1 additional roll if rank O1 or O2
	2 additional rolls if rank O3 or O4
	3 additional rolls if ranks O5 or O6

	If rank O5 or O6 +1 on benefits/muster table
	If Gambling Skill 1 or more, + gambling level on cash tables

	If only one muster roll, take from cash table
	If more than one, first comes from the cash table
	Additional rolls, randomly select either cash or benefits/muster table
	Cash table rolls are limited to a maximum of three rolls.
"""

from dice import *
import random

# Book 4
army_cash_table = [2000, 5000, 10000, 10000, 10000, 20000, 30000]
marine_cash_table = [2000, 5000, 5000, 10000, 20000, 30000, 40000]
army_muster_table = ['Low Psg', '+1 int', '+2 edu', 'Gun', 'High Psg', 'Mid Psg', '+1 soc']
marine_muster_table = ['Low Psg', '+2 int', '+1 edu', 'Blade', 'Travellers', 'High Psg', '+2 soc']

# Book 5 Navy
navy_cash_table = [1000, 5000, 5000, 10000, 20000, 50000, 50000]
navy_muster_table = ['Low Psg', '+1 int', '+2 edu', 'Blade', 'Travellers', 'High Psg', '+2 soc']


def muster_out_rolls(grunt):
    """Calculate number of muster out rolls.
    Only actual Navy service terms count. Education time does NOT count as terms."""
    grunt.muster_rolls = grunt.term   # Pure service terms only

    # Rank bonuses (still fully apply)
    if grunt.officer:
        if grunt.rank < 3:        # O1 / O2
            grunt.muster_rolls += 1
        elif grunt.rank <= 4:     # O3 / O4
            grunt.muster_rolls += 2
        else:                     # O5+
            grunt.muster_rolls += 3


def retirement_pay(grunt):
    """Calculate retirement pension."""
    if grunt.term == 5:
        grunt.r_pay = 4000
    elif grunt.term == 6:
        grunt.r_pay = 6000
    elif grunt.term == 7:
        grunt.r_pay = 8000
    elif grunt.term >= 8:
        grunt.r_pay = 10000 + (grunt.term - 8) * 2000
        
        
def apply_navy_muster_benefit(grunt, benefit):
    """Apply Navy muster benefit safely - passages are loot, not skills."""
    if not isinstance(benefit, str):
        return

    # Material / Passage benefits - do NOT go into skills
    if benefit in ['Low Psg', 'Mid Psg', 'High Psg', 'Travellers']:
        grunt.muster_loot.append(benefit)
        grunt.history.append(f"Muster Benefit: {benefit}")
        return

    # Stat bonuses
    if benefit.startswith('+'):
        try:
            parts = benefit.split()
            val = int(parts[0])
            stat = parts[1].lower()
            grunt.stat_change(stat, val)
            grunt.history.append(f"Muster Benefit: {benefit}")
        except:
            grunt.history.append(f"Muster Benefit: {benefit} (applied)")
        return

    # Normal skills
    grunt.apply_skill(benefit)
    grunt.history.append(f"Muster Benefit: {benefit}")
        
def apply_armymarine_muster_benefit(grunt, roll):
    """Apply Army or Marine muster-out benefits correctly."""
    if grunt.is_army():
        benefit_table = army_muster_table
    elif grunt.is_marine():
        benefit_table = marine_muster_table
    else:
        grunt.history.append(f"ERROR: apply_armymarine_muster_benefit called on non-Army/Marine ({grunt.branch})")
        return

    benefit = benefit_table[roll]

    if benefit in ['Low Psg', 'High Psg', 'Mid Psg', 'Travellers', 'Blade', 'Gun']:
        grunt.muster_loot.append(benefit)
        grunt.history.append(f'Muster Benefit: {benefit}')
    elif benefit == '+1 int':
        grunt.stat_change("int", 1)
    elif benefit in ('+2 edu', '+1 edu'):
        adj = 2 if '+2 edu' in benefit else 1
        grunt.stat_change("edu", adj)
    elif benefit in ('+1 soc', '+2 soc'):
        adj = 1 if '+1 soc' in benefit else 2
        grunt.stat_change("soc", adj)
    else:
        grunt.history.append(f'Muster Benefit: {benefit}')

def muster_out(grunt):
    """Unified muster out with correct cash/benefit separation"""
    if grunt.is_dead():
        return

    muster_out_rolls(grunt)
    if grunt.term >= 5:
        retirement_pay(grunt)

    total_rolls = max(getattr(grunt, 'muster_rolls', 1), 1)
    cash = 0
    grunt.muster_cash = []
    grunt.muster_loot = []

    # First roll is always cash
    roll = dice() + grunt.skills.get('Gambling', 0)
    roll = min(roll, 7) - 1

    if grunt.branch == 'Imperial Navy':
        cash_amount = navy_cash_table[roll]
    else:
        cash_amount = army_cash_table[roll] if grunt.is_army() else marine_cash_table[roll]

    cash += cash_amount
    grunt.muster_cash.append(cash_amount)
    grunt.history.append(f"Muster Cash: Cr{cash_amount:,}")

    # Remaining rolls: 50/50 cash or benefit (max 3 cash total)
    cash_rolls = 1
    for _ in range(total_rolls - 1):
        if cash_rolls < 3 and random.random() < 0.5:
            # Cash roll
            roll = dice() + grunt.skills.get('Gambling', 0)
            roll = min(roll, 7) - 1
            if grunt.branch == 'Imperial Navy':
                cash_amount = navy_cash_table[roll]
            else:
                cash_amount = army_cash_table[roll] if grunt.is_army() else marine_cash_table[roll]
            cash += cash_amount
            grunt.muster_cash.append(cash_amount)
            grunt.history.append(f"Muster Cash: Cr{cash_amount:,}")
            cash_rolls += 1
        else:
            # Benefit roll
            roll = dice() + (1 if grunt.rank >= 5 else 0)
            roll = min(roll, 7) - 1
            if grunt.branch == 'Imperial Navy':
                benefit = navy_muster_table[roll]
                apply_navy_muster_benefit(grunt, benefit)
            else:
                benefit = army_muster_table[roll] if grunt.is_army() else marine_muster_table[roll]
                grunt.muster_loot.append(benefit)
                grunt.history.append(f"Muster Benefit: {benefit}")

    grunt.cash = cash

    if grunt.branch == 'Imperial Navy':
        grunt.history.append('Imperial Navy Muster Out completed')
    else:
        grunt.history.append(f'{grunt.branch} Muster Out completed')




