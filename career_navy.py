import b5_data       #unique book 5 data

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
        grunt.die(year)
    grunt.history.append('#####')
    return True

# end of navy_term()

