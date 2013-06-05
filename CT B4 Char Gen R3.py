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

import time
#import sprint       #to print to to screen or file
import b5_data       #unique book 5 data
#import branch_win   #wxpython module to pop up a window to pick the branch
from character import *
from career import *
import muster


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
        career(b4g)
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
        career(b4g)
        if b4g.alive:
           muster.muster_out(b4g)
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
        grunt.branch = 'Imperial Marines'  # Imperial Marines
    elif 'A' == line[6]:
        grunt.branch = 'Imperial Army'  # Imperial Army
    elif 'N' == line[6]:
        grunt.branch = 'Imperial Navy'  # Imperial Navy

    if grunt.branch == 'Imperial Marines' or grunt.branch == 'Imperial Army':
        if 'I' == line[7]:
            grunt.arm = 'Infantry'   #set arm to Infantry
        elif 'C' == line[7]:
            grunt.arm = 'Cavalry'   #set arm to Cavalry
        elif 'I' == line[7]:
            grunt.arm = 'Artillery'   #set arm to artillery
        elif 'S' == line[7]:
            grunt.arm = 'Support'   #set arm to Support'
        elif 'X' == line[7]:
            grunt.arm = 'Commando'   #set arm to Commando
    else:
        grunt.arm = b5_data.arm_enlisted_Table[0]  #Imperial Navy.  Set up later

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

    #Sb4g.arm = 'Commando'   #debug - set arm to Commando

    career(b4g)

    if b4g.alive:  
        if b4g.branch == 'Imperial Army' or b4g.branch == 'Imperial Marines':
            muster.muster_out(b4g)
        else:
            b5_data2.muster_out(b4g)
            
    print_history(b4g)
    print '+++++'
    print_Char_Data(b4g)
#end of single_char

# Start of main code execution   

single_Char()

#looper(100)

#looper2(20)


# Then the final character data, including the final UPP, any noble title, schools, etc.

