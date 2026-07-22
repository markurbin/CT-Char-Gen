# career_navy.py
# Book 5 - Imperial Navy Career Logic
# Clean term handling respecting education rules
'''
General statement: Stop relying on flags to set age after events. 
Just increment age as the events happen. For example, 
Naval Academy pass/fail & Flight/Medical School
'''

import b5_data
import career

def navy_term(grunt):
    """Work through a term in the Imperial Navy (Book 5)"""
    
    if grunt.term == 1:
        # Handle ALL pre-enlistment education + aging
        years_aged = b5_data.navy_year_one(grunt)
        grunt.age += years_aged 

        # Determine if this is a short 3-year first term
        short_term = (getattr(grunt, 'flight', False) or 
                      getattr(grunt, 'academy_fail', False) or
                      getattr(grunt, 'med_fail', False) or
                      getattr(grunt, 'college_fail', False))

        if short_term:
            b5_data.navy_short_term_one(grunt)
        else:
            # Normal 4-year term
            # Year 1: BAT only (no navy_year call)
            grunt.history.append('Term 1 Year 1')
            if getattr(grunt, 'needs_officer_bat', False):
                b5_data.navy_officer_bat(grunt)
                grunt.needs_officer_bat = False
            elif (not getattr(grunt, 'bat', False) and 
                  not getattr(grunt, 'flight', False) and
                  not getattr(grunt, 'officer', False)):
                b5_data.navy_bat(grunt)
                grunt.bat = True
            else:
                b5_data.navy_year(grunt, 1)

            if grunt.alive:
                grunt.age += 1

            # Years 2-4: Normal navy_year calls ONLY
            for year in range(2, 5):
                if not grunt.alive:
                    break
                grunt.history.append(f'Term 1 Year {year}')
                b5_data.navy_year(grunt, year)
                if grunt.alive:
                    grunt.age += 1
                if not grunt.alive or getattr(grunt, 'musOut', False):
                    break
    else:
        # Normal term (Term 2+)
        max_years = 4
        start_year = 1
        for year in range(start_year, max_years + 1):
            if not grunt.alive:
                break
            grunt.history.append(f'Term {grunt.term} Year {year}')
            b5_data.navy_year(grunt, year)
            if grunt.alive:
                grunt.age += 1
            if not grunt.alive or getattr(grunt, 'musOut', False):
                break

    # ====================== END OF TERM ======================
    if grunt.alive and not getattr(grunt, 'musOut', False):
        grunt.term += 1

        if grunt.term >= 7:
            if career.check_reenlist(grunt) == 2:
                grunt.history.append(f'Mandatory re-enlistment after term {grunt.term-1}')
                grunt.reenlist = True
            else:
                grunt.reenlist = False
        else:
            grunt.reenlist = career.check_reenlist(grunt)
    else:
        grunt.die()

    grunt.history.append('#####')
    return True
