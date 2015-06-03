from b5_data import display_b5_rank   # 6/11/13 MU

def display_noble_rank(grunt):
    'Display the nobla rank, from Knight to Duke'
    title = grunt.noble_rank()
    if title==None: return False
    print("Noble Title: " + title)
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
    if grunt.branch == 'Imperial Navy':
        b5_data.display_b5_rank(grunt)
    else:
        print(grunt.military_rank())
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
    #grunt.skills.sort()
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
